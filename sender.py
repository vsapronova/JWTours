from configuration import get_param
import smtplib


class Sender:
    def __init__(self):
        path = "~/jw-tour.ini"
        from_address = get_param(path, 'SMTP', 'from_address')
        username = get_param(path, 'SMTP', 'username')
        password = get_param(path, 'SMTP', 'password')
        address = get_param(path, 'SMTP', 'address')
        port = int(get_param(path, 'SMTP', 'port'))
        server = smtplib.SMTP(address, port)
        server.starttls()
        server.login(username, password)
        self.server = server
        self.from_address = from_address

    def quit(self):
        self.server.quit()

    def send_email(self, client_email, subject, message):
        smtp_message = 'Subject: {}\n\n{}'.format(subject, message)
        self.server.sendmail(self.from_address, client_email, smtp_message)
        print("Email was sent to: {}".format(client_email))


    def send_email_to_request(self, email, key, subject, message):
        unsub_link = "http://127.0.0.1:5000/unsubscribe_request?key={0}&email={1}".format(key, email)
        unsub_message = 'If you want to unsubscribe click here: {}.'.format(unsub_link)
        self.send_email(email, subject, message + unsub_message)