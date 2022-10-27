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

from flask import Flask, request, Response
import informacast_api
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

#Webhook Receiver Route
@app.route('/webhookreceiver', methods=['POST'])
def integrate():
    
    print("Meraki MT30 Webhook-Alert received!")
    #Read webhook event data
    webhook_alert_data = request.json

    #Read enviroment variables
    MERAKI_WEBHOOK_SECRET= os.environ['MERAKI_WEBHOOK_SECRET']
    MESSAGE_TEMPLATE_ID = os.environ['MESSAGE_TEMPLATE_ID']
    DISTRIBUTION_LIST_ID = os.environ['DISTRIBUTION_LIST_ID']

    #Compare webhook secret and trigger notification
    if (webhook_alert_data['sharedSecret'] == MERAKI_WEBHOOK_SECRET):
        deviceLocation = webhook_alert_data['deviceName']

        informacast_api.sendNotification(deviceLocation, MESSAGE_TEMPLATE_ID, DISTRIBUTION_LIST_ID)

        return Response(status=200)
    else:
        return Response(status=500)


if __name__ == "__main__":
    app.run()
