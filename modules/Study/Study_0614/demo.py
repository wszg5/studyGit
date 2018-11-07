# coding:utf-8
import imaplib
import smtplib

import sys
from imaplib import IMAP4
from poplib import POP3
import re

reload(sys)
sys.setdefaultencoding( 'utf-8' )

# mail_text = 'From: "=?gb18030?B?xeW3sg==?=" <2099513152@qq.com>'
# result1 = re.search(r'From:.*[a-zA-Z0-9]+@(qq)?(foxmail)?\.com',mail_text)
# if result1:
#     result1 = result1.group(0)
#     result = re.search(r'[a-zA-Z0-9]+@(qq)?(foxmail)?\.com',result1)
#     print result.group(0)



# try:
#     server = POP3( "pop.wo.cn", 110 )  # 发件人邮箱中的SMTP服务器，端口是25
#     server.login( "20002189221@wo.cn", 'sohSOH845SO' )  # 括号中对应的是发件人邮箱账号、邮箱密码
#     # server.quit( )  # 这句是关闭连接的意思
# except Exception,e:
#     print e
    # r = e.args[1]
    # r = str(e)
    # r = r.replace("(535, 'Error: ",'').replace(": http://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256')","")
    # print r.decode("gbk")
# 账户密码
email='20002189221@wo.cn'
password='sohSOH845SO'

# 链接邮箱服务器
conn = imaplib.IMAP4("imap.wo.cn", 143)
# 登录
conn.login(email,password)
# 收邮件
INBOX = conn.select("INBOX")
# 全部邮件
type, data = conn.search(None, 'ALL')
# # 邮件列表
msgList = data[0].split()
# # 最后一封
# last = msgList[len(msgList) - 1]
# # 取最后一封
# type, datas = conn.fetch(last, '(RFC822)')
# #把取回来的邮件写入txt文档
# with open('email.txt','w')as f:
#     f.write(datas[0][1].decode('utf-8'))
# datas = []
for i in range(1,len(msgList)):
    ty, datas = conn.fetch(i, '(RFC822)')
    mail_text = datas[0][1]
    result1 = re.search( r'From:.*[a-zA-Z0-9]+@(qq)?(foxmail)?\.com', mail_text )
    if result1:
        result1 = result1.group( 0 )
        result = re.search( r'[a-zA-Z0-9]+@(qq)?(foxmail)?\.com', result1 )
        print result.group(0)

    # with open( 'email.txt', 'a' )as f:
    #     try:
    #         f.write( datas[0][1].decode( 'utf-8' ) )
    #     except Exception,e:
    #         print e
