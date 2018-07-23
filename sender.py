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