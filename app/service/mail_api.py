from app.foo.user.user import CheckMail
from app.foo.mail.MailApi import OrangeMailApi


# 用户相关邮件接口
def mail_send_user():
    orange = CheckMail()
    return orange.send()


# 自由发送邮件接口
def mail_send():
    orange = OrangeMailApi()
    return orange.send()
