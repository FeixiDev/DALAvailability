import smtplib
from email.mime.text import MIMEText
from email.header import Header

class STMPEmail(object):

    def __init__(self,receivers,
                 message1 = '',
                 message2 = ''):
        self.mail_host = ''
        self.mail_user = ''
        self.mail_pass = ''
        self.sender = ''
        self.receivers = receivers
        self.message1 = message1
        self.message2 = message2


    def connect_stmp(self):
        """
        STMP连接
        """
        try:
            smtpobj = smtplib.SMTP()
            smtpobj.connect(self.mail_host, 25)
        except:
            print("Failed to connect smtp server!")
            return False

        try:
            smtpobj.login(self.mail_user, self.mail_pass)
        except:
            print("User or password is wrong")
            return False

        return smtpobj





    def send_succeed(self):
        """
        测试成功，发送邮件
        """
        smtpobj = self.connect_stmp()
        message = MIMEText(self.message1, 'plain', 'utf-8')
        message['From'] = Header("VersaTST", 'utf-8')
        message['To'] = Header("接收方", 'utf-8')

        subject = 'The test of VersaTST'
        message['Subject'] = Header(subject, 'utf-8')
        try:
          smtpobj.sendmail(self.sender, self.receivers, message.as_string())
        except smtplib.SMTPSenderRefused:
            print('mail from address must be same as authorization user')
        smtpobj.quit()


    def send_fail(self):
        """
        测试失败，发送邮件
        """
        smtpobj = self.connect_stmp()
        message = MIMEText(self.message2, 'plain', 'utf-8')
        message['From'] = Header("VersaTST", 'utf-8')

        message['To'] = ','.join(self.receivers)

        subject = 'The test of VersaTST'
        message['Subject'] = Header(subject, 'utf-8')
        try:
          smtpobj.sendmail(self.sender, self.receivers, message.as_string())
        except smtplib.SMTPSenderRefused:
            print('mail from address must be same as authorization user')
        smtpobj.quit()