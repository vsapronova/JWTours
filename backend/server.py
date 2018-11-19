from flask import Flask, send_from_directory, make_response
from flask import request
from datetime import datetime
import db
from sender import Sender
from db import Request
import json
from flask import jsonify
from flask_cors import cross_origin

app = Flask("HelloWorld")

import re

from typing import Dict

@app.route('/<path:filename>')
def static_file(filename):
    return send_from_directory('/Users/victoria/Projects/JWTours/frontend', filename)


class Validator:
    def __init__(self, request_data):
        self.params_errors = []
        self.request_data = request_data

    def present(self, param_name):
        if param_name not in self.request_data:
            self.params_errors.append(param_name)
        return param_name in self.request_data

    def email(self):
        if self.present('email'):
            if not re.match(r'[^@]+@[^@]+\.[^@]+', self.request_data['email']):
                self.params_errors.append('email')
            else:
                return self.request_data['email']
        return None

    def has_errors(self):
        return len(self.params_errors) > 0

    def error_response(self):
        return jsonify({"error": "Bad parameters", "params_errors": self.params_errors}), 400


@app.route('/api/create_request', methods=['POST'])
@cross_origin()
def create_request():
    #result = request.get_json()
    request_data = json.loads(request.data)

    validator = Validator(request_data)

    email = validator.email()

    if validator.has_errors():
        return validator.error_response()

    requested_date = datetime.strptime(request_data['requested_date'], "%Y-%m-%d")
    key = db.create_unique_key()
    req = Request(email, requested_date, key)
    db.insert_request(config, req)
    conf_link = "http://127.0.0.1:5000/confirm_request?key={0}&email={1}".format(key, email)
    subject = 'Please confirm your email'
    message = 'Please click on {} to confirm your email.'.format(conf_link)
    #sender.send_email_to_request(email, key, subject, message)
    return jsonify(success=True)


@app.route('/confirm_request', methods=['GET'])
def confirm_request():
    key = request.args.get('key')
    email = request.args.get('email')
    req = db.find_request_by_key(config, key)
    if req is not None and email == req.email:
        db.confirm_request(config, key)
        return "Thank you! Email is confirmed."
    else:
        return "NO"


@app.route('/unsubscribe_request', methods=['GET'])
def unsubscribe_request():
    key = request.args.get('key')
    email = request.args.get('email')
    req = db.find_request_by_key(config, key)
    if req is not None and email == req.email:
        db.unsubscribe_request(config, key)
        return "Email is successfully unsubscribed."
    else:
        return "No"




path = "~/jw-tour.ini"
config = db.DBConfig(path)
sender = Sender()
app.run()