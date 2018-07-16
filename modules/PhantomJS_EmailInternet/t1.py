#coding:utf-8   #强制使用utf-8编码格式
import email
import mimetypes
import os
import random
import smtplib
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

import logging

import time

import datetime
from email.utils import formataddr

from timeout_decorator import timeout_decorator

from Repo import Repo


def GetUnique():
    nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )  # 生成当前时间
    randomNum = random.randint( 0, 1000 )  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str( 00 ) + str( randomNum )
    uniqueNum = str( nowTime ) + str( randomNum )
    return uniqueNum
@timeout_decorator.timeout( 50 )
def mail():
    ret=True
    numbers = Repo().GetAccount( "304", 30, 1 )
    if len( numbers ) == 0:
        print u"%s号仓库没有数据,等待5分钟" % 304
        time.sleep( 300 )
        return

    account = numbers[0]['number']  # 即将登陆的帐号
    password = numbers[0]['password']
    # password = "sihSIH221SI"
    my_sender = account  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
    # my_user=['2351382894@qq.com',"1003629707@qq.ocm"] #收件人邮箱账号，为了后面易于维护，所以写成了变量
    my_user = '455854284@qq.com'
    bcc = ['2351382894@qq.com']

    mail_msg = """
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <p>Python 邮件发送测试...</p>
        <p><a href="http://zunyun.net/">尊云群控</a></p>
        <p><img src="cid:image1"></p>
        """

    try:
        msg = MIMEMultipart( 'related' )
        msg['From']=formataddr(["zg",my_sender])   #括号里的对应发件人邮箱昵称、发件人邮箱账号
        # msg['To']=formataddr(["",my_user])   #括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = ', '.join( my_user )
        msg['Subject']=GetUnique() #邮件的主题，也可以说是标题
        msg['Bcc'] = ', '.join( bcc )

        msgAlternative = MIMEMultipart( 'alternative' )
        msg.attach( msgAlternative )
        msgAlternative.attach( MIMEText( mail_msg, 'html', 'utf-8' ) )

        file_name = "/home/zunyun/workspace/TaskConsole/modules/PhantomJS_EmailInternet/coding.png"
        jpgpart = MIMEApplication(
            open( file_name ).read( ),"rb" )
        jpgpart.add_header( 'Content-Disposition','attachment', filename="%s.png"%GetUnique() )
        msg.attach( jpgpart )

        server = smtplib.SMTP( "smtp.wo.cn", 25 )  # 发件人邮箱中的SMTP服务器，端口是25

        server.login( my_sender, password )  # 括号中对应的是发件人邮箱账号、邮箱密码

        # listMyUsers = my_user + bcc
        listMyUsers = my_user
        server.sendmail(my_sender,listMyUsers,msg.as_string())   #括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        # server.quit()   #这句是关闭连接的意思
        print u"%s 发送成功 给 %s" % (my_sender, my_user)  # 发送成功，稍等20秒左右就可以收到邮件
    except Exception, e:  # 如果try中的语句没有执行，则会执行下面的ret=False
        # logging.exception( "Exception Logged" )
        print e
        # print type(e)
        print u"%s 发送失败 给 %s" % (my_sender, my_user)
        ex =str(e)
        # if len(e.args)>1:
        #     ex = e.args[1]
        # print ex
        if ex!="":
            if "The email message was detected as spam" in ex:
                print u"进垃圾箱了"
            elif "5.7.1 Too many spam messages sent" in ex:
                print u"可能ip黑了"
            elif "Timed Out" in ex:
                print u"超时了"
            elif "554, '5.7.1 Access denied" in ex:
                print u"拒绝访问"
            elif "5.7.1 Too many messages sent" in ex:
                print u"可能达到上限了"
            elif "The email message was detected as spam" in ex:
                print u"进垃圾箱了"
            elif "Connection unexpectedly closed" in ex:
                print u"连接意外关闭"
            else:
                print u"暂时没遇到"

        ret=False
    try:
        server.quit( )
    except:
        pass
    return ret

while True:
    ret=mail()
    if ret:
        print "ok" #如果发送成功则会返回ok，稍等20秒左右就可以收到邮件
    else:
        print "filed"  #如果发送失败则会返回filed


