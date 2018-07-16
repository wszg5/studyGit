# coding:utf-8
from __future__ import division
import base64
import httplib
import logging
import poplib
import socket
import urllib
import urllib2
import codecs

import os, time, datetime, random
import sys
import smtplib  # 加载smtplib模块
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from threading import Timer
from Repo import *
# sys.path.append("/home/zunyun/workspace/TaskConsole")



class GGO_SMTP:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        num = ""
        for i in range(0, random.randint(1, 8)):
            n = random.choice("qwertyuiopasdfghjklzxcvbnm")
            num = n + num
        for i in range(0, random.randint(1, 5)):
            n = random.choice("0123456789")
            num = num + n

        return num

    def deleteImg(self):
        imgpath = r"C:\water"
        g = os.walk(imgpath)
        for path, d, filelist in g:
            for filename in filelist:
                # print os.path.join(path, filename)
                os.remove(os.path.join(path, filename))

    def getTime(self, timeType):
        path = "/cgi-bin/cgi_svrtime"
        conn = httplib.HTTPConnection("cgi.im.qq.com", None, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        data = response.read().replace("\n", "")
        # if response.status == 200:
        #   data = response.read()
        # else:
        #   print u"http://cgi.im.qq.com/cgi-bin/cgi_svrtime 失效了"
        #  return ""
        timea = datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        if timeType == "EnTime":
            return timea.strftime("%a, %b %d,  %Y %I:%M %p")
        elif timeType == "CnTime":
            nt = timea
            w = ""
            weekday = nt.weekday()
            if weekday == 0:
                w = "星期一"
            elif weekday == 1:
                w = "星期二"
            elif weekday == 2:
                w = "星期三"
            elif weekday == 3:
                w = "星期四"
            elif weekday == 4:
                w = "星期五"
            elif weekday == 5:
                w = "星期六"
            elif weekday == 6:
                w = "星期日"
            p = nt.strftime("%p")
            if p == "PM" or p == "pm":
                p = "下午"
            else:
                p = "上午"

            nowtime = nt.strftime('%Y年%m月%d日%I:%M')
            nowtime = nowtime.replace("日", "日 (%s) %s" % (w, p))
            return nowtime
        else:
            return timea.strftime("%a, %b %d,  %Y %I:%M %p")

    def getIp(self):
        path = "/plain"
        conn = httplib.HTTPConnection("ipecho.net", None, timeout=30)
        conn.request("GET", path)
        time.sleep(3)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            return data
        else:
            return []

    def getPIC(self):
        imgName = self.GetUnique()
        imgpath = r"/home/zunyun/text/img"
        if not os.path.exists(imgpath):
            return ""
        g = os.listdir(imgpath)
        if len(g) == 0:
            return ""
        for i in g:
            name = i.split(".")
            os.rename(imgpath + "\%s" % i, imgpath + "\%s.%s" % (imgName, name[1]))
            imgpath = imgpath + "\%s.%s" % (imgName, name[1])
            return imgpath
        else:
            return ""

    def send(self, message, my_sender, password, my_user, theme, bcc, name, imgpath,fjFlag):
        ret = True
        try:
            # message = "hello +img+ asdf"
            message = message.replace("+FromMail+", my_sender)
            try:
                message = message.replace("+ToMail+", my_user[0])
            except:
                message = message.replace("+ToMail+", bcc[0])
            message = message.replace("+Subject+", theme)
            try:
                message = message.replace("+CnTime+", self.getTime("CnTime"), 10)
            except:
                pass
            try:
                message = message.replace("+EnTime+", self.getTime("EnTime"), 10)
            except:
                pass
            # if imgpath != None and imgpath != "":
            # my_user = ["1619125378@qq.com"]  # 测试用的
            my_user = ["1058653991@qq.com"]
            # bcc = ["1951380199@qq.com"]

            msg = MIMEMultipart('related')
            num = ""
            for i in range( 0, random.randint(4,30) ):
                n = random.choice( "1234567890" )
                num = n + num
            num = num + "@"
            ym = ["ggo.com","ggo.cn","ggo.org","ggo.la","ggo.net"]
            ym = num + ym[random.randint(0,len(ym)-1)]
            msg['From'] = formataddr([name, ym])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            # msg['From'] = name +" <" + my_sender +">"

            # msg['From'] = Header( my_sender, 'utf-8' )
            # msg['From'].append( my_sender, 'utf-8' )

            # msg['To']=formataddr(["",my_user])   #括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['To'] = ', '.join(my_user)
            msg['Subject'] = theme  # 邮件的主题，也可以说是标题
            if bcc != []:
                msg['Bcc'] = ', '.join(bcc)

            msg['Accept-Language'] = 'zh-CN'
            msg['Accept-Charset'] = 'ISO-8859-1,utf-8'
            msgAlternative = MIMEMultipart('alternative')
            msg.attach(msgAlternative)
            # listImagePath = ["C:\PIC\ezofv5477.jpg"]
            # message = "<a>测试中。。。</a>+img+"
            msgAlternative.attach(MIMEText(message, 'html', 'utf-8'))
            if fjFlag:
                if imgpath != "" and imgpath != None:
                    att1 = MIMEText(open(imgpath, 'rb').read(), 'base64', 'utf-8')
                    att1["Content-Type"] = 'application/octet-stream'
                    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                    att1["Content-Disposition"] = 'attachment; filename="%s.jpg"' % self.GetUnique()
                    msg.attach(att1)
            server = smtplib.SMTP("smtp.ggo.la", 25)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
            listMyUsers = my_user + bcc
            server.sendmail(my_sender, listMyUsers, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 这句是关闭连接的意思
            print u"%s 发送成功 给 %s ,密送号码为%s" % (my_sender, my_user, bcc)  # 发送成功，稍等20秒左右就可以收到邮件
            return None
        except Exception, e:  # 如果try中的语句没有执行，则会执行下面的ret=False
            # logging.exception("ds")
            print u"%s 发送失败 给 %s,密送号码为%s" % (my_sender, my_user, bcc)
            try:
                server.quit()  # 这句是关闭连接的意思
            except:
                pass
            return e

    def getImg(self, html):
        imgName = self.GetUnique()
        imgpath = r"/home/zunyun/text/img"
        if not os.path.exists(imgpath):
            return
        g = os.listdir(imgpath)
        if len(g) == 0:
            listImg = html.split("/")
            while listImg == [] or listImg is None:
                print "请检查附件链接地址是否正确，等100秒再看连接是否正确"
                time.sleep(100)
                listImg = html.split("/")
            imgName = listImg[len(listImg) - 1]
            imgpath = r"/home/zunyun/text/img"
            if not os.path.exists(imgpath):
                os.mkdir(imgpath)
            if not os.path.exists(imgpath + '/%s' % imgName):
                g = os.walk(imgpath)
                for path, d, filelist in g:
                    for filename in filelist:
                        # print os.path.join(path, filename)
                        os.remove(os.path.join(path, filename))
                imgpath = imgpath + "/%s" % imgName
                urllib.urlretrieve(html, imgpath)
                try:
                    g = os.listdir(imgpath)
                    if len(g) == 0:
                        return
                except:
                    pass
        for i in g:
            name = i.split(".")
            os.rename(imgpath + "\%s" % i, imgpath + "\%s.%s" % (imgName, name[1]))
            imgpath = imgpath + "\%s.%s" % (imgName, name[1])
            return imgpath
        else:
            return None

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
        sendTime = task["x12"]
        my_userCount = task["x13"]
        bccCount = task["x14"]
        sendCount = task["x15"]
        loopAccountNumber = task["x16"]
        myNumber = task["x17"]
        if loopAccountNumber == None or loopAccountNumber == "":
            loopAccountNumber = 1000
        else:
            loopAccountNumber = int(loopAccountNumber)
        if sendCount is None or sendCount == '' or sendCount == 0:
            print u"发送次数没有设置或设置为0了,使用默认发送次数2"
            sendCount = 2
        else:
            sendCount = int(sendCount)

        # if imgUrl is None or imgUrl == '':
        #     imgpath = ""
        # else:
        #     # imgpath = o.getImg(imgUrl)
        #     # imgpath = self.getPIC()
        #     imgpath = "a"
        if my_userCount is None or my_userCount == "" or my_userCount == 0 or my_userCount == "0":
            my_userCount = 0
        else:
            my_userCount = int(my_userCount)
        if bccCount is None or bccCount == "":
            bccCount = 0
        else:
            bccCount = int(bccCount)

        if my_userCount == 0 and bccCount == 0:
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
                "loopBcc": loopBcc, "sendTime": sendTime, "sendCount": sendCount, "cateId": cateId,
                "phonenumber": phonenumber
            , "loopAccountNumber": loopAccountNumber, "myNumber": myNumber}  # cate_id是仓库号，length是数量
        return args

    def sendProcess(self):
        try:
            count = 0
            changeCount = 0
            failCount = 0
            asdlFalg = False
            flag = True
            while True:
                args = self.getargs()
                loopAccountNumber = args["loopAccountNumber"]
                repo_account_cate_id = args["repo_account_cate_id"]
                numbers = self.repo.GetAccount("normal", repo_account_cate_id, 1440, 1)
                if len(numbers) == 0:
                    numbers = self.repo.GetAccount("normal", repo_account_cate_id, 1440, 1)
                    if len(numbers) == 0:
                        print u"%s号仓库没有数据,等待5分钟" % repo_account_cate_id
                        time.sleep(300)
                        return
                if failCount >= 3 and asdlFalg:
                    flag = True
                    asdlFalg = False
                    self.deleteImg()
                    failCount = 0

                if changeCount >= loopAccountNumber and asdlFalg:
                    flag = True
                    changeCount = 0
                    self.deleteImg()
                account = numbers[0]['number']  # 即将登陆的QQ号
                password = numbers[0]['password']

                changeCount += 1
                my_sender = account  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
                args = self.getargs()
                sendCount = args["sendCount"]
                my_userCount = args["my_userCount"]
                bccCount = args["bccCount"]

                for i in range(0, sendCount + 1):
                    emailnumbers = []
                    if my_userCount != 0 and i != sendCount:
                        args = self.getargs()
                        repo_number_cate_id = args["repo_number_cate_id"]
                        emailnumbers = self.repo.GetNumber(repo_number_cate_id, 0, my_userCount)  # 取出没有用过的号码
                        while len(emailnumbers) == 0:
                            loopNumber = args["loopNumber"].encode("utf-8")
                            if loopNumber == "true" or loopNumber is True:
                                print u"%s 号仓库没有数据可用,自动恢复循环取" % repo_number_cate_id
                                path = "/repo_api/receive/emptyCate?cate_id=%s" % (
                                    repo_number_cate_id)
                                conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                                conn.request("GET", path)
                                time.sleep(5)
                                emailnumbers = self.repo.GetNumber(repo_number_cate_id, 0, my_userCount)
                            else:
                                print u"%s号仓库没有数据" % repo_number_cate_id
                                # time.sleep( 150 )
                                break
                    else:
                        emailnumbers = []
                    bccs = []
                    if bccCount != 0 and i != sendCount:
                        args = self.getargs()
                        repo_bcc_cate_id = args["repo_bcc_cate_id"]
                        bccs = self.repo.GetNumber(repo_bcc_cate_id, 0, bccCount)  # 取出add_count条两小时内没有用过的号码
                        while len(bccs) == 0:
                            loopBcc = args["loopBcc"].encode("utf-8")
                            if loopBcc == "true" or loopBcc is True:
                                print u"%s 号仓库没有数据可用,自动恢复循环取" % repo_bcc_cate_id
                                path = "/repo_api/receive/emptyCate?cate_id=%s" % (
                                    repo_bcc_cate_id)
                                conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                                conn.request("GET", path)
                                time.sleep(20)
                                bccs = self.repo.GetNumber(repo_bcc_cate_id, 0, bccCount)
                            else:
                                print u"%s号仓库没有数据" % repo_bcc_cate_id
                                break
                                # time.sleep( 300 )
                                # return
                    else:
                        bccs = []

                    if bccs == [] and emailnumbers == [] and i != sendCount:
                        print u"收件箱没有设置 or 仓库没有数据,请到公网上修改邮件任务参数"
                        time.sleep(300)
                        return

                    myNumber = args["myNumber"]
                    thisMyNumbers = []
                    if myNumber == "" or myNumber is None:
                        pass
                    else:
                        thisMyNumbers = self.repo.GetNumber(myNumber, 0, 1)  # 取出add_count条两小时内没有用过的号码
                        if len(thisMyNumbers) == 0:
                            print u"%s号仓库没有数据" % myNumber

                    bcc = []
                    args = self.getargs()
                    emailType = args["emailType"]
                    # bcc = ["3192932338"]
                    for item in bccs:
                        if item != "\n" and item != "":
                            itemNumber = item['number'].replace("\n", "")
                        else:
                            continue
                        if r"\xef\xbb\xbf" in itemNumber:
                            itemNumber2.replace("\xef\xbb\xbf", "")
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
                    if i == sendCount and len(thisMyNumbers) > 0:
                        emailnumbers = thisMyNumbers
                    for item in emailnumbers:
                        codecs.BOM_UTF8
                        # my_user = emailnumbers[0]['number'].encode("utf-8")  # 收件人邮箱账号
                        if item != "\n" and item != "":
                            itemNumber2 = item['number'].encode("utf-8").replace("\n", "")
                        else:
                            continue
                        if r"\xef\xbb\xbf" in itemNumber2:
                            itemNumber2.replace("\xef\xbb\xbf", "")

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

                    # for ib in my_user:
                    #   print ib
                    # my_user = "2351382894@qq.com"   #测试使用

                    args = self.getargs()
                    repo_theme_cateId = args["repo_theme_cateId"]

                    if repo_theme_cateId == "" or repo_theme_cateId is None:
                        theme = ""
                    else:
                        Material = self.repo.GetMaterial(repo_theme_cateId, 0, 1)
                        if len(Material) == 0:
                            Material = self.repo.GetMaterial(repo_theme_cateId, 0, 1)
                            if len(Material) == 0:
                                print u"%s  号仓库为空，没有取到消息" % repo_theme_cateId
                                time.sleep(100)
                                return
                        theme = Material[0]['content']
                    args = self.getargs()
                    repo_message_cateId = args["repo_message_cateId"]
                    if repo_message_cateId == "" or repo_message_cateId is None:
                        message = ""
                    else:
                        Material2 = self.repo.GetMaterial(repo_message_cateId, 0, 1)
                        if len(Material2) == 0:
                            Material2 = self.repo.GetMaterial(repo_message_cateId, 0, 1)
                            if len(Material2) == 0:
                                print u"%s号仓库为空，没有取到消息" % repo_message_cateId
                                time.sleep(100)
                                return
                        message = Material2[0]['content'].encode("utf-8")
                    args = self.getargs()
                    repo_name_cateId = args["repo_name_cateId"]
                    if repo_name_cateId == "" or repo_name_cateId is None:
                        name = ""
                    else:
                        Material3 = self.repo.GetMaterial(repo_name_cateId, 0, 1)
                        if len(Material3) == 0:
                            Material3 = self.repo.GetMaterial(repo_name_cateId, 0, 1)
                            if len(Material3) == 0:
                                print u"%s号仓库为空，没有取到消息" % repo_name_cateId
                                time.sleep(100)
                                return
                        name = Material3[0]['content'].encode("utf-8")

                    args = self.getargs()
                    sendTime = self.getargs()["sendTime"]
                    if sendTime == None or sendTime == "":
                        time.sleep(1)
                    else:
                        sendTimeArr = sendTime.split("-")
                        try:
                            time_delayStart = int(sendTimeArr[0])
                            time_delayEnd = int(sendTimeArr[1])
                        except:
                            print  u"参数格式有误"
                            time_delayStart = 2
                            time_delayEnd = 4
                        try:
                            fj =  sendTimeArr[2].upper()
                        except:
                            fj = "Y"
                        if fj == "Y":
                            fjFlag = True
                        else:
                            fjFlag = False
                        try:
                            sleepStart = int(sendTimeArr[3])
                            sleepEnd = int(sendTimeArr[4])
                        except:
                            print  u"参数格式有误"
                            sleepStart = 30
                            sleepEnd = 60
                    imgpath = ""

                    try:
                        my_sender = "wuzhou21@ggo.la"
                        password = "13141314"
                        e = self.send(message, my_sender, password, my_user, theme, bcc, name, imgpath,fjFlag)
                    except Exception, e:
                        flag = False

                    time.sleep(random.randint(time_delayStart, time_delayEnd))
                    # signal.alarm( 0 )
                    asdlFalg = True
                    if e != None:
                        print e
                        ex = ""
                        if len(e.args) > 1:
                            try:
                                ex = str(e)
                            except:
                                ex = e.args[1]
                        else:
                            ex = str(e)
                        failCount = failCount + 1
                        if ex != "":
                            ip = self.getIp()
                            if "authentication failed" in ex:
                                print u"帐号或密码错误"
                                path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                    repo_account_cate_id, "exception", account, "", "")
                                conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                                conn.request("GET", path)
                                time.sleep(3)
                            elif "Connection timed out" in ex:
                                print u"连接超时"
                            elif "timeout for" in ex:
                                print u"超时了"
                            elif "Connection unexpectedly closed" in ex:
                                print u"连接意外关闭"
                            elif "The email message was detected as spam" in ex:
                                self.deleteImg()
                            elif "554" in ex and " 5.7.1 This email from IP" in ex:
                                self.deleteImg()
                            elif "server reply: 554 5.7.1 Access denied" in ex:

                                ipArr = ip.split(".")
                                ip2 = ipArr[0] + "." + ipArr[1] + "." + ipArr[2]
                                path = "/repo_api/screen/numberInfo?PhoneNumber=%s&cate_id=%s&guolv=%s" % (
                                    ip2, "468", "N")
                                conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                                conn.request("GET", path)
                                time.sleep(3)
                                print u"可能ip黑了,[ip:%s]" % ip
                                flag = True
                                asdlFalg = False
                                self.deleteImg()
                            elif "5.7.1 Access denied" in ex:
                                ip = self.getIp()
                                ipArr = ip.split(".")
                                ip2 = ipArr[0] + "." + ipArr[1] + "." + ipArr[2]
                                path = "/repo_api/screen/numberInfo?PhoneNumber=%s&cate_id=%s&guolv=%s" % (
                                    ip2, "468", "N")
                                conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                                conn.request("GET", path)
                                time.sleep(3)
                                print u"可能ip黑了,[ip:%s]" % ip
                                flag = True
                                asdlFalg = False
                                self.deleteImg()
                            elif "5.7.1 Too many spam messages sent" in ex:
                                self.deleteImg()
                            elif "5.7.1 Too many messages sent" in ex:
                                print u"可能达到上限了"
                            else:
                                print u"暂时没遇到"
                        else:
                            if type(e) == smtplib.SMTPServerDisconnected:
                                print u"连接意外关闭"
                                pass
                        for item in bcc:
                            it = item[:-7]
                            path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                it, repo_bcc_cate_id, "not_exist")
                            conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                            conn.request("GET", path)
                            time.sleep(0.5)
                        for item in my_user:
                            it2 = item[:-7]
                            path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                it2, repo_number_cate_id, "not_exist")
                            conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                            conn.request("GET", path)
                            time.sleep(0.5)
                        break
                    else:
                        asdlFalg = True
                        failCount = 0
                    if failCount >= 3 and asdlFalg:
                        flag = True
                        self.deleteImg()
                        failCount = 0

                time.sleep(1)
                if changeCount >= loopAccountNumber and asdlFalg:
                    flag = True
                    self.deleteImg()
                    changeCount = 0
        except:
            logging.exception("exception")


    def action(self):
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
    return GGO_SMTP


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    clazz = getPluginClass()
    o = clazz()

    # path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
    #     "312", "using", "1002946809", "", "")
    # conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
    # conn.request( "GET", path )
    # x = Repo( ).GetAccount( "using", "312", 0, 1 )
    while True:
        try:
            o.action()
        except:
            logging.exception("Exception")

