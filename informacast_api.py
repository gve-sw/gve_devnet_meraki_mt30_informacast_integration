""" Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

import requests
from requests.exceptions import RequestException
import json
from dotenv import load_dotenv
import os

load_dotenv()

APP_TOKEN = os.environ['APP_TOKEN']
BASE_URL = os.environ['BASE_URL']

HEADER = {
    "Authorization": "Bearer " + APP_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
    }

def sendNotification(location, message_template_id, distribution_list_id):
    url = BASE_URL + "/v1/notifications"
    
    data = {
        "distributionListIds": [distribution_list_id],
        "messageTemplateId": message_template_id,
        "customVars": {
            "affectedLocation": location
        }
    }

    response = requests.post(url, headers=HEADER, data=json.dumps(data))
    print("Informatcast notification triggered!")
    print(response.status_code)


def getMessageTemplates():
    url = BASE_URL + "/v1/message-templates"
    response = requests.get(url, headers=HEADER)
    return response.json()


def getDistributionLists():
    url = BASE_URL + "/v1/distribution-lists"
    response = requests.get(url, headers=HEADER)
    return response.json()


