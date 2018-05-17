#!/usr/bin/env python

from flask import Flask, request, make_response, jsonify
import json
import requests
import os
import urllib3

urllib3.disable_warnings()

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)

@app.route('/webhook/relay', methods=['POST'])
def relay():
    webhook_url = '{webhook URL from Slack}'
    text_template = '>>> *From*: {}\n*Subject*: {}\n*Message*:\n\n{}'
    # process the meaningful parts of the Sendgrid webhook push
    email_from = request.form.get('from')
    email_subject = request.form.get('subject')
    email_text = request.form.get('text')
    if any((email_from, email_subject, email_text)):
        # send the email to Slack
        slack_data = {'text': text_template.format(email_from, email_subject, email_text)}
        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        message = 'Webhook relayed.'
        return jsonify(message=message)
    else:
        message = 'Webhook relay failed!'
        return make_response(jsonify(message=message), 400)
