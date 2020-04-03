#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os, sys
import ffmpy

logger = logging.getLogger("speech-server")

class Ffmpeg(object):

    def __init__(self, profile):
        try:
            self.profile = profile
            self.plataform = sys.platform.lower()

        except Exception as e:
            logger.error(e)


    def convertAudioFile(self, filename, asr = True):
        r = None
        try:
            audio = open(os.path.join('', filename), 'rb').read()

            f = '%s_C.wav' % filename[:-4]

            if (asr == True):
                s = self.profile.getFfmpegParametersAsr()
            else:
                s = self.profile.getFfmpegParametersTts()

            fp = os.path.join(self.profile.getFilePath(), f)

            exe = './ffmpeg/ffmpeg'
            if self.plataform == "linux" or self.plataform == "linux2":
                exe = 'ffmpeg'

            ff = ffmpy.FFmpeg(
                  executable=exe
                , inputs={os.path.join(self.profile.getFilePath(), filename): None}
                , outputs={fp: s}
            )

            ff.run()

            r = open(fp, 'rb').read()

        except Exception as e:
            logger.error(e)

        return r