#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import json
from flask import jsonify, Response, Request, make_response
from auth import auth
from urllib.parse import urlparse

logger = logging.getLogger('speech-server')

class MiddleWare(object):

    def __init__(self, app, profile):
        self.profile = profile
        self.app = app
        self.oauth = auth.OAuth(self.profile)

    def login(self, headers):
        try:
            username = headers.get('username')
            password = headers.get('password')
            service  = headers.get('service')

            token = self.oauth.login(username, password, service)
            message = 'Ok'
            b = True

            if (token == -1):
                message = 'Service is not exist.'
                b = False
            elif (token == -2):
                message = 'Service is wrong.'
            elif (token == -3 or token == -4):
                message = 'Username or Password invalid.'
                b = False

            r = {
                'success': b
                , 'message' : message
                , 'token': token
            }
            return r
        except Exception as e:
            logger.error(e)

    def checkToken(self, headers):
        token = headers.get('token')
        return self.oauth.checkToken(token)

    def __call__(self, environ, start_response):
        try:
            request = Request(environ)
            url = urlparse(request.url)
            headers = request.headers

            if ( '/auth/login' in url.path):
                r = json.dumps({'result':  self.login(headers)})
                body = bytes(r, 'utf-8')
                status = '200 OK'
                headers = [('Content-type', 'application/json')]
                start_response(status, headers)
                return [body]
            else:
                if (self.checkToken(headers)):
                    return self.app(environ, start_response)
                else:
                    print("Aqui")
                    r = {
                        'success': False
                        , 'message': 'Token is invalid.'
                        , 'token': -7
                    }
                    r = json.dumps({'result': r})
                    body = bytes(r, 'utf-8')
                    status = '401  Unauthorized'
                    headers = [('Content-type', 'application/json')]
                    start_response(status, headers)
                    return [body]

        except Exception as e:
            logger.error(e)


