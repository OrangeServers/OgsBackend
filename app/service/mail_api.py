from app.foo.user.user import CheckMail
from app.foo.mail.MailApi import OrangeMailApi
from app.tools.at import ogs_auth_token


# 用户相关邮件接口
@ogs_auth_token
def mail_send_user():
    orange = CheckMail()
    return orange.send()


# 自由发送邮件接口
def mail_send():
    orange = OrangeMailApi()
    return orange.send()
