from flask import Flask
from flask import request
from datetime import datetime
import db
from sender import Sender


app = Flask("HelloWorld")


@app.route('/create_request', methods=['POST'])
def create_request():
    result = request.get_json()
    email = result['email']
    requested_date = datetime.strptime(result['requested_date'], "%Y-%m-%d")
    db.insert_request(config, email, requested_date)
    return "bla"


@app.route('/confirm_request', methods=['GET'])
def confirm_request():
    pass


def send_email_with_a_key(email, ukey):
    subject = 'Please confirm your email'
    message = 'Please click on this link to confirm your email'
    sender.send_email(email, subject, message)


path = "~/jw-tour.ini"
config = db.DBConfig(path)
sender = Sender()
app.run()