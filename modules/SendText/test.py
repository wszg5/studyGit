# -*- coding:utf-8 -*-
import smtplib
import os
import logging

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger("django")

class EmailHandler(object):
    def __init__(self, smtpserver, user, pwd):
        self.smtp = smtplib.SMTP()
        self.smtpserver = smtpserver
        self.smtpuser = user
        self.smtppwd = pwd

    def generateAlternativeEmailMsgRoot(self, strFrom, listTo, listCc, strSubJect, strMsgText, strMsgHtml, listImagePath):
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = strSubJect
        msgRoot['From'] = strFrom
        msgRoot['To'] = ",".join(listTo)
        if listCc:
            msgRoot['Cc'] = ",".join(listCc)
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgContent = strMsgText.replace("\n","<br>") if strMsgText else ""
        msgContent += "<br>" + strMsgHtml if strMsgHtml else ""

        # We reference the image in the IMG SRC attribute by the ID we give it below
        if listImagePath and len(listImagePath)>0:
            msgHtmlImg = msgContent + "<br>"
            for imgcount in range(0, len(listImagePath)):
                msgHtmlImg += '<img src="cid:image{count}"><br>'.format(count=imgcount)
            msgText = MIMEText(msgHtmlImg, 'html')
            msgAlternative.attach(msgText)
            # print(msgHtmlImg)

            # This example assumes the image is in the current directory
            for i,imgpath in enumerate(listImagePath):
                fp = open(imgpath, 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()

                # Define the image's ID as referenced above
                msgImage.add_header('Content-ID', '<image{count}>'.format(count=i))
                msgRoot.attach(msgImage)
        else:
            msgText = MIMEText(msgContent, 'html')
            msgAlternative.attach(msgText)

        return msgRoot

    # Send the email (this example assumes SMTP authentication is required)
    def sendemail(self, strFrom, listTo, strSubJect, strMsgText, strMsgHtml=None, listImagePath=None, listCc=None):
        msgRoot = self.generateAlternativeEmailMsgRoot(strFrom, listTo, listCc, strSubJect, strMsgText, strMsgHtml, listImagePath)

        try:
            self.smtp = smtplib.SMTP()
            self.smtp.connect(self.smtpserver)
            self.smtp.login(self.smtpuser, self.smtppwd)
            if listCc:
                listTo = listTo + listCc
            self.smtp.sendmail(strFrom, listTo, msgRoot.as_string())
            self.smtp.quit()
            logger.info("Send mail success {0}".format(strSubJect))
        except Exception as e:
            logging.exception("s")
            logger.error("ERROR:Send mail failed {0} with {1}".format(strSubJect, str(e)))

if __name__ == "__main__":
    smtpserver = 'smtp.wo.cn'
    smtpport = 465
    username = '20003645550@wo.cn'
    password = 'otiOTI436OT'
    strFrom = '20003645550@wo.cn'
    strTo = ['2351382894@qq.com']
    strCc = ['2351382894@qq.com']
    strSubJect = 'test email - text with image'
    eh = EmailHandler(smtpserver,username,password)
    imgpath = "/home/zunyun/text/img/test.png"
    imgpath2 = "/home/zunyun/text/img/test02.png"
    # eh.sendemail(strFrom,strTo,"text mail","Hi it's Max, this is a test maill-----1","<h2>test html content</h2>")
    eh.sendemail(strFrom,strTo,"image mail","Hi it's Max,\n this is a test maill-----2","<h2>test html content</h2>", [imgpath,imgpath2], listCc=strCc)
    # eh.sendemail(strFrom,strTo,"image mail","Hi it's Max, this is a test maill-----2",listImagePath=[imgpath])