# coding:utf-8
from __future__ import division

import base64
import httplib
import sys
import logging
import re
import socket
import urllib
import urllib2

import thread
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs


import os, time, datetime, random
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
sys.path.append("/home/zunyun/workspace/TaskConsole")
# from IPChange import IPChange
from Repo import Repo


class Phone_PC_Chrome:
    def __init__(self):

        self.repo = Repo()
        # self.ipChange = IPChange()

        # 写入剪切板内容
    def settext(self, aString):
        pass
        # w.OpenClipboard( )
        # w.EmptyClipboard( )
        # w.SetClipboardData( win32con.CF_TEXT, aString )
        # w.CloseClipboard( )

    def checkIp(self,status, cateId, interval, limit):
        path = "/repo_api/account/pick?status=%s&cate_id=%s&interval=%s&limit=%s" % (status,cateId, interval, limit)
        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def delete(self):
        path = "C:\Users\Administrator\AppData\Local\Temp"
        g = os.listdir(path)
        import shutil
        for i in g:
            x = path + "\\%s"% i
            try:
                shutil.rmtree(x)
            except:
                pass

    def getTime(self, timeType):
        path = "/cgi-bin/cgi_svrtime"
        conn = httplib.HTTPConnection("cgi.im.qq.com", None, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        data = response.read().replace("\n", "")
        #if response.status == 200:
         #   data = response.read()
        #else:
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

    def updateNumberStatus(self,emailnumber,repo_number_cate_id):
        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
            emailnumber, repo_number_cate_id, "normal")
        conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
        conn.request("GET", path)
        time.sleep(3)

    def getIp(self):
        path = "/plain"
        conn = httplib.HTTPConnection( "ipecho.net", None, timeout=30 )
        conn.request( "GET", path )
        time.sleep( 3 )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            return data
        else:
            return []

    def updateAccountStatus(self,repo_cate_id,account,status):
        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
            repo_cate_id, status, account, "", "")
        conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
        conn.request("GET", path)
        time.sleep(3)

    def lockAccount(self,account,repo_cate_id,QQType):
        path = "/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
            account, repo_cate_id,QQType)
        conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
        conn.request("GET", path)
        time.sleep(3)

    def GetUnique(self):
        num = ""
        for i in range(0,random.randint(1,8)):
            n = random.choice("qwertyuiopasdfghjklzxcvbnm")
            num = n + num
        for i in range(0,random.randint(1,5)):
            n = random.choice("0123456789")
            num =  num + n

        return num

    def getImg(self,driver):
        imgName = self.GetUnique()
        # imgpath = r"C:\PIC"
        imgpath = "/home/zunyun/text/img"
        if not os.path.exists(imgpath ):
            return
        g = os.listdir(imgpath)

        for i in g:
            name = i.split(".")
            os.rename( imgpath + "/%s" % i, imgpath + "/%s.%s" % (imgName, name[1]) )
            imgpath = imgpath + "/%s.%s" % (imgName, name[1])
            # os.rename(imgpath + "\%s" % i, imgpath + "\%s.%s" % (imgName, name[1]))
            # imgpath = imgpath + "\%s.%s" % (imgName,name[1])
            try:
                driver.find_element_by_xpath('//*[@id="attachUpload"]/a/input').send_keys(imgpath)
                time.sleep(2)
                return
            except:
                pass

        return imgpath

    def getArgs(self,specifiedTaskId):
        asdlFile = open( r"/home/zunyun/text/asdl.txt", "r" )
        # asdlFile = open( r"c:\asdl.txt", "r" )
        asdlList = asdlFile.readlines( )
        while True:
            if len( asdlList ) > 2:
                specifiedTaskId = int( asdlList[2] )
                taskList = self.repo.GetSpecifiedPhantomJSTask( specifiedTaskId, "phantomjs_task" )
            else:
                taskList = self.repo.GetPhantomJSTaskInfo( "phantomjs_param" )
                if len( taskList ) == 0:
                    print u"检查是否有任务可运行"
                    time.sleep( 30 )
                    continue

            task = taskList[random.randint( 0, len( taskList ) ) - 1]
            phonenumber = task["phonenumber"]
            cateId = task["cateId"]
            repo_material_cateId = task["x01"]
            repo_material_cateId2 = task["x02"]
            repo_number_cate_id = task["x03"]
            user_agent_id = task["x07"]
            repo_cate_id = task["x08"]
            my_userCount= task["x09"]
            bccCount = task["x10"]
            if my_userCount is None or my_userCount == "" or my_userCount == 0 or my_userCount == "0":
                my_userCount = 0
            else:
                my_userCount = int(my_userCount)

            if bccCount is None or bccCount == "":
                bccCount = 0
            else:
                bccCount = int(bccCount)

            if my_userCount == 0 and bccCount == 0:
                # print u"不能没有收件人,请到公网上修改邮件任务信息"
                print u'收件人没有设置或设置为0了,使用默认 1--->1'
                my_userCount = 1
                bccCount = 1


            while True:
                paramList = self.repo.GetPhantomJSParamInfo( "phantomjs_param" )
                if len( paramList ) == 0:
                    time.sleep( 30 )
                    continue
                else:
                    break

            param = paramList[random.randint( 0, len( paramList ) ) - 1]
            time_delay = param["x01"]
            sendTime = param["x02"]
            emailType = param["x03"]

            args = {"time_delay": time_delay, "sendTime": sendTime, "repo_cate_id": repo_cate_id,
                    "repo_number_cate_id": repo_number_cate_id, "repo_material_cateId": repo_material_cateId,
                    "repo_material_cateId2": repo_material_cateId2, "emailType": emailType,
                    "user_agent_id": user_agent_id,"phonenumber":phonenumber,"cateId":cateId,"my_userCount":my_userCount,"bccCount":bccCount}  # cate_id是仓库号，length是数量
            return args

    def login(self,mailType):
        args = self.getArgs( "1" )
        user_agent_id = args["user_agent_id"]
        repo_cate_id = args["repo_cate_id"]
        repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
        time_delay = args["time_delay"].split( "-" )
        try:
            time_delayStart = int( time_delay[0] )
            time_delayEnd = int( time_delay[1] )
        except:
            print  u"参数格式有误"
            time_delayStart = 3
            time_delayEnd = 5
        numbers = self.repo.GetAccount( "normal", repo_cate_id, 0, 1 )
        if len( numbers ) == 0:
            print u"%s号仓库没有数据" % repo_cate_id
            time.sleep( 300 )
            return
        QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        QQPassword = numbers[0]['password']
        # QQNumber = "1538278341"
        # QQPassword = "kdlx8565"
        print QQNumber
        # user_agent = numbers[0]['imei']
        user_agent = ""
        if user_agent is None or user_agent == '':
            user_agentList = self.repo.GetMaterial( user_agent_id, 0, 1 )
            if len( user_agentList ) == 0:
                user_agentList = self.repo.GetMaterial( user_agent_id, 0, 1 )
                if len( user_agentList ) == 0:
                    print u"%s号仓库为空，没有取到消息" % user_agent_id
                    return
            user_agent = user_agentList[0]['content']
        print user_agent
        try:
            command = 'taskkill /F /IM chromedriver.exe'
            os.system( command )
            # print u'close02'
        except:
            pass
        try:
            command = 'taskkill /F /IM chrome.exe'
            os.system( command )
            # print u'close02'
        except:
            pass
        time.sleep( 2 )
        options = webdriver.ChromeOptions( )
        options.add_argument( 'disable-infobars' )
        options.add_argument( 'lang=zh_CN.UTF-8' )
        fl = False
        # options.add_argument( 'headless' )
        # 更换头部
        # options.add_argument(user_agent)
        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
        options.add_argument( 'user-agent="%s' % user_agent )
        try:
            driver = webdriver.Chrome( chrome_options=options, executable_path="/opt/google/chrome/chromedriver" )
        except:
            if not os.path.exists( "C:\Users\Administrator\AppData\Local\Temp" ):
                os.mkdir( "C:\Users\Administrator\AppData\Local\Temp" )

        emailnumbers = self.repo.GetNumber( repo_number_cate_id, 0, 1 )  # 取出add_count条两小时内没有用过的号码
        if len( emailnumbers ) == 0:
            print u"%s号仓库没有数据" % repo_number_cate_id
            time.sleep( 300 )
            try:
                driver.close( )
                driver.quit( )
            except:
                pass
            return
        emailnumber = emailnumbers[0]['number']
        # driver.get(
        #     "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
        #         emailnumber, repo_number_cate_id, "normal"))
        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
            emailnumber, repo_number_cate_id, "normal")
        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
        conn.request( "GET", path )
        time.sleep( 3 )
        if mailType=="phone":

            # 打开QQ邮箱登陆界面
            driver.get( "https://w.mail.qq.com/" )
            # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled')
            time.sleep( 3 )
            # driver.save_screenshot("01.png")
            # driver.save_screenshot("0.png")
            # 点 进入网页版QQ邮箱 (模拟手机版会有这个)
            try:
                obj = driver.find_element_by_xpath( "//td[@class='enter_mail_button_td']/a" )
                obj.click( )

            except:
                print u"使用的是电脑版头信息"

            try:
                # 若帐号输入框有内容先清空
                driver.find_element_by_id( "u" ).clear( )
            except:
                pass
            try:
                # ///
                # 输入框输入帐号和密码
                driver.find_element_by_id( "u" ).send_keys( QQNumber )
                driver.find_element_by_id( "p" ).send_keys( QQPassword )
                # driver.save_screenshot( "222.png" )
                time.sleep( 1 )
                driver.find_element_by_id( "go" ).click( )
                time.sleep( random.randint( time_delayStart, time_delayEnd ) )
            except:
                pass
        else:
            driver.get( r'https://mail.qq.com/' )
            try:
                driver.switch_to_frame( 'login_frame' )  # 需先跳转到iframe框架
            except:
                print u"https://mail.qq.com/ 不支持手机版头信息,仓库号为--->%s,素材为----->%s" % (user_agent_id, user_agent)
                return
            time.sleep( 1 )

            try:
                # 若帐号输入框有内容先清空
                driver.find_element_by_id( "u" ).clear( )
                driver.find_element_by_id( "p" ).clear( )
            except:
                pass
            try:
                driver.find_element_by_id( "u" ).send_keys( QQNumber )
                driver.find_element_by_id( "p" ).send_keys( QQPassword )
                # driver.save_screenshot( "222.png" )
                time.sleep( 0.5 )
                driver.find_element_by_id( "p" ).send_keys( Keys.ENTER )
                time.sleep(2)
                try:
                    driver.find_element_by_xpath('//*[@id="pp"]').send_keys("Abc"+QQNumber)
                except:
                    pass
                time.sleep( random.randint( time_delayStart, time_delayEnd ) )
            except:
                pass

        try:
            if mailType == "phone":
                obj = driver.find_element_by_class_name( "qm_btnIcon" )
            else:
                driver.find_element_by_xpath( '//*[@id="composebtn"]' )
            print u"%s  登陆成功" % QQNumber
            #Repo( ).BackupInfo( repo_cate_id, 'normal', QQNumber, user_agent, '' )
            # driver.save_screenshot("SSS.png")
        except:
            print u"%s  登陆失败" % QQNumber
            # driver.save_screenshot( "002.png" )
            time.sleep( 2 )
            # 登陆出现异常状况
            errorPage = driver.page_source.encode( "utf-8" )

            if "拖动下方滑块完成拼图" in errorPage:
                print u"%s  拖动下方滑块完成拼图" % QQNumber
            elif "安全验证" in errorPage:
                print u"安全验证"
            elif "帐号或密码不正确" in errorPage:
                print u"%s  帐号或密码不正确" % QQNumber
            elif "你的帐号存在安全隐患" in errorPage:
                print u"你的帐号存在安全隐患"
                self.updateAccountStatus( repo_cate_id, QQNumber, "frozen" )
            elif "冻结" in errorPage:
                print u"%s  冻结" % QQNumber
                #         repo_cate_id, "frozen", QQNumber, "", ""))
                self.updateAccountStatus(repo_cate_id,QQNumber,"frozen")
            try:
                obj = driver.find_element_by_class_name( "content" )
            except:
                time.sleep( 2 )
            try:
                driver.close( )
                driver.quit( )
            except:
                pass
            # self.ipChange.ooo()
            # self.ipChange.ooo()
            time.sleep( 5 )
        argsL = {"driver":driver,"QQNumber":QQNumber,"repo_cate_id":repo_cate_id}
        return argsL

    def phoneSendMsg(self,driver,QQNumber,repo_cate_id,tourl):
        flag = True
        flag2 = False
        count = 0
        yc = 0
        while flag:
            if flag:
                driver.get(tourl)
                time.sleep(1)
            args = self.getArgs( "1" )
            emailType = args["emailType"]
            repo_material_cateId2 = args["repo_material_cateId2"]
            repo_material_cateId = args["repo_material_cateId"]
            repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
            sendTime = args["sendTime"].split( "-" )
            my_userCount = args["my_userCount"]
            bccCount = args["bccCount"]
            try:
                sendTimeStart = int( sendTime[0] )
                sendTimeEnd = int( sendTime[1] )
            except:
                print  u"发送时间间隔的参数格式有误"
                sendTimeStart = 3
                sendTimeEnd = 5
            if my_userCount > 0:
                emailnumbers = self.repo.GetNumber( repo_number_cate_id, 0, my_userCount )  # 取出add_count条两小时内没有用过的号码
                emailnumbersArr = []
                if len( emailnumbers ) == 0 and my_userCount > 0:
                    print u"%s号仓库没有数据" % repo_number_cate_id
                    # print u'close08'
                    time.sleep( 100 )
                    try:
                        driver.close( )
                        driver.quit( )
                    except:
                        pass
                    return
                else:
                    for item in emailnumbers:
                        emailnumbersArr.append( item["number"] )
                bccnumbersArr = []
            if bccCount > 0:
                bccnumbers = self.repo.GetNumber( repo_number_cate_id, 0, bccCount )
                if len( bccnumbers ) == 0 and bccCount > 0:
                    print u"%s号仓库没有数据" % repo_number_cate_id
                    # print u'close08'
                else:
                    for itrm2 in bccnumbers:
                        bccnumbersArr.append( itrm2["number"] )

            if repo_material_cateId == "" or repo_material_cateId is None:
                selectContent1 = ""
            else:
                selectContent1 = "只发主题"
                Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                if len( Material ) == 0:
                    Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                    if len( Material ) == 0:
                        print u"%s  号仓库为空，没有取到消息" % repo_material_cateId
                        # print u'close09'
                        try:
                            driver.close( )
                            driver.quit( )
                        except:
                            pass
                        return
                message = Material[0]['content']
            if repo_material_cateId2 == "" or repo_material_cateId2 is None:
                selectContent2 = ""
            else:
                selectContent2 = "只发内容"
                Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                if len( Material2 ) == 0:
                    Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                    if len( Material2 ) == 0:
                        print u"%s号仓库为空，没有取到消息" % repo_material_cateId
                        try:
                            driver.close( )
                            driver.quit( )
                        except:
                            pass
                        return
                message2 = Material2[0]['content']

            # emailnumber = emailnumbers[0]['number']
            # bccnumber = bccnumbers[0]['number']
            try:
                emailnumberObj = driver.find_element_by_id( "showto" )
            except:
                try:
                    emailnumberObj = driver.find_element_by_id( "to" )
                except:
                    driver.get( tourl )
                    time.sleep( 2 )
                    print "ye mian mei jia zai chu lai"
                    try:
                        self.repo.UpdateNumberStauts( emailnumber, repo_number_cate_id, "normal" )
                        driver.get("http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (emailnumber, repo_number_cate_id, "normal") )
                    except:
                        pass
                    # print u'close11'
                    # self.ipChange.ooo()
                    # self.ipChange.ooo()
                    time.sleep( 3 )
                    try:
                        driver.close( )
                        driver.quit( )
                    except:
                        pass
                    return "false"
            if my_userCount > 0:
                if yc==1:
                    emailnumber = [QQNumber]
                for emailnumber in emailnumbersArr:
                    if "@" not in emailnumber:
                        if emailType == "QQ邮箱":
                            emailnumberObj.send_keys( emailnumber + "@qq.com;" )
                        elif emailType == "189邮箱":
                            emailnumberObj.send_keys( emailnumber + "@189.cn;" )
                        elif emailType == "139邮箱":
                            emailnumberObj.send_keys( emailnumber + "@139.com;" )
                        elif emailType == "163邮箱":
                            emailnumberObj.send_keys( emailnumber + "@163.com;" )
                        elif emailType == "wo邮箱":
                            emailnumberObj.send_keys( emailnumber + "@wo.cn;" )
                        else:
                            emailnumberObj.send_keys( emailnumber + "@qq.com;" )
                    else:
                        emailnumberObj.send_keys( emailnumber + ";" )

            # 密送
            if bccCount > 0:
                time.sleep( 2 )
                try:
                    driver.find_element_by_xpath( '//*[@id="more"]/div/a' ).click( )
                except:
                    driver.find_element_by_xpath( '//*[@id="composeMain"]/div/div/div[2]/div/a' ).click( )
                time.sleep( 1 )
                try:
                    bccnumberObj = driver.find_element_by_xpath( '//*[@id="showbcc"]' )
                except:
                    bccnumberObj = driver.find_element_by_xpath( '//*[@id="bcc"]' )
                for bccnumber in bccnumbersArr:
                    if "@" not in bccnumber:
                        if emailType == "QQ邮箱":
                            bccnumberObj.send_keys( bccnumber + "@qq.com;" )
                        elif emailType == "189邮箱":
                            bccnumberObj.send_keys( bccnumber + "@189.cn;" )
                        elif emailType == "139邮箱":
                            bccnumberObj.send_keys( bccnumber + "@139.com;" )
                        elif emailType == "163邮箱":
                            bccnumberObj.send_keys( bccnumber + "@163.com;" )
                        elif emailType == "wo邮箱":
                            bccnumberObj.send_keys( bccnumber + "@wo.cn;" )
                        else:
                            bccnumberObj.send_keys( bccnumber + "@qq.com;" )
                    else:
                        bccnumberObj.send_keys( bccnumber + ";" )
            if flag2:
                try:
                    self.getImg( driver )  # 附件
                except:
                    logging.exception( "dfsdc" )
                    pass
            if selectContent1 == "只发主题":
                driver.find_element_by_id( "subject" ).send_keys( message )
            if selectContent2 == "只发内容":
                driver.find_element_by_id( "content" ).send_keys( message2 )
            time.sleep( 3 )
            driver.implicitly_wait( 15 )
            try:
                try:
                    # windows
                    driver.find_element_by_name( "RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__" ).click( )
                except:
                    driver.find_element_by_id( "composeSend" ).click( )
                time.sleep( random.randint( sendTimeStart, sendTimeEnd ) )
                page_source = driver.page_source
            except:
                page_source = u"您发送的邮件已经达到上限"

            # page_source = "验证码"
            flagFirst = False
            if "发送成功" in page_source and "验证码" not in page_source and "主题：" not in page_source:
                print u"%s 发送成功 给 %s ,密送号码为%s" % (QQNumber, emailnumbersArr, bccnumbersArr)
                count = 0
            else:
                print u"%s 发送失败 给 %s ,密送号码为%s" % (QQNumber, emailnumbersArr, bccnumbersArr)
                if "主题：" in page_source and "收件人：" in page_source:
                    print u"还在当前页面"

                try:
                    self.repo.UpdateNumberStauts( emailnumber, repo_number_cate_id, "normal" )
                    # driver.get(
                    #     "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                    #     emailnumber, repo_number_cate_id, "normal"))
                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                        emailnumber, repo_number_cate_id, "normal")
                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                    conn.request( "GET", path )
                    time.sleep( 1 )
                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                        bccnumber, repo_number_cate_id, "normal")
                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                    conn.request( "GET", path )
                    time.sleep( 1 )
                except:
                    pass
                flag = False
                if "邮件中可能包含不合适的用语或内容" in page_source:
                    # 需要解锁
                    print u"%s  邮件中可能包含不合适的用语或内容" % QQNumber
                    self.repo.BackupInfo( repo_cate_id, 'exception', QQNumber, '', '' )
                    # driver.get(
                    #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                    #         repo_cate_id, "exception", QQNumber, "", ""))
                    path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        repo_cate_id, "exception", QQNumber, "", "")
                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                    conn.request( "GET", path )
                    time.sleep( 3 )
                    # driver.delete_all_cookies()
                elif "<html><head></head><body></body></html>" in page_source:
                    print "%s  空" % QQNumber
                    flag2 = True
                    # driver.delete_all_cookies()
                    # self.ipChange.ooo()
                    # self.ipChange.ooo()
                elif "验证码" in page_source:
                    flagFirst = True
                    flag = True
                    flag2 = True
                    yc =yc + 1
                    print u"%s  需要验证码" % QQNumber
                    count = count + 1
                    if count >= 3:
                        flag = False
                        count = 0
                elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                    print u"%s  您发送的邮件已经达到上限，请稍候再发" % QQNumber
                    # driver.delete_all_cookies()
                    # path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                    #   repo_cate_id, "exception", QQNumber, "", "")
                    # conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                    # conn.request("GET", path)
                    # time.sleep(3)
                elif "垃圾邮件" in page_source:
                    print u"垃圾邮件"
                    flag = True
                    count = count + 1
                    if count >= 3:
                        flag = False
                        count = 0
                elif "您的域名邮箱账号存在异常行为" in page_source:
                    # driver.delete_all_cookies()
                    print u"您的域名邮箱账号存在异常行为"
                    # self.repo.BackupInfo(repo_cate_id, 'frozen', QQNumber, '', '')
                    # driver.get("http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                    #     repo_cate_id, "exception", QQNumber, "", ""))
                    # path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                    #    repo_cate_id, "exception", QQNumber, "", "")
                    # conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                    # conn.request("GET", path)
                    # time.sleep(3)
                    self.updateAccountStatus( repo_cate_id, QQNumber, "exception" )
                elif "您的帐号存在安全隐患" in page_source:
                    # driver.delete_all_cookies()
                    print u"您的帐号存在安全隐患"
                    # self.repo.BackupInfo(repo_cate_id, 'exception', QQNumber, '', '')
                    # driver.get(
                    #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                    #         repo_cate_id, "frozen", QQNumber, "", ""))
                    self.updateAccountStatus( repo_cate_id, QQNumber, "frozen" )
                else:
                    flag = False
                    driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                    print u"%s  该情况没判断出来" % QQNumber
                    # driver.delete_all_cookies()
                    # self.ipChange.ooo()
                    # self.ipChange.ooo()
                    time.sleep( 5 )

    def phoneSendBottle(self, driver):
        d = driver.find_element_by_xpath('//*[@id="ct"]/div[3]/div[1]/a')
        if d.text=="点亮灯塔":
            d.click()
            time.sleep(1)

        driver.find_element_by_xpath('//*[@id="ct"]/div[2]/a[1]/span[1]').click()

        driver.find_element_by_xpath('//*[@id="bottlelist"]/ul/li[3]/a/div/span').click()
        driver.find_element_by_xpath('//*[@id="province"]').click()





        bottleUrls = []
        for i in range( 0, 15 ):
            driver.find_element_by_xpath(
                '/html/body/div/section[1]/div/ul/li[4]/a/span[2]/span[1]' ).click( )
            driver.find_element_by_xpath( '//*[@id="ct"]/div[2]/a[3]/div/div' ).click( )
            bottles = driver.find_elements_by_xpath(
                '//*[@class="qm_list_item qm_list_item_Accessory qm_list_item_Style2 bottle_chat_list_item"]/a' )

            for bottle in bottles:
                if bottle.get_attribute( "href" ) not in bottleUrls:
                    bottleUrls.append( bottle.get_attribute( "href" ) )
            driver.refresh( )
            time.sleep( 1.5 )
            if "频繁" in driver.page_source.encode( "utf-8" ):
                break
        for bottleUrl in bottleUrls:
            args = self.getArgs( "3" )
            repo_material_cateId2 = args["repo_material_cateId2"]
            if "您请求的频率太快" in driver.page_source.encode( "utf-8" ):
                break
            if repo_material_cateId2 == "" or repo_material_cateId2 is None:
                selectContent2 = ""
                print u"3号任务没有选择内容仓库即没有选择漂流瓶内容"
                break

            else:
                Material = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                if len( Material ) == 0:
                    Material = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                    if len( Material ) == 0:
                        print u"%s  号仓库为空，没有取到消息" % repo_material_cateId2
                        # print u'close09'
                        break
                    else:
                        message2 = Material[0]['content']
                else:
                    message2 = Material[0]['content']
            try:
                driver.get( bottleUrl )
                time.sleep( 2 )
                if "您请求的频率太快" in driver.page_source.encode( "utf-8" ):
                    break
                driver.find_element_by_xpath( '//*[@id="postform"]/div[2]/div/div[1]/div/textarea' ).send_keys(
                    message2 )
                # driver.find_element_by_xpath( '//*[@id="postform"]/div[2]/div/div[2]/div/div/input' ).send_keys( Keys.SHIFT, Keys.TAB,Keys.SHIFT, message2 )
                driver.find_element_by_xpath( '//*[@id="postform"]/div[2]/div/div[2]/div/div/input' ).click( )
                time.sleep( 2 )
                if "您的漂流瓶已漂向对方" in driver.page_source.encode( "utf-8" ):
                    continue
                elif "您请求的频率太快" in driver.page_source.encode( "utf-8" ):
                    break
                elif "频率" in driver.page_source.encode( "utf-8" ):
                    break
                elif "验证码" in driver.page_source.encode( "utf-8" ):
                    print u"漂流瓶出验证码"
                    break
                else:
                    break
            except:
                # logging.exception("dfsds")
                pass

    def phoneSendCard(self, driver,sid,QQNumber,repo_cate_id):
        count = 0
        flag = True
        while flag:
            args = self.getArgs( "4" )
            repo_material_cateId2 = args["repo_material_cateId2"]
            repo_material_cateId = args["repo_material_cateId"]
            emailType = args["emailType"]
            repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
            sendNumbers = self.repo.GetNumber( repo_number_cate_id, 0, 1 )
            if len( sendNumbers ) == 0:
                print u"%s号仓库没有数据" % repo_number_cate_id
                break
            else:
                sendNumber = sendNumbers[0]["number"]
            if repo_material_cateId == "" or repo_material_cateId is None:
                selectContent1 = ""
                print u"4号任务没有选择主题仓库即没有选择贺卡编号"
                Material = self.repo.GetMaterial( "441", 0, 1 )
                if len( Material ) == 0:
                    Material = self.repo.GetMaterial( "441", 0, 1 )
                    if len( Material ) == 0:
                        cardIds = [99917, 99918, 99920, 99921, 99922, 99923, 99924, 99925, 99926, 99927, 99928, 99929]
                        cardId = cardIds[random.randint( 0, len( cardIds ) - 1 )]
                    else:
                        cardId = Material[0]['content']
                else:
                    cardId = Material[0]['content']

            else:
                Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                if len( Material ) == 0:
                    Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                    if len( Material ) == 0:
                        print u"%s  号仓库为空，没有取到消息" % repo_material_cateId
                        # print u'close09'
                        if len( Material ) == 0:
                            cardIds = [99917, 99918, 99920, 99921, 99922, 99923, 99924, 99925, 99926, 99927, 99928,
                                       99929]
                            cardId = cardIds[random.randint( 0, len( cardIds ) - 1 )]
                    else:
                        message2 = Material[0]['content']
                else:
                    cardId = Material[0]['content']
            if repo_material_cateId2 == "" or repo_material_cateId2 is None:
                selectContent2 = ""
                print u"4号任务没有选择内容仓库即没有选择贺卡内容"
                break

            else:
                Material = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                if len( Material ) == 0:
                    Material = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                    if len( Material ) == 0:
                        print u"%s  号仓库为空，没有取到消息" % repo_material_cateId2
                        # print u'close09'
                        break
                    else:
                        message2 = Material[0]['content']
                else:
                    message2 = Material[0]['content']

            if "@" not in sendNumber:
                if emailType == "QQ邮箱":
                    sendNumber2 = sendNumber + "@qq.com;"
                elif emailType == "189邮箱":
                    sendNumber2 = sendNumber + "@189.cn;"
                elif emailType == "139邮箱":
                    sendNumber2 = sendNumber + "@139.com;"
                elif emailType == "163邮箱":
                    sendNumber2 = sendNumber + "@163.com;"
                elif emailType == "wo邮箱":
                    sendNumber2 = sendNumber + "@wo.cn;"
                else:
                    sendNumber2 = sendNumber + "@qq.com;"
            else:
                sendNumber2 = sendNumber + ";"
            # driver.find_element_by_xpath('/html/body/div/section[1]/div/ul/li[9]/a/span[2]/span').click()
            #
            # driver.find_element_by_xpath('//*[@id="ct"]/div[3]/div[%s]/div/div[3]/a'%random.randint(1,4)).click()
            cardUrl = "https://w.mail.qq.com/cgi-bin/cardlist?sid=%s" \
                      "&s=&t=compose_card&cardid=%s&bccsingle=&ListType=OneCard&rpycard=&p=0&Cate1Idx=hot&bccs=&birthCard=" % (
                      sid, cardId)
            driver.get( cardUrl )
            # sendNumber = "2351382894@qq.com"
            driver.find_element_by_xpath( '//*[@id="showbcc"]' ).send_keys( sendNumber2 )
            # driver.find_element_by_xpath('//*[@id="content"]').send_keys(Keys.CONTROL, 'a',Keys.DELETE)
            driver.find_element_by_xpath( '//*[@id="content"]' ).send_keys( "\n", "\n", "\n", message2 )
            driver.find_element_by_xpath( '//*[@id="ct"]/form/div[1]/input[2]' ).click( )
            time.sleep( 10 )
            page_source = driver.page_source.encode( "utf-8" )
            if "发送成功" in page_source and "验证码" not in page_source and "主题：" not in page_source:
                print u"%s 发送成功 给 %s ," % (QQNumber, sendNumber2)
                count = 0
            else:
                print u"%s 发送失败 给%s" % (QQNumber, sendNumber2)
                if "贺卡" in page_source and "收件人：" in page_source:
                    print u"还在当前页面"

                try:
                    self.repo.UpdateNumberStauts( sendNumber, repo_number_cate_id, "normal" )
                    # driver.get(
                    #     "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                    #     emailnumber, repo_number_cate_id, "normal"))
                except:
                    pass
                flag = False
                if "邮件中可能包含不合适的用语或内容" in page_source:
                    # 需要解锁
                    print u"%s  邮件中可能包含不合适的用语或内容" % QQNumber
                    self.repo.BackupInfo( repo_cate_id, 'exception', QQNumber, '', '' )
                    # driver.get(
                    #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                    #         repo_cate_id, "exception", QQNumber, "", ""))
                    path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        repo_cate_id, "exception", QQNumber, "", "")
                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                    conn.request( "GET", path )
                    time.sleep( 3 )
                    # driver.delete_all_cookies()
                elif "<html><head></head><body></body></html>" in page_source:
                    print "%s  空" % QQNumber
                    # driver.delete_all_cookies( )
                    # self.ipChange.ooo()
                    # self.ipChange.ooo()
                elif "验证码" in page_source:
                    flagFirst = True
                    flag = True
                    print u"%s  需要验证码" % QQNumber
                    count = count + 1
                    if count >= 3:
                        flag = False
                        count = 0
                elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                    print u"%s  您发送的邮件已经达到上限，请稍候再发" % QQNumber
                    # driver.delete_all_cookies()
                    # path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                    #   repo_cate_id, "exception", QQNumber, "", "")
                    # conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
                    # conn.request("GET", path)
                    # time.sleep(3)
                elif "垃圾邮件" in page_source:
                    print u"垃圾邮件"
                    flag = True
                    count = count + 1
                    if count >= 3:
                        flag = False
                        count = 0
                elif "您的域名邮箱账号存在异常行为" in page_source:
                    # driver.delete_all_cookies( )
                    print u"您的域名邮箱账号存在异常行为"
                    self.updateAccountStatus( repo_cate_id, QQNumber, "exception" )
                    self.updateAccountStatus( repo_cate_id, QQNumber, "exception" )
                elif "您的帐号存在安全隐患" in page_source:
                    # driver.delete_all_cookies( )
                    print u"您的帐号存在安全隐患"
                    self.updateAccountStatus( repo_cate_id, QQNumber, "frozen" )
                else:
                    flag = False
                    driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                    print u"%s  该情况没判断出来" % QQNumber
                    # driver.delete_all_cookies( )
                    # self.ipChange.ooo()
                    # self.ipChange.ooo()
                    time.sleep( 5 )

    def pcSendMsg(self,driver,repo_cate_id,QQNumber,startUrl):
        count_Y = 0
        flag = True
        count = 0
        while flag:
            args = self.getArgs( "2" )
            emailType = args["emailType"]
            repo_material_cateId2 = args["repo_material_cateId2"]
            repo_material_cateId = args["repo_material_cateId"]
            sendTime = args["sendTime"]
            sendTime = sendTime.split( "-" )
            try:
                sendTimeStart = int( sendTime[0] )
                sendTimeEnd = int( sendTime[1] )
            except:
                print  u"发送时间间隔的参数格式有误"
                sendTimeStart = 3
                sendTimeEnd = 5
            repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
            bccCount = args["bccCount"]
            my_userCount = args["my_userCount"]
            emailnumbers = Repo( ).GetNumber( repo_number_cate_id, 0, my_userCount )  # 取出add_count条两小时内没有用过的号码
            emailnumberArr = []
            if len( emailnumbers ) == 0 and my_userCount > 0:
                print u"QQ号码库%s号仓库为空" % repo_number_cate_id
                time.sleep( 100 )
                try:
                    driver.close( )
                    driver.quit( )
                except:
                    pass
                return
            else:
                for item in emailnumbers:
                    emailnumberArr.append( item['number'] )
            bccnumbers = self.repo.GetNumber( repo_number_cate_id, 0, bccCount )  # 取出add_count条两小时内没有用过的号码
            bccnumberArr = []
            if len( bccnumbers ) == 0 and bccCount > 0:
                print u"QQ号码库%s号仓库为空" % repo_number_cate_id
                if my_userCount == 0:
                    time.sleep( 100 )
                    try:
                        driver.close( )
                        driver.quit( )
                    except:
                        pass
                    return
            else:
                for item in bccnumbers:
                    bccnumberArr.append( item['number'] )

            if repo_material_cateId == "" or repo_material_cateId is None:
                selectContent1 = ""
            else:
                selectContent1 = "只发主题"
                Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                if len( Material ) == 0:
                    Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                    if len( Material ) == 0:
                        print u"%s  号仓库为空，没有取到消息" % repo_material_cateId
                        try:
                            driver.close( )
                            driver.quit( )
                        except:
                            pass
                        return
                message = Material[0]['content']
            if repo_material_cateId2 == "" or repo_material_cateId2 is None:
                selectContent2 = ""
            else:
                selectContent2 = "只发内容"
                Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                if len( Material2 ) == 0:
                    Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                    if len( Material2 ) == 0:
                        # print "%s号仓库为空，没有取到消息" % repo_material_cateId
                        try:
                            driver.close( )
                            driver.quit( )
                        except:
                            pass
                        return
                message2 = Material2[0]['content']

            try:
                driver.switch_to_frame( 'mainFrame' )  # 需先跳转到iframe框架
                time.sleep( 1 )
                emailnumberObj = driver.find_element_by_xpath( '//*[@id="subject"]' )  # 定位到主题
                # emailnumberObj = driver.find_element_by_xpath( '//*[@id="toAreaCtrl"]' )
            except:
                pass

            if selectContent1 == "只发主题":
                try:
                    # emailnumberObj.send_keys( Keys.TAB )
                    emailnumberObj.send_keys( message )
                    time.sleep( 0.5 )
                except:
                    pass

            bccObj = driver.find_element_by_xpath( '//*[@id="aBCC"]' )
            text = bccObj.get_attribute( "text" ).encode( "utf-8" )
            if text == "删除密送":
                bccObj.click( )

            j = 2
            # emailnumberArr = ['2351382894@qq.com']
            account = QQNumber

            for emailnumber in emailnumberArr:
                if "@" not in emailnumber:
                    # emailnumber = "455854284"
                    if emailType == "QQ邮箱":
                        driver.find_element_by_xpath( '//*[@id="toAreaCtrl"]/div[%s]/input' % j ).send_keys(
                            emailnumber + "@qq.com " )
                    elif emailType == "189邮箱":
                        driver.find_element_by_xpath( '//*[@id="toAreaCtrl"]/div[%s]/input' % j ).send_keys(
                            emailnumber + "@189.cn " )
                    elif emailType == "139邮箱":
                        driver.find_element_by_xpath( '//*[@id="toAreaCtrl"]/div[%s]/input' % j ).send_keys(
                            emailnumber + "@139.com " )
                    elif emailType == "163邮箱":
                        driver.find_element_by_xpath( '//*[@id="toAreaCtrl"]/div[%s]/input' % j ).send_keys(
                            emailnumber + "@163.com " )
                    elif emailType == "wo邮箱":
                        driver.find_element_by_xpath( '//*[@id="toAreaCtrl"]/div[%s]/input' % j ).send_keys(
                            emailnumber + "@wo.cn " )
                    else:
                        driver.find_element_by_xpath( '//*[@id="toAreaCtrl"]/div[%s]/input' % j ).send_keys(
                            emailnumber + "@qq.com " )
                else:
                    driver.find_element_by_xpath( '//*[@id="toAreaCtrl"]/div[%s]/input' % j ).send_keys(
                        emailnumber + " " )
                j = j + 1
            # driver.save_screenshot( "mmm.png" )
            time.sleep( 2 )
            emailnumberObj.click( )
            time.sleep( 1 )
            if bccnumberArr != []:
                # if count_Y == 0:
                driver.find_element_by_xpath( '//*[@id="aBCC"]' ).click( )
                time.sleep( 2 )
                j = 2
                for bcc in bccnumberArr:
                    if "@" not in bcc:
                        # emailnumber = "455854284"
                        if emailType == "QQ邮箱":
                            driver.find_element_by_xpath( '//*[@id="bccAreaCtrl"]/div[%s]/input' % j ).send_keys(
                                bcc + "@qq.com " )
                        elif emailType == "189邮箱":
                            driver.find_element_by_xpath( '//*[@id="bccAreaCtrl"]/div[%s]/input' % j ).send_keys(
                                bcc + "@189.cn " )
                        elif emailType == "139邮箱":
                            driver.find_element_by_xpath( '//*[@id="bccAreaCtrl"]/div[%s]/input' % j ).send_keys(
                                bcc + "@139.com " )
                        elif emailType == "163邮箱":
                            driver.find_element_by_xpath( '//*[@id="bccAreaCtrl"]/div[%s]/input' % j ).send_keys(
                                bcc + "@163.com " )
                        elif emailType == "wo邮箱":
                            driver.find_element_by_xpath( '//*[@id="bccAreaCtrl"]/div[%s]/input' % j ).send_keys(
                                bcc + "@wo.cn " )
                        else:
                            driver.find_element_by_xpath( '//*[@id="bccAreaCtrl"]/div[%s]/input' % j ).send_keys(
                                bcc + "@qq.com " )
                    else:
                        driver.find_element_by_xpath( '//*[@id="bccAreaCtrl"]/div[%s]/input' % j ).send_keys(
                            bcc + " " )
                    j = j + 1
            time.sleep( 2 )
            driver.find_element_by_xpath( '//*[@id="editor_toolbar_btn_container"]/font' ).click( )
            driver.find_element_by_xpath(
                '// *[ @ id = "QMEditorArea"] / table / tbody / tr[1] / td / div / div[1] / div[15] / div / input' ).click( )
            time.sleep( 0.5 )
            emailnumberObj.click( )
            time.sleep( 0.5 )

            if selectContent2 == "只发内容":
                if "@qq.com" not in account:
                    account2 = account + "@qq.com"
                else:
                    account2 = account
                message2 = message2.replace( "+FromMail+", account2 )
                email = emailnumberArr[0]
                if "@" not in email:
                    # emailnumber = "455854284"
                    if emailType == "QQ邮箱":
                        email = email + "@qq.com "
                    elif emailType == "189邮箱":
                        email = email + "@189.cn "
                    elif emailType == "139邮箱":
                        email = email + "@139.com "
                    elif emailType == "163邮箱":
                        email = email + "@163.com "
                    elif emailType == "wo邮箱":
                        email = email + "@wo.cn "
                    else:
                        email = email + "@qq.com "
                message2 = message2.replace( "+ToMail+", email )
                message2 = message2.replace( "+Subject+", message )
                try:
                    message2 = message2.replace( "+CnTime+", self.getTime( "CnTime" ) )
                except:
                    pass
                try:
                    message2 = message2.replace( "+EnTime+", self.getTime( "EnTime" ) )
                except:
                    pass

                # msg = message2.encode("gbk")
                # message2 = message2.encode('GB18030')
                self.settext( message2 )
                emailnumberObj.send_keys( Keys.TAB, Keys.CONTROL, 'a', Keys.DELETE )
                time.sleep( 1 )
                emailnumberObj.click( )
                # emailnumberObj.send_keys(Keys.TAB,Keys.CONTROL,'v')
                emailnumberObj.send_keys( Keys.TAB, message2 )
                # emailnumberObj.click()
                # time.sleep(2.5)
                # emailnumberObj.send_keys(Keys.TAB)
                # 粘贴（ctrl + v）
                # for i in range(0,2):
                # try:
                # driver.find_element_by_xpath('/html/body').click()
                # except:
                # pass
                # try:
                # 自动粘贴剪切板中的内容
                # win32api.keybd_event(17, 0, 0, 0)  # 按下按键 ctrl
                # time.sleep(3)
                # win32api.keybd_event(86, 0, 0, 0)  # 按下按键 v
                # time.sleep(0.5)
                # time.sleep(3)
                # win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 升起按键 ctrl
                # win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 升起按键 v
                # time.sleep(1)
                # win32api.keybd_event(17, 0, 0, 0)  # ctrl的键位码是17
                # win32api.keybd_event(86, 0, 0, 0)  # v的键位码是86
                # # time.sleep(0.5)
                # win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
                # win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
                # # time.sleep(0.5)
                # win32api.keybd_event(13, 0, 0, 0)  # Enter的键位码是13
                # win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
                # except:
                # pass
                # time.sleep(1)

            driver.find_element_by_xpath(
                '//*[@id="QMEditorArea"]/table/tbody/tr[1]/td/div/div[2]/div[2]' ).click( )
            time.sleep( 0.5 )

            # time.sleep( 1 )
            try:
                driver.find_element_by_xpath( '//*[@id="toolbar"]/div/a[1]' ).click( )

            except:
                emailnumberObj.send_keys( Keys.TAB )
                emailnumberObj.send_keys( Keys.ENTER )
            # time.sleep(random.randint(sendTimeStart, sendTimeEnd))
            time.sleep( 2 )
            # try:
            #     try:
            #         driver.find_element_by_id("composeSend")
            #     except:
            #         driver.find_element_by_name("RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__")
            #     time.sleep(3)
            # except:
            #     pass

            page_source = driver.page_source.encode( "utf-8" )
            if "发送成功" in page_source and "验证码" not in page_source:
                try:
                    emailnumberObj = driver.find_element_by_xpath( '//*[@id="subject"]' )
                    print u"点击发送还在原界面"
                    for item in emailnumberArr:
                        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                            item, repo_number_cate_id, "normal")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 0.5 )
                    for item2 in bccnumberArr:
                        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                            item2, repo_number_cate_id, "normal")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 0.5 )
                    if "您的帐号因频繁发送广告或垃圾邮件，已被禁止发信。" in page_source:
                        print u'您的帐号因频繁发送广告或垃圾邮件，已被禁止发信'
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "frozen", account, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                        flag = False
                        count_Y = 3
                    count_Y = count_Y + 1
                    if count_Y >= 3:
                        flag = False
                    else:
                        time.sleep( random.randint( 3, 5 ) )

                except:
                    count_Y = 0
                    print u"%s 发送成功 给 %s ,密送号码为%s" % (account, emailnumberArr, bccnumberArr)  # 发送成功

            else:
                # driver.save_screenshot("qqq.png")
                print u"%s 发送失败 给 %s ,密送号码为%s" % (account, emailnumberArr, bccnumberArr)
                try:
                    if "验证码" in page_source:
                        print u"需要验证码"
                        flag = False
                        flagFirst = True
                        sc = 0
                        count = count + 1
                        if count >= 2:
                            # self.ipChange.ooo()
                            # self.ipChange.ooo()
                            time.sleep( 3 )
                            count = 0
                    elif "邮件中可能包含不合适的用语或内容" in page_source:
                        sc = 0
                        flag = False

                        print u"%s  邮件中可能包含不合适的用语或内容" % account
                    elif "<html><head></head><body></body></html>" in page_source:
                        sc = 0
                        flag = False
                        print "空"
                        # self.ipChange.ooo()
                        # self.ipChange.ooo()
                        time.sleep( 3 )
                    elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                        sc = 0
                        flag = False
                        flagFirst2 = True
                        print u"您发送的邮件已经达到上限，请稍候再发"
                    elif "您的域名邮箱账号存在异常行为" in page_source:
                        sc = 0
                        flag = False
                        print u"您的域名邮箱账号存在异常行为"
                        # self.repo.BackupInfo(repo_cate_id, 'exception', account, '', '')
                        # driver.get("http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #     repo_cate_id, "exception", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    elif "您的帐号存在安全隐患" in page_source:
                        sc = 0
                        flag = False
                        print u"您的帐号存在安全隐患"
                        # self.repo.BackupInfo(repo_cate_id, 'frozen', account, '', '')
                        # driver.get(
                        #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #         repo_cate_id, "frozen", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    else:
                        driver.find_element_by_class_name( "qm_icon_Compose" )
                        sc = sc + 1
                        if sc >= 20:
                            flag = False
                            sc = 0
                        print u"%s发送成功2" % account
                        flagFirst = False
                        flagFirst2 = False
                except:
                    print u"%s 发送失败 给 %s ,密送号码为%s" % (account, emailnumberArr, bccnumberArr)
                    try:
                        # self.repo.UpdateNumberStauts(emailnumber, repo_number_cate_id, "normal")
                        # driver.get(
                        #     "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                        #     emailnumber, repo_number_cate_id, "normal"))
                        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                            emailnumber, repo_number_cate_id, "normal")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 1 )
                    except:
                        pass
                    print u"%s 发送失败 给 %s ,密送号码为%s" % (account, emailnumberArr, bccnumberArr)
                    sc = 0
                    flag = False
                    if "验证码" in page_source:
                        print u"需要验证码"
                        flagFirst = False
                        count = count + 1
                        if count >= 2:
                            # self.ipChange.ooo()
                            # self.ipChange.ooo()
                            time.sleep( 3 )
                            count = 0
                    if "邮件中可能包含不合适的用语或内容" in page_source:
                        print u"%s  邮件中可能包含不合适的用语或内容" % account
                    elif "<html><head></head><body></body></html>" in page_source:
                        print "空"
                        driver.get( startUrl )
                        # self.ipChange.ooo()
                        # self.ipChange.ooo()
                        time.sleep( 3 )
                    elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                        flagFirst2 = True
                        print u"您发送的邮件已经达到上限，请稍候再发"
                    elif "您的域名邮箱账号存在异常行为" in page_source:
                        print u"您的域名邮箱账号存在异常行为"
                        # self.repo.BackupInfo(repo_cate_id, 'exception', account, '', '')
                        # driver.get(
                        #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #     repo_cate_id, "exception", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    elif "您的帐号存在安全隐患" in page_source:
                        print u"您的帐号存在安全隐患"
                        # self.repo.BackupInfo(repo_cate_id, 'exception', account, '', '')
                        # driver.get(
                        #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #         repo_cate_id, "frozen", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "frozen", account, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    else:
                        print page_source
                        # driver.save_screenshot( "%s-%s.png" % (account, self.GetUnique( )) )
                        print "error"
            driver.get( startUrl )
            time.sleep( 2 )
            try:
                driver.switch_to.default_content( )
                # driver.switch_to_frame( 'actionFrame' )
                driver.find_element_by_xpath( '//*[@id="composebtn"]' ).click( )
            except:
                pass

    def pcDeleteMsg(self, driver,startUrl):
        driver.get( startUrl )
        floders = ['//*[@id="folder_1"]', '//*[@id="folder_3"]', '//*[@id="folder_4"]', '//*[@id="folder_5"]',
                   '//*[@id="folder_6"]']
        try:
            for floder in floders:
                driver.find_element_by_xpath( floder ).click( )
                driver.switch_to_frame( 'mainFrame' )  # 需先跳转到iframe框架
                time.sleep( 1 )
                while True:
                    try:
                        if "没有邮件" in driver.page_source.encode( "utf-8" ):
                            break
                        driver.find_element_by_xpath( '//*[@id="ckb_selectAll"]' ).click( )
                        time.sleep( 2 )
                        try:
                            driver.find_element_by_xpath( '//*[@id="quick_completelydel"]' ).click( )
                        except:
                            driver.find_element_by_xpath( '//*[@id="quick_del"]' ).click( )
                        try:
                            driver.switch_to_default_content( )
                            driver.find_element_by_xpath( '//*[@id="QMconfirm_QMDialog_confirm"]' ).click( )
                            driver.switch_to_frame( 'mainFrame' )  # 需先跳转到iframe框架
                        except:
                            driver.switch_to_alert( )
                            driver.find_element_by_xpath( '//*[@id="QMconfirm_QMDialog_confirm"]' ).click( )
                            driver.find_element_by_xpath( '//*[@id="ckb_selectAll"]' ).send_keys( Keys.DELETE,
                                                                                                  Keys.ENTER,
                                                                                                  Keys.ENTER )
                        time.sleep( 2 )
                    except:
                        driver.find_element_by_xpath( floder ).click( )
                        time.sleep( 2 )
                driver.get( startUrl )
                time.sleep( 1 )
                driver.switch_to.default_content( )
        except:
            pass

    def sendProcess(self):
        try:
            count = 0
            changeCount = 0
            for loop in range(0,2):
                #登陆
                if loop ==1:
                    mailType = "phone"
                else:
                    mailType = "pc"
                argsL = self.login( mailType )

                driver = argsL["driver"]
                QQNumber = argsL["QQNumber"]
                repo_cate_id = argsL["repo_cate_id"]
                if mailType == "pc":
                    startUrl = driver.current_url
                    sid2 = startUrl.split( "sid=" )[1].split( "&" )[0]
                    qie = "https://w.mail.qq.com/cgi-bin/mobile?sid=" + sid2 + "&t=phone#today"
                    try:
                        driver.find_element_by_xpath( '/html/body/div[7]/span/div/a' ).click( )
                    except:
                        driver.get( qie )
                        time.sleep( 2 )
                url = driver.current_url
                sid = url.split( "sid=" )[1].split( "&" )[0]
                print sid
                print url
                # cookies = driver.get_cookies( )
                # driver.close( )
                # driver.quit( )
                # options = webdriver.ChromeOptions( )
                # options.add_argument( 'disable-infobars' )
                # options.add_argument( 'lang=zh_CN.UTF-8' )
                # fl = False
                # # options.add_argument( 'headless' )
                # # 更换头部
                # # options.add_argument(user_agent)
                # user_agent = "MQQBrowser/26Mozilla/6.0(Linux;U;Android6.3.7;zh-cn;MB200Build/GRJ22;CyanogenMod-7)AppleWebKit/533.1(KHTML,likeGecko)Version/4.0MobileSafari/533.1"
                # options.add_argument( 'user-agent="%s' % user_agent )
                # try:
                #     driver = webdriver.Chrome( chrome_options=options,
                #                                executable_path="/opt/google/chrome/chromedriver" )
                # except:
                #     if not os.path.exists( "C:\Users\Administrator\AppData\Local\Temp" ):
                #         os.mkdir( "C:\Users\Administrator\AppData\Local\Temp" )
                # driver.get( "https://w.mail.qq.com/" )
                # for cookie in cookies:
                #     #cookie2 = {"name":cookie["name"],"value":cookie["value"]}
                #     try:
                #         driver.add_cookie( cookie )
                #     except:
                #         logging.exception("")
                #         pass
                #
                # driver.refresh()
                # driver.get( "https://w.mail.qq.com/" )
                # print driver.current_url


                for i in range(0,2):
                    url = driver.current_url
                    sid = url.split("sid=")[1].split("&")[0]
                    driver.find_element_by_xpath("//span[@class='qm_icon qm_icon_Compose']").click()
                    time.sleep(3)
                    tourl = driver.current_url.encode("utf-8")
                    flag = False
                    flag2 = False
                    # 手机版发邮件
                    # time.sleep(random.randint(1,5))
                    print u"手机版发邮件"

                    self.phoneSendMsg(driver,QQNumber,repo_cate_id,tourl)
                    time.sleep(2)
                    driver.get( url )
                    try:
                        driver.find_element_by_xpath('/html/body/div/section[1]/div/ul/li[3]/a/span[2]/span[1]').click()
                    except:
                        driver.find_element_by_xpath('//*[@id="fl"]/div/div/ul/li[3]/a/span[2]/span[1]').click()

                    # 手机版发漂流瓶
                    self.phoneSendBottle(driver)

                    # 手机版发贺卡
                    self.phoneSendCard(driver,sid,QQNumber,repo_cate_id)

                    driver.get(url)
                    time.sleep(3)
                    # 切换到pc版
                    driver.find_element_by_xpath('//*[@id="footer"]/nav/a[3]').click()
                    errorPage = driver.page_source.encode("utf-8")
                    if "你的帐号存在安全隐患" in errorPage:
                        print u"你的帐号存在安全隐患"
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "exception", QQNumber, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    elif "帐号或密码不正确" in errorPage:
                        print u"帐号或密码不正确"
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "frozen", QQNumber, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    startUrl = driver.current_url
                    sid2 = startUrl.split( "sid=" )[1].split( "&" )[0]
                    try:
                        driver.find_element_by_xpath( '//*[@id="composebtn"]' ).click( )
                        time.sleep( 3 )
                    except:
                        pass

                    # pc版发邮件
                    self.pcSendMsg(driver,repo_cate_id,QQNumber,startUrl)
                    # 删除邮件
                    self.pcDeleteMsg(driver,startUrl)

                    driver.get(startUrl)
                    time.sleep(1)
                    #切换到手机版
                    qie = "https://w.mail.qq.com/cgi-bin/mobile?sid="+sid2+"&t=phone#today"
                    try:
                        driver.find_element_by_xpath('/html/body/div[7]/span/div/a').click()
                    except:
                        driver.get(qie)
                        time.sleep(2)

            import shutil
            deletepath = "C:\Users\Administrator\AppData\Local\Temp"
            # shutil.rmtree(deletepath)
            try:
                g = os.walk(deletepath)
                for path, d, filelist in g:
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
            except:
                pass
            try:
                driver.close( )
                driver.quit( )
            except:
                pass

        except Exception,e:
            logging.exception("s")
            command = 'taskkill /F /IM chromedriver.exe'
            os.system(command)
            try:
                driver.close( )
                driver.quit( )
            except:
                pass
            self.delete()
            # result = [driver]
            return []

    def action(self):
        # data = self.ipChange.Check_for_Broadband()
        # if data != None:
        #     print u"宽带确认已连接,模块继续运行"
        # else:
        #     print u"宽带未连接,连接宽带,sleep 150 s"
        #     time.sleep(150)
        #     self.ipChange.ooo()
        #     time.sleep(5)
        # try:
        #     thread.start_new_thread( self.sendProcess, () )
        #     thread.start_new_thread( self.sendProcess, () )
        #     # time.sleep(1000)
        # except:
        #     print "Error: unable to start thread"

        x = self.sendProcess( )
        if x == "false":
            sta = "normal"
        elif type( x ) == list:
            # d = x[0]
            # try:
            #     d.close()
            #     d.quit()
            # except:
            #     pass
            sta = "normal"
        else:
            sta = "stopped"
        self.delete()
        args = self.getArgs("1")
        phonenumber = args["phonenumber"]
        cateId = args["cateId"]
        para = {"phoneNumber": phonenumber, "x_04": sta}
        self.repo.PostInformation( cateId, para )



