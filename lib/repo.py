#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import urllib
import os, sys
import time
import threading
import datetime

logger = logging.getLogger("speech-server")

class Repo(object):

    def __init__(self, profile):
        try:
            self.profile = profile
            self.garbageThread = threading.Timer(8640.0, self.__garbage__())
            self.garbageThread.daemon = True
            self.garbageThread.start()

        except Exception as e:
            logger.error(e)

    def download(self, url):
        self.filename = None
        try:
            self.filename = url.rsplit('/', 1)[1]
            self.filename = self.filename.split('?')[0]
            self.ts = time.time()

            if (self.filename == 'original'):
                self.filename = '{}.wav'.format(self.ts)

            r = requests.get(url, stream=True)
            with open(self.profile.getFilePath() + self.filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
        except Exception as e:
            logger.error(e)

        return self.filename

    def __garbage__(self):
        try:
            dir = self.profile.getFilePath()

            if (os.path.exists(dir) == False):
                raise ValueError('Directory not exists.')

            for filename in os.listdir(dir):
                fullPath = dir + filename
                mtime = datetime.datetime.fromtimestamp(os.path.getctime(fullPath)).date()
                now = datetime.datetime.now().date()
                if ((now - mtime).days > 3):
                    os.remove(fullPath)

                #print(filename)
                #print(mtime)
                #print(now)
                #print(now - mtime)

        except Exception as e:
            logger.error(e)
            #print(e)

if __name__ == '__main__':
    repo = Repo(None)
    repo.__garbage__()
