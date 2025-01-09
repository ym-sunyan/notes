#coding:utf-8
#python:3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header

import win_unicode_console
win_unicode_console.enable()

class SendEmailC(object):
    '''利用email发送不同格式的邮件
    邮件实现的邮件类型：文本类型，超链接类型， 带附件类型'''
    #基本内容：发送者， 接收者，标题，内容
    def __init__(self, from_=None, to_=None, cc_=None, title=None, email_info=None):
        self.from_ = from_
        self.to_ = to_
        self.cc_ = cc_
        self.title = title
        self.email_info = email_info
        pass

    def Check(self):
        '''检查重要参数'''
        if self.from_ == None or self.from_ == "":
            print("邮件无发送者")
            exit()
        if self.to_ == None or self.to_ == []:
            print("邮件无接收者")
            exit()
        if self.title == None:
            print("邮件无标题")
        if self.email_info == None or self.email_info == "":
            print("邮件无正文")

    def Set(self, from_=None, to_=None, cc_=None, title=None, email_info=None):
        '''重新设定邮件的所有基础信息'''
        if from_ != None:
            self.from_ = from_

        if to_ != None:
            self.to_ = to_
        
        if cc_ != None:
            self.cc_ = cc_

        if title != None:
            self.title = title

        if email_info != None:
            self.email_info = email_info

    def AddRecipient(self, *recipient_list):
        '''增加接收邮件的人'''
        for recipient in recipient_list:
            self.to_.append(recipient)

    def DelRecipient(self, *recipient_list):
        '''删除一个或者多个邮件接收者'''
        for recipient in recipient_list:
            if recipient in self.to_:
                self.to_.remove(recipient)
        if len(self.to_) == 0:
            print("邮件无接收者")

    def OutAllRecipient(self):
        '''返回所有的邮件接收者'''
        return self.to_

    def SendEmailBase(self, message):
        '''邮件发送'''
        try:
            smtpObj = smtplib.SMTP("smtphost.qualcomm.com",timeout=120)
            # smtpObj = smtplib.SMTP("smtp-mail.outlook.com", timeout=120)
            smtpObj.sendmail(self.from_, self.to_, message.as_string())
            print("send ok")
        except smtplib.SMTPException:
            print("Error: send error")

    # def BaseInfo(self, message):
    #     '''邮件内容组织'''
    #     message['From'] = Header(self.from_, 'utf-8')
    #     for t in self.to_:
    #         message['To'] = Header(t, 'utf-8')
    #     message['Subject'] = Header(self.title, 'utf-8')
    #     return message
    def BaseInfo(self, message):
        '''邮件内容组织'''
        message['From'] = Header(self.from_)
        for t in self.to_:
            message['To'] = Header(t)
        for t in self.cc_:
            message['Cc'] = Header(t)
        message['Subject'] = Header(self.title, 'utf-8')
        return message

    def SendEamilText(self):
        '''发送文本邮件'''
        self.Check()
        message = MIMEText(self.email_info, 'plain', 'utf-8')
        message = self.BaseInfo(message)
        self.SendEmailBase(message)

    def SendEmailLink(self):
        '''发送超链接邮件'''
        self.Check()
        message = MIMEText(self.email_info, 'html', 'utf-8')
        message = self.BaseInfo(message)
        self.SendEmailBase(message)

    def SendEmailEnclosure(self, imageFile_list):
        '''发送附件邮件'''
        self.Check()
        message = MIMEMultipart()
        message = self.BaseInfo(message)
        message.attach(MIMEText(self.email_info, 'plain', 'utf-8'))

        # 添加附件
        for imageFile in imageFile_list:
            imageApart = MIMEImage(open(imageFile, 'rb').read(), imageFile.split('.')[-1])
            imageFile = os.path.split(imageFile)[1]
            imageApart.add_header('Content-Disposition', 'attachment', filename=imageFile)
            message.attach(imageApart)

        self.SendEmailBase(message)

# from_ = 'c_yansun@qti.qualcomm.com'
# to_ = ['c_yansun@qti.qualcomm.com']
# title = 'test web kba'
# email_info = None

# sec = SendEmailC(from_, to_, title, email_info)
# mail_msg = "this is test "
# sec.Set(title="test test test", email_info=mail_msg)
# # sec.SendEamilText()
# sec.SendEmailLink()


