#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import random
import time
from bs4 import BeautifulSoup

logger = logging.getLogger("speech-server")

class Cpqd(object):

    def __init__(self, profile):
        try:
            self.profile = profile

        except Exception as e:
            logger.error(e)

    def createFileTts(self, text, voice):
        self.filename = None
        try:
            self.ts = time.time()
            self.filename = '%s.wav' % (self.ts + random.random())

            auth = (self.profile.getUsernameTts(),self.profile.getPasswordTts())
            params = {'text':text, 'voice':voice}
            r = requests.get(self.profile.getUrlTts(), params=params, auth=auth)

            #print(r.content.decode('UTF-8'))

            self.soup = BeautifulSoup(r.content,"html.parser")
            self.urlWav = self.soup.url.string

            r = requests.get(self.urlWav, stream=True, params=params, auth=auth)
            with open(self.profile.getFilePath() + self.filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)

        except Exception as e:
            logger.error(e)

        return self.filename

    def createFileTtsV2(self, text, voice):
        self.filename = None
        try:
            url = self.profile.getUrlTts()

            querystring = {
                "text": text,
                "voice": voice}

            payload = ""
            headers = {
                'Accept': "application/octet-stream",
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            self.filename = response.headers['Content-Disposition'].split(';')[1]
            self.filename = self.filename.replace('filename="','').replace('"','').strip()
            #print(self.filename)

            with open(self.profile.getFilePath() + self.filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)

        except Exception as e:
            logger.error(e)

        return self.filename


    def sendAudioFile(self, audio):
        r = None
        try:
            self.audio = audio
            auth = (self.profile.getUsernameAsr(),self.profile.getPasswordAsr())
            params = {'lm':'builtin:slm/general'}
            headers = {'Content-Type':'audio/wav', 'Accept':'application/json'}
            r = requests.post(self.profile.getUrlAsr(), params=params, headers=headers, auth=auth, data=self.audio)
            r = r.content.decode('UTF-8')
        except Exception as e:
            logger.error(e)

        return r