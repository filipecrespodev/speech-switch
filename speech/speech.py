#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "1.30.0"

import sys
import logging
from cpqd.cpqd import Cpqd
from api.google_api import GoogleApi

if sys.platform.lower().startswith('win'):
    from api.microsoft_api import Sapi

logger = logging.getLogger("speech-server")

class Speech(object):

    def __init__(self, profile):
        try:
            self.profile = profile
            self.isWin = sys.platform.lower().startswith('win')

            if (self.isWin):
                self.sapi = Sapi(profile)
            self.cpqd = Cpqd(profile)
            self.google = GoogleApi(profile)
            self.asr = self.profile.getServiceAsr()
            self.tts = self.profile.getServiceTts()

        except Exception as e:
            logger.error(e)

    def createFileTts(self, text, voice):
        r = None
        if (self.tts.lower() == "cpqd"):
            r = self.cpqd.createFileTtsV2(text, voice)
        elif (self.tts.lower() == "google"):
            r = self.google.createFileTts(text, voice)
        else:
            if (self.isWin):
                r = self.sapi.createFileTts(text)
            else:
                logger.error("System is not support sapi.")

        return r

    def sendAudioFile(self, audio, speakers=1, punctuation=False):
        r = None
        if (self.asr.lower() == "google"):
            r = self.google.sendAudioFile(audio, speakers, punctuation)
        else:
            r = self.cpqd.sendAudioFile(audio)

        return r

    def analizeSentiment(self, text):
        r = self.google.analyzeSentiment(text)
        return r