#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import logging

logger = logging.getLogger('speech-server')

class Profile():

    def __init__(self):
        try:
            self.cfg = configparser.ConfigParser()
            self.cfg.read('./conf/config.ini')

            self.voicesCpqd   = self.cfg.get('CPQD TTS', 'voices').split(';')
            self.voicesGoogle = self.cfg.get('GOOGLE TTS', 'voices').split(';')
            self.convertTts = self.cfg.getboolean('CPQD TTS', 'convert')
            self.urlTts = self.cfg.get('CPQD TTS', 'url')
            self.usernameTts = self.cfg.get('CPQD TTS', 'username')
            self.passwordTts = self.cfg.get('CPQD TTS', 'password')
            self.urlAsr = self.cfg.get('CPQD ASR', 'url')
            self.convertAsr = self.cfg.getboolean('CPQD ASR', 'convert')
            self.usernameAsr = self.cfg.get('CPQD ASR', 'username')
            self.passwordAsr = self.cfg.get('CPQD ASR', 'password')
            self.file_path = self.cfg.get('PATH', 'file_path')
            self.ffmpeg_parametersAsr = self.cfg.get('FFMPEG', 'parameters_asr')
            self.ffmpeg_parametersTts = self.cfg.get('FFMPEG', 'parameters_tts')

            self.allowed_extensions = self.cfg.get('FFMPEG', 'allowed_extensions').split(';')

            self.token_name = self.cfg.get('SAPI', 'token_name')
            self.format = self.cfg.getint('SAPI', 'format')
            self.service_tts = self.cfg.get('SERVICE', 'tts')

            self.service_asr = self.cfg.get('SERVICE', 'asr')
            self.url_nlp = self.cfg.get('NLP', 'url')

            self.port = self.cfg.getint('WS', 'port')
            self.expires = self.cfg.getint('WS', 'expires')
            self.use_auth = self.cfg.getboolean('WS', 'use_auth')

            self.tls = self.cfg.getboolean('WS', 'tls')
            self.key = self.cfg.get('WS', 'key')
            self.certified = self.cfg.get('WS', 'certified')

            self.logins = {}
            self.services = {}

            self.__loadLogins__()

        except Exception as e:
            logger.error(e)

    def getVoicesCpqd(self):
         return self.voicesCpqd

    def getVoicesGoogle(self):
         return self.voicesGoogle

    def getPort(self):
         return self.port

    def getFilePath(self):
         return self.file_path

    def getUrlTts(self):
         return self.urlTts

    def getUsernameTts(self):
         return self.usernameTts

    def getPasswordTts(self):
         return self.passwordTts

    def getUrlAsr(self):
         return self.urlAsr

    def getUsernameAsr(self):
         return self.usernameAsr

    def getPasswordAsr(self):
         return self.passwordAsr

    def getFfmpegParametersAsr(self):
         return self.ffmpeg_parametersAsr

    def getFfmpegParametersTts(self):
         return self.ffmpeg_parametersTts

    def getAllowedExtensions(self):
         return self.allowed_extensions

    def getServiceAsr(self):
         return self.service_asr

    def getUrlNlp(self):
        return self.url_nlp

    def getConvertTts(self):
        return self.convertTts

    def getConvertArs(self):
        return self.convertAsr

    def getTokenName(self):
        return self.token_name

    def getFormat(self):
        return self.format

    def getServiceTts(self):
        return self.service_tts

    def getLogins(self):
        return self.logins

    def getServices(self):
        return self.services

    def getExpires(self):
        return self.expires

    def useAuth(self):
        return self.use_auth

    def isTls(self):
        return self.tls

    def getKey(self):
        return self.key

    def getCertified(self):
        return self.certified

    def __loadLogins__(self):
        l = self.cfg.get('WS', 'auth_username').split(";")
        p = self.cfg.get('WS', 'auth_password').split(";")
        s = self.cfg.get('WS', 'auth_service').split(";")

        idx = 0

        for v in l:
            self.logins[v] = p[idx]
            self.services[s[idx]] = v
            idx = idx + 1

