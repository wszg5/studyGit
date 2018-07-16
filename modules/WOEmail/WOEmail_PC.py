# coding:utf-8
from __future__ import division
import base64
import httplib
import logging
import re
import socket
import urllib2
from pyvirtualdisplay import Display
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs


import os, time, datetime, random
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from timeout_decorator import timeout_decorator

sys.path.append("/home/zunyun/workspace/TaskConsole")
# sys.path.append("C:\TaskConsole-master")
# from IPChange import IPChange
from Repo import Repo
class WOEmail_PC:
    def __init__(self):
        self.repo = Repo()
        # self.ipChange = IPChange()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
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
            my_userCount = task["x09"]
            bccCount = task["x10"]
            if my_userCount is None or my_userCount == "" or my_userCount == 0 or my_userCount == "0":
                my_userCount = 0
            else:
                my_userCount = int( my_userCount )

            if bccCount is None or bccCount == "":
                bccCount = 0
            else:
                bccCount = int( bccCount )
            if my_userCount == 0 and bccCount == 0:
                print u"不能没有收件人,默认使用1-->1"
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
                    "user_agent_id": user_agent_id, "phonenumber": phonenumber, "cateId": cateId,
                    "my_userCount": my_userCount, "bccCount": bccCount}  # cate_id是仓库号，length是数量
            return args

    @timeout_decorator.timeout( 120 )
    def login(self,driver,account,password,time_delayStart,time_delayEnd):
        try:

            driver.find_element_by_xpath( '//*[@id="Cname_content"]' ).clear( )
            driver.find_element_by_xpath( '//*[@id="Cname_content"]' ).send_keys( account )
            driver.find_element_by_xpath( '// *[ @ id = "Cpwd_pwd"]' ).send_keys( password )
            driver.find_element_by_xpath( '//*[@id="isAutoLogin"]' ).click( )
            time.sleep( 0.1 )
            driver.find_element_by_xpath( '//*[@id="loginSubmitBtn"]' ).click( )
            # page1 = driver.page_source
            time.sleep( random.randint( time_delayStart, time_delayEnd ) )
            # page2 = driver.page_source
            # if page1 == page2:
            #     time.sleep( 3 )
            #     if page2 == page1:
            #         driver.refresh( )
            #         self.login( driver, account, password, time_delayStart, time_delayEnd )
        except:
            pass

        while True:
            try:
                driver.find_element_by_xpath( '//*[@id="ServiceTerms"]' ).click( )
                time.sleep( 0.5 )
                driver.find_element_by_xpath( '// *[ @ id = "clauseSubmit"]' ).click( )
                time.sleep( 1.5 )
                driver.refresh( )
                time.sleep( 2 )
                # driver.find_element_by_xpath( '//*[@id="writeMailBtn"]/span' )
                return True
            except:
                try:
                    driver.find_element_by_xpath( '//*[@id="writeMailBtn"]/span' )
                    return True
                except:
                    time.sleep( 2 )

    def sendProcess(self):
        try:
            sc = 0
            flagFirst = False
            flagFirst2 = False

            count = 0
            changeCount = 0
            while True:
                args = self.getArgs()
                # user_agentid = args["user_agent_id"]
                user_agent_id = args["user_agent_id"]
                repo_cate_id = args["repo_cate_id"]
                time_delay = args["time_delay"]
                time_delay = time_delay.split( "-" )
                try:
                    time_delayStart = int( time_delay[0] )
                    time_delayEnd = int( time_delay[1] )
                except:
                    print  u"参数格式有误"
                    time_delayStart = 3
                    time_delayEnd = 5

                #测试
                numbers = Repo( ).GetAccount( "normal",repo_cate_id, 60, 1 )
                if len( numbers ) == 0:
                    print u"%s号仓库没有数据,等待5分钟" % repo_cate_id
                    time.sleep(300)
                    return


                account = numbers[0]['number']  # 即将登陆的QQ号
                password = numbers[0]['password']
                accountArr = account.split("@")
                account = accountArr[0]
                # account2 = accountArr[0] + "%40" + accountArr[1]
                # user_agent = numbers[0]['imei']
                # if user_agent!=u"":
                #     print "user_agent%s"%user_agent
                changeCount = changeCount + 1
                # if user_agent is None or user_agent == '':
                user_agentList = self.repo.GetMaterial( user_agent_id, 0, 1 )
                if len( user_agentList ) == 0:
                    print u"%s号仓库为空" % user_agent_id
                    return
                user_agent = user_agentList[0]['content']
                # user_agent = "Mozilla/5.0(Linux;U;Android2.3.7;en-us;NexusOneBuild/FRF91)AppleWebKit/533.1(KHTML,likeGecko)Version/4.0MobileSafari/533.1"
                print user_agent
                command = 'taskkill /F /IM chromedriver.exe'
                os.system(command)

                try:
                    driver.close()
                    driver.quit()
                except:
                    pass
                # display = Display( visible=0, size=(800, 600) )
                # display.start( )
                options = webdriver.ChromeOptions( )
                options.add_argument( 'disable-infobars' )
                options.add_argument( 'lang=zh_CN.UTF-8' )
                # options.add_argument( 'headless' )
                # 更换头部
                # options.add_argument(user_agent)
                options.add_argument('user-agent="%s'%user_agent )
                driver = webdriver.Chrome( chrome_options=options,executable_path="/opt/google/chrome/chromedriver")

                # driver.get( r'https://mail.wo.cn/' )
                # time.sleep( 2 )
                # cookie = {'domain': 'mail.wo.cn', 'name': u'accessID',
                #           'value': u'"120693269314774020003900881:0"'}
                # driver.add_cookie( cookie )
                driver.get( r'https://mail.wo.cn/' )
                time.sleep(2)
                # driver.delete_all_cookies()

                try:
                    loginStatus = self.login( driver, account, password, time_delayStart, time_delayEnd )
                except:
                    loginStatus = False
                if loginStatus:
                    print u"%s  登陆成功" % account
                    # Repo( ).BackupInfo( repo_cate_id, 'normal', QQNumber, user_agent, '' )
                    startUrl = driver.current_url
                else:
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
                    elif "你的帐号存在安全隐患" in errorPage:
                        print u"你的帐号存在安全隐患"
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    elif "帐号或密码不正确" in errorPage:
                        print u"帐号或密码不正确"
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "frozen", account, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    elif "冻结" in errorPage:
                        print u"冻结"
                        self.repo.BackupInfo( repo_cate_id, 'frozen', account, '', '' )
                        # driver.get(
                        #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #         repo_cate_id, "frozen", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                repo_cate_id, "frozen", account, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep(3)
                    elif "请输入完整的成员帐号，包括域名。" in errorPage:
                        print  u"%s 冻结" % account
                        try:
                            # self.repo.BackupInfo(repo_cate_id, 'frozen', account, '', '')
                            # driver.get(
                            #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            #         repo_cate_id, "frozen", account, "", ""))
                            path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                repo_cate_id, "frozen", account, "", "")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
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

                # cookies = driver.get_cookies( )
                # for cookie in cookies:
                #     print("%s->%s" % (cookie['name'], cookie['value']))



                # driver.get( startUrl )
                # time.sleep(1)
                try:
                    driver.find_element_by_xpath( '//*[@id="writeMailBtn"]/span' ).click( )  # 写信
                except:
                    driver.refresh()
                    time.sleep(5)
                    try:
                        driver.find_element_by_xpath( '//*[@id="writeMailBtn"]/span' ).click( )  # 写信
                    except:
                        pass

                # textContent = u'<h2 style="box-sizing:border-box;font-family:-apple-system, &quot;SF UI Text&quot;, Arial, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, &quot;WenQuanYi Micro Hei&quot;, sans-serif;line-height:1.7;color:#2f2f2f;margin:0px 0px 15px;font-size:24px;text-rendering:optimizeLegibility;background-color:#ffffff;">五、 总结</h2>'
                # driver.find_element_by_xpath( '//*[@id="mailSubject"]' ).send_keys( Keys.TAB, Keys.TAB, Keys.TAB,
                #                                                                     Keys.TAB, Keys.TAB, Keys.TAB,
                #                                                                     Keys.TAB, Keys.TAB, textContent )

                flag = True
                count_Y = 0
                # flag = True
                while flag:
                    args = self.getArgs( )
                    emailType = args["emailType"]
                    repo_material_cateId2 = args["repo_material_cateId2"]
                    repo_material_cateId = args["repo_material_cateId"]
                    my_userCount = args["my_userCount"]
                    bccCount = args["bccCount"]
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
                    emailnumbers = Repo( ).GetNumber( repo_number_cate_id, 0, my_userCount )  # 取出add_count条两小时内没有用过的号码
                    emailnumbersArr = []
                    if len( emailnumbers ) == 0:
                        print u"QQ号码库%s号仓库为空" % repo_number_cate_id
                        time.sleep(100)
                        try:
                            driver.close( )
                            driver.quit( )
                        except:
                            pass
                        return
                    else:
                        for item in emailnumbers:
                            emailnumbersArr.append(item["number"])
                    # emailnumber = emailnumbers[0]['number']
                    bccnumbers = self.repo.GetNumber( repo_number_cate_id, 0, bccCount )  # 取出add_count条两小时内没有用过的号码
                    bccnumbersArr = []
                    if len( bccnumbers ) == 0:
                        print u"QQ号码库%s号仓库为空" % repo_number_cate_id
                        bccnumber = ''
                    else:
                        for item2 in bccnumbers:
                            bccnumbersArr.append(item2["number"])
                    # emailnumber = emailnumbers[0]['number']

                    if repo_material_cateId=="" or repo_material_cateId is None:
                        selectContent1 = ""
                    else:
                        selectContent1 = "只发主题"
                        Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                        if len( Material ) == 0:
                            print u"%s  号仓库为空，没有取到消息"%repo_material_cateId
                            try:
                                driver.close( )
                                driver.quit( )
                            except:
                                pass
                            return
                        message = Material[0]['content']
                    if repo_material_cateId2=="" or repo_material_cateId2 is None:
                        selectContent2 = ""
                    else:
                        selectContent2 = "只发内容"
                        Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                        if len( Material2 ) == 0:
                            # print "%s号仓库为空，没有取到消息" % repo_material_cateId
                            try:
                                driver.close( )
                                driver.quit( )
                            except:
                                pass
                            return
                        message2 = Material2[0]['content'].encode("utf-8")
                        message2 = message2.replace("\"","\\\"")
                        message2 = message2.replace("\n","" )
                        # message2 = message2.replace("\n","\\\n")

                        # message2 = message2.replace("\n","<br>")
                    #driver.save_screenshot("test01.png")
                    # try:
                    #     emailnumberObj = driver.find_element_by_id( "to" )
                    #     emailnumberObj.click()
                    # except:
                    #     emailnumberObj = driver.find_element_by_id( "showto" )
                    # message = "hello"
                    # message2 = u"老同学"

                    try:
                        time.sleep(3)
                        emailnumberObj = driver.find_element_by_xpath( '//*[@id="mailToText"]' )   #定位到收件人
                    except:
                        pass
                    # emailnumber = "75800508@qq.com"
                    emailnumbersArr = ['75800508@qq.com']
                    for emailnumber in emailnumbersArr:
                        if "@" not in emailnumber:
                            if emailType == "QQ邮箱":
                                emailnumberObj.send_keys( emailnumber + "@qq.com;" )
                            elif emailType == "189邮箱":
                                emailnumberObj.send_keys(emailnumber + "@189.cn;" )
                            elif emailType == "139邮箱":
                                emailnumberObj.send_keys(emailnumber + "@139.com;" )
                            elif emailType == "163邮箱":
                                emailnumberObj.send_keys(emailnumber + "@163.com;" )
                            elif emailType == "wo邮箱":
                                emailnumberObj.send_keys(emailnumber + "@wo.cn;" )
                            else:
                                emailnumberObj.send_keys(emailnumber + "@qq.com;" )
                        else:
                            emailnumberObj.send_keys( emailnumber+";" )

                    time.sleep(0.5)
                    driver.find_element_by_xpath( '//*[@id="addBcc"]' ).click( )
                    bccnumbersArr = ["2351382894@qq.com"]
                    for bccnumber in bccnumbersArr:
                        if "@" not in bccnumber:
                            # emailnumber = "455854284"
                            if emailType == "QQ邮箱":
                                bcc =  bccnumber + "@qq.com;"
                            elif emailType == "189邮箱":
                                bcc = bccnumber + "@189.cn;"
                            elif emailType == "139邮箱":
                                bcc = bccnumber + "@139.com;"
                            elif emailType == "163邮箱":
                                bcc = bccnumber + "@163.com;"
                            elif emailType == "wo邮箱":
                                bcc = bccnumber + "@wo.cn;"
                            else:
                                bcc = bccnumber + "@qq.com;"
                        else:
                            bcc = bccnumber + ";"
                        #driver.save_screenshot( "mmm.png" )
                        time.sleep(1)
                        driver.find_element_by_xpath( '//*[@id="mailBccText"]' ).send_keys( bcc )
                        time.sleep(0.5)

                    if selectContent1 == "只发主题":
                        try:
                            driver.find_element_by_xpath( '//*[@id="mailSubject"]' ).send_keys( message )  # 主题
                            time.sleep(0.5)
                        except:
                            pass

                    # try:
                    #     obj = driver.find_element_by_xpath( '//*[@id="attachFile"]' ).click( )
                    #     driver.find_element_by_xpath( '//*[@id="attachFile"]' ).send_keys(
                    #         "/home/zunyun/text/images/1" )
                    # except:
                    #     obj = driver.find_element_by_xpath( '//*[@id="attachFile"]' )
                    #     obj.send_keys( "/home/zunyun/text/images/1" )
                    #     logging.exception( "xx" )
                    # time.sleep(2)
                    # driver.find_element_by_xpath('//*[@id="editor_toolbar_btn_container"]').click()
                    # time.sleep(1.5)
                    #
                    # driver.find_element_by_xpath( '// *[ @ id = "QMEditorArea"] / table / tbody / tr[1] / td / div / div[1] / div[15] / div / input' ).click( )
                    if selectContent2 == "只发内容":
                        driver.switch_to_frame( 'mailEditorIframeId' )
                        time.sleep(2)
                        js = "setMailEditorContentHtml('%s') ;" % message2.encode("utf-8")
                        # js = "var x = setMailEditorContentHtml(\"<h1>Hi</h1> <sapn id='s'></sapn>\");"
                        # js = "setMailEditorContentHtml('<h1>Hi</h1> <span style=\"font-size:1px\">乓</span>ｖ<span>乓</span>的发<v>sdfs</v>送ｖ发财<sapn id=\"s\"></sapn>');"
                        # js = "setMailEditorContentHtml('<h1>Hi</h1> <sapn style="font-size:0px">456825</sapn>');"

                        try:
                            driver.execute_script( js )
                        except Exception,e:
                            print e
                        time.sleep(2)


                    driver.switch_to_default_content( )
                    driver.find_element_by_xpath( '//*[@id="sendMailBtn"]' ).click( )
                    time.sleep(3)

                    page_source = driver.page_source.encode("utf-8")
                    for i in range(0,30):
                        if "邮件发送中" in page_source:
                            time.sleep(2)
                            page_source = driver.page_source.encode( "utf-8" )
                        else:
                            break
                    # page_source = driver.page_source.encode( "utf-8" )
                    if "发送成功" in page_source and "验证码" not in page_source and "发送失败" not in page_source:
                        page_source = driver.page_source.encode( "utf-8" )
                        try:
                            if "我去~楼太高，这个页面被挡住了" in driver.page_source:
                                print u"我去~楼太高，这个页面被挡住了"
                                print u"%s 发送失败 给 %s,密送号码为%s" % (account, emailnumbersArr, bccnumbersArr)
                                for it in emailnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                for it2 in bccnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                            emailnumberObj = driver.find_element_by_xpath( '//*[@id="mailToText"]' )
                            print "点击发送还在原界面"
                            for it in emailnumbersArr:
                                path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                    it, repo_number_cate_id, "normal")
                                conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                conn.request( "GET", path )
                                time.sleep( 1 )
                            for it2 in bccnumbersArr:
                                path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                    it, repo_number_cate_id, "normal")
                                conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                conn.request( "GET", path )
                                time.sleep( 1 )
                            flagFirst2 = True
                            count_Y = count_Y + 1
                            if count_Y >= 2:
                                flag = False
                            else:
                                time.sleep( random.randint( 5, 10 ) )
                        except:
                            flag = False
                            if "Connection timed out" in page_source:
                                for it in emailnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                for it2 in bccnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                print u"连接超时"
                            elif "Timed Out" in page_source:
                                for it in emailnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                for it2 in bccnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                print u"超时了"
                            elif "Connection unexpectedly closed" in page_source:
                                for it in emailnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                for it2 in bccnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                print u"连接意外关闭"
                            elif "The email message was detected as spam" in page_source:
                                for it in emailnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                for it2 in bccnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                print u"可能ip黑了"
                                # self.ipChange.ooo()
                                # self.ipChange.ooo()
                            elif "5.7.1 Too many spam messages sent" in page_source:
                                for it in emailnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                for it2 in bccnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                print u"可能ip黑了"
                                # self.ipChange.ooo()
                                # self.ipChange.ooo()
                            elif "5.7.1 Too many messages sent" in page_source:
                                for it in emailnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                for it2 in bccnumbersArr:
                                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                        it, repo_number_cate_id, "normal")
                                    conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                    conn.request( "GET", path )
                                    time.sleep( 1 )
                                print u"可能达到上限了"
                            else:
                                count_Y = 0
                                flag = True
                                print u"%s 发送成功 给 %s,密送号码为%s" % (account, emailnumbersArr, bccnumbersArr)
                                flagFirst = False
                                flagFirst2 = False
                        # flag = False

                    else:
                        flag = False
                        print u"%s 发送失败 给 %s,密送号码为%s" % (account, emailnumbersArr, bccnumbersArr)
                        for it in emailnumbersArr:
                            path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                it, repo_number_cate_id, "normal")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                            time.sleep( 1 )
                        for it2 in bccnumbersArr:
                            path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                it, repo_number_cate_id, "normal")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                            time.sleep( 1 )
                        if "我去~楼太高，这个页面被挡住了" in page_source:
                            print u"我去~楼太高，这个页面被挡住了"
                        elif "Connection timed out" in page_source:
                            print u"连接超时"
                        elif "Timed Out" in page_source:
                            print u"超时了"
                        elif "Connection unexpectedly closed" in page_source:
                            print u"连接意外关闭"
                        elif "The email message was detected as spam" in page_source:
                            print u"可能ip黑了"
                            # self.ipChange.ooo()
                            # self.ipChange.ooo()
                        elif "5.7.1 Too many spam messages sent" in page_source:
                            print u"可能ip黑了"
                            # self.ipChange.ooo()
                            # self.ipChange.ooo()
                        elif "5.7.1 Too many messages sent" in page_source:
                            print u"可能达到上限了"
                        elif "验证码" in page_source:
                            print u"需要验证码"
                            flag = False
                            flagFirst = True
                            sc = 0
                            count = count + 1
                            if count >= 2:
                                # self.ipChange.ooo()
                                # self.ipChange.ooo()
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
                            # self.ipChange.ooo()
                            # self.ipChange.ooo()
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
                                    repo_cate_id, "frozen", account, "", "")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                            time.sleep( 3 )
                    if flagFirst:
                        try:
                            # self.repo.AccountFrozenTimeDelay(account, repo_cate_id)
                            # driver.get(
                            #     "http://data.zunyun.net/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                            #         account, repo_cate_id,"PT_QQ"))
                            path = "/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                                    account, repo_cate_id,"PT_QQ")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                            time.sleep(1)
                        except:
                            pass
                    if flagFirst2:
                        try:
                            # driver.get("http://data.zunyun.net/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                            #         account, repo_cate_id, "PT_QQ") )
                            path = "/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                                account, repo_cate_id, "PT_QQ")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                        except:
                            pass
                    driver.get( startUrl )
                    time.sleep(3)
                    try:
                        driver.switch_to.default_content( )
                        # driver.switch_to_frame( 'actionFrame' )
                        driver.find_element_by_xpath( '//*[@id="writeMailBtn"]/span' ).click( )
                        time.sleep(2)
                    except:
                        pass
                # 删除邮件
                driver.switch_to_default_content()
                driver.get( startUrl )
                time.sleep(2)
                floders = ['//*[@id="draft"]','//*[@id="sent"]','//*[@id="trash"]','//*[@id="junkmail"]','//*[@id="li1"]/span[3]']
                for floder in floders:
                    driver.find_element_by_xpath( floder ).click( )
                    # driver.switch_to_frame( 'mainFrame' )  # 需先跳转到iframe框架
                    time.sleep( 1 )
                    while True:
                        try:
                            if "您没有邮件。" in driver.page_source.encode("utf-8"):
                                break
                            driver.find_element_by_xpath( '//*[@id="selectallrows"]' ).click()
                            time.sleep(2)
                            driver.find_element_by_xpath('//*[@id="mailWLDelBtn"]').click()
                            time.sleep(1)
                            driver.switch_to_alert( )
                            driver.find_element_by_xpath('//*[@id="popup_ok"]').click()
                            # driver.find_element_by_xpath( '//*[@id="selectallrows"]' ).send_keys(Keys.DELETE,Keys.ENTER)
                            # driver.find_element_by_xpath('// *[ @ id = "quick_completelydel"]').click()
                            # time.sleep(0.5)
                            # # driver.switch_to_frame( 'actionFrame' )  # 需先跳转到iframe框架
                            # driver.find_element_by_xpath( '//*[@id="QMconfirm_QMDialog_confirm"]' ).click()
                            time.sleep( 2 )
                            # driver.find_element_by_xpath(floder ).send_keys( Keys.CONTROL, 'a' )
                            # driver.find_element_by_xpath( floder).send_keys(Keys.DELETE)
                        except:
                            break
                    driver.get( startUrl )
                    time.sleep(1)
                    driver.switch_to.default_content( )

                # if not flag:
                #     try:
                #         driver.delete_all_cookies()
                #     except:
                #         pass
                #     if changeCount >= 5:
                #         # self.ipChange.ooo()
                #         # self.ipChange.ooo()
                #         time.sleep(3)
                #         changeCount = 0


                # 退出帐号重新登陆
                # try:
                #     obj = driver.find_elements_by_xpath( '//*[@id="SetInfo"]/div[1]/a[3]' )
                #     obj[0].click( )
                #     # for handle in driver.window_handles:  # 方法二，始终获得当前最后的窗口
                #     #     driver.switch_to_window( handle )
                #     #     driver.close()
                #     time.sleep( 2 )
                #     if changeCount >= 5:
                #         # self.ipChange.ooo()
                #         # self.ipChange.ooo()
                #         time.sleep(3)
                #         changeCount = 0
                # IPChange().ooo()
                # IPChange().ooo()
                # time.sleep(3)
                # driver.save_screenshot( "exit.png" )
                driver.delete_all_cookies()
                driver.close()
                driver.quit()
                # IPChange().ooo()
                # IPChange().ooo()
                # time.sleep(3)
                # except:
                #     if changeCount >= 5:
                #         # self.ipChange.ooo()
                #         # self.ipChange.ooo()
                #         time.sleep(3)
                #         changeCount = 0
                    # driver.save_screenshot("exceptionError.png")
                    # driver.save_screenshot("444.png")


        except:
            logging.exception( "Exception" )
            try:
                driver.close( )
                driver.quit( )
            except:
                pass

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
    return WOEmail_PC

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()
    # time.sleep(150)
    while True:
        try:
            o.action()
        except:
            logging.exception("Exception")
    # numbers = Repo().GetAccount("303", 5, 1)
    # if len(numbers) == 0:
    #     print u"%s号仓库没有数据,等待5分钟" % "303"
    #     time.sleep(300)
    #
    #
    # account = numbers[0]['number']  # 即将登陆的QQ号
    #
    # accountArr = account.split("@")
    # account = accountArr[0] + "%40" + accountArr[1]
    # cap = webdriver.DesiredCapabilities.PHANTOMJS
    # cap["phantomjs.page.settings.resourceTimeout"] = 1000
    # cap["phantomjs.page.settings.loadImages"] = True
    # cap["phantomjs.page.settings.disk-cache"] = True
    #
    # driver = webdriver.PhantomJS(desired_capabilities=cap, executable_path=r"C:\phantomjs\bin\phantomjs.exe")
    # driver.get(
    #     "http://data.zunyun.net/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
    #         account, "303", "PT_QQ"))