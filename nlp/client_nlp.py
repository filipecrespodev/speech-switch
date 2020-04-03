#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger("speech-server")

class ClientNLP(object):

    def __init__(self, profile):
        try:
            self.profile = profile

        except Exception as e:
            logger.error(e)

    def classifyTextByIntent(self, message, domain):
        response = None
        try:
            session = requests.Session()
            session.trust_env = False
            headers = {
                'User-Agent': 'Speech-Server'
                ,'Content-Type': 'application/json'
            }
            postdata = {'Message': message, 'Domain': domain}
            response = session.post(self.profile.getUrlNlp() +  '/intent/classifyText', data=json.dumps(postdata), headers = headers, verify=False)

            if response.status_code != 200:
                raise ValueError(
                    'Request to NLP returned an error %s, the response is:\n%s'
                    % (response.status_code, response.text)
                )

        except Exception as e:
            logger.error(e)

        return response.content


if __name__ == '__main__':
    session = requests.Session()
    session.trust_env = False

    headers = {
        'User-Agent': 'Speech-Server'
        ,'Content-Type': 'application/json'
    }
    postdata = {'Message': 'sim'}
    response = session.post('http://localhost:83/intent/classifyText', data=json.dumps(postdata), headers = headers, verify=False)

    if response.status_code != 200:
        raise ValueError(
            'Request to NLP returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

    print(response.content)