#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = "1.30.0"

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from rest import ws_rest
from conf import profile
from sys import platform
import signal

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ("%s/conf/novax-188819-190ffc7cc46c.json" % (os.path.dirname(os.path.abspath(__file__))))

file_name = ("%s/log/speech_server.log" % (os.path.dirname(os.path.abspath(__file__))))

file_handler = RotatingFileHandler(file_name, maxBytes=1024 * 1024 * 10, backupCount=20)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - module: %(module)s - line: %(lineno)d - func: %(funcName)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger = logging.getLogger("speech-server")
logger.addHandler(file_handler)

def writePidFile():
    pid = str(os.getpid())
    f = open('speech-server.pid', 'w')
    f.write(pid)
    f.close()

def checkKillProcess():
    try:
        f = open('speech-server.pid', 'r')
        pid = f.readline()
        f.close()
        os.kill(int(pid), signal.SIGKILL)
    except Exception as e:
        print(e)
        logger.error(e)

if __name__ == '__main__':
    try:
        if platform == "linux" or platform == "linux2":
            checkKillProcess()
        writePidFile()
        p = profile.Profile()
        sc = ws_rest.SpeechWS(p)
    except KeyboardInterrupt:
        print("\nSpeechServer-Down because keyboard interrupt")
        logger.error("\nSpeechServer-Down because keyboard interrupt")
        sys.exit(0)
    except Exception as e:
        print(e)
        logger.error(e)
