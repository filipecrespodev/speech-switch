#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib
import os, sys
import json
from bs4 import BeautifulSoup

session = requests.Session()
session.trust_env = False

headers = {
    'User-Agent': 'Speech-Server'
    ,'Content-Type': 'application/json'
}
# Botão Começar
#postdata = {'get_started': {'payload' : 'Começar'}}
#response = session.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAASFDsgS2J4BAO0uZCCPTnWSuMvi0tF9YZCbz5RiswQZClzYZAP9TqBQeycApsHUlclbyQYQZCQCJ1HoUXBV78KOhjVOZATxWmGtWI52TVAEpWfujLDi1RDr6bc95oJiRn3yZB99rwJCORZCVvZC4XiQMULITWvEsWJOItnJ0ZCEdIZCwZDZD', data=json.dumps(postdata), headers = headers, verify=False)

# Menu Persistente
postdata = {  "persistent_menu":[    {      "locale":"default",      "composer_input_disabled": "false",      "call_to_actions":[        {          "title":"ACI",          "type":"nested",          "call_to_actions":[            {              "title":"Benefícios",              "type":"postback",              "payload":"/beneficios"            },            {              "title":"Seguro de Vida",              "type":"postback",              "payload":"/seguro.vida"            },            {              "title":"Liq Med",              "type":"postback",              "payload":"/liq.med"            }          ]        },                       {          "title":"Institucional",          "type":"nested",          "call_to_actions":[            {              "title":"Soluções",              "type":"postback",              "payload":"/institucional.solucoes"            },                                               {              "title":"Sobre Nós",              "type":"postback",              "payload":"/institucional.sobre"            }]        },                             {          "title":"Sair",          "type":"postback",                         "payload":"/sair"        }      ]    }  ]}
response = session.post('https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAASFDsgS2J4BAO0uZCCPTnWSuMvi0tF9YZCbz5RiswQZClzYZAP9TqBQeycApsHUlclbyQYQZCQCJ1HoUXBV78KOhjVOZATxWmGtWI52TVAEpWfujLDi1RDr6bc95oJiRn3yZB99rwJCORZCVvZC4XiQMULITWvEsWJOItnJ0ZCEdIZCwZDZD', data=json.dumps(postdata), headers = headers, verify=False)

if response.status_code != 200:
    raise ValueError(
        'Request to NLP returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )

print response.content