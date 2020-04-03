#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import logging

logger = logging.getLogger('speech-server')

class Session():

    def __init__(self, service, token):
        try:
            self.dt_created = datetime.datetime.now()
            self.token = token
            self.service = service

        except Exception as e:
            logger.error(e)

    def getDtCreated(self):
        return self.dt_created

    def getService(self):
        return self.service