def getPluginClass():
    return Phone_PC_Chrome

if __name__ == "__main__":

    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()
    # o.getArgs("1")
    # ip = o.getIp()
    # print ip
    # o.delete()
    # time.sleep(150)

    # Material = Repo().GetMaterial( "490", "0", 1 )
    # if len( Material ) == 0:
    #     print u"%s  号仓库为空，没有取到消息" % "314"
    #     # print u'close09'
    #
    # else:
    #     message2 = Material[0]['content']
    #     print message2
    while True:
        repo_number_cate_id = "273"
        emailnumbers = o.repo.GetNumber( repo_number_cate_id, 0, 1 )  # 取出add_count条两小时内没有用过的号码
        if len( emailnumbers ) == 0:
            print u"%s号仓库没有数据" % repo_number_cate_id
            time.sleep( 300 )
        emailnumber = emailnumbers[0]['number']
        print emailnumber
        # repo_cate_id = "226"
        # numbers = o.repo.GetAccount(repo_cate_id, 0,1 )
        # if len( numbers ) == 0:
        #     print u"%s号仓库没有数据" % repo_cate_id
        #     time.sleep( 300 )
        # QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        # QQPassword = numbers[0]['password']

    # while True:
    #     try:
    #         o.action()
    #     except Exception,e:
    #         print e




