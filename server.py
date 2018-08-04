from flask import Flask
from flask import request
from datetime import datetime
import db
from sender import Sender
from db import Request


app = Flask("HelloWorld")


@app.route('/create_request', methods=['POST'])
def create_request():
    result = request.get_json()
    email = result['email']
    requested_date = datetime.strptime(result['requested_date'], "%Y-%m-%d")
    key = db.create_unique_key()
    req = Request(email, requested_date, key)
    db.insert_request(config, req)
    conf_link = "http://127.0.0.1:5000/confirm_request?key={0}&email={1}".format(key, email)
    subject = 'Please confirm your email'
    message = 'Please click on {} to confirm your email'.format(conf_link)
    sender.send_email(email, subject, message)
    return conf_link


@app.route('/confirm_request', methods=['GET'])
def confirm_request():
    key = request.args.get('key')
    email = request.args.get('email')
    req = db.find_request_by_key(config, key)
    if req is not None and email == req.email:
        db.confirm_request(config, key)
        return "Email is confirmed"
    else:
        return "NO"







path = "~/jw-tour.ini"
config = db.DBConfig(path)
sender = Sender()
app.run()