from flask import request, jsonify
from app.tools.sendmail import SendMail
from app.conf.conf import MAIL_CONF


class OrangeMailApi:
    def __init__(self):
        self.sendmail = SendMail(MAIL_CONF['form_mail'], MAIL_CONF['password'], MAIL_CONF['smtp_server'])
        self.to_amil = request.values.get('to_mail')
        self.header = request.values.get('header')
        self.message = request.values.get('message')

    def send(self):
        try:
            self.sendmail.send(self.to_amil, 'OrangeServer', self.header, self.message)
            return jsonify({'send_status': 'true'})
        except Exception:
            return jsonify({'send_status': 'fail'})
