# coding:utf-8
from __future__ import division
import base64
import httplib
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
sys.path.append("/home/zunyun/workspace/TaskConsole")
# sys.path.append("C:\TaskConsole-master")
from IPChange import IPChange
from Repo import Repo
class Email_PC_Chrome:
    def __init__(self):
        self.repo = Repo()
        # self.ipChange = IPChange()

    def getTime(self, timeType):
        path = "/cgi-bin/cgi_svrtime"
        conn = httplib.HTTPConnection( "cgi.im.qq.com", None, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( ).replace("\n","")
        else:
            print u"http://cgi.im.qq.com/cgi-bin/cgi_svrtime 失效了"
            return ""
        timea = datetime.datetime.strptime(data,'%Y-%m-%d %H:%M:%S')
        if timeType == "EnTime":
            return timea.strftime( "%a, %b %d,  %Y %I:%M %p")
        elif timeType == "CnTime":
            nt = timea
            w = ""
            weekday = nt.weekday( )
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
            p = nt.strftime( "%p" )
            if p == "PM" or p == "pm":
                p = "下午"
            else:
                p = "上午"

            nowtime = nt.strftime( '%Y年%m月%d日%I:%M' )
            nowtime = nowtime.replace( "日", "日 (%s) %s" % (w, p) )
            return nowtime
        else:
            return timea.strftime( "%a, %b %d,  %Y %I:%M %p" )

    def getImg(self,driver):
        imgName = self.GetUnique()
        imgpath = r"/home/zunyun/text/images"
        if not os.path.exists(imgpath ):
            return
        g = os.listdir(imgpath)

        for i in g:
            name = i.split(".")
            os.rename(imgpath + "\%s" % i, imgpath + "\%s.%s" % (imgName, name[1]))
            imgpath = imgpath + "\%s.%s" % (imgName,name[1])
            try:
                driver.find_element_by_xpath('//*[@id="postform"]/div[2]/div/div[7]/input').send_keys(imgpath)
                time.sleep(2)
                return
            except:
                pass

        return imgpath

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

    def updateNumberStatus(self,emailnumber,repo_number_cate_id):
        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
            emailnumber, repo_number_cate_id, "normal")
        conn = httplib.HTTPConnection("data.zunyun.net", None, timeout=30)
        conn.request("GET", path)
        time.sleep(3)

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

    def getArgs(self):
        # asdlFile = open( r"/home/zunyun/text/asdl.txt", "r" )
        asdlFile = open( r"/home/zunyun/text/asdl.txt", "r" )
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
            sleepTime = param["x04"]
            if sleepTime is None or sleepTime == '':
                sleepTime = "10-15"

            args = {"time_delay": time_delay, "sendTime": sendTime, "repo_cate_id": repo_cate_id,
                    "repo_number_cate_id": repo_number_cate_id, "repo_material_cateId": repo_material_cateId,
                    "repo_material_cateId2": repo_material_cateId2, "emailType": emailType,
                    "user_agent_id": user_agent_id,"phonenumber":phonenumber,"cateId":cateId,"my_userCount":my_userCount,"bccCount":bccCount,"sleepTime":sleepTime}  # cate_id是仓库号，length是数量
            return args

    def sendProcess(self):
        try:
            sc = 0
            flagFirst = False
            flagFirst2 = False
            count = 0
            changeCount = 0
            while True:
                args = self.getArgs()
                user_agent_id = args["user_agent_id"]
                time_delay = args["time_delay"]
                time_delay = time_delay.split("-")
                try:
                    time_delayStart = int(time_delay[0])
                    time_delayEnd = int(time_delay[1])
                except:
                    print  u"参数格式有误"
                    time_delayStart = 3
                    time_delayEnd = 5
                user_agentid = args["user_agent_id"]
                repo_cate_id = args["repo_cate_id"]
                numbers = Repo( ).GetAccount( "normal",repo_cate_id, 90, 1 )
                if len( numbers ) == 0:
                    print u"%s号仓库没有数据,等待5分钟" % repo_cate_id
                    time.sleep(300)
                    return

                account = numbers[0]['number']  # 即将登陆的QQ号
                time.sleep(1)
                password = numbers[0]['password']
                accountArr = account.split("@")
                account2 = accountArr[0] + "%40" + accountArr[1]
                # user_agent = numbers[0]['imei']
                changeCount = changeCount + 1
                # if user_agent is None or user_agent == '':
                user_agentList = self.repo.GetMaterial( user_agent_id, 0, 1 )
                if len( user_agentList ) == 0:
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
                    command = 'taskkill /F /IM chrome.exe'
                    os.system(command)
                    # print u'close02'
                except:
                    pass
                options = webdriver.ChromeOptions()
                options.add_argument('disable-infobars')
                options.add_argument('lang=zh_CN.UTF-8')
                # options.add_argument( 'headless' )
                # 更换头部
                # options.add_argument(user_agent)
                options.add_argument('user-agent="%s' % user_agent)
                try:
                    driver = webdriver.Chrome(chrome_options=options,
                                              executable_path="/opt/google/chrome/chromedriver")
                except:
                    if not os.path.exists("C:\Users\Administrator\AppData\Local\Temp"):
                        os.mkdir("C:\Users\Administrator\AppData\Local\Temp")

                driver.get( "https://exmail.qq.com/cgi-bin/loginpage" )
                # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled')
                time.sleep( 3 )
                if changeCount >= 5:
                    # self.ipChange.ooo()
                    # self.ipChange.ooo()
                    time.sleep(5)
                    changeCount = 0
                    continue

                # driver.save_screenshot( "111.png" )
                # account = 'jd29@skjiu.com'
                # password = 'Abcd0029'

                try:
                    driver.find_element_by_id( "inputuin" ).clear( )
                    driver.find_element_by_id( "pp" ).clear()
                except:
                    pass
                try:
                    driver.find_element_by_id( "inputuin" ).send_keys( account )
                    time.sleep( 0.5 )
                    driver.find_element_by_id( "pp" ).send_keys(password)
                    #driver.save_screenshot( "222.png" )
                    time.sleep( 1 )
                    driver.find_element_by_id( "pp" ).send_keys( Keys.ENTER )
                    time.sleep( random.randint( time_delayStart, time_delayEnd ) )
                    #driver.save_screenshot( "333.png" )
                except:
                    pass

                try:
                    # obj = driver.find_element_by_class_name( "qm_icon_Compose" )
                    obj = driver.find_element_by_xpath('//*[@id="composebtn"]')
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
                    elif "帐号或密码不正确" in errorPage and "验证码" not in errorPage:
                        print u"帐号或密码不正确"
                        self.updateAccountStatus(repo_cate_id, account, "frozen")
                    elif "看不清" in errorPage:
                        print u"需要验证码"
                    elif "验证码" in errorPage:
                        print u"验证码"

                    elif "冻结" in errorPage:
                        print u"冻结"
                        # self.repo.BackupInfo( repo_cate_id, 'frozen', account, '', '' )
                        self.updateAccountStatus(repo_cate_id,account,"frozen")
                    elif "请输入完整的成员帐号，包括域名。" in errorPage:
                        print  u"%s 冻结" % account
                        self.updateAccountStatus(repo_cate_id, account, "frozen")
                    else:
                        driver.save_screenshot("%s-%s.png"%(account,self.GetUnique()))
                    try:
                        obj = driver.find_element_by_class_name( "content" )
                    except:
                        time.sleep( 2 )
                    continue

                url = driver.current_url.encode( "utf-8" )
                obj.click( )
                time.sleep(2)
                flag = True
                # while flag:
                args = self.getArgs()
                emailType = args["emailType"]
                sendTime = args["sendTime"]
                my_userCount = args["my_userCount"]
                bccCount = args["bccCount"]
                sleepTime = args["sleepTime"]
                sleepTime = sleepTime.split("-")
                try:
                    sleepTime_Start = int(sleepTime[0])
                    sleepTime_delayEnd = int(sleepTime[1])
                except:
                    print  u"参数格式有误"
                    sleepTime_Start = 10
                    sleepTime_delayEnd = 15
                sendTime = sendTime.split("-")
                try:
                    sendTimeStart = int(sendTime[0])
                    sendTimeEnd = int(sendTime[1])
                except:
                    print  u"发送时间间隔的参数格式有误"
                    sendTimeStart = 3
                    sendTimeEnd = 5
                repo_material_cateId2 = args["repo_material_cateId2"]
                repo_material_cateId = args["repo_material_cateId"]
                repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
                emailnumbers = Repo().GetNumber(repo_number_cate_id, 0, my_userCount)  # 取出add_count条两小时内没有用过的号码
                emailnumberArr = []
                if len(emailnumbers) == 0 and my_userCount!=0:
                    print u"QQ号码库%s号仓库为空" % repo_number_cate_id
                    time.sleep(100)
                    try:
                        driver.close()
                        driver.quit()
                    except:
                        pass
                    return
                else:
                    for item in emailnumbers:
                        emailnumberArr.append(item['number'])

                # emailnumber = emailnumbers[0]['number']

                bccnumbers = self.repo.GetNumber(repo_number_cate_id, 0, bccCount)  # 取出add_count条两小时内没有用过的号码
                bccnumberArr = []
                if len(bccnumbers) == 0 and bccCount!=0:
                    print u"QQ号码库%s号仓库为空" % repo_number_cate_id
                else:
                    for item in bccnumbers:
                        bccnumberArr.append(item['number'])

                if repo_material_cateId == "" or repo_material_cateId is None:
                    selectContent1 = ""
                else:
                    selectContent1 = "只发主题"
                    Material = self.repo.GetMaterial(repo_material_cateId, 0, 1)
                    if len(Material) == 0:
                        Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                        if len( Material ) == 0:
                            print u"%s  号仓库为空，没有取到消息" % repo_material_cateId
                            try:
                                driver.close()
                                driver.quit()
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
                        Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                        if len( Material2 ) == 0:
                            # print "%s号仓库为空，没有取到消息" % repo_material_cateId
                            try:
                                driver.close()
                                driver.quit()
                            except:
                                pass
                            return
                    message2 = Material2[0]['content']
                # emailnumber = emailnumbers[0]['number']
                # driver.save_screenshot("test01.png")
                # try:
                #     emailnumberObj = driver.find_element_by_id( "to" )
                #     emailnumberObj.click()
                # except:
                #     emailnumberObj = driver.find_element_by_id( "showto" )
                # message = "hello"
                # message2 = u"老同学"

                try:
                    driver.switch_to_frame('mainFrame')  # 需先跳转到iframe框架
                    time.sleep(1)
                    emailnumberObj = driver.find_element_by_xpath('//*[@id="subject"]')  # 定位到主题
                    # emailnumberObj = driver.find_element_by_xpath( '//*[@id="toAreaCtrl"]' )
                except:
                    pass

                if selectContent1 == "只发主题":
                    try:
                        emailnumberObj.send_keys(message)
                        time.sleep(0.5)
                    except:
                        pass

                bccObj = driver.find_element_by_xpath('//*[@id="aBCC"]')
                text = bccObj.get_attribute("text").encode("utf-8")
                if text == "删除密送":
                    bccObj.click()

                j = 2
                # emailnumberArr = ["455854284@qq.com"]
                for emailnumber in emailnumberArr:
                    if "@" not in emailnumber:
                        # emailnumber = "455854284"
                        if emailType == "QQ邮箱":
                            driver.find_element_by_xpath('//*[@id="toAreaCtrl"]/div[%s]/input' % j).send_keys(
                                emailnumber + "@qq.com ")
                        elif emailType == "189邮箱":
                            driver.find_element_by_xpath('//*[@id="toAreaCtrl"]/div[%s]/input' % j).send_keys(
                                emailnumber + "@189.cn ")
                        elif emailType == "139邮箱":
                            driver.find_element_by_xpath('//*[@id="toAreaCtrl"]/div[%s]/input' % j).send_keys(
                                emailnumber + "@139.com ")
                        elif emailType == "163邮箱":
                            driver.find_element_by_xpath('//*[@id="toAreaCtrl"]/div[%s]/input' % j).send_keys(
                                emailnumber + "@163.com ")
                        elif emailType == "wo邮箱":
                            driver.find_element_by_xpath('//*[@id="toAreaCtrl"]/div[%s]/input' % j).send_keys(
                                emailnumber + "@wo.cn ")
                        else:
                            driver.find_element_by_xpath('//*[@id="toAreaCtrl"]/div[%s]/input' % j).send_keys(
                                emailnumber + "@qq.com ")
                    else:
                        driver.find_element_by_xpath('//*[@id="toAreaCtrl"]/div[%s]/input' % j).send_keys(
                            emailnumber + " ")
                    j = j + 1
                # driver.save_screenshot( "mmm.png" )
                time.sleep(2)
                emailnumberObj.click()
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="aBCC"]').click()
                time.sleep(2.5)
                if bccnumberArr != []:
                    pass
                    j = 2
                    for bcc in bccnumberArr:
                        if "@" not in bcc:
                            # emailnumber = "455854284"
                            if emailType == "QQ邮箱":
                                driver.find_element_by_xpath(
                                    '//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                    bcc + "@qq.com ")
                            elif emailType == "189邮箱":
                                driver.find_element_by_xpath(
                                    '//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                    bcc + "@189.cn ")
                            elif emailType == "139邮箱":
                                driver.find_element_by_xpath(
                                    '//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                    bcc + "@139.com ")
                            elif emailType == "163邮箱":
                                driver.find_element_by_xpath(
                                    '//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                    bcc + "@163.com ")
                            elif emailType == "wo邮箱":
                                driver.find_element_by_xpath(
                                    '//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                    bcc + "@wo.cn ")
                            else:
                                driver.find_element_by_xpath(
                                    '//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                    bcc + "@qq.com ")
                        else:
                            driver.find_element_by_xpath('//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                bcc + " ")
                        j = j + 1
                time.sleep(2)
                # driver.find_element_by_xpath('//*[@id="editor_toolbar_btn_container"]/a').click()
                # driver.find_element_by_xpath('//*[@id="QMEditorArea"]/table/tbody/tr[1]/td/div/div[1]/div[17]/div').click()
                # emailnumberObj.send_keys(message2)
                # time.sleep(1)
                # emailnumberObj.send_keys(Keys.CONTROL,'a')
                # emailnumberObj.send_keys( Keys.CONTROL, 'x' )
                # try:
                #     driver.find_element_by_xpath('//*[@id="editor_toolbar_btn_container"]/a').click()
                #     driver.find_element_by_xpath('//*[@id="QMEditorArea"]/table/tbody/tr[1]/td/div/div[1]/div[17]/div').click()
                # except:
                #     pass
                time.sleep(1)
                # msg = u'简单邮，邮件推送专家。WWW.JDEDM.COM QQ：52388580，微信同号 地域性精准邮件投放，客户自己提供收件人邮箱，也可以由我们精准采集； 主题和内容由客户提供，可带附件，我们负责审查整理，违法行业请绕道； 发件人的邮箱种类，有QQ邮箱，163邮箱，189邮箱，WO邮箱，新浪邮箱等； 发送时间或发送日期可根据客户的要求投放，没有具体的要求24小时投放。'
                if selectContent2 == "只发内容":
                    emailnumberObj.send_keys(Keys.TAB,message2)
                    # driver.find_element_by_xpath('//*[@id="QMEditorArea"]/table/tbody/tr[2]/td/textarea[1]').clear()

                # driver.switch_to_default_content()

                # driver.find_element_by_xpath(
                #     '//*[@id="QMEditorArea"]/table/tbody/tr[1]/td/div/div[2]/div[2]').click()
                # time.sleep(0.5)

                time.sleep( 1 )
                try:
                    driver.find_element_by_xpath('//*[@id="toolbar"]/div/input[1]').click()
                except:
                    emailnumberObj.send_keys(Keys.TAB)
                    emailnumberObj.send_keys(Keys.ENTER)
                time.sleep(random.randint(sendTimeStart, sendTimeEnd))

                try:
                    driver.implicitly_wait(30)
                except:
                    pass
                page_source = driver.page_source.encode("utf-8")
                if "发送成功" in page_source and "验证码" not in page_source and "，并已保存到“已发送”文件夹" in page_source:
                    # nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    # driver.save_screenshot("%s.png" % nowTime)
                    driver.switch_to_default_content( )
                    if '为了保障你的邮箱安全，请输入验证码以完成本次发送。' in driver.page_source.encode( "utf-8" ):
                        print u'为了保障你的邮箱安全，请输入验证码以完成本次发送。'
                    elif "邮件中可能包含不合适的用语或内容" in driver.page_source.encode( "utf-8" ):
                        print u'邮件中可能包含不合适的用语或内容'
                    elif "您的帐号因频繁发送广告或垃圾邮件，已被禁止发信。" in driver.page_source.encode( "utf-8" ):
                        self.updateAccountStatus(repo_cate_id,account,"frozen")
                        time.sleep( 3 )
                        flag = False
                    else:
                        print u"%s 发送成功 给 %s ,密送号码为%s" % (account, emailnumberArr, bccnumberArr)  # 发送成功
                    driver.switch_to_frame( 'mainFrame' )
                else:
                    flag = False
                    for it in emailnumberArr:
                        self.updateNumberStatus( it, repo_number_cate_id )
                    for it2 in bccnumberArr:
                        self.updateNumberStatus( it2, repo_number_cate_id )
                    enclosure = False
                    driver.switch_to_default_content( )
                    page_source = driver.page_source.encode( "utf-8" )
                    if '但您可能忘记了添加附件' in page_source:
                        driver.find_element_by_xpath( '//*[@id="QMconfirm_g_confirm"]' ).click( )
                        time.sleep( 1 )
                        enclosure = True
                    page_source = driver.page_source.encode( "utf-8" )
                    if '为了保障你的邮箱安全，请输入验证码以完成本次发送。' in page_source:
                        print u'为了保障你的邮箱安全，请输入验证码以完成本次发送。'
                        driver.find_element_by_xpath('//*[@id="QMVerify_g_btnCancel"]').click()
                        time.sleep(1)
                        flag = False
                    elif "邮件中可能包含不合适的用语或内容" in page_source:
                        print u'邮件中可能包含不合适的用语或内容'
                        flag = False
                    elif "您的帐号因频繁发送广告或垃圾邮件，已被禁止发信。" in driver.page_source.encode( "utf-8" ):
                        print u'您的帐号因频繁发送广告或垃圾邮件，已被禁止发信'
                        self.updateAccountStatus( repo_cate_id, account, "frozen" )
                        time.sleep( 3 )
                        flag = False
                    elif "邮件中可能包含不合适的用语或内容" in page_source:
                        sc = 0
                        print u"%s  邮件中可能包含不合适的用语或内容"%account
                    elif "<html><head></head><body></body></html>" in page_source:
                        sc = 0
                        flag = False
                        print "空"
                        self.lockAccount(account2, repo_cate_id, "PT_QQ")
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
                        self.updateAccountStatus(repo_cate_id, account, "exception")
                    elif "您的帐号存在安全隐患" in page_source:
                        sc = 0
                        flag = False
                        print u"您的帐号存在安全隐患"
                        self.updateAccountStatus(repo_cate_id, account, "frozen")
                    elif "主题：" in page_source and "收件人：" in page_source:
                        print u"还在当前页面"
                    else:
                        if enclosure:
                            if "发送成功" in page_source and "验证码" not in page_source and "，并已保存到“已发送”文件夹" in page_source:
                                print u"%s 发送成功 给 %s ,密送号码为%s" % (account, emailnumberArr, bccnumberArr)  # 发送成功
                                flag = True
                            else:
                                print u"暂时没遇到"
                        else:
                            driver.switch_to_frame( 'mainFrame' )
                            if "主题：" in page_source and "收件人：" in driver.page_source.encode("utf-8"):
                                print u"还在当前页面"
                            else:
                                print u"暂时没遇到"
                try:
                    driver.switch_to_frame( 'mainFrame' )
                except:
                    pass
                if flagFirst:
                    self.lockAccount(account, repo_cate_id, "QY_QQ")
                if flagFirst2:
                    self.lockAccount(account2, repo_cate_id, "PT_QQ")
                driver.get( url )
                time.sleep(2)
                try:
                    driver.find_element_by_xpath('//*[@id="composebtn"]').click()
                except:
                    pass

                # 删除邮件
                driver.get(startUrl)
                floders = ['//*[@id="folder_1"]', '//*[@id="folder_3"]', '//*[@id="folder_4"]',
                           '//*[@id="folder_5"]', '//*[@id="folder_6"]']
                try:
                    for floder in floders:
                        driver.find_element_by_xpath(floder).click()
                        driver.switch_to_frame('mainFrame')  # 需先跳转到iframe框架
                        time.sleep(1)
                        while True:
                            try:
                                if "没有邮件" in driver.page_source.encode("utf-8"):
                                    break
                                driver.find_element_by_xpath('//*[@id="frm"]/table/tbody/tr/td[1]/input').click()
                                time.sleep(2)
                                driver.find_element_by_xpath('//*[@id="frm"]/table/tbody/tr/td[1]/input').send_keys(Keys.DELETE)
                                try:
                                    driver.switch_to_default_content()
                                    driver.find_element_by_xpath('//*[@id="QMconfirm_g_confirm"]').click()
                                except:
                                    pass
                                # driver.find_element_by_xpath('// *[ @ id = "quick_completelydel"]').click()
                                # time.sleep(0.5)
                                # # driver.switch_to_frame( 'actionFrame' )  # 需先跳转到iframe框架
                                # driver.find_element_by_xpath( '//*[@id="QMconfirm_QMDialog_confirm"]' ).click()
                                time.sleep(2)
                                # driver.find_element_by_xpath(floder ).send_keys( Keys.CONTROL, 'a' )
                                # driver.find_element_by_xpath( floder).send_keys(Keys.DELETE)
                            except:
                                driver.find_element_by_xpath(floder).click()
                                time.sleep(2)
                        driver.get(startUrl)
                        time.sleep(1)
                        driver.switch_to.default_content()
                except:
                    pass



                if not flag:
                    try:
                        driver.delete_all_cookies()
                    except:
                        pass
                    if changeCount >= 5:
                        # self.ipChange.ooo()
                        # self.ipChange.ooo()
                        time.sleep(3)
                        changeCount = 0
                    continue


                # 退出帐号重新登陆
                try:
                    obj = driver.find_element_by_xpath( '//*[@id="SetInfo"]/div[1]/a[4]' ).click()
                    time.sleep( 2 )
                    # self.ipChange.ooo()
                    # self.ipChange.ooo()
                    time.sleep(3)
                    changeCount = 0
                    # IPChange().ooo()
                    # IPChange().ooo()
                    # time.sleep(3)
                    # driver.save_screenshot( "exit.png" )
                    driver.delete_all_cookies()
                except:
                    # self.ipChange.ooo()
                    # self.ipChange.ooo()
                    time.sleep(3)
                    changeCount = 0
                    # driver.save_screenshot("exceptionError.png")
                    # driver.save_screenshot("444.png")
                    print "error"
                self.delete()


        except Exception,e:
            logging.exception("d")
                # result = [driver]
            self.delete()
            return []

    def action(self):
        # data = self.ipChange.Check_for_Broadband()
        # if data != None:
        #     print u"宽带确认已连接,模块继续运行"
        # else:
        #     print u"宽带未连接,连接宽带"
        #     time.sleep(150)
        #     self.ipChange.ooo()
        #     time.sleep(5)

        x = self.sendProcess()
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
        self.delete()
        args = self.getArgs()
        phonenumber = args["phonenumber"]
        cateId = args["cateId"]
        para = {"phoneNumber": phonenumber, "x_04": sta}
        self.repo.PostInformation(cateId, para)

def getPluginClass():
    return Email_PC_Chrome

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()
    # y  = Repo().GetMaterial( "358", 0, 1 )


    while True:
        try:
            o.action()
        except Exception,e:
            print e

    # print o.getTime("CnTime")
    # print o.getTime( "EnTime" )