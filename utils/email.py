import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email(object):
    def __init__(self):
        self.__subject = None
        self.__body = None
        self.__sender = None
        self.__recipients = ''
        self.__cc = ''
        self.__password = None

    def subject(self, subject=''):
        self.__subject = subject
        return self

    def body(self, body=''):
        self.__body = body
        return self

    def sender(self, sender=''):
        self.__sender = sender
        return self

    def recipients(self, recipients=None):
        self.__recipients = recipients
        return self

    def password(self, password=''):
        self.__password = password
        return self

    def send(self):
        msg = MIMEMultipart()
        msg['Subject'] = self.__subject
        msg['From'] = self.__sender
        msg['To'] = ', '.join(self.__recipients)
        msg.attach(MIMEText(self.__body, 'html'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(self.__sender, self.__password)
            smtp_server.sendmail(self.__sender, [self.__recipients, self.__cc], msg.as_string())
