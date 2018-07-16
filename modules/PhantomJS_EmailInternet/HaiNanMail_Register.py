# coding:utf-8
from __future__ import division
import base64
import httplib
import logging
import re
import socket
import urllib2

# from PIL import Image
from  PIL import Image
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs


import os, time, datetime, random
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from imageCode import imageCode
from smsCode import smsCode

sys.path.append("/home/zunyun/workspace/TaskConsole")
# sys.path.append("C:\TaskConsole-master")
from IPChange import IPChange
from Repo import Repo
class HaiNanMail_Register:
    def __init__(self):
        self.repo = Repo()
        # self.ipChange = IPChange()
        self.type = 'yixin'

    def getImgCode(self,driver):
        img = driver.find_element_by_xpath('//*[@id="codePic"]' )
        # 取验证码的x,y
        captchaX = int( img.location['x'] )
        captchaY = int( img.location['y'] )

        # 取验证码的宽度和高度
        captchaWidth = img.size['width']
        captchaHeight = img.size['height']
        captchaRight = captchaX + captchaWidth
        captchaBottom = captchaY + captchaHeight
        # 通过Image处理图像，第一种方法：在frame区域截取
        path1 = "/home/zunyun/text/z.png" #截屏图片
        path2 = "/home/zunyun/text/captcha.png" # 验证码图片
        driver.save_screenshot( path1 )
        imgObject = Image.open( path1 )
        imgCaptcha = imgObject.crop( (captchaX, captchaY, captchaRight, captchaBottom) )  # 裁剪
        imgCaptcha.save( path2 )
        icode = imageCode( )
        im = open( path2, 'rb' )
        codeResult = icode.getCode( im, icode.CODE_TYPE_4_NUMBER_CHAR )

        imgcode = codeResult["Result"]
        im_id = codeResult["Id"]
        os.remove( "/home/zunyun/text/z.png" )
        os.remove( "/home/zunyun/text/captcha.png" )
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

    def GetToken(self, username="powerman",password="12341234abc"):
        path = "/Login?uName=%s&pWord=%s&Developer=" % (username,password)
        conn = httplib.HTTPConnection( "xapi.xunma.net", None, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            token = data.split("&")[0]
            return token
        else:
            print "帐号或密码错误"
            return []

    def GetPhoneNumber(self, ItemId,token):
        path = "/getPhone?ItemId=%s&token=%s" % (ItemId,token)
        conn = httplib.HTTPConnection( "xapi.xunma.net", None, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        # data = response.read( )
        if response.status == 200:
            data = response.read( )
            if u'Session 过期' in data or u'Session过期' in data:
                # self.GetToken(False)
                return "False"
            phone = data[:-1]
            return phone
        else:
            return

    def GetCode(self,token, phone,ItemId=2124):
        try:
            path = "/getMessage?token=%s&itemId=%s&phone=%s" % (token, ItemId, phone)
            conn = httplib.HTTPConnection( "xapi.xunma.net", None, timeout=30 )
            conn.request("GET", path)
            response = conn.getresponse()
            if response.status == 200:
                data = response.read().decode('GBK')
                code = None
                print(data)
                if u'Session 过期' in data or u'Session过期' in data:
                    # self.GetToken(False)
                    return "False"
                elif u"您正在申请注册网易免费企业邮箱" in data:
                    # searchObj = re.search( r'验证.*?"', data, re.M | re.I )
                    # code = searchObj.group( )[-6:]
                    code = data.split('，')[1]
                    code = code[3:9]
                    return code
                elif u'单笔充值满 50元送 5%单笔充值满100元送10%自动赠送！上不封顶' in data:
                    pass
                return code
        except Exception,e:
            print e
            return None

    def getArgs(self):
        # asdlFile = open( r"/home/zunyun/text/asdl.txt", "r" )
        path = "/home/zunyun/text/register.txt"
        asdlFile = open( path, "r" )
        asdlList = asdlFile.readlines( )
        try:
            if len( asdlList )>=8:
                user_agent_id = int(asdlList[0].split(":")[1])
                ym_cate_id = int(asdlList[1].split( ":" )[1])
                organization_cate_id = int(asdlList[2].split( ":" )[1])
                address_cate_id = int(asdlList[3].split( ":" )[1])
                scaleCount = int(asdlList[4].split( ":" )[1])
                username_cate_id = int(asdlList[5].split( ":" )[1])
                manageAccount_cate_id = int(asdlList[6].split( ":" )[1])
                mail_cate_id = int(asdlList[7].split( ":" )[1])
                ymMail_cate_id = int(asdlList[8].split( ":" )[1])
                ym_zlk_Id = int( asdlList[9].split( ":" )[1] )
                xunma_itemId = int( asdlList[10].split( ":" )[1] )
                cardId_id = int( asdlList[11].split( ":" )[1] )
            else:
                print u"%s没有写入相关参数,请尽快写入"%path
                time.sleep(120)
                return


            args = {"ym_cate_id": ym_cate_id, "organization_cate_id": organization_cate_id, "address_cate_id": address_cate_id,
                    "username_cate_id": username_cate_id, "manageAccount_cate_id": manageAccount_cate_id,
                    "mail_cate_id": mail_cate_id, "ymMail_cate_id": ymMail_cate_id,
                    "user_agent_id": user_agent_id,"xunma_itemId":xunma_itemId,"ym_zlk_Id":ym_zlk_Id,"scaleCount":scaleCount,"cardId_id":cardId_id}  # cate_id是仓库号，length是数量
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
                if flag1:
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
                    # options.add_argument( 'headless' )
                    #更换头部
                    options.add_argument(user_agent)
                    options.add_argument('user-agent="%s' % user_agent)
                    try:
                        driver = webdriver.Chrome( chrome_options=options,
                                                   executable_path="/opt/google/chrome/chromedriver" )
                    except:
                        if not os.path.exists("C:\Users\Administrator\AppData\Local\Temp"):
                            os.mkdir("C:\Users\Administrator\AppData\Local\Temp")

                    driver.get( "http://mail.hainan.net/webmailhainan/register.jsp" )
                    # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled')
                    time.sleep( 3 )
                    driver.find_element_by_xpath('//*[@id="email_text"]').send_keys("dwdada")
                    try:

                        al =  driver.switch_to_alert()
                        al.accept()
                    except:
                        pass
                    selectArr = ('//*[@id="email_type"]/option[2]','//*[@id="email_type"]/option[2]')
                    driver.find_element_by_xpath(selectArr[random.randint(0,1)]).click()
                    try:

                        al =  driver.switch_to_alert()
                        al.accept()
                    except:
                        pass
                    driver.find_element_by_xpath('//*[@id="pwd"]').send_keys("13141314abc")
                    time.sleep(2)
                    try:

                        al =  driver.switch_to_alert()
                        al.accept()
                    except:
                        pass
                    driver.find_element_by_xpath('//*[@id="pwd_again"]').send_keys("13141314abc")
                    code = self.getImgCode(driver)
                    driver.find_element_by_xpath('//*[@id="codetext"]').send_keys(code)

                cardId = self.repo.GetMaterial( "356", 0, 1 )
                if len( address ) == 0:
                    address = self.repo.GetMaterial( "356", 0, 1 )
                    if len( address ) == 0:
                        print u"%s号仓库为空，没有取到消息" % "356"
                        time.sleep( 100 )
                        return
                name = address[0]['name']  #
                if name is None or name == "":
                    cards = address[0]['content'].encode( "utf-8" ).spilt( "----" )  # 市
                    if len( cards ) == 2:
                        name = cards[0]
                        cardId = cards[1]
                else:
                    cardId = address[0]['content'].encode( "utf-8" )

                driver.find_element_by_xpath('//*[@id="js-submitSucWrap"]/div/div/div/div/div/div[3]/a/span').click()
                driver.find_element_by_xpath('//*[@id="domain_try"]/p[1]/a').click()
                driver.find_element_by_xpath('//*[@id="nickname"]').send_keys(name)
                driver.find_element_by_xpath( '//*[@id="id_code"]' ).send_keys( cardId )
                driver.find_element_by_xpath('//*[@id="info"]').click()
                driver.find_element_by_xpath('//*[@id="apply_form"]/table/tbody/tr[5]/td[2]/input').click()

                myuser = "cfs"
                pwd = "d"
                self.repo.RegisterAccount( myuser, pwd, "", "dsa")
                flag1 = True
                flag2 = True
                flag3 = True



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
    return HaiNanMail_Register

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()

    while True:
        try:
            o.action()
        except Exception,e:
            print e