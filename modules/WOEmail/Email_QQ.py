# coding:utf-8
from __future__ import division
import base64
import logging
import socket
import urllib2


import os, time, datetime, random
import sys
import smtplib  #加载smtplib模块
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from threading import  Timer


# sys.path.append("C:\TaskConsole-master")
# from IPChange import IPChange
from Repo import *
# from Timeout import timelimited

class Email_QQ:
    def __init__(self):
        self.repo = Repo()
        # self.ipChange = IPChange()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 1000)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum)
        uniqueNum = str(randomNum) + str(nowTime)
        return uniqueNum

    def getargs(self):
        # asdlFile = open(r"C:\asdl.txt", "r")
        asdlFile = open( r"/home/zunyun/text/asdl.txt", "r" )
        asdlList = asdlFile.readlines()
        if len(asdlList) > 2:
            specifiedTaskId = int(asdlList[2])
            taskList = self.repo.GetSpecifiedPhantomJSTask(specifiedTaskId, "smtpemail_task")
        else:
            taskList = self.repo.GetPhantomJSTaskInfo("smtpemail_task")
            while len(taskList) == 0:
                print u"检查是否有任务可运行"
                time.sleep(30)
                taskList = self.repo.GetPhantomJSTaskInfo("smtpemail_task")

        task = taskList[random.randint(0, len(taskList)) - 1]
        phonenumber = task["phonenumber"]
        cateId = task["cateId"]
        repo_theme_cateId = task["x01"]
        repo_message_cateId = task["x02"]
        repo_name_cateId = task["x07"]
        repo_number_cate_id = task["x03"]
        repo_account_cate_id = task["x08"]
        repo_bcc_cate_id = task["x09"]
        loopNumber = task["x10"]
        loopBcc = task["x11"]
        imgUrl = task["x12"]
        my_userCount = task["x13"]
        bccCount = task["x14"]
        sendCount = task["x15"]
        if sendCount is None or sendCount == '' or sendCount == 0:
            print u"发送次数没有设置或设置为0了,使用默认发送次数2"
            sendCount = 2
        else:
            sendCount = int(sendCount)

        if imgUrl is None or imgUrl == '':
            imgpath = ""
        else:
            imgpath = o.getImg(imgUrl)

        if my_userCount is None or my_userCount == "" or my_userCount == 0 or my_userCount == "0":
            my_userCount = 0
        else:
            my_userCount = int(my_userCount)

        if bccCount is None or bccCount == "":
            bccCount = 0
        else:
            bccCount = int(bccCount)

        if my_userCount==0 and bccCount==0:
            print u"不能没有收件人,请到公网上修改邮件任务信息"
            time.sleep(150)
            return
        while True:
            paramList = self.repo.GetPhantomJSParamInfo("smtpemail_param")
            if len(paramList) == 0:
                time.sleep(30)
                continue
            else:
                break

        param = paramList[random.randint(0, len(paramList)) - 1]

        emailType = param["x01"]

        args = {"repo_account_cate_id": repo_account_cate_id, "repo_number_cate_id": repo_number_cate_id,
                "repo_theme_cateId": repo_theme_cateId,
                "repo_message_cateId": repo_message_cateId, "repo_bcc_cate_id": repo_bcc_cate_id,
                "my_userCount": my_userCount, "bccCount": bccCount,
                "emailType": "QQ邮箱", "repo_name_cateId": repo_name_cateId, "loopNumber": loopNumber,
                "loopBcc": loopBcc, "imgpath": imgpath, "sendCount": sendCount,"cateId":cateId,"phonenumber":phonenumber}  # cate_id是仓库号，length是数量
        return args

    def getImg(self,html):
        listImg = html.split( "/" )
        while listImg == [] or listImg is None:
            print "请检查附件链接地址是否正确，等100秒再看连接是否正确"
            time.sleep( 100 )
            listImg = html.split( "/" )
        imgName = listImg[len( listImg ) - 1]
        imgpath = r"C:\images"
        if not os.path.exists(imgpath ):
            os.mkdir( imgpath )
        if not os.path.exists(imgpath+ '/%s'%imgName ):
            g = os.walk( imgpath )
            for path, d, filelist in g:
                for filename in filelist:
                    # print os.path.join(path, filename)
                    os.remove(os.path.join(path, filename))
            imgpath = imgpath + "/%s" % imgName
            urllib.urlretrieve( html, imgpath )
            return imgpath
        else:
            return None

    # @timelimited(60)
    def send(self,message,my_sender,password,my_user,theme,bcc,name,imgpath):
        ret = True
        try:
            # bcc = bcc + ['1002494035@qq.com']     #测试用的
            msg = MIMEMultipart( 'related' )
            msg['From'] = formataddr( [name, my_sender] )  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            # msg['From'] = Header( name, 'utf-8' )
            # msg['From'].append( my_sender, 'utf-8' )

            # msg['To']=formataddr(["",my_user])   #括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['To'] = ', '.join( my_user )
            msg['Subject'] = theme  # 邮件的主题，也可以说是标题
            if bcc!= []:
                msg['Bcc'] = ', '.join( bcc )

            msg['Accept-Language'] = 'zh-CN'
            msg['Accept-Charset'] = 'ISO-8859-1,utf-8'

            msgAlternative = MIMEMultipart( 'alternative' )
            msg.attach( msgAlternative )
            msgAlternative.attach( MIMEText( message, 'html', 'utf-8' ) )
            if imgpath!="":
                jpgpart = MIMEApplication(
                    open( imgpath ).read( ), "rb" )
                jpgpart.add_header( 'Content-Disposition', 'attachment', filename="%s.png" % self.GetUnique( ) )
                msg.attach( jpgpart )

            # serverArr = my_sender.split("@")
            # if len(serverArr)>0:
            #     my_server = serverArr[1]

            server = smtplib.SMTP( "smtp.qq.com", 25 )  # 发件人邮箱中的SMTP服务器，端口是25
            # server.login( my_sender, password )  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.login( "2351382894@qq.com", "wuzhou455854284" )  # 括号中对应的是发件人邮箱账号、邮箱密码
            listMyUsers = my_user + bcc
            server.sendmail( my_sender, listMyUsers, msg.as_string( ) )  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit( )  # 这句是关闭连接的意思
            print u"%s 发送成功 给 %s ,密送号码为%s" % (my_sender, my_user,bcc)  # 发送成功，稍等20秒左右就可以收到邮件
            return None
        except Exception, e:  # 如果try中的语句没有执行，则会执行下面的ret=False
            print u"%s 发送失败 给 %s,密送号码为%s" % (my_sender, my_user,bcc)
            try:
                server.quit( )  # 这句是关闭连接的意思
            except:
                pass
            return e

    def sendProcess(self):
        try:
            count = 0
            changeCount = 0
            while True:
                args = self.getargs()
                repo_account_cate_id = args["repo_account_cate_id"]
                numbers = self.repo.GetAccount( "normal",repo_account_cate_id, 30, 1 )
                if len( numbers ) == 0:
                    print u"%s号仓库没有数据,等待5分钟" % repo_account_cate_id
                    time.sleep(300)
                    return

                if changeCount >= 5:
                    # self.ipChange.ooo()
                    # self.ipChange.ooo()
                    time.sleep(5)
                    changeCount = 0

                account = numbers[0]['number'] + "@qq.com"  # 即将登陆的号
                password = numbers[0]['password']

                my_sender = account # 发件人邮箱账号，为了后面易于维护，所以写成了变量
                args = self.getargs()
                sendCount = args["sendCount"]
                my_userCount = args["my_userCount"]
                repo_number_cate_id = args["repo_number_cate_id"]
                for i in range( 0, sendCount ):
                    if my_userCount != 0:
                        emailnumbers = self.repo.GetNumber( repo_number_cate_id, 0, my_userCount )  # 取出没有用过的号码
                        while len( emailnumbers ) == 0:
                            loopNumber = args["loopNumber"].encode( "utf-8" )
                            if loopNumber == "true" or loopNumber is True:
                                print u"%s 号仓库没有数据可用,自动恢复循环取" % repo_number_cate_id
                                path = "/repo_api/receive/emptyCate?cate_id=%s" % (
                                    repo_number_cate_id)
                                conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                conn.request( "GET", path )
                                time.sleep( 5 )
                                emailnumbers = self.repo.GetNumber( repo_number_cate_id, 0, my_userCount )
                            else:
                                print u"%s号仓库没有数据" % repo_number_cate_id
                                # time.sleep( 150 )
                                # return
                    else:
                        emailnumbers = []
                    args = self.getargs()
                    bccCount = args["bccCount"]
                    if bccCount != 0:
                        repo_bcc_cate_id = args["repo_bcc_cate_id"]
                        bccs = self.repo.GetNumber( repo_bcc_cate_id, 0, bccCount )  # 取出add_count条两小时内没有用过的号码
                        while len( bccs ) == 0:
                            loopBcc = args["loopBcc"].encode( "utf-8" )
                            if loopBcc == "true" or loopBcc is True:
                                print u"%s 号仓库没有数据可用,自动恢复循环取" % repo_bcc_cate_id
                                path = "/repo_api/receive/emptyCate?cate_id=%s" % (
                                    repo_bcc_cate_id)
                                conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                conn.request( "GET", path )
                                time.sleep( 5 )
                                bccs = self.repo.GetNumber( repo_bcc_cate_id, 0, bccCount )
                            else:
                                print u"%s号仓库没有数据" % repo_bcc_cate_id
                                # time.sleep( 300 )
                                # return
                    else:
                        bccs = []

                    if bccs==[] and emailnumbers==[]:
                        print u"收件箱没有数据,请到公网上修改邮件任务参数信息"
                        time.sleep(300)
                        return

                    bcc = []
                    args = self.getargs()
                    emailType = args["emailType"]
                    for item in bccs:
                        if item!="\n" and item!="":
                            itemNumber = item['number'].encode("utf-8").replace("\n", "")
                        else:
                            continue
                        if r"\xef\xbb\xbf" in itemNumber:
                            itemNumber2.replace("\xef\xbb\xbf","")
                        if "@" not in itemNumber:
                            if emailType == "QQ邮箱":
                                itemNumber = itemNumber + "@qq.com"
                            elif emailType == "189邮箱":
                                itemNumber = itemNumber + "@189.cn"
                            elif emailType == "139邮箱":
                                itemNumber = itemNumber + "@139.com"
                            elif emailType == "163邮箱":
                                itemNumber = itemNumber + "@163.com"
                            elif emailType == "wo邮箱":
                                itemNumber = itemNumber + "@wo.cn"
                            else:
                                itemNumber = itemNumber + "@qq.com"

                        bcc.append(itemNumber)

                    my_user = []
                    for item in emailnumbers:
                        if item!="\n" and item!="":
                            itemNumber2 = item['number'].encode("utf-8").replace("\n", "")
                        else:
                            continue
                        if r"\xef\xbb\xbf" in itemNumber2:
                            itemNumber2.replace("\xef\xbb\xbf","")

                    # my_user = emailnumbers[0]['number'].encode("utf-8")  # 收件人邮箱账号

                        if "@" not in itemNumber2:
                            if emailType == "QQ邮箱":
                                itemNumber2 = itemNumber2 + "@qq.com"
                            elif emailType == "189邮箱":
                                itemNumber2 = itemNumber2 + "@189.cn"
                            elif emailType == "139邮箱":
                                itemNumber2 = itemNumber2 + "@139.com"
                            elif emailType == "163邮箱":
                                itemNumber2 = itemNumber2 + "@163.com"
                            elif emailType == "wo邮箱":
                                itemNumber2 = itemNumber2 + "@wo.cn"
                            else:
                                itemNumber2 = itemNumber2 + "@qq.com"

                        my_user.append(itemNumber2)

                    # my_user = "2351382894@qq.com"   #测试使用
                    args = self.getargs()
                    repo_theme_cateId = args["repo_theme_cateId"]
                    if repo_theme_cateId == "" or repo_theme_cateId is None:
                        theme = ""
                    else:
                        Material = self.repo.GetMaterial( repo_theme_cateId, 0, 1 )
                        if len( Material ) == 0:
                            print u"%s  号仓库为空，没有取到消息" % repo_theme_cateId
                            time.sleep(100)
                            return
                        theme = Material[0]['content']
                    args = self.getargs()
                    repo_message_cateId = args["repo_message_cateId"]
                    if repo_message_cateId == "" or repo_message_cateId is None:
                        message = ""
                    else:
                        Material2 = self.repo.GetMaterial( repo_message_cateId, 0, 1 )
                        if len( Material2 ) == 0:
                            print u"%s号仓库为空，没有取到消息" % repo_message_cateId
                            time.sleep(100)
                            return
                        message = Material2[0]['content'].encode("utf-8")
                    args = self.getargs()
                    repo_name_cateId = args["repo_name_cateId"]

                    if repo_name_cateId == "" or repo_name_cateId is None:
                        name = ""
                    else:
                        Material3 = self.repo.GetMaterial( repo_name_cateId, 0, 1 )
                        if len( Material3 ) == 0:
                            print u"%s号仓库为空，没有取到消息" % repo_name_cateId
                            time.sleep(100)
                            return
                        name = Material3[0]['content'].encode("utf-8")
                    args = self.getargs()
                    imgpath = args["imgpath"]
                    # my_user = []
                    try:
                        e = self.send(message, my_sender, password, my_user, theme, bcc, name, imgpath)
                    except Exception, e:
                        pass
                    # signal.alarm( 0 )
                    if e != None:
                        print e
                        ex = ""
                        if len(e.args) > 1:
                            ex = e.args[1]
                        else:
                            ex = str(e)
                        if ex != "":
                            changeCount += 1
                            if "authentication failed" in ex:
                                print u"帐号或密码错误"
                                path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                    repo_account_cate_id, "exception", account, "", "")
                                conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                                conn.request("GET", path)
                            elif "Connection timed out" in ex:
                                print u"连接超时"
                            elif "timeout for" in ex:
                                print u"超时了"
                            elif "Connection unexpectedly closed" in ex:
                                print u"连接意外关闭"
                            elif "The email message was detected as spam" in ex:
                                print u"可能ip黑了"
                                # self.ipChange.ooo()
                                # self.ipChange.ooo()
                                time.sleep(5)
                            elif "5.7.1 Too many spam messages sent" in ex:
                                print u"可能ip黑了"
                                # self.ipChange.ooo()
                                # self.ipChange.ooo()
                                time.sleep(5)
                            elif "5.7.1 Too many messages sent" in ex:
                                print u"可能达到上限了"
                            else:
                                print u"暂时没遇到"
                        else:
                            if type(e) == smtplib.SMTPServerDisconnected:
                                print u"连接意外关闭"
                        for item in bcc:
                            it = item[:-7]
                            path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                it, repo_bcc_cate_id, "normal")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                            time.sleep(0.5)
                        for item in my_user:
                            it2 = item[:-7]
                            path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                it2, repo_number_cate_id, "normal")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                            time.sleep( 0.5 )
                        break
                    else:
                        changeCount = 0
                time.sleep( 3 )
                if changeCount >= 5:
                    # self.ipChange.ooo()
                    # self.ipChange.ooo()
                    time.sleep(5)
                    changeCount = 0
        except:
            logging.exception("exception")

    def action(self):
        # data = self.ipChange.Check_for_Broadband()
        # if data != None:
        #     print u"宽带确认已连接,模块继续运行"
        # else:
        #     print u"宽带未连接,连接宽带"
        #     self.ipChange.ooo()
        #     time.sleep(5)
        x = self.sendProcess()
        if x == "false":
            sta = "normal"
        else:
            sta = "stopped"
        args = self.getargs()
        phonenumber = args["phonenumber"]
        cateId = args["cateId"]
        para = {"phoneNumber": phonenumber, "x_04": sta}
        self.repo.PostInformation(cateId, para)



def getPluginClass():
    return Email_QQ

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()
    # time.sleep(100)

    # url = "http://seopic.699pic.com/photo/50030/5545.jpg_wh1200.jpg"
    # imgpath = o.getImg(url)

    while True:
        try:
            o.action()
        except:
            logging.exception("Exception")

