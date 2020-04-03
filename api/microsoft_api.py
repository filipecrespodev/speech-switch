#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "1.30.0"

import time
import logging
import comtypes
from comtypes.client import CreateObject

logger = logging.getLogger("speech-server")

class Sapi(object):

    def __init__(self, profile):
        try:
            self.profile = profile
            self.tokenName = self.profile.getTokenName()

            self.engine = CreateObject("SAPI.SpVoice")
            self.stream = CreateObject("SAPI.SpFileStream")
            # stereo = add 1
            # 16-bit = add 2
            # 8KHz = 4
            # 11KHz = 8
            # 12KHz = 12
            # 16KHz = 16
            # 22KHz = 20
            # 24KHz = 24
            # 32KHz = 28
            # 44KHz = 32
            # 48KHz = 36
            self.stream.Format.Type = self.profile.getFormat()
            self.engine.Voice = self.getToken(self.tokenName)

        except Exception as e:
            logger.error(e)

    def createFileTts(self, text):
        self.filename = None
        try:
            comtypes.CoInitialize()
            self.ts = time.time()
            self.filename = '%s.wav' % self.ts
            self.path=self.profile.getFilePath()
            self.stream.Open(self.path + self.filename, 3) #SSFMCreateForWrite
            self.engine.AudioOutputStream = self.stream
            self.engine.speak(text)
            self.stream.Close()

        except Exception as e:
            logger.error(e)

        return self.filename

    def getVoices(self):
        return self.engine.GetVoices()

    def getToken(self, tokenName):
        tokens = self.getVoices()
        for token in tokens:
            logger.info(token.Id)
            if token.Id == tokenName: break
        return token

