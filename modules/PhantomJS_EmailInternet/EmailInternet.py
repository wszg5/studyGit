# coding:utf-8
from __future__ import division

import base64
import sys
import logging
import re
import socket
import urllib2

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs


import os, time, datetime, random
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
# sys.path.append("C:\TaskConsole-master")
# from IPChange import IPChange
from Repo import Repo


class EmailInternet:
    def __init__(self):

        self.repo = Repo()
        # self.ipChange = IPChange()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 1000)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

    def getArgs(self):
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
            sleepTime = param["x04"]

            args = {"time_delay": time_delay, "sendTime": sendTime, "repo_cate_id": repo_cate_id,
                    "repo_number_cate_id": repo_number_cate_id, "repo_material_cateId": repo_material_cateId,
                    "repo_material_cateId2": repo_material_cateId2, "emailType": emailType,
                    "user_agent_id": user_agent_id,"phonenumber":phonenumber,"cateId":cateId,"sleepTime":sleepTime}  # cate_id是仓库号，length是数量
            return args

    def sendProcess(self):
        try:
            # cap = webdriver.DesiredCapabilities.PHANTOMJS
            # cap["phantomjs.page.settings.resourceTimeout"] = 1000
            # cap["phantomjs.page.settings.loadImages"] = False
            # cap["phantomjs.page.settings.disk-cache"] = True

            count = 0
            changeCount = 0
            while True:
                args = self.getArgs()
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
                changeCount = changeCount + 1
                numbers = self.repo.GetAccount("normal",repo_cate_id, 20, 1)
                if len(numbers) == 0:
                    print u"%s号仓库没有数据" % repo_cate_id
                    time.sleep(300)
                    try:
                        driver.close( )
                        driver.quit( )
                    except:
                        pass
                    return
                QQNumber = numbers[0]['number']  # 即将登陆的QQ号
                QQPassword = numbers[0]['password']
                user_agent = numbers[0]['imei']
                if user_agent is None or user_agent == '':
                    user_agentList = self.repo.GetMaterial(user_agent_id, 0, 1)
                    if len(user_agentList) == 0:
                        # print "%s号仓库为空，没有取到消息"%repo_material_cateId
                        try:
                            driver.close( )
                            driver.quit( )
                        except:
                            pass
                        return
                    user_agent = user_agentList[0]['content']
                print user_agent
                try:
                    command = 'taskkill /F /IM phantomjs.exe'
                    os.system(command)
                    # print u'close02'
                except:
                    pass
                # user_agent = "Mozilla/5.0(hp-tablet;Linux;hpwOS/3.0.0;U;en-US)AppleWebKit/534.6(KHTML,likeGecko)wOSBrowser/233.70Safari/534.6TouchPad/1.0"
                # user_agent = "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;"
                # cap["phantomjs.page.settings.userAgent"] = user_agent
                # cap["phantomjs.page.customHeaders.User-Agent"] = user_agent
                # driver = webdriver.PhantomJS( desired_capabilities=cap,
                #                               executable_path=r"/usr/local/phantomjs/bin/phantomjs" )
                user_agent = "Mozilla/5.0(BlackBerry;U;BlackBerry9800;en)AppleWebKit/534.1+(KHTML,likeGecko)Version/6.0.0.337MobileSafari/534.1+"
                options = webdriver.ChromeOptions( )
                options.add_argument( 'disable-infobars' )
                options.add_argument( 'lang=zh_CN.UTF-8' )
                # options.add_argument( 'headless' )
                # 更换头部
                # options.add_argument(user_agent)
                options.add_argument( 'user-agent="%s' % user_agent )
                driver = webdriver.Chrome( chrome_options=options, executable_path="/opt/google/chrome/chromedriver" )

                emailnumbers = self.repo.GetNumber(repo_number_cate_id, 0, 1)  # 取出add_count条两小时内没有用过的号码
                if len(emailnumbers) == 0:
                    print u"%s号仓库没有数据" % repo_number_cate_id
                    time.sleep(300)
                    try:
                        driver.close( )
                        driver.quit( )
                    except:
                        pass
                    return
                emailnumber = emailnumbers[0]['number']
                driver.get(
                    "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                        emailnumber, repo_number_cate_id, "normal"))

                # 检查是否连接网络
                # driver.get("https://www.baidu.com/")
                # if "百度一下" in driver.page_source.encode("utf-8"):
                #     print "Internet OK"
                # else:
                #     print "Internet NO"
                #     return

                # 打开QQ邮箱登陆界面
                driver.delete_all_cookies()
                driver.get("https://w.mail.qq.com/")
                # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled')
                time.sleep(3)
                driver.save_screenshot("01.png")
                # driver.save_screenshot("0.png")
                # 点 进入网页版QQ邮箱 (模拟手机版会有这个)
                try:
                    obj = driver.find_element_by_xpath("//td[@class='enter_mail_button_td']/a")
                    obj.click()

                except:
                    print "error"

                try:
                    # 若帐号输入框有内容先清空
                    driver.find_element_by_id("u").clear()
                except:
                    pass
                try:
                    # ///
                    # 输入框输入帐号和密码
                    driver.find_element_by_id("u").send_keys(QQNumber)
                    driver.find_element_by_id("p").send_keys(QQPassword)
                    # driver.save_screenshot( "222.png" )
                    time.sleep(1)
                    driver.find_element_by_id("go").click()
                    time.sleep(random.randint(time_delayStart, time_delayEnd))
                except:
                    pass

                try:
                    obj = driver.find_element_by_class_name("qm_btnIcon")
                    print u"%s  登陆成功" % QQNumber
                    Repo().BackupInfo(repo_cate_id, 'normal', QQNumber, user_agent, '')
                    # driver.save_screenshot("SSS.png")
                except:
                    print u"%s  登陆失败" % QQNumber
                    driver.save_screenshot("002.png")
                    time.sleep(2)
                    # 登陆出现异常状况
                    errorPage = driver.page_source.encode("utf-8")

                    if "拖动下方滑块完成拼图" in errorPage:
                        print u"%s  拖动下方滑块完成拼图" % QQNumber
                    elif "帐号或密码不正确" in errorPage:
                        print u"%s  帐号或密码不正确" % QQNumber
                    elif "冻结" in errorPage:
                        print u"%s  冻结" % QQNumber
                        self.repo.BackupInfo(repo_cate_id, 'frozen', QQNumber, '', '')
                        driver.get(
                            "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                repo_cate_id, "frozen", QQNumber, "", ""))

                        # try:
                        #     obj = driver.find_element_by_id("p")
                        #     text = obj.get_attribute("text")
                        #
                        #     driver.find_element_by_id("p").send_keys(QQPassword)
                        #
                        #     driver.find_element_by_id("go").click()
                        #     try:
                        #         driver.find_element_by_id("go")
                        #         print u"%s  冻结" % QQNumber
                        #         self.repo.BackupInfo(repo_cate_id, 'frozen', QQNumber, '', '')
                        #         driver.get(
                        #             "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #                 repo_cate_id, "frozen", QQNumber, "", ""))
                        #     except:
                        #         pass
                        #         self.repo.BackupInfo(repo_cate_id, 'frozen', QQNumber, '', '')
                        # except:
                        #     pass
                    try:
                        obj = driver.find_element_by_class_name("content")
                    except:
                        time.sleep(2)
                    try:
                        driver.close( )
                        driver.quit( )
                    except:
                        pass
                    # self.ipChange.ooo()
                    # self.ipChange.ooo()
                    time.sleep(5)
                    continue


                url = driver.current_url.encode("utf-8")
                driver.find_element_by_xpath("//span[@class='qm_icon qm_icon_Compose']").click()
                time.sleep(3)
                while driver.current_url == url:
                    time.sleep(2)
                    print "mei jin qu"
                    try:
                        driver.find_element_by_class_name("qm_btnIcon").click()
                    except:
                        pass

                tourl = driver.current_url.encode("utf-8")
                flag = True
                while flag:
                    args = self.getArgs()
                    emailType = args["emailType"]
                    repo_material_cateId2 = args["repo_material_cateId2"]
                    repo_material_cateId = args["repo_material_cateId"]
                    repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
                    sendTime = args["sendTime"].split( "-" )
                    try:
                        sendTimeStart = int( sendTime[0] )
                        sendTimeEnd = int( sendTime[1] )
                    except:
                        print  u"发送时间间隔的参数格式有误"
                        sendTimeStart = 3
                        sendTimeEnd = 5
                    emailnumbers = self.repo.GetNumber(repo_number_cate_id, 0, 1)  # 取出add_count条两小时内没有用过的号码
                    bccnumbers = self.repo.GetNumber( repo_number_cate_id, 0, 1 )
                    if len(emailnumbers) == 0:
                        print u"%s号仓库没有数据" % repo_number_cate_id
                        # print u'close08'
                        try:
                            driver.close( )
                            driver.quit( )
                        except:
                            pass
                        return
                    if repo_material_cateId == "" or repo_material_cateId is None:
                        selectContent1 = ""
                    else:
                        selectContent1 = "只发主题"
                        Material = self.repo.GetMaterial(repo_material_cateId, 0, 1)
                        if len(Material) == 0:
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
                        Material2 = self.repo.GetMaterial(repo_material_cateId2, 0, 1)
                        if len(Material2) == 0:
                            print u"%s号仓库为空，没有取到消息" % repo_material_cateId
                            try:
                                driver.close( )
                                driver.quit( )
                            except:
                                pass
                            return
                        message2 = Material2[0]['content']

                    time.sleep(2)
                    try:
                        obj = driver.find_element_by_xpath('//*[@id="attachUpload"]/a/input')
                        obj.send_keys("/home/zunyun/text/images/55555.jpg")
                    except:
                        pass


                    emailnumber = emailnumbers[0]['number']
                    bccnumber = bccnumbers[0]['number']
                    try:
                        emailnumberObj = driver.find_element_by_id("showto")
                    except:
                        try:
                            emailnumberObj = driver.find_element_by_id("to")
                        except:
                            driver.get(tourl)
                            time.sleep(2)
                            print "ye mian mei jia zai chu lai"
                            try:
                                self.repo.UpdateNumberStauts(emailnumber, repo_number_cate_id, "normal")
                                driver.get(
                                    "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        emailnumber, repo_number_cate_id, "normal"))
                            except:
                                pass
                            # print u'close11'
                            # self.ipChange.ooo()
                            # self.ipChange.ooo()
                            time.sleep(3)
                            try:
                                driver.close( )
                                driver.quit( )
                            except:
                                pass
                            return "false"

                    if "@" not in emailnumber:
                        if emailType == "QQ邮箱":
                            emailnumberObj.send_keys(emailnumber + "@qq.com")
                        elif emailType == "189邮箱":
                            emailnumberObj.send_keys(emailnumber + "@189.cn")
                        elif emailType == "139邮箱":
                            emailnumberObj.send_keys(emailnumber + "@139.com")
                        elif emailType == "163邮箱":
                            emailnumberObj.send_keys(emailnumber + "@163.com")
                        elif emailType == "wo邮箱":
                            emailnumberObj.send_keys(emailnumber + "@wo.cn")
                        else:
                            emailnumberObj.send_keys(emailnumber + "@qq.com")
                    else:
                        emailnumberObj.send_keys(emailnumber)

                    #密送
                    try:
                        driver.find_element_by_xpath( '//*[@id="more"]/div/a' ).click( )
                    except:
                        driver.find_element_by_xpath('//*[@id="composeMain"]/div/div/div[2]/div/a').click()
                    time.sleep( 1 )
                    try:
                        bccnumberObj = driver.find_element_by_xpath( '//*[@id="showbcc"]' )
                    except:
                        bccnumberObj = driver.find_element_by_xpath( '//*[@id="bcc"]' )

                    if "@" not in bccnumber:
                        if emailType == "QQ邮箱":
                            bccnumberObj.send_keys(bccnumber + "@qq.com")
                        elif emailType == "189邮箱":
                            bccnumberObj.send_keys(bccnumber + "@189.cn")
                        elif emailType == "139邮箱":
                            bccnumberObj.send_keys(bccnumber + "@139.com")
                        elif emailType == "163邮箱":
                            bccnumberObj.send_keys(bccnumber + "@163.com")
                        elif emailType == "wo邮箱":
                            bccnumberObj.send_keys(bccnumber + "@wo.cn")
                        else:
                            bccnumberObj.send_keys(bccnumber + "@qq.com")
                    else:
                        bccnumberObj.send_keys(bccnumber)

                    if selectContent1 == "只发主题":
                        driver.find_element_by_id("subject").send_keys(message)
                    if selectContent2 == "只发内容":
                        driver.find_element_by_id("content").send_keys(message2)
                    time.sleep(3)
                    try:
                        # windows
                        driver.find_element_by_name("RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__").click()
                    except:
                        driver.find_element_by_id("composeSend").click()
                    time.sleep(random.randint(sendTimeStart, sendTimeEnd))
                    page_source = driver.page_source
                    flagFirst = False
                    if "发送成功" in page_source and "验证码" not in page_source:
                        print u"%s  发送成功" % QQNumber
                        count = 0
                    else:
                        print u"%s  发送不成功" % QQNumber

                        try:
                            self.repo.UpdateNumberStauts(emailnumber, repo_number_cate_id, "normal")
                            driver.get(
                                "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                emailnumber, repo_number_cate_id, "normal"))
                        except:
                            pass
                        flag = False
                        if "邮件中可能包含不合适的用语或内容" in page_source:
                            # 需要解锁
                            print u"%s  邮件中可能包含不合适的用语或内容" % QQNumber
                            self.repo.BackupInfo(repo_cate_id, 'exception', QQNumber, '', '')
                            driver.get(
                                "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                    repo_cate_id, "exception", QQNumber, "", ""))
                            driver.delete_all_cookies()
                        elif "<html><head></head><body></body></html>" in page_source:
                            print "%s  空" % QQNumber
                            driver.delete_all_cookies()
                            # self.ipChange.ooo()
                            # self.ipChange.ooo()
                        elif "验证码" in page_source:
                            flagFirst = True
                            print u"%s  需要验证码" % QQNumber
                            driver.delete_all_cookies()
                            count = count + 1
                            if count >= 2:
                                # self.ipChange.ooo()
                                # self.ipChange.ooo()
                                time.sleep(5)
                                count = 0
                        elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                            driver.delete_all_cookies()
                            print u"%s  您发送的邮件已经达到上限，请稍候再发" % QQNumber
                        elif "您的域名邮箱账号存在异常行为" in page_source:
                            driver.delete_all_cookies()
                            print u"您的域名邮箱账号存在异常行为"
                            self.repo.BackupInfo(repo_cate_id, 'frozen', QQNumber, '', '')
                            driver.get("http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                repo_cate_id, "exception", QQNumber, "", ""))
                        elif "您的帐号存在安全隐患" in page_source:
                            driver.delete_all_cookies()
                            print u"您的帐号存在安全隐患"
                            self.repo.BackupInfo(repo_cate_id, 'exception', QQNumber, '', '')
                            driver.get(
                                "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                    repo_cate_id, "frozen", QQNumber, "", ""))
                        else:
                            driver.save_screenshot("%s-%s.png" % (QQNumber, self.GetUnique()))
                            print u"%s  该情况没判断出来" % QQNumber
                            driver.delete_all_cookies()
                            # self.ipChange.ooo()
                            # self.ipChange.ooo()
                            time.sleep(5)
                    if flagFirst:
                        try:
                            # self.repo.AccountFrozenTimeDelay(QQNumber, repo_cate_id)
                            driver.get(
                                "http://data.zunyun.net/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                                    QQNumber, repo_cate_id,"PT_QQ"))
                        except:
                            pass

                    if flag:
                        driver.get(tourl)
                        time.sleep(2)
                        try:
                            driver.find_element_by_xpath("//span[@class='qm_icon qm_icon_Compose']").click()
                        except:
                            pass
                    else:
                        pass

                if not flag:
                    if changeCount >= 5:
                        # self.ipChange.ooo()
                        # self.ipChange.ooo()
                        time.sleep(3)
                        changeCount = 0
                driver.get(url)
                time.sleep(2)
                try:
                    driver.find_element_by_link_text("退出").click()
                    time.sleep(2)
                    try:
                        driver.close( )
                        driver.quit( )
                    except:
                        pass
                    driver.delete_all_cookies()
                    if changeCount >= 5:
                        # self.ipChange.ooo()
                        # self.ipChange.ooo()
                        time.sleep(3)
                        changeCount = 0
                except:
                    try:
                        driver.close( )
                        driver.quit( )
                    except:
                        pass
                    print "error"
        except:
            logging.exception("dds")
            command = 'taskkill /F /IM phantomjs.exe'
            os.system(command)
            try:
                driver.close( )
                driver.quit( )
            except:
                pass
            # result = [driver]
            return []

    def action(self):
        # data = self.ipChange.Check_for_Broadband()
        # if data != None:
        #     print u"宽带确认已连接,模块继续运行"
        # else:
        #     print u"宽带未连接,连接宽带"
        #     self.ipChange.ooo()
        #     time.sleep(5)

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
        args = self.getArgs( )
        phonenumber = args["phonenumber"]
        cateId = args["cateId"]
        para = {"phoneNumber": phonenumber, "x_04": sta}
        self.repo.PostInformation( cateId, para )



def getPluginClass():
    return EmailInternet

if __name__ == "__main__":

    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()

    # time.sleep(150)
    # while True:
    #     try:
    #         o.action()
    #     except Exception,e:
    #         print e

    Material2 = Repo().GetMaterial( "362", 0, 1 )
    if len( Material2 ) == 0:
        print u"%s号仓库为空，没有取到消息" % "362"
    message2 = Material2[0]['content']

    print message2.encode("GB18030")

