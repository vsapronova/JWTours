from flask import Flask, send_from_directory
from flask import request
from datetime import datetime
import db
from sender import Sender
from db import Request
import json
from flask import jsonify
from flask_cors import cross_origin

app = Flask("HelloWorld")


@app.route('/<path:filename>')
def static_file(filename):
    return send_from_directory('/Users/victoria/Projects/JWTours/frontend', filename)


@app.route('/api/create_request', methods=['POST'])
@cross_origin()
def create_request():
    #result = request.get_json()
    result = json.loads(request.data)
    email = result['email']
    requested_date = datetime.strptime(result['requested_date'], "%Y-%m-%d")
    key = db.create_unique_key()
    req = Request(email, requested_date, key)
    db.insert_request(config, req)
    conf_link = "http://127.0.0.1:5000/confirm_request?key={0}&email={1}".format(key, email)
    subject = 'Please confirm your email'
    message = 'Please click on {} to confirm your email.'.format(conf_link)
    sender.send_email_to_request(email, key, subject, message)
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