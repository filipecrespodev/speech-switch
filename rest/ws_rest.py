#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, abort, send_file, Response
from flask_cors import CORS, cross_origin
from speech import speech
from ffmpeg import ffmpeg, what
from lib import repo
from logging.handlers import RotatingFileHandler
from nlp import client_nlp
import os
import logging
from OpenSSL import SSL
from rest import middleware
import time

logger = logging.getLogger('speech-server')

context = SSL.Context(SSL.SSLv23_METHOD)
app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})


me = None

class SpeechWS(object):

    SYSTEM_NAME  = "Speech Server"
    SYSTEM_VERSION = "1.30.0"
    SYSTEM_ORIGIN  = "*"

    def __init__(self, profile):
        try:
            self.version = self.SYSTEM_NAME + " v " + self.SYSTEM_VERSION
            self.profile = profile

            if (self.profile.useAuth()):
                app.wsgi_app = middleware.MiddleWare(app.wsgi_app, self.profile)

            app.config['UPLOAD_FOLDER'] = profile.getFilePath()
            self.ffmpeg = ffmpeg.Ffmpeg(self.profile)
            self.repo = repo.Repo(self.profile)
            self.obj = speech.Speech(self.profile)
            self.nlp = client_nlp.ClientNLP(self.profile)
            global me
            me = self
            file_handler = RotatingFileHandler(("%s/log/speech_ws.log" % os.path.dirname(os.path.abspath(__file__))), maxBytes=1024 * 1024 * 10, backupCount=20)
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s - module: %(module)s - line: %(lineno)d - func: %(funcName)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            global logger
            logger = logging.getLogger('werkzeug')
            logger.addHandler(file_handler)

            context = None

            if (self.profile.isTls()):
                context = (self.profile.getCertified(), self.profile.getKey())

            app.run(host='0.0.0.0', port=me.profile.getPort(), threaded=True, debug=True, ssl_context=context)

        except Exception as e:
            logger.error(e)

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in me.profile.getAllowedExtensions()

    def allowed_voice(self, voice):
        voices = me.profile.getVoicesCpqd()

        if (self.profile.getServiceTts().lower() == "google"):
            voices = me.profile.getVoicesGoogle()

        return voice.lower() in voices

    @app.route('/')
    @cross_origin(origin=SYSTEM_ORIGIN)
    def index():
        return "Welcome, it is " + me.version

    @app.route('/message/requestTextToSpeech', methods=['POST'])
    @cross_origin(origin=SYSTEM_ORIGIN)
    def requestTextToSpeech():
        if not request.json or not 'Message' in request.json or not 'Voice' in request.json:
            abort(400, 'Parameter Message or Voice not found.')
        msg = request.json.get('Message', "")
        voice = request.json.get('Voice', "")
        if ((voice and me.allowed_voice(voice)) == False):
            abort(400, 'Invalid voice.')

        filename = app.config['UPLOAD_FOLDER'] + me.obj.createFileTts(msg, voice)

        if (me.profile.getConvertTts()):
            audio = me.ffmpeg.convertAudioFile(filename, asr=False)
            filename = filename.replace('.wav', '_C.wav')

        return send_file(filename, mimetype='application/audio')

    @app.route('/message/recordTextToSpeech', methods=['POST'])
    @cross_origin(origin=SYSTEM_ORIGIN)
    def recordTextToSpeech():
        if not request.json or not 'Message' in request.json or not 'Voice' in request.json:
            abort(400, 'Parameter Message or Voice not found.')
        msg = request.json.get('Message', "")
        voice = request.json.get('Voice', "")
        if ((voice and me.allowed_voice(voice)) == False):
            abort(400, 'Invalid voice.')

        filename = app.config['UPLOAD_FOLDER'] + me.obj.createFileTts(msg, voice)

        if (me.profile.getConvertTts()):
            audio = me.ffmpeg.convertAudioFile(filename, asr=False)
            filename = filename.replace('.wav', '_C.wav')

        r = {
            'File': filename
        }
        return jsonify({'result': r}), 200

    @app.route('/message/sendAudioByRecognize', methods=['POST'])
    @cross_origin(origin=SYSTEM_ORIGIN)
    def sendAudioByRecognize():
        # check if the post request has the file part
        if 'file' not in request.files:
            abort(400, 'Parameter File not found.')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            abort(400, 'FileName not found.')
        if ((file and me.allowed_file(file.filename)) == False):
            abort(400, 'Invalid extension file.')

        speakers = 1
        punctuation = False

        if 'speakers' in request.form:
            speakers = int(request.form['speakers'])

        if 'punctuation' in request.form:
            if (request.form['punctuation'] == 'True'):
                punctuation = True

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        audio = open(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), 'rb').read()
        r = me.obj.sendAudioFile(audio, speakers, punctuation)
        return jsonify({'result': r}), 200

    @app.route('/message/sendAudioConvertByRecognize', methods=['POST'])
    @cross_origin(origin=SYSTEM_ORIGIN)
    def sendAudioConvertByRecognize():
        # check if the post request has the file part
        if 'file' not in request.files:
            abort(400, 'Parameter File not found.')
        if 'Nlp' not in request.form:
            abort(400, 'Parameter Nlp not found.')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            abort(400, 'FileName not found.')
        if ((file and me.allowed_file(file.filename)) == False):
            abort(400, 'Invalid extension file.')

        speakers = 1
        punctuation = False

        if 'speakers' in request.form:
            speakers = int(request.form['speakers'])

        if 'punctuation' in request.form:
            if (request.form['punctuation'] == 'True'):
                punctuation = True

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        audio = me.ffmpeg.convertAudioFile(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        r = me.obj.sendAudioFile(audio, speakers, punctuation)

        logger.info(r)

        return jsonify({'result': r}), 200

    @app.route('/message/downloadAudioConvertByRecognize', methods=['POST'])
    @cross_origin(origin=SYSTEM_ORIGIN)
    def downloadAudioConvertByRecognize():
        if not request.json or not 'Url' in request.json:
            abort(400, 'Parameter Url not found.')
        if not request.json or not 'Nlp' in request.json:
            abort(400, 'Parameter Nlp not found.')
        url = request.json.get('Url', "")
        domain = request.json.get('Nlp', "")
        #filename = me.repo.download(url) #now is not used
        filename = url # FIXME, because line up
        # if user does not select file, browser also
        # submit a empty part without filename
        if ((filename and me.allowed_file(filename)) == False):
            abort(400, 'Invalid extension file.')

        audio = open(filename, 'rb').read()
        if (me.profile.getConvertArs()):
            format = what.what(filename)
            if (format != None):
                (typeFile, rate, channels, frames, bits) = format
                if ((typeFile != 'wav') or ((rate > 8000) and (me.profile.getServiceAsr() == 'cpqd')) or ((rate > 16000) and (me.profile.getServiceAsr() == 'google'))):
                    audio = me.ffmpeg.convertAudioFile(filename)
                    logger.info('Converting file {}'.format(filename))
            else:
                audio = me.ffmpeg.convertAudioFile(filename)
                logger.info('Converting file {}'.format(filename))

        r = me.obj.sendAudioFile(audio)

        logger.info(r)

        return jsonify({'result': r}), 200

    @app.route('/message/analizeSentiment', methods=['POST'])
    @cross_origin(origin=SYSTEM_ORIGIN)
    def requestAnalizeSentiment():
        if not request.json or not 'Message' in request.json:
            abort(400, 'Parameter Message not found.')
        msg = request.json.get('Message', "")

        r = me.obj.analizeSentiment(msg)
        return jsonify({'result': r}), 200


    @app.route('/version', methods=['GET'])
    @cross_origin(origin=SYSTEM_ORIGIN)
    def getVersion():
        version = me.version
        r = {
            'System': version
            ,'Cmd': 'version'
        }
        return jsonify({'result': r}), 200
