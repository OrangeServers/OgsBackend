import smtplib
from email.mime.text import MIMEText
from email.header import Header
from app.conf.conf import MAIL_CONF


# 发送电子邮件
class SendMail:
    def __init__(self, form_mail, password, smtp_server):
        """
        form_mail-->发送端配置的邮箱名,str类型
        password-->发送端配置的邮箱密码,str类型
        smtp_server-->使用的邮件服务器地址,str类型
        """
        self.form_mail = form_mail
        self.password = password
        self.smtp_server = smtp_server
        self.smtp = smtplib.SMTP()

    def send(self, to_mail, to_send, header, message):
        """
        to_mail-->发送到目的邮箱的邮箱名,str类型
        to_send-->指定发送的名称,str类型
        header-->发送的邮箱标题,str类型
        message-->发送的邮件内容信息,str类型
        """
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = Header(to_send)
        msg['To'] = Header(to_mail)
        msg['Subject'] = Header(header)
        self.smtp.connect(self.smtp_server, 25)
        self.smtp.login(self.form_mail, self.password)
        self.smtp.sendmail(self.form_mail, to_mail, msg.as_string())
        self.smtp.quit()


if __name__ == "__main__":
    sendmail = SendMail(MAIL_CONF['form_mail'], MAIL_CONF['password'], MAIL_CONF['smtp_server'])
    sendmail.send('18301022797@163.com', 'orange', '测试', '这是一封测试邮件')
