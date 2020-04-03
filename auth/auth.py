#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import uuid
import datetime
from auth import session

logger = logging.getLogger('speech-server')

class OAuth():

    def __init__(self, profile):
        try:
            self.expires  = profile.getExpires()
            self.logins   = profile.getLogins()
            self.services = profile.getServices()
            self.sessions = {}
            self.tokens   = {}

        except Exception as e:
            logger.error(e)

    def __getToken__(self, service):
        try:
            if (service in self.tokens):
                u = self.tokens[service]
            else:
                u = str(uuid.uuid4())
                cache = session.Session(service, u)
                self.tokens[service] = u
                self.sessions[u] = cache
            return u
        except Exception as e:
            logger.error(e)

    def login(self, username, passwd, service):
        try:
            if (service not in self.services):
                return -1 # service invalid

            if (self.services[service] != username):
                return -2 # username is not owner of the service

            if (username in self.logins):
                if (self.logins[username] != passwd):
                    return -3 # password is wrong
                u = self.__getToken__(service)

                return u
            else:
                return -4 # username invalid
        except Exception as e:
            logger.error(e)

    def checkToken(self, token):
        b = token in self.sessions
        if (b):
            now = datetime.datetime.now()
            cache = self.sessions.get(token)

            if ((now - cache.getDtCreated()).seconds > self.expires):
                del self.sessions[token]
                b = False #Expires
        return b


if __name__ == '__main__':
    #oauth = OAuth(None)
    #print(oauth.__getToken__('a7:c2:8d:15:87:1d:15:bb:82:75:f8:5a:73:19:ef:6f'))
    e = 'a' in {'b': 'legal', 'a' : 'isso'}
    print(e)