# coding:utf-8
from __future__ import division
import base64
import logging
import re
import socket
import urllib2

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs


import os, time, datetime, random
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
sys.path.append("C:\TaskConsole-master")
from IPChange import IPChange
from Repo import Repo
class Email:
    def __init__(self):
        self.repo = Repo()
        self.ipChange = IPChange()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def sendProcess(self, args):
        try:
            emailType = args["emailType"]
            repo_material_cateId2 = args["repo_material_cateId2"]
            repo_material_cateId = args["repo_material_cateId"]
            sendTime = args["sendTime"]
            sendTime = sendTime.split( "-" )
            user_agent_id = args["user_agent_id"]
            sc = 0
            flagFirst = False
            flagFirst2 = False
            try:
                sendTimeStart = int( sendTime[0] )
                sendTimeEnd = int( sendTime[1] )
            except:
                print  u"发送时间间隔的参数格式有误"
                sendTimeStart = 3
                sendTimeEnd = 5

            time_delay = args["time_delay"]
            time_delay = time_delay.split( "-" )
            try:
                time_delayStart = int( time_delay[0] )
                time_delayEnd = int( time_delay[1] )
            except:
                print  u"参数格式有误"
                time_delayStart = 3
                time_delayEnd = 5
            count = 0
            changeCount = 0
            while True:
                user_agentid = args["user_agent_id"]
                repo_cate_id = args["repo_cate_id"]
                numbers = Repo( ).GetAccount( repo_cate_id, 5, 1 )
                if len( numbers ) == 0:
                    print u"%s号仓库没有数据,等待5分钟" % repo_cate_id
                    time.sleep(300)
                    return

                account = numbers[0]['number']  # 即将登陆的QQ号
                password = numbers[0]['password']
                accountArr = account.split("@")
                account2 = accountArr[0] + "%40" + accountArr[1]
                user_agent = numbers[0]['imei']
                changeCount = changeCount + 1
                if user_agent is None or user_agent == '':
                    user_agentList = Repo( ).GetMaterial( user_agent_id, 0, 1 )
                    if len( user_agentList ) == 0:
                        print u"%s号仓库为空" % repo_material_cateId
                        return
                    user_agent = user_agentList[0]['content']
                # user_agent = "Mozilla/5.0(Linux;U;Android2.3.7;en-us;NexusOneBuild/FRF91)AppleWebKit/533.1(KHTML,likeGecko)Version/4.0MobileSafari/533.1"
                print user_agent
                command = 'taskkill /F /IM phantomjs.exe'
                os.system(command)
                cap = webdriver.DesiredCapabilities.CHROME
                cap["chromedriver.page.settings.resourceTimeout"] = 1000
                cap["chromedriver.page.settings.loadImages"] = True
                cap["chromedriver.page.settings.disk-cache"] = True
                cap[
                    "chromedriver.page.settings.userAgent"] = "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"

                cap[
                    "phantomjs.page.customHeaders.User-Agent"] = "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
                driver = webdriver.Chrome( desired_capabilities=cap, executable_path="/opt/google/chrome/chromedriver" )

                driver.get( "https://m.exmail.qq.com/cgi-bin/loginpage" )

                driver.get( "https://m.exmail.qq.com/cgi-bin/loginpage" )
                # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled')
                time.sleep( 3 )
                if changeCount >= 5:
                    self.ipChange.ooo()
                    self.ipChange.ooo()
                    time.sleep(5)
                    changeCount = 0
                    continue

                # driver.save_screenshot( "111.png" )
                try:
                    driver.find_element_by_id( "uin" ).clear( )
                except:
                    pass
                try:
                    driver.find_element_by_id( "uin" ).send_keys( account )
                    time.sleep( 0.5 )
                    driver.find_element_by_id( "pwd" ).send_keys(password)
                    #driver.save_screenshot( "222.png" )
                    time.sleep( 1 )
                    driver.find_element_by_id( "pwd" ).send_keys( Keys.ENTER )
                    time.sleep( random.randint( time_delayStart, time_delayEnd ) )
                    #driver.save_screenshot( "333.png" )
                except:
                    pass

                try:
                    obj = driver.find_element_by_class_name( "qm_icon_Compose" )
                    print u"%s  登陆成功" % account
                    # Repo( ).BackupInfo( repo_cate_id, 'normal', QQNumber, user_agent, '' )
                    startUrl = driver.current_url
                except:
                    print u"%s  登陆失败" % account

                    time.sleep( 2 )
                    # 登陆出现异常状况
                    errorPage = driver.page_source.encode( "utf-8" )
                    if "拖动下方滑块完成拼图" in errorPage:
                        print u"拖动下方滑块完成拼图"
                    elif "看不清" in errorPage:
                        print u"需要验证码"
                    elif "验证码" in errorPage:
                        print u"验证码"
                    elif "帐号或密码不正确" in errorPage:
                        print u"帐号或密码不正确"
                    elif "冻结" in errorPage:
                        print u"冻结"
                        self.repo.BackupInfo( repo_cate_id, 'frozen', account, '', '' )
                        driver.get(
                            "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                repo_cate_id, "frozen", account, "", ""))
                    elif "请输入完整的成员帐号，包括域名。" in errorPage:
                        print  u"%s 冻结" % account
                        try:
                            self.repo.BackupInfo(repo_cate_id, 'frozen', account, '', '')
                            driver.get(
                                "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                    repo_cate_id, "frozen", account, "", ""))
                        except:
                            pass
                    else:
                        driver.save_screenshot("%s-%s.png"%(account,self.GetUnique()))
                    try:
                        obj = driver.find_element_by_class_name( "content" )
                        #driver.save_screenshot( "aaa.png" )

                        # Repo().BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )
                    except:
                        time.sleep( 2 )
                        #driver.save_screenshot( "%s.png"%(account) )
                    continue

                url = driver.current_url.encode( "utf-8" )
                obj.click( )
                time.sleep(2)
                #driver.save_screenshot( "444.png" )
                flag = True
                while flag:
                    repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
                    emailnumbers = Repo( ).GetNumber( repo_number_cate_id, 0, 1 )  # 取出add_count条两小时内没有用过的号码
                    if len( emailnumbers ) == 0:
                        print u"QQ号码库%s号仓库为空" % repo_number_cate_id
                        driver.quit( )
                        return
                    # emailnumber = emailnumbers[0]['number']

                    if repo_material_cateId=="" or repo_material_cateId is None:
                        selectContent1 = ""
                    else:
                        selectContent1 = "只发主题"
                        Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                        if len( Material ) == 0:
                            print u"%s  号仓库为空，没有取到消息"%repo_material_cateId
                            driver.quit( )
                            return
                        message = Material[0]['content']
                    if repo_material_cateId2=="" or repo_material_cateId2 is None:
                        selectContent2 = ""
                    else:
                        selectContent2 = "只发内容"
                        Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                        if len( Material2 ) == 0:
                            # print "%s号仓库为空，没有取到消息" % repo_material_cateId
                            driver.quit( )
                            return
                        message2 = Material2[0]['content']
                    emailnumber = emailnumbers[0]['number']
                    #driver.save_screenshot("test01.png")
                    # try:
                    #     emailnumberObj = driver.find_element_by_id( "to" )
                    #     emailnumberObj.click()
                    # except:
                    #     emailnumberObj = driver.find_element_by_id( "showto" )
                    try:
                        emailnumberObj = driver.find_element_by_id( "showto" )
                    except:
                        #driver.save_screenshot("to.png")
                        try:
                            emailnumberObj = driver.find_element_by_id( "to" )
                        except:
                            driver.get( url )
                            print "ye mian mei jia zai chu lai"
                            try:
                                self.repo.UpdateNumberStauts(emailnumber, repo_number_cate_id, "normal")
                                driver.get(
                                    "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                    emailnumber, repo_number_cate_id, "normal"))
                            except:
                                pass
                            # driver.get(url)  # mu di shi chu cuo tiao chu gai ren wu dan biao ji wei zhengchang
                            return "false"
                    if "@" not in emailnumber:
                        if emailType == "QQ邮箱":
                            emailnumberObj.send_keys( emailnumber + "@qq.com" )
                        elif emailType == "189邮箱":
                            emailnumberObj.send_keys( emailnumber + "@189.cn" )
                        elif emailType == "139邮箱":
                            emailnumberObj.send_keys( emailnumber + "@139.com" )
                        elif emailType == "163邮箱":
                            emailnumberObj.send_keys( emailnumber + "@163.com" )
                        elif emailType == "wo邮箱":
                            emailnumberObj.send_keys( emailnumber + "@wo.cn" )
                        else:
                            emailnumberObj.send_keys( emailnumber + "@qq.com" )
                    else:
                        emailnumberObj.send_keys( emailnumber)
                    #driver.save_screenshot( "mmm.png" )

                    if selectContent1 == "只发主题":
                        driver.find_element_by_id("subject").send_keys(message)
                    if selectContent2 == "只发内容":
                        driver.find_element_by_id("content").send_keys(message2)

                    time.sleep( 3 )
                    try:
                        driver.find_element_by_id( "composeSend" ).click( )
                    except:
                        driver.find_element_by_name( "RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__" ).click( )
                    time.sleep( random.randint( sendTimeStart, sendTimeEnd ) )

                    try:
                        try:
                            driver.find_element_by_id("composeSend")
                        except:
                            driver.find_element_by_name("RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__")
                        time.sleep(3)

                    except:
                        pass

                    page_source = driver.page_source.encode("utf-8")
                    if "发送成功" in page_source and "验证码" not in page_source:
                        # nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                        # driver.save_screenshot("%s.png" % nowTime)
                        try:
                            try:
                                driver.find_element_by_id("composeSend")
                            except:
                                driver.find_element_by_name("RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__")
                            flag = False
                            print u"发送后还在发信页面"
                            # self.repo.AccountFrozenTimeDelay(account, repo_cate_id,)
                            driver.get("http://data.zunyun.net/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                                    account2, repo_cate_id, "PT_QQ"))
                            try:
                                # self.repo.UpdateNumberStauts(emailnumber, repo_number_cate_id, "normal")
                                driver.get(
                                    "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                    emailnumber, repo_number_cate_id, "normal"))
                            except:
                                pass

                        except:
                            print u"发送成功"
                            flagFirst = False
                            flagFirst = False
                            # sc = sc + 1
                            # if sc>=20:
                            #     flag = False
                            #     sc = 0
                            count = 0
                    else:
                        # driver.save_screenshot("qqq.png")
                        try:
                            # if flagFirst:
                            #     try:
                            #         self.repo.AccountFrozenTimeDelay(account,repo_cate_id)
                            #     except:
                            #         pass
                            if "验证码" in page_source:
                                print u"需要验证码"
                                flag = False
                                flagFirst = True
                                sc = 0
                                count = count + 1
                                if count >= 2:
                                    self.ipChange.ooo()
                                    self.ipChange.ooo()
                                    time.sleep(3)
                                    count = 0
                            elif "邮件中可能包含不合适的用语或内容" in page_source:
                                sc = 0
                                flag = False

                                print u"%s  邮件中可能包含不合适的用语或内容"%account
                            elif "<html><head></head><body></body></html>" in page_source:
                                sc = 0
                                flag = False
                                print "空"
                                driver.get(
                                    "http://data.zunyun.net/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                                        account2, repo_cate_id, "PT_QQ"))
                                self.ipChange.ooo()
                                self.ipChange.ooo()
                                time.sleep(3)
                            elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                                sc = 0
                                flag = False
                                flagFirst2 = True
                                print u"您发送的邮件已经达到上限，请稍候再发"
                            elif "您的域名邮箱账号存在异常行为" in page_source:
                                sc = 0
                                flag = False
                                print u"您的域名邮箱账号存在异常行为"
                                self.repo.BackupInfo(repo_cate_id, 'exception', account, '', '')
                                driver.get("http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                    repo_cate_id, "exception", account, "", ""))
                            elif "您的帐号存在安全隐患" in page_source:
                                sc = 0
                                flag = False
                                print u"您的帐号存在安全隐患"
                                self.repo.BackupInfo(repo_cate_id, 'frozen', account, '', '')
                                driver.get(
                                    "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                        repo_cate_id, "frozen", account, "", ""))
                            else:
                                driver.find_element_by_class_name( "qm_icon_Compose" )
                                sc = sc + 1
                                if sc >= 20:
                                    flag = False
                                    sc = 0
                                print u"%s发送成功2"%account
                                flagFirst = False
                                flagFirst2 = False
                        except:

                            try:
                                self.repo.UpdateNumberStauts(emailnumber, repo_number_cate_id, "normal")
                                driver.get(
                                    "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                    emailnumber, repo_number_cate_id, "normal"))
                            except:
                                pass
                            print u"%s  发送不成功"%account
                            sc = 0
                            flag = False
                            if "验证码" in page_source:
                                print u"需要验证码"
                                flagFirst = False
                                count = count + 1
                                if count >= 2:
                                    self.ipChange.ooo()
                                    self.ipChange.ooo()
                                    time.sleep(3)
                                    count = 0
                            if "邮件中可能包含不合适的用语或内容" in page_source:
                                print u"%s  邮件中可能包含不合适的用语或内容"%account
                            elif "<html><head></head><body></body></html>" in page_source:
                                print "空"
                                driver.get(
                                    "http://data.zunyun.net/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                                        account2, repo_cate_id, "PT_QQ"))
                                driver.get(url)
                                self.ipChange.ooo()
                                self.ipChange.ooo()
                                time.sleep(3)
                            elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                                flagFirst2 = True
                                print u"您发送的邮件已经达到上限，请稍候再发"
                            elif "您的域名邮箱账号存在异常行为" in page_source:
                                print u"您的域名邮箱账号存在异常行为"
                                self.repo.BackupInfo(repo_cate_id, 'exception', account, '', '')
                                driver.get(
                                    "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                    repo_cate_id, "exception", account, "", ""))
                            elif "您的帐号存在安全隐患" in page_source:
                                print u"您的帐号存在安全隐患"
                                self.repo.BackupInfo(repo_cate_id, 'exception', account, '', '')
                                driver.get(
                                    "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                        repo_cate_id, "frozen", account, "", ""))
                            else:
                                print page_source
                                driver.save_screenshot( "%s-%s.png" % (account, self.GetUnique( )) )
                                print "error"
                    if flagFirst:
                        try:
                            # self.repo.AccountFrozenTimeDelay(account, repo_cate_id)
                            driver.get(
                                "http://data.zunyun.net/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                                    account, repo_cate_id,"QY_QQ"))
                        except:
                            pass
                    if flagFirst2:
                        try:
                            # self.repo.AccountFrozenTimeDelay(account, repo_cate_id)
                            driver.get(
                                "http://data.zunyun.net/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                                    account2, repo_cate_id,"PT_QQ"))

                        except:
                            pass
                    driver.get( url )
                    time.sleep(2)
                    try:
                        driver.find_element_by_class_name( "qm_icon_Compose" ).click()
                    except:
                        pass

                # 删除邮件
                driver.get( startUrl )
                folderList = driver.find_elements_by_xpath("//span[@class='qm_list_item_title']")
                for index in folderList:
                    if index.text == '文件夹':
                        index.click()
                        break
                # folder = driver.find_elements_by_xpath( "//span[@class='qm_list_item_title']" )[5]
                # folder.click( )
                #driver.save_screenshot( "folder.png" )
                folderUrl = driver.current_url
                folderList_del = driver.find_elements_by_xpath( "//span[@class='qm_list_item_title']" )
                del_folerArr = []
                for index in folderList_del:
                    if index.text == '收件箱' or index.text == '已发送' or index.text == '已删除':
                       del_folerArr.append(index)

                i = 0
                del_folerArr[i].click()
                while True:
                    try:
                        try:
                            driver.find_element_by_id( "selectall" ).click( )
                        except:
                            if "没有邮件" in driver.page_source.encode( "utf-8" ):
                                if i == 2:
                                    break
                                i = i + 1
                                driver.get( folderUrl )
                                if i == 1:
                                   del_folerArr[i].click( )
                                else:
                                    del_folerArr[i].click()
                                # driver.save_screenshot("delete02.png")
                                time.sleep( 1 )
                                continue
                        # driver.save_screenshot( "delete.png" )
                        deleteObj = None
                        if i == 1 :
                            try:
                                deleteObj = driver.find_element_by_xpath("//div[@class='qm_actionBar_listItem qm_btnGroup func_posRelative']/input[@class='qm_btn']" )
                            except:
                               pass
                        else:
                            try:
                                deleteObj = driver.find_elements_by_xpath("//div[@class='qm_actionBar_listItem qm_btnGroup func_posRelative']/input[@class='qm_btn']" )[1]
                            except:
                                deleteObj = driver.find_element_by_xpath("//div[@class='qm_actionBar_listItem qm_btnGroup func_posRelative']/input[@class='qm_btn']" )
                        if not deleteObj is None:
                            deleteObj.click( )
                        else:
                            i = i + 1
                            driver.get(folderUrl)
                            time.sleep(3)
                            del_folerArr[i].click()
                        #driver.save_screenshot( "delete2.png" )
                        if "没有邮件" in driver.page_source.encode( "utf-8" ):
                            if i == 2:
                                break
                            i = i + 1
                            driver.get( folderUrl )
                            if i == 1:
                                del_folerArr[i].click()
                            else:
                                del_folerArr[i].click()
                            # driver.save_screenshot("delete02.png")
                            time.sleep( 1 )
                        #driver.save_screenshot( "get.png" )
                    except:
                        break

                if not flag:
                    try:
                        driver.delete_all_cookies()
                    except:
                        pass
                    if changeCount >= 5:
                        self.ipChange.ooo()
                        self.ipChange.ooo()
                        time.sleep(3)
                        changeCount = 0
                    continue

                # 退出帐号重新登陆
                try:
                    obj = driver.find_elements_by_xpath( "//p[@class='qm_footer_userInfo']/a" )
                    obj[0].click( )
                    time.sleep( 2 )
                    if changeCount >= 5:
                        self.ipChange.ooo()
                        self.ipChange.ooo()
                        time.sleep(3)
                        changeCount = 0
                    # IPChange().ooo()
                    # IPChange().ooo()
                    # time.sleep(3)
                    # driver.save_screenshot( "exit.png" )
                    driver.delete_all_cookies()
                except:
                    if changeCount >= 5:
                        self.ipChange.ooo()
                        self.ipChange.ooo()
                        time.sleep(3)
                        changeCount = 0
                    # driver.save_screenshot("exceptionError.png")
                    # driver.save_screenshot("444.png")
                    print "error"


        except:
                # result = [driver]
            return []

    def action(self):
        data = self.ipChange.Check_for_Broadband()
        if data != None:
            print u"宽带确认已连接,模块继续运行"
        else:
            print u"宽带未连接,连接宽带"
            self.ipChange.ooo()
            time.sleep(5)

        asdlFile = open(r"c:\asdl.txt", "r")
        asdlList = asdlFile.readlines()
        while True:
            if len(asdlList) > 2:
                specifiedTaskId = asdlList[2]
                taskList = self.repo.GetSpecifiedPhantomJSTask(specifiedTaskId)
            else:
                taskList = self.repo.GetPhantomJSTaskInfo("")
                if len(taskList) == 0:
                    print u"检查是否有任务可运行"
                    time.sleep(30)
                    continue

            task = taskList[random.randint(0, len(taskList)) - 1]
            phonenumber = task["phonenumber"]
            cateId = task["cateId"]
            repo_material_cateId = task["x01"]
            repo_material_cateId2 = task["x02"]
            repo_number_cate_id = task["x03"]
            user_agent_id = task["x07"]
            repo_cate_id = task["x08"]

            while True:
                paramList = self.repo.GetPhantomJSParamInfo()
                if len(paramList) == 0:
                    time.sleep(30)
                    continue
                else:
                    break

            param = paramList[random.randint(0, len(paramList)) - 1]
            time_delay = param["x01"]
            sendTime = param["x02"]
            emailType = param["x03"]

            args = {"time_delay": time_delay, "sendTime": sendTime, "repo_cate_id": repo_cate_id,
                    "repo_number_cate_id": repo_number_cate_id, "repo_material_cateId": repo_material_cateId,
                    "repo_material_cateId2": repo_material_cateId2, "emailType": emailType,
                    "user_agent_id": user_agent_id}  # cate_id是仓库号，length是数量

            x = self.sendProcess(args)
            if x == "false":
                sta = "normal"
            elif type(x) == list:
                # d = x[0]
                # try:
                #     d.close()
                #     d.quit()
                # except:
                #     pass
                sta = "normal"
            else:
                sta = "stopped"

            para = {"phoneNumber": phonenumber, "x_04": sta}
            self.repo.PostInformation(cateId, para)

def getPluginClass():
    return Email

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()
    # time.sleep(150)
    # o.action()
