# coding:utf-8
from __future__ import division
import base64
import httplib
import logging
import re
import socket
import urllib
import urllib2
from ctypes import *

from PIL import Image
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs


import os, time, datetime, random
import json
import sys
sys.path.append("C:\TaskConsole-master")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# from imageCode import imageCode
# from smsCode import smsCode

# sys.path.append("/home/zunyun/workspace/TaskConsole")
# from imageCode import imageCode


from IPChange import IPChange
from Repo import Repo
class Email_163_add:
    def __init__(self):
        self.repo = Repo()
        self.ipChange = IPChange()
        # self.type = 'yixin'

    def getImgCode(self,driver):
        img = driver.find_element_by_xpath('//*[@id="code-img"]' )
        # 取验证码的x,y
        captchaX = int( img.location['x'] )
        captchaY = int( img.location['y'] )

        # 取验证码的宽度和高度
        captchaWidth = img.size['width']
        captchaHeight = img.size['height']
        captchaRight = captchaX + captchaWidth
        captchaBottom = captchaY + captchaHeight
        # # 通过Image处理图像，第一种方法：在frame区域截取
        path1 = r"C:\YZM\z.jpeg"  # 截屏图片
        path2 = r"C:\YZM\captcha.jpeg"  # 验证码图片
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

        time.sleep(3)
        with open(path2, 'rb') as f:
            data = f.read()
        dll = windll.LoadLibrary('OCR163.dll')
        time.sleep(3)
        ret = dll.OCR(data, len(data))
        time.sleep(3)
        ocrVal = c_char_p(ret)
        time.sleep(2)
        ocrCode = str(ocrVal.value)
        print(ocrCode)
        if ocrCode == "-10":
            print "验证码没识别出来"
            return
        else:
            return ocrCode
        os.remove(path1)

        # captchaX = 556
        # captchaY = 445
        # captchaRight = 726
        # captchaBottom = 505

        # os.remove(path2 )
        return imgcode


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
        conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
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
        path = r"C:\add.txt"
        asdlFile = open( path, "r" )
        asdlList = asdlFile.readlines( )
        try:
            if len( asdlList )>=5:
                user_agent_id = int(asdlList[0].split(":")[1])
                ym_cate_id = int(asdlList[1].split( ":" )[1])
                account_cate_id = int(asdlList[2].split( ":" )[1])
                accountCount = int(asdlList[3].split( ":" )[1])
                name_cate_id = int(asdlList[4].split(":")[1])
            else:
                print u"%s没有写入相关参数,请尽快写入"%path
                time.sleep(120)
                return


            args = {"ym_cate_id": ym_cate_id,"user_agent_id": user_agent_id,"account_cate_id":account_cate_id,"accountCount":accountCount,"name_cate_id":name_cate_id}
            return args
        except:
            print u"参数格式可能存在错误"

    def sendProcess(self):
        try:
            flag1 = True
            flag2 = True
            flag3 = True
            #flag4 = True
            while True:
                args = self.getArgs()
                user_agent_id = args["user_agent_id"]
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
                fl = False
                # options.add_argument( 'headless' )
                # 更换头部
                # options.add_argument(user_agent)
                # user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
                options.add_argument('user-agent="%s' % user_agent)
                try:
                    driver = webdriver.Chrome(chrome_options=options,
                                              executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")
                except:
                    if not os.path.exists("C:\Users\Administrator\AppData\Local\Temp"):
                        os.mkdir("C:\Users\Administrator\AppData\Local\Temp")

                # driver.get( "http://app.ym.163.com/ym/reg/view/index#" )
                # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled')
                time.sleep( 3 )

                ym_cate_id = args["ym_cate_id"]
                account_cate_id = args["account_cate_id"]
                accountCount = int(args["accountCount"])
                name_cate_id = args['name_cate_id']

                numbers = self.repo.GetAccount("normal", ym_cate_id, 0, 1)
                # numbers = [{"number":"RIj@vip.qkljko.info","password":"13141314Abc"}]
                if len(numbers) == 0:
                    numbers = self.repo.GetAccount("normal", ym_cate_id, 0, 1)
                    if len(numbers) == 0:
                        print u"%s号仓库没有数据" % ym_cate_id
                        time.sleep(300)
                        return
                account = numbers[0]['number']  # 即将登陆的QQ号
                password = numbers[0]['password']
                driver.get( r'https://qiye.163.com/login/?from=ym' )
                time.sleep( 2 )

                try:
                    # 若帐号输入框有内容先清空
                    driver.find_element_by_id( "accname" ).clear( )
                    driver.find_element_by_id( "accpwd" ).clear( )
                except:
                    pass
                try:
                    # ///
                    # 输入框输入帐号和密码
                    # account = "ixm@666.NANWAZI.COM"
                    # password = "13141314Abc"
                    driver.find_element_by_id( "accname" ).send_keys( account )
                    driver.find_element_by_id( "accpwd" ).send_keys( password )
                    # driver.save_screenshot( "222.png" )
                    time.sleep( 0.5 )
                    driver.find_element_by_id( "accpwd" ).send_keys( Keys.ENTER )
                    time.sleep( random.randint( 2, 4 ) )
                except:
                    pass

                if driver.current_url != "https://qiye.163.com/login/?from=ym" and "该域名未开通企业邮箱，请联系经销商或客服" not in driver.page_source:
                    # driver.find_element_by_xpath( '//*[@id="nav-mbox"]/div[1]/a[1]/div' )   #网易的logo
                    print u"%s  登陆成功" % account
                    # Repo( ).BackupInfo( repo_cate_id, 'normal', account, user_agent, '' )
                    startUrl = driver.current_url
                    aid = startUrl.split("aid=")[1].split("&")[0]
                else:
                    print u"%s  登陆失败" % account
                    errorPage = driver.page_source.encode("utf-8")
                    if "拖动下方滑块完成拼图" in errorPage:
                        print u"拖动下方滑块完成拼图"
                    elif "看不清" in errorPage:
                        print u"需要验证码"
                    elif "验证码" in errorPage and (not "邮箱帐号和密码不匹配" in errorPage):
                        print u"验证码"
                    elif "你的帐号存在安全隐患" in errorPage:
                        print u"你的帐号存在安全隐患"
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            ym_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                        conn.request("GET", path)
                        time.sleep(3)
                    elif "该域名未开通企业邮箱，请联系经销商或客服" in errorPage:
                        print u"该域名未开通企业邮箱，请联系经销商或客服"
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            ym_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                        conn.request("GET", path)
                        time.sleep(3)
                    return

                thiscount = 0
                try:
                    count = driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/p')
                    thisCount = count.text.split("有")[1].split("个")[0]
                    try:
                        thiscount = int(thisCount)
                        if thiscount>=accountCount:
                            print u"已有%s个子账号了"%thiscount
                            path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                ym_cate_id, "using", account, "", "")
                            conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                            conn.request("GET", path)
                            time.sleep(3)
                            continue
                        # else:
                        #     accountCount = accountCount - thiscount
                    except:
                        pass
                    driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/div/div[1]/span').click()
                except:
                    driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[2]/div/div[1]/span').click()
                    pass
                ym = account.split("@")[1]
                # for i in range(thiscount,accountCount+1):
                addCount = thiscount
                errorCount = 0
                while addCount in range(thiscount,accountCount+1):
                    if errorCount >=5:
                        break
                    names = self.repo.GetMaterial(name_cate_id, 0, 1)
                    if len(names) == 0:
                        names = self.repo.GetMaterial(name_cate_id, 0, 1)
                        if len(names) == 0:
                            print u"%s号仓库为空，没有取到消息" % name_cate_id
                            return
                    name = names[0]['content']
                    driver.find_element_by_xpath('//*[@id="nickname"]').clear()
                    driver.find_element_by_xpath('//*[@id="nickname"]').send_keys(name)
                    time.sleep(4)
                    num = ""
                    for j in range(0, random.randint(2, 4)):
                        n = random.choice("qwertyuiopasdfghjklzxcvbnm")
                        num = n + num
                    if addCount<10:
                        addaccount = num +"00" + str(addCount)
                    elif addCount>=10 and addCount<100:
                        addaccount = num + "0" + str(addCount)
                    elif addCount >= 100:
                        addaccount = num+str(addCount)
                    driver.find_element_by_xpath('//*[@id="account_name"]').click()
                    driver.find_element_by_xpath('//*[@id="account_name"]').clear()
                    for it in addaccount:
                        driver.find_element_by_xpath('//*[@id="account_name"]').send_keys(it)
                    driver.find_element_by_xpath('//*[@id="pass_re"]').click()
                    time.sleep(4)
                    psw = ""
                    for j in range(0, random.randint(4, 6)):
                        n = random.choice("qwertyuiopasdfghjklzxcvbnm")
                        psw = n + psw
                    for j in range(0, random.randint(4, 6)):
                        n = random.choice("0123456789")
                        psw = psw + n
                    driver.find_element_by_xpath('//*[@id="pass_re"]').clear()
                    driver.find_element_by_xpath('//*[@id="pass_re"]').send_keys(psw)
                    time.sleep(4)
                    driver.find_element_by_xpath('//*[@id="sub-btn"]').click()
                    time.sleep(2)
                    for i in range(0,2):
                        if "该账号被系统判断为垃圾账号，请注册其他账号" in driver.page_source and (not "添加成功" in driver.page_source):
                            # print u"该账号被系统判断为垃圾账号，请注册其他账号"
                            try:
                                driver.find_element_by_xpath('//*[@id="code-input"]').send_keys("a")
                                break
                            except:
                                pass
                            try:
                                driver.find_element_by_xpath('//*[@id="nickname"]').clear()
                                names = self.repo.GetMaterial(name_cate_id, 0, 1)
                                if len(names) == 0:
                                    names = self.repo.GetMaterial(name_cate_id, 0, 1)
                                    if len(names) == 0:
                                        print u"%s号仓库为空，没有取到消息" % name_cate_id
                                        return
                                name = names[0]['content']
                                driver.find_element_by_xpath('//*[@id="nickname"]').clear()
                                driver.find_element_by_xpath('//*[@id="nickname"]').send_keys(name)
                                time.sleep(4)
                                driver.find_element_by_xpath('//*[@id="account_name"]').clear()
                                num = ""
                                for j in range(0, random.randint(2, 4)):
                                    n = random.choice("qwertyuiopasdfghjklzxcvbnm")
                                    num = n + num
                                if addCount < 10:
                                    addaccount = num + "00" + str(addCount)
                                elif addCount >= 10 and addCount < 100:
                                    addaccount = num + "0" + str(addCount)
                                elif addCount >= 100:
                                    addaccount = num + str(addCount)
                                driver.find_element_by_xpath('//*[@id="account_name"]').clear()
                                driver.find_element_by_xpath('//*[@id="account_name"]').send_keys(addaccount)
                                time.sleep(4)
                                driver.find_element_by_xpath('//*[@id="pass_re"]').clear()
                                psw = ""
                                for j in range(0, random.randint(4, 6)):
                                    n = random.choice("qwertyuiopasdfghjklzxcvbnm")
                                    psw = n + psw
                                for j in range(0, random.randint(4, 6)):
                                    n = random.choice("0123456789")
                                    psw = psw + n
                                driver.find_element_by_xpath('//*[@id="pass_re"]').send_keys(psw)
                                time.sleep(4)
                                driver.find_element_by_xpath('//*[@id="pass_re"]').click()
                                time.sleep(3)
                            except:
                                break
                                # pass
                            try:
                                driver.find_element_by_xpath('//*[@id="sub-btn"]').click()
                                time.sleep(4)
                            except:
                                pass
                        else:
                            break
                    # else:
                    #     print u"一直是该账号被系统判断为垃圾账号"
                    #     return

                    if "添加成功" in driver.page_source:
                        print u"添加成功"
                        errorCount = 0
                        addCount = addCount + 1
                        if i!=accountCount:
                            w = addaccount + "@" + ym + "----" + psw+"\n"
                        else:
                            w = addaccount + "@" + ym + "----" + psw
                        fo = open(r"C:\account.txt", "a+")
                        fo.write(w)
                        # 关闭打开的文件
                        fo.close()
                        # data = {"account":addaccount+"@"+ym ,"password": "13141314Abc", 'PhoneNumber': None,
                        #         'cate_id': account_cate_id,
                        #         'status': "normal", 'IMEI': None, "cardslot": None}
                        # path = "/repo_api/register/numberInfo"
                        # headers = {"Content-Type": "application/x-www-form-urlencoded",
                        #            "Connection": "Keep-Alive"};
                        # conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                        # params = urllib.urlencode(data)
                        # conn.request(method="POST", url=path, body=params, headers=headers)
                        # conn.close()
                        if i != accountCount:
                            driver.find_element_by_xpath('/html/body/div/div[2]/div/div[3]/div[2]/div[2]/span').click()
                            driver.find_element_by_xpath('/html/body/div[2]/div[2]/table/tbody/tr/td[2]/div[1]/div/a/div/span').click()
                    else:
                        try:
                            driver.find_element_by_xpath('//*[@id="code-input"]').clear()
                            code = self.getImgCode(driver)
                            driver.find_element_by_xpath('//*[@id="code-input"]').send_keys(code)
                            driver.find_element_by_xpath('//*[@id="sub-btn"]').click()
                            time.sleep(4)
                            if "添加成功" in driver.page_source:
                                print u"添加成功"
                                errorCount = 0
                                addCount = addCount + 1
                                if i != accountCount:
                                    w = addaccount + "@" + ym + "----" +psw+ "\n"
                                else:
                                    w = addaccount + "@" + ym + "----" + psw
                                fo = open(r"C:\account.txt", "a+")
                                fo.write(w)
                                # 关闭打开的文件
                                fo.close()
                                # data = {"account":addaccount+"@"+ym ,"password": "13141314Abc", 'PhoneNumber': None,
                                #         'cate_id': account_cate_id,
                                #         'status': "normal", 'IMEI': None, "cardslot": None}
                                # path = "/repo_api/register/numberInfo"
                                # headers = {"Content-Type": "application/x-www-form-urlencoded",
                                #            "Connection": "Keep-Alive"};
                                # conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                                # params = urllib.urlencode(data)
                                # conn.request(method="POST", url=path, body=params, headers=headers)
                                # conn.close()
                                if i != accountCount:
                                    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[3]/div[2]/div[2]/span').click()
                                    driver.find_element_by_xpath('/html/body/div[2]/div[2]/table/tbody/tr/td[2]/div[1]/div/a/div/span').click()
                        except:
                            # logging.exception("a")
                            errorCount = errorCount + 1

                #拨号
                data = self.ipChange.Check_for_Broadband()
                if data != None:
                    self.ipChange.ooo("10001", "ABCDEF")
                    time.sleep(5)
                    data = self.ipChange.Check_for_Broadband()
                    if data != None:
                        pass
                    else:
                        self.ipChange.ooo("10001", "ABCDEF")
                        time.sleep(10)
                        data = self.ipChange.Check_for_Broadband()
                        if data != None:
                            print u"宽带确认已连接"
                else:
                    self.ipChange.ooo("10001", "ABCDEF")
                    time.sleep(10)
                    data = self.ipChange.Check_for_Broadband()
                    if data != None:
                        print u"宽带确认已连接"
                    else:
                        self.ipChange.ooo("10001", "ABCDEF")
                        time.sleep(10)

        except Exception,e:
            logging.exception("d")
                # result = [driver]
            # self.delete()
            return []

    def action(self):
        # data = self.ipChange.Check_for_Broadband()
        # if data != None:
        #     print u"宽带确认已连接,模块继续运行"
        # else:
        #     print u"宽带未连接,连接宽带"
        #     time.sleep(150)
        #     self.ipChange.ooo("10001", "ABCDEF")
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

def getPluginClass():
    return Email_163_add

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()
    # path2 = "C:\YZM\captcha.jpeg"
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
    # if ocrCode == "-10":
    #     print "验证码没识别出来"
    while True:
        try:
            o.action()
        except Exception,e:
            print e