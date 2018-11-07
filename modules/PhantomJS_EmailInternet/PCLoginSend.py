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

import win32api

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs


import os, time, datetime, random
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


sys.path.append("C:\TaskConsole-master")
from IPChange import IPChange
from WaterMark import WaterMark
from Repo import Repo
import win32clipboard as w
import win32con
from PIL import Image, ImageDraw, ImageFont


class PCLoginSend:
    def __init__(self):

        self.repo = Repo()
        self.ipChange = IPChange()
        self.wateMark = WaterMark()
        self.domain = self.repo.domain
        self.port = self.repo.port

        # 写入剪切板内容
    def settext(self, aString):
        w.OpenClipboard( )
        w.EmptyClipboard( )
        w.SetClipboardData( win32con.CF_TEXT, aString )
        w.CloseClipboard( )

    def deleteImg(self):
        imgpath = r"C:\water"
        g = os.walk(imgpath)
        for path, d, filelist in g:
            for filename in filelist:
                # print os.path.join(path, filename)
                os.remove(os.path.join(path, filename))

    def getImgCode(self,driver):
        img = driver.find_element_by_xpath('//*[@id="QMVerify_QMDialog_verify_img_code"]')
        # 取验证码的x,y
        captchaX = int( img.location['x'] )
        captchaY = int( img.location['y'] )
        # 取验证码的宽度和高度
        captchaWidth = img.size['width']
        captchaHeight = img.size['height']
        captchaRight = captchaX + captchaWidth
        captchaBottom = captchaY + captchaHeight
        # # 通过Image处理图像，第一种方法：在frame区域截取
        path1 = r"C:\YZM\z.png"  # 截屏图片
        path2 = r"C:\YZM\captcha.png"  # 验证码图片
        driver.save_screenshot(path1)
        imgObject = Image.open(path1)
        imgCaptcha = imgObject.crop((captchaX, captchaY, captchaRight, captchaBottom))  # 裁剪
        imgCaptcha.save(path2)
        # icode = imageCode()
        # im = open(path2, 'rb')
        # codeResult = icode.getCode(im, icode.CODE_TYPE_8_NUMBER_CHAR)
        #
        # imgcode = codeResult["Result"]
        # im_id = codeResult["Id"]

        # time.sleep(3)
        # with open(path2, 'rb') as f:
        #     data = f.read()
        # dll = windll.LoadLibrary('OCR163.dll')
        # time.sleep(3)
        # ret = dll.OCR(data, len(data))
        # time.sleep(3)
        # ocrVal = c_char_p(ret)
        # time.sleep(2)
        # ocrCode = str(ocrVal.value)
        # print(ocrCode)
        # if ocrCode == "-10" or len(ocrCode)<4:
        #     print "验证码没识别出来"
        #     return
        # else:
        #     return ocrCode

        with open(path2, 'rb') as f:
            # file = f.read()
            file = "data:image/jpeg;base64," + base64.b64encode(f.read())
            da = {"IMAGES": file}

            path = "/ocr.index"
            headers = {"Content-Type": "application/x-www-form-urlencoded",
                       "Connection": "Keep-Alive"};
            conn = httplib.HTTPConnection("162626i1w0.51mypc.cn", 10082, timeout=30)
            params = urllib.urlencode(da)
            conn.request(method="POST", url=path, body=params, headers=headers)
            response = conn.getresponse()
            if response.status == 200:
                imgcode = response.read()
            else:
                imgcode = "-1"
                # numbers = json.loads(data)
            # print r.status_code
            print imgcode
        os.remove(path1)

        # captchaX = 556
        # captchaY = 445
        # captchaRight = 726
        # captchaBottom = 505

        # os.remove(path2 )
        return imgcode

    def sendImg(self,driver):
        imgpath = self.getImg(driver,"pc")
        if imgpath != None and imgpath != r"C:\water":
            #video = driver.find_element_by_xpath('//*[@id="AttachFrame"]/span')
            #video.send_keys(imgpath)
            self.settext(imgpath)
            #video.send_keys(Keys.CONTROL, 'a')  # selenium的send_keys（ctrl+a）
            #video.send_keys(Keys.CONTROL, 'x')  # (ctrl+x)
            try:
                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="AttachFrame"]/span').click()  # 点击上传按钮，打开上传框
                time.sleep(5)
            except:
                pass

            # 粘贴（ctrl + v）
            try:
                win32api.keybd_event(17, 0, 0, 0)  # 按下按键 ctrl
                # time.sleep(3)
                win32api.keybd_event(86, 0, 0, 0)  # 按下按键 v
                # time.sleep(3)
                win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 升起按键 v
                # time.sleep(3)
                win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 升起按键 ctrl
                time.sleep(1)

                # 回车（enter）
                win32api.keybd_event(13, 0, 0, 0)  # 按下按键 enter
                win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)  # 升起按键 enter
            except:
                pass

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
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
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
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        time.sleep(3)

    def lockAccount(self,account,repo_cate_id,QQType):
        path = "/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
            account, repo_cate_id,QQType)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
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

    def getImg(self,driver,img = "phone"):
        imgName = self.GetUnique()
        imgpath = r"C:\water"
        #imgpath = "/home/zunyun/text/img"
        if not os.path.exists(imgpath ):
            return
        g = os.listdir(imgpath)

        for i in g:
            name = i.split(".")
            #os.rename( imgpath + "/%s" % i, imgpath + "/%s.%s" % (imgName, name[1]) )
            #imgpath = imgpath + "/%s.%s" % (imgName, name[1])
            os.rename(imgpath + "\%s" % i, imgpath + "\%s.%s" % (imgName, name[1]))
            imgpath = imgpath + "\%s.%s" % (imgName,name[1])
            if img == "phone":
                try:
                    driver.find_element_by_xpath('// *[ @ id = "attachUpload"] / form / a / input[1]').send_keys(imgpath)
                    time.sleep(1)
                    return
                except:
                    driver.find_element_by_xpath('//*[@id="attachUpload"]/a/input').send_keys(imgpath)
                    time.sleep(1)
                    pass
            break

        return imgpath

    def getArgs(self):
        #asdlFile = open( r"/home/zunyun/text/asdl.txt", "r" )
        asdlFile = open( r"c:\asdl.txt", "r" )
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
            sendCount = task["x11"]
            loopFalg = task["x12"]
            name_cate_id = ""
            nameswitch = True
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

            sendSwitch = True

            if sendCount is None or sendCount == "" or sendCount == "0":
                sendCount = 0
                print u"发信个数为0，默认为10"
            else:
                try:
                    sendCount = int(sendCount)
                except:
                    sendCountArr =  sendCount.split("-")
                    if len(sendCountArr)>=4:
                        sendCount = sendCountArr[0]
                        name_cate_id = sendCountArr[1]
                        if sendCountArr[2]:
                            if sendCountArr[2].upper()=="Y":
                                nameswitch = True
                            else:
                                nameswitch = False
                        else:
                            popFlag = True

                        if sendCountArr[3]:
                            if sendCountArr[3].upper()=="Y":
                                sendSwitch = True
                            else:
                                sendSwitch = False
                        else:
                            popFlag = True
                        try:
                            fjSwitch = sendCountArr[4]
                            if sendCountArr[4].upper() == "Y":
                                fjSwitch = True
                            else:
                                fjSwitch = False
                        except:
                            fjSwitch = True
                    else:
                        print u"参数错误"
                        time.sleep(60)
                        return
                sendCount = int(sendCount)


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
                    "user_agent_id": user_agent_id,"phonenumber":phonenumber,"cateId":cateId,"my_userCount":my_userCount,'fjSwitch':fjSwitch,"bccCount":bccCount,"loopFalg":loopFalg,"sendCount":sendCount,"name_cate_id":name_cate_id,"sendSwitch":sendSwitch,"nameswitch":nameswitch}  # cate_id是仓库号，length是数量
            return args

    def login(self, mailType):
        args = self.getArgs()
        user_agent_id = args["user_agent_id"]
        repo_cate_id = args["repo_cate_id"]
        repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        time_delay = args["time_delay"].split("-")
        try:
            time_delayStart = int(time_delay[0])
            time_delayEnd = int(time_delay[1])
        except:
            print  u"参数格式有误"
            time_delayStart = 3
            time_delayEnd = 5
        numbers = self.repo.GetAccount("normal", repo_cate_id, 0, 1)
        if len(numbers) == 0:
            numbers = self.repo.GetAccount("normal", repo_cate_id, 0, 1)
            if len(numbers) == 0:
                print u"%s号仓库没有数据" % repo_cate_id
                time.sleep(300)
                return
        QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        QQPassword = numbers[0]['password']
        # user_agent = numbers[0]['imei']
        user_agent = ""
        if user_agent is None or user_agent == '':
            user_agentList = self.repo.GetMaterial(user_agent_id, 0, 1)
            if len(user_agentList) == 0:
                user_agentList = self.repo.GetMaterial(user_agent_id, 0, 1)
                if len(user_agentList) == 0:
                    print u"%s号仓库为空，没有取到消息" % user_agent_id
                    return
            user_agent = user_agentList[0]['content']
        print user_agent
        try:
            command = 'taskkill /F /IM chromedriver.exe'
            os.system(command)
            # print u'close02'
        except:
            pass
        try:
            command = 'taskkill /F /IM chrome.exe'
            os.system(command)
            # print u'close02'
        except:
            pass
        time.sleep(2)
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        options.add_argument('lang=zh_CN.UTF-8')
        fl = False
        # options.add_argument( 'headless' )
        # 更换头部
        # options.add_argument(user_agent)
        # user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
        if mailType == "phone":
            user_agentid = self.getArgs()["user_agent_id"]
            user_agentList = self.repo.GetMaterial(user_agent_id, 0, 1)
            if len(user_agentList) == 0:
                user_agentList = self.repo.GetMaterial(user_agentid, 0, 1)
                if len(user_agentList) == 0:
                    print u"%s号仓库为空，没有取到消息" % user_agentid
                    return
            user_agent = user_agentList[0]['content']
        options.add_argument('user-agent="%s' % user_agent)
        try:
            driver = webdriver.Chrome(chrome_options=options,
                                      executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")
        except:
            if not os.path.exists("C:\Users\Administrator\AppData\Local\Temp"):
                os.mkdir("C:\Users\Administrator\AppData\Local\Temp")

        emailnumbers = self.repo.GetNumber(repo_number_cate_id, 0, 1)  # 取出add_count条两小时内没有用过的号码
        if len(emailnumbers) == 0:
            print u"%s号仓库没有数据" % repo_number_cate_id
            time.sleep(300)
            try:
                driver.close()
                driver.quit()
            except:
                pass
            return
        emailnumber = emailnumbers[0]['number']
        # driver.get(
        #     "http://data.161998.com/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
        #         emailnumber, repo_number_cate_id, "normal"))
        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
            emailnumber, repo_number_cate_id, "normal")
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET", path)
        time.sleep(3)

        # QQNumber = "1006329641"
        # QQPassword = "tqly7732"
        registerFlag = True
        if mailType == "phone":
            print u"手机版登陆"
            # 打开QQ邮箱登陆界面
            driver.get("https://w.mail.qq.com/")
            # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled')
            time.sleep(3)
            # driver.save_screenshot("01.png")
            # driver.save_screenshot("0.png")
            # 点 进入网页版QQ邮箱 (模拟手机版会有这个)
            try:
                obj = driver.find_element_by_xpath("//td[@class='enter_mail_button_td']/a")
                obj.click()

            except:
                print u"使用的是电脑版头信息"

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
                time.sleep(1)
                if "请使用邮箱的“独立密码”登录" in driver.page_source:
                    driver.find_element_by_xpath('//*[@id="pwd"]').send_keys("Abc" + QQNumber)
                    driver.find_element_by_xpath('//*[@id="submitBtn"]').click()
                time.sleep(random.randint(time_delayStart, time_delayEnd))
            except:
                pass
        else:
            print u"PC登陆"
            driver.get(r'https://mail.qq.com/')
            try:
                driver.switch_to_frame('login_frame')  # 需先跳转到iframe框架
            except:
                # print u"https://mail.qq.com/ 不支持手机版头信息,仓库号为--->%s,素材为----->%s" % (user_agent_id, user_agent)
                return "s"
            time.sleep(1)

            try:
                # 若帐号输入框有内容先清空
                driver.find_element_by_id("u").clear()
                driver.find_element_by_id("p").clear()
            except:
                pass
            try:
                driver.find_element_by_id("u").send_keys(QQNumber)
                driver.find_element_by_id("p").send_keys(QQPassword)
                # driver.save_screenshot( "222.png" )
                time.sleep(0.5)
                driver.find_element_by_id("p").send_keys(Keys.ENTER)

                time.sleep(1)
                if "验证独立密码" in driver.page_source:
                    try:
                        driver.find_element_by_xpath('//*[@id="pp"]').send_keys("Abc" + QQNumber)
                        driver.find_element_by_xpath('//*[@id="btlogin"]').click()
                        registerFlag = False
                    except:
                        pass

                time.sleep(random.randint(time_delayStart, time_delayEnd))
            except:
                pass

        try:
            if mailType == "phone":
                obj = driver.find_element_by_class_name("qm_btnIcon")
            else:
                driver.find_element_by_xpath('//*[@id="composebtn"]')
            print u"%s  登陆成功" % QQNumber

            cookies = driver.get_cookies()
            # for cookie in cookies:
            #     print cookie
            #     try:
            #         command = 'taskkill /F /IM chromedriver.exe'
            #         os.system(command)
            #         # print u'close02'
            #     except:
            #         pass
            #     try:
            #         command = 'taskkill /F /IM chrome.exe'
            #         os.system(command)
            #         # print u'close02'
            #     except:
            #         pass
            #     time.sleep(2)
            #     options = webdriver.ChromeOptions()
            #     options.add_argument('disable-infobars')
            #     options.add_argument('lang=zh_CN.UTF-8')
            #     fl = False
            #     # options.add_argument( 'headless' )
            #     # 更换头部
            #     # options.add_argument(user_agent)
            #     # user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
            #     if mailType == "phone":
            #         user_agentid = self.getArgs()["user_agent_id"]
            #         user_agentList = self.repo.GetMaterial(user_agent_id, 0, 1)
            #         if len(user_agentList) == 0:
            #             user_agentList = self.repo.GetMaterial(user_agentid, 0, 1)
            #             if len(user_agentList) == 0:
            #                 print u"%s号仓库为空，没有取到消息" % user_agentid
            #                 return
            #         user_agent = user_agentList[0]['content']
            #     options.add_argument('user-agent="%s' % user_agent)
            #     try:
            #         driver = webdriver.Chrome(chrome_options=options,
            #                                   executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")
            #     except:
            #         if not os.path.exists("C:\Users\Administrator\AppData\Local\Temp"):
            #             os.mkdir("C:\Users\Administrator\AppData\Local\Temp")
            #
            #     driver.get(r'https://mail.qq.com/')
            #     driver.add_cookie(cookie)
            #     driver.get(r'https://mail.qq.com/')

            startUrl = driver.current_url

        except:
            print u"%s  登陆失败" % QQNumber
            time.sleep(2)
            # 登陆出现异常状况
            errorPage = driver.page_source.encode("utf-8")

            if "拖动下方滑块完成拼图" in errorPage:
                print u"%s  拖动下方滑块完成拼图" % QQNumber
            elif "安全验证" in errorPage:
                print u"安全验证"
                # self.updateAccountStatus(repo_cate_id, QQNumber, "question")
            elif "帐号或密码不正确" in errorPage:
                print u"%s  帐号或密码不正确" % QQNumber
            elif "您输入的独立密码有误，请重新输入" in errorPage:
                print u"您输入的独立密码有误，请重新输入"
            elif "修改密码" in errorPage:
                print u"修改密码"
                self.updateAccountStatus(repo_cate_id, QQNumber, "exception")
            elif "你的帐号存在安全隐患" in errorPage:
                print u"你的帐号存在安全隐患"
                self.updateAccountStatus(repo_cate_id, QQNumber, "exception")
            elif "您的域名邮箱账号存在异常行为" in errorPage:
                print u"您的域名邮箱账号存在异常行为"
                self.updateAccountStatus(repo_cate_id, QQNumber, "exception")
            elif "冻结" in errorPage:
                print u"%s  冻结" % QQNumber
                #         repo_cate_id, "frozen", QQNumber, "", ""))
                self.updateAccountStatus(repo_cate_id, QQNumber, "frozen")
            try:
                obj = driver.find_element_by_class_name("content")
            except:
                time.sleep(2)
            try:
                driver.close()
                driver.quit()
            except:
                pass
            # self.ipChange.ooo()
            # self.ipChange.ooo()
            self.changeIp()
            return
        argsL = {"driver": driver, "QQNumber": QQNumber, "repo_cate_id": repo_cate_id, "registerFlag": registerFlag}
        return argsL

    def changeIp(self):
        data = self.ipChange.Check_for_Broadband()
        if data != None:
            self.ipChange.ooo("10000", "AB")
            time.sleep(5)
            data = self.ipChange.Check_for_Broadband()
            if data != None:
                pass
            else:
                self.ipChange.ooo("10000", "AB")
                time.sleep(10)
                data = self.ipChange.Check_for_Broadband()
                if data != None:
                    print u"宽带确认已连接"
        else:
            self.ipChange.ooo("10000", "AB")
            time.sleep(10)
            data = self.ipChange.Check_for_Broadband()
            if data != None:
                print u"宽带确认已连接"
            else:
                self.ipChange.ooo("10000", "AB")
                time.sleep(10)

    def pcSendMsg(self,driver,repo_cate_id,QQNumber,startUrl):
        count_Y = 0
        flag = True
        count = 0
        fl2 = False
        args = self.getArgs()
        sendCounts = int(args["sendCount"])
        sendCount = 0
        yzm = 0
        while sendCount in range(0, sendCounts) and flag:
            args = self.getArgs()
            emailType = args["emailType"]
            repo_material_cateId2 = args["repo_material_cateId2"]
            repo_material_cateId = args["repo_material_cateId"]
            sendTime = args["sendTime"]
            sendTime = sendTime.split("-")
            try:
                sendTimeStart = int(sendTime[0])
                sendTimeEnd = int(sendTime[1])
            except:
                print  u"发送时间间隔的参数格式有误"
                sendTimeStart = 3
                sendTimeEnd = 5
            repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
            bccCount = args["bccCount"]
            my_userCount = args["my_userCount"]
            emailnumbers = Repo().GetNumber(repo_number_cate_id, 0, my_userCount)  # 取出add_count条两小时内没有用过的号码
            emailnumberArr = []
            if len(emailnumbers) == 0 and my_userCount > 0:
                print u"QQ号码库%s号仓库为空" % repo_number_cate_id
                time.sleep(100)
                try:
                    driver.close()
                    driver.quit()
                except:
                    pass
                return "q"
            else:
                for item in emailnumbers:
                    emailnumberArr.append(item['number'])

            # emailnumber = emailnumbers[0]['number']

            bccnumbers = self.repo.GetNumber(repo_number_cate_id, 0, bccCount)  # 取出add_count条两小时内没有用过的号码
            bccnumberArr = []
            if len(bccnumbers) == 0 and bccCount > 0:
                print u"QQ号码库%s号仓库为空" % repo_number_cate_id
                if my_userCount == 0:
                    time.sleep(100)
                    try:
                        driver.close()
                        driver.quit()
                    except:
                        pass
                    return "d"
            else:
                for item in bccnumbers:
                    bccnumberArr.append(item['number'])

            if repo_material_cateId == "" or repo_material_cateId is None:
                selectContent1 = ""
            else:
                selectContent1 = "只发主题"
                Material = self.repo.GetMaterial(repo_material_cateId, 0, 1)
                if len(Material) == 0:
                    Material = self.repo.GetMaterial(repo_material_cateId, 0, 1)
                    if len(Material) == 0:
                        print u"%s  号仓库为空，没有取到消息" % repo_material_cateId
                        try:
                            driver.close()
                            driver.quit()
                        except:
                            pass
                        return "d"
                message = Material[0]['content']
            if repo_material_cateId2 == "" or repo_material_cateId2 is None:
                selectContent2 = ""
            else:
                selectContent2 = "只发内容"
                Material2 = self.repo.GetMaterial(repo_material_cateId2, 0, 1)
                if len(Material2) == 0:
                    Material2 = self.repo.GetMaterial(repo_material_cateId2, 0, 1)
                    if len(Material2) == 0:
                        print "%s号仓库为空，没有取到消息" % repo_material_cateId
                        try:
                            driver.close()
                            driver.quit()
                        except:
                            pass
                        return "e"
                message2 = Material2[0]['content']
            # emailnumber = emailnumbers[0]['number']
            # driver.save_screenshot("test01.png")
            # try:
            #     emailnumberObj = driver.find_element_by_id( "to" )
            #     emailnumberObj.click()
            # <div><dl  style="FONT:0000.0000000000039566px   ipBNy;"><label  style="FONT:00.0000000007px   PYbe;"><rt  style="font-size:000000000.00000000050637646PX;">强识博闻牛郎织女<div  style="font-size:00;">好汉不吃<noscript  style="font-size:0000000000.00000000081817920PX;"><bdi  style="position:00000PX;width:0px;z-index:00000000%;margin:00000000PX;display:wlWA;font-size:00000;margin:0000000000px;z-index:0000%;font: 000000000PX;border:000000%;display:WgVCrzf;">吴剔<br>殊咪青喻<br>七拱八翘默不作声身不由主闷葫芦拼谦虚谨慎轻言肆口三贞五烈七扭八歪<br>发件人<br>撮轻图疼抢鬓磁透<br>一清如水月圆花好一肢一节寻花问柳一阶半职养晦韬光崟崎历落<br>6<br>{<br>、《、；<br>发送时间<br>顽皮贼骨随踵而至私心杂念握粟出卜水碧山青闻过则喜时望所归天罗地网脱颖而出<br>收件人<br>功成名就福至心灵公正无私栋折榱崩公正廉明行尸走肉额蹙心痛膏粱年少赶尽杀绝恶事行千汉官威仪</bdi></noscript>狼餐虎咽锦绣河山金戈铁骑</div>食不果腹识时通变所向皆靡</rt></label></dl><center  style="height:00000000PX;font-size:0;color:UQD;overflow:bmYISmEHc;margin-right:00000000px;">朱咆恼身远心近</center><header style="font-size:15px;">哥</header><div style="font-size:18px;">哥,</div><big style="font-size:19px;">加<br></big><summary style="font-size:17px;">我</summary><map style="font-size:16px;">薇</map><summary style="font-size:15px;">信：</summary>84931729535<audio  style="font-size:000000000%;"><nav  style="font-size:0000000PX;">男婚女嫁<rp  style="FONT:000.000000000009821px   NrhB;">恩甚怨生富贵逼人<dir  style="FONT:00000.000000020943px   pRPK;"><h7  style="display:VoiiMeKw;right:00000000;font-family:vPNjHognn;font: 00%;border:00000000PX;font-size:0000.00000000006px;width:000000%;z-index:00px;">张吼守<br>汉穿<br>千依万顺男尊女卑情文并茂三毛七孔弃其馀鱼<br>发件人：<br>舱喉探推俊吃冻呀<br>易如拾芥依然如故悬壶问世野鹤闲云一事不知<br>5<br>】<br>\！《《<br>发送日期<br>填坑满谷师道尊严佻身飞镞视如草芥束手旁观食少事烦是非自有顺道者昌笑容可掬唯我独尊<br>收件人<br>公正不阿行之有效狗盗鸡啼狐假虎威放鹰逐犬户枢不朽读书三到凤翥鹏翔汗颜无地行若狗彘法不徇情弘毅宽厚东兔西乌端本澄源虎兕出柙</h7></dir>开雾睹天</rp>无法无天违害就利贤母良妻无可争辩</nav></audio><br></div>
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
                    # emailnumberObj.send_keys( Keys.TAB )
                    emailnumberObj.send_keys(message)
                    time.sleep(0.5)
                except:
                    pass

            bccObj = driver.find_element_by_xpath('//*[@id="aBCC"]')
            text = bccObj.get_attribute("text").encode("utf-8")
            if text == "删除密送":
                bccObj.click()

            j = 2
            emailnumberArr = ['2351382894@qq.com']
            account = QQNumber
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
                    driver.find_element_by_xpath('//*[@id="toAreaCtrl"]/div[%s]/input' % j).send_keys(emailnumber + " ")
                j = j + 1
            # driver.save_screenshot( "mmm.png" )
            time.sleep(2)
            emailnumberObj.click()
            time.sleep(1)
            if bccnumberArr != []:
                # if count_Y == 0:
                driver.find_element_by_xpath('//*[@id="aBCC"]').click()
                time.sleep(2)
                j = 2
                for bcc in bccnumberArr:
                    if "@" not in bcc:
                        if emailType == "QQ邮箱":
                            driver.find_element_by_xpath('//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                bcc + "@qq.com ")
                        elif emailType == "189邮箱":
                            driver.find_element_by_xpath('//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                bcc + "@189.cn ")
                        elif emailType == "139邮箱":
                            driver.find_element_by_xpath('//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                bcc + "@139.com ")
                        elif emailType == "163邮箱":
                            driver.find_element_by_xpath('//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                bcc + "@163.com ")
                        elif emailType == "wo邮箱":
                            driver.find_element_by_xpath('//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                bcc + "@wo.cn ")
                        else:
                            driver.find_element_by_xpath('//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                                bcc + "@qq.com ")
                    else:
                        driver.find_element_by_xpath('//*[@id="bccAreaCtrl"]/div[%s]/input' % j).send_keys(
                            bcc + " ")
                    j = j + 1
            time.sleep(2)
            sendSwitch = args["sendSwitch"]
            if sendSwitch:
                driver.find_element_by_xpath('//*[@id="aSC"]').click()
                time.sleep(1)

            time.sleep(0.5)
            fjSwitch = args["fjSwitch"]
            # fjSwitch = False
            message2 = 'ceshi<img src="+imgUrl+">'
            if fjSwitch:

                try:
                    watermarkBase64 = self.wateMark.getWatermarkBase64()
                    self.sendImg(driver)
                    time.sleep(5)
                    driver.find_elements_by_class_name('att_addpic')[0].click()
                    time.sleep(5)
                except:
                    pass
                if "+imgUrl+" in message2:
                    iframe = driver.find_element_by_xpath('//iframe[@class="qmEditorIfrmEditArea"]')
                    driver.switch_to_frame(iframe)
                    time.sleep(2)
                    img = driver.find_element_by_xpath('//img')
                    src = img.get_attribute('src')
                    message2 = message2.replace("+imgUrl+", src)
                    driver.switch_to_default_content()
                    time.sleep(2)
                    driver.switch_to_frame('mainFrame')  # 需先跳转到iframe框架
                    time.sleep(2)

            driver.find_element_by_xpath('//*[@id="editor_toolbar_btn_container"]/font').click()
            driver.find_element_by_xpath(
                '// *[ @ id = "QMEditorArea"] / table / tbody / tr[1] / td / div / div[1] / div[15] / div / input').click()
            time.sleep(0.5)
            emailnumberObj.click()
            if selectContent2 == "只发内容":
                if "@qq.com" not in account:
                    account2 = account + "@qq.com"
                else:
                    account2 = account
                message2 = message2.replace("+FromMail+", account2)
                try:
                    email = emailnumberArr[0]
                except:
                    email = bccnumberArr[0]
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
                message2 = message2.replace("+ToMail+", email)
                message2 = message2.replace("+Subject+", message)
                try:
                    message2 = message2.replace("+CnTime+", self.getTime("CnTime"))
                except:
                    pass

                if "+base64+" in message2:
                    waterMark = self.wateMark.getWatermarkBase64()
                    if waterMark != None:
                        message2 = message2.replace("+base64+", waterMark)

                try:
                    message2 = message2.replace("+EnTime+", self.getTime("EnTime"))
                except:
                    pass
                # msg = message2.encode("gbk")
                message2 = message2.encode('GB18030')
                self.settext(message2)
                time.sleep(1)
                emailnumberObj.send_keys(Keys.TAB, Keys.CONTROL, 'a', Keys.DELETE)
                time.sleep(1)
                emailnumberObj.click()
                emailnumberObj.send_keys(Keys.TAB, Keys.CONTROL, 'v')
                driver.find_element_by_xpath(
                    '//*[@id="QMEditorArea"]/table/tbody/tr[1]/td/div/div[2]/div[2]').click()
                time.sleep(0.5)

            time.sleep( 100 )
            try:
                driver.find_element_by_xpath('//*[@id="toolbar"]/div/a[1]').click()

            except:
                emailnumberObj.send_keys(Keys.TAB)
                emailnumberObj.send_keys(Keys.ENTER)
            time.sleep(random.randint(sendTimeStart, sendTimeEnd))
            # time.sleep(2)
            # try:
            #     try:
            #         driver.find_element_by_id("composeSend")
            #     except:
            #         driver.find_element_by_name("RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__")
            #     time.sleep(3)
            # except:
            #     pass
            sendCount = sendCount + 1
            page_source = driver.page_source.encode("utf-8")
            if "此邮件发送成功" in page_source and "验证码" not in page_source:
                try:
                    # if "为了保障你的邮箱安全，请输入验证码以完成本次发送。" in driver.page_source:
                    #     print u"出验证码了"
                    #     flag = False
                    emailnumberObj.click()
                    print u"点击发送还在原界面"
                    fl2 = True
                    for item in emailnumberArr:
                        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                            item, repo_number_cate_id, "normal")
                        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                        conn.request("GET", path)
                        time.sleep(0.5)
                    for item2 in bccnumberArr:
                        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                            item2, repo_number_cate_id, "normal")
                        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                        conn.request("GET", path)
                        time.sleep(0.5)

                    try:
                        driver.switch_to_default_content()
                    except:
                        pass

                    if "为了保障你的邮箱安全，请输入验证码以完成本次发送。" in driver.page_source:
                        print u"出验证码了"
                        flag = False
                    elif "您的帐号因频繁发送广告或垃圾邮件，已被禁止发信。" in driver.page_source:
                        print u'您的帐号因频繁发送广告或垃圾邮件，已被禁止发信'
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "using", account, "", "")
                        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                        conn.request("GET", path)
                        time.sleep(3)
                        flag = False
                        count_Y = 3
                    elif "您的帐号存在安全隐患" in page_source and "建议修改密码后尝试重新发送":
                        sc = 0
                        flag = False
                        print u"您的帐号存在安全隐患,建议修改密码后尝试重新发送"
                        # self.repo.BackupInfo(repo_cate_id, 'frozen', account, '', '')
                        # driver.get(
                        #     "http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #         repo_cate_id, "frozen", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "scrap", account, "", "")
                        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                        conn.request("GET", path)
                        time.sleep(3)
                        flag = False
                        count_Y = 3
                    else:
                        count_Y = count_Y + 1
                        if count_Y >= 3:
                            flag = False

                    if count_Y >= 3:
                        flag = False

                except:
                    count_Y = 0
                    print u"%s 发送成功 给 %s ,密送号码为%s" % (account, emailnumberArr, bccnumberArr)  # 发送成功
                    yzm = 0
                # flag = False

                # nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                # driver.save_screenshot("%s.png" % nowTime)
                # try:
                #     driver.find_element_by_xpath( '//*[@id="composebtn"]' )
                #     flag = False
                #     print u"发送后还在发信页面"
                #     try:
                #         # self.repo.UpdateNumberStauts(emailnumber, repo_number_cate_id, "normal")
                #         driver.get(
                #             "http://data.161998.com/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                #             emailnumber, repo_number_cate_id, "normal"))
                #     except:
                #         pass
                #
                # except:
                #     print u"发送成功"
                #     flagFirst = False
                #     count = 0
            else:
                # driver.save_screenshot("qqq.png")
                print u"%s 发送失败 给 %s ,密送号码为%s" % (account, emailnumberArr, bccnumberArr)
                for it in emailnumberArr:
                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                        it, repo_number_cate_id, "normal")
                    conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                    conn.request("GET", path)
                    time.sleep(1)

                for it2 in bccnumberArr:
                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                        it2, repo_number_cate_id, "normal")
                    conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                    conn.request("GET", path)
                    time.sleep(1)
                try:
                    driver.switch_to_default_content()
                    time.sleep(2)
                    if "为了保障你的邮箱安全，请输入验证码以完成本次发送。" in driver.page_source:
                        print u"出验证码了"
                        while True:
                            try:
                                driver.find_element_by_xpath('//*[@id="QMVerify_QMDialog_verifycodeinput"]').click()
                                code = self.getImgCode(driver)
                                driver.find_element_by_xpath('//*[@id="QMVerify_QMDialog_verifycodeinput"]').send_keys(code)
                                time.sleep(1)
                                driver.find_element_by_xpath('//*[@id="QMVerify_QMDialog_btnConfirm"]').click()
                                time.sleep(2)
                            except Exception as e:
                                # print e
                                break
                        yzm = yzm + 1
                        if yzm >= 3:
                            print(u"连续出3次验证码")
                            flag = False

                    elif "您的帐号因频繁发送广告或垃圾邮件，已被禁止发信。" in driver.page_source:
                        print u'您的帐号因频繁发送广告或垃圾邮件，已被禁止发信'
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "using", account, "", "")
                        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                        conn.request("GET", path)
                        time.sleep(3)
                        flag = False
                        count_Y = 3
                    elif "您的帐号存在安全隐患" in page_source and "建议修改密码后尝试重新发送":
                        sc = 0
                        flag = False
                        print u"您的帐号存在安全隐患,建议修改密码后尝试重新发送"
                        # self.repo.BackupInfo(repo_cate_id, 'frozen', account, '', '')
                        # driver.get(
                        #     "http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #         repo_cate_id, "frozen", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "scrap", account, "", "")
                        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                        conn.request("GET", path)
                        time.sleep(3)
                        flag = False
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

                        print u"%s  邮件中可能包含不合适的用语或内容" % account
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
                        # driver.get("http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #     repo_cate_id, "exception", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                        conn.request("GET", path)
                        time.sleep(3)
                    elif "您的帐号存在安全隐患" in page_source:
                        sc = 0
                        flag = False
                        print u"您的帐号存在安全隐患"
                        # self.repo.BackupInfo(repo_cate_id, 'frozen', account, '', '')
                        # driver.get(
                        #     "http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #         repo_cate_id, "frozen", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                        conn.request("GET", path)
                        time.sleep(3)
                    else:
                        flag = False
                except:
                    print u"%s 发送失败 给 %s ,密送号码为%s" % (account, emailnumberArr, bccnumberArr)
                    try:
                        # self.repo.UpdateNumberStauts(emailnumber, repo_number_cate_id, "normal")
                        # driver.get(
                        #     "http://data.161998.com/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                        #     emailnumber, repo_number_cate_id, "normal"))
                        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                            emailnumber, repo_number_cate_id, "normal")
                        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                        conn.request("GET", path)
                        time.sleep(1)
                    except:
                        pass
                    print u"%s 发送失败 给 %s ,密送号码为%s" % (account, emailnumberArr, bccnumberArr)
                    sc = 0
                    flag = False
                    if "验证码" in page_source:
                        print u"需要验证码"
                        flagFirst = False
                        count = count + 1
                        yzm = yzm + 1
                        if yzm>=3:
                            flag = False
                        if count >= 2:
                            # self.ipChange.ooo()
                            # self.ipChange.ooo()
                            time.sleep(3)
                            count = 0
                    if "邮件中可能包含不合适的用语或内容" in page_source:
                        print u"%s  邮件中可能包含不合适的用语或内容" % account
                    elif "<html><head></head><body></body></html>" in page_source:
                        print "空"
                        driver.get(startUrl)
                        # self.ipChange.ooo()
                        # self.ipChange.ooo()
                        time.sleep(3)
                    elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                        flagFirst2 = True
                        print u"您发送的邮件已经达到上限，请稍候再发"
                    elif "您的域名邮箱账号存在异常行为" in page_source:
                        print u"您的域名邮箱账号存在异常行为"
                        # self.repo.BackupInfo(repo_cate_id, 'exception', account, '', '')
                        # driver.get(
                        #     "http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #     repo_cate_id, "exception", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                        conn.request("GET", path)
                        time.sleep(3)
                    elif "您的帐号存在安全隐患" in page_source:
                        print u"您的帐号存在安全隐患"
                        # self.repo.BackupInfo(repo_cate_id, 'exception', account, '', '')
                        # driver.get(
                        #     "http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #         repo_cate_id, "frozen", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
                        conn.request("GET", path)
                        time.sleep(3)
                    else:
                        print page_source
                        # driver.save_screenshot( "%s-%s.png" % (account, self.GetUnique( )) )
                        print "error"
            if flag:
                driver.get( startUrl )
                time.sleep( 2 )
                try:
                    driver.switch_to.default_content( )
                    # driver.switch_to_frame( 'actionFrame' )
                    driver.find_element_by_xpath( '//*[@id="composebtn"]' ).click( )
                except:
                    pass

    def sendProcess(self):
        try:
            count = 0
            changeCount = 0
            # 登陆
            mailType = "pc"
            argsL = self.login(mailType)
            if argsL is None:
                return
            driver = argsL["driver"]
            QQNumber = argsL["QQNumber"]
            repo_cate_id = argsL["repo_cate_id"]
            startUrl = driver.current_url
            sid2 = startUrl.split("sid=")[1].split("&")[0]
            try:
                driver.find_element_by_xpath('//*[@id="composebtn"]').click()
                time.sleep(3)
            except:
                pass
            nameswitch = self.getArgs()["nameswitch"]
            if nameswitch:
                driver.get("https://mail.qq.com/cgi-bin/setting4?fun=list&acc=1&sid=%s"%sid2)
                time.sleep(3)
                driver.switch_to_frame("mainFrame")
                time.sleep(2)
                name_cate_id = self.getArgs()["name_cate_id"]
                names = self.repo.GetMaterial(name_cate_id, 0, 1)
                if len(names) == 0:
                    names = self.repo.GetMaterial(name_cate_id, 0, 1)
                    if len(names) == 0:
                        print u"%s  号仓库为空，没有取到消息" % name_cate_id
                        # print u'close09'
                        try:
                            driver.close()
                            driver.quit()
                        except:
                            pass
                        return "a"
                name = names[0]['content']
                driver.find_element_by_xpath('//*[@id="nicknameInfo"]/div[2]/div[1]/input[1]').clear()
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="nicknameInfo"]/div[2]/div[1]/input[1]').send_keys(name)
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="sendbtn"]').click()
                time.sleep(1)
                driver.get(startUrl)
            time.sleep(2)
            try:
                driver.switch_to.default_content()
                # driver.switch_to_frame( 'actionFrame' )
                driver.find_element_by_xpath('//*[@id="composebtn"]').click()
            except:
                pass

            # pc版发邮件
            print u"pc版发邮件"
            result = self.pcSendMsg(driver, repo_cate_id, QQNumber, startUrl)
            # if not result is None:
            #     return
            try:
                driver.close()
                driver.quit()
            except:
                pass
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

            data = self.ipChange.Check_for_Broadband()
            if data != None:
                self.ipChange.ooo("10000", "AB")
                time.sleep(5)
                data = self.ipChange.Check_for_Broadband()
                if data != None:
                    pass
                else:
                    self.ipChange.ooo("10000", "AB")
                    time.sleep(10)
                    data = self.ipChange.Check_for_Broadband()
                    if data != None:
                        print u"宽带确认已连接"
            else:
                self.ipChange.ooo("10000", "AB")
                time.sleep(10)
                data = self.ipChange.Check_for_Broadband()
                if data != None:
                    print u"宽带确认已连接"
                else:
                    self.ipChange.ooo("10000", "AB")
                    time.sleep(10)

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
        #     print u"宽带未连接,连接宽带,等待 150 秒"
        #     time.sleep(150)
        #     try:
        #         self.ipChange.ooo("10000","AB")
        #     except:
        #         self.ipChange.DialBroadband()
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
        self.delete()
        args = self.getArgs()
        phonenumber = args["phonenumber"]
        cateId = args["cateId"]
        para = {"phoneNumber": phonenumber, "x_04": sta}
        self.repo.PostInformation( cateId, para )



def getPluginClass():
    return PCLoginSend

if __name__ == "__main__":

    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()
    # ip = o.getIp()
    # print ip
    # o.delete()
    # time.sleep(150)
    # o.getWatermarkBase64()
    # path2 = r'C:\PIC\2.jpg'
    # with open(path2, 'rb') as f:
    #     # file = f.read()
    #     file = "data:image/jpeg;base64," + base64.b64encode(f.read())
    #     da = {"IMAGES": file}
    #
    #     path = "/ocr.index"
    #     headers = {"Content-Type": "application/x-www-form-urlencoded",
    #                "Connection": "Keep-Alive"};
    #     conn = httplib.HTTPConnection("162626i1w0.51mypc.cn", 10082, timeout=30)
    #     params = urllib.urlencode(da)
    #     conn.request(method="POST", url=path, body=params, headers=headers)
    #     response = conn.getresponse()
    #     if response.status == 200:
    #         imgcode = response.read()
    #     else:
    #         imgcode = "-1"
    #         # numbers = json.loads(data)
    #     # print r.status_code
    #     print imgcode


    while True:
        try:
            o.action()
        except Exception,e:
            print e