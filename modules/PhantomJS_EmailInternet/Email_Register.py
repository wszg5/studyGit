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
class Email_Register:
    def __init__(self):
        self.repo = Repo()
        # self.ipChange = IPChange()
        self.type = 'yixin'

    def getImgCode(self,driver):
        img = driver.find_element_by_xpath(
            '//*[@id="js-mobileSettingWrap"]/div/form/div/div[1]/div[2]/div/div/div/span/img' )
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

                    driver.get( "http://app.ym.163.com/ym/reg/view/index#" )
                    # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled')
                    time.sleep( 3 )
                    ym_cate_id = args["ym_cate_id"]
                    organization_cate_id = args["organization_cate_id"]
                    address_cate_id = args["address_cate_id"]
                    username_cate_id = args["username_cate_id"]
                    manageAccount_cate_id = args["manageAccount_cate_id"]
                    mail_cate_id = args["mail_cate_id"]
                    ymMail_cate_id = args["ymMail_cate_id"]
                    xunma_itemId = args["xunma_itemId"]
                    ym_zlk_Id = args["ym_zlk_Id"]
                    scaleCount = args["scaleCount"]
                    cardId_id = args["cardId_id"]
                    flag1 = False
                if flag2:
                    ym = self.repo.GetNumber( ym_cate_id, 0, 1 )  # 取出add_count条两小时内没有用过的号码
                    for i in range(0,5):
                        if len( ym ) == 0:
                            print u"%s号仓库没有数据" % ym_cate_id
                            time.sleep( 60 )
                            ym = self.repo.GetNumber( ym_cate_id, 0, 1 )
                        else:
                            ym = ym[0]["number"]
                            print u"要注册的域名为%s"%ym
                            break
                    else:
                        print u"仓库没有数据请尽快处理"
                        return
                    driver.find_element_by_xpath('//*[@id="js-domainSettingWrap"]/div/form/div/div[1]/div[2]/div/div[1]/div/input').send_keys(ym)
                    driver.find_element_by_xpath('//*[@id="js-domainSettingWrap"]/div/form/div/div[2]/div[2]/div/div[1]/div/input').click()
                    if '该域名已经注册了域名邮' in driver.page_source.encode("utf-8"):
                        print u"该域名已经注册了域名邮"
                        driver.find_element_by_xpath(
                            '//*[@id="js-domainSettingWrap"]/div/form/div/div[1]/div[2]/div/div[1]/div/input' ).clear()
                        continue
                    elif '系统黑名单' in driver.page_source:
                        print u"该域名在系统黑名单中"
                        driver.find_element_by_xpath('//*[@id="js-domainSettingWrap"]/div/form/div/div[1]/div[2]/div/div[1]/div/input' ).clear( )
                        continue
                    elif '域名格式错误' in driver.page_source:
                        print u"域名格式错误"
                        driver.find_element_by_xpath('//*[@id="js-domainSettingWrap"]/div/form/div/div[1]/div[2]/div/div[1]/div/input' ).clear( )
                        continue

                    organization = self.repo.GetMaterial( organization_cate_id, 0, 1 )
                    if len( organization ) == 0:
                        organization = self.repo.GetMaterial( organization_cate_id, 0, 1 )
                        if len( organization ) == 0:
                            print u"%s号仓库为空，没有取到消息" % organization_cate_id
                            time.sleep( 100 )
                            return
                    organization = organization[0]['content']

                    address = self.repo.GetMaterial( address_cate_id, 0, 1 )
                    if len( address ) == 0:
                        address = self.repo.GetMaterial( address_cate_id, 0, 1 )
                        if len( address ) == 0:
                            print u"%s号仓库为空，没有取到消息" % address_cate_id
                            time.sleep( 100 )
                            return
                    address1 = address[0]['name']  #省
                    address2 = address[0]['content']  #市
                    driver.find_element_by_xpath(
                        '//*[@id="js-domainSettingWrap"]/div/form/div/div[2]/div[2]/div/div[1]/div/input' ).send_keys(organization )

                    driver.find_element_by_xpath('//*[@id="js-domainSettingWrap"]/div/form/div/div[3]/div[2]/div/div[1]/a/span').click()
                    obj = driver.find_elements_by_class_name('item-value')
                    for item in obj:
                        if item.text==address1:
                            item.click()
                            break
                    else:
                        obj[random.randint( 0, 33 )].click( )
                    driver.find_element_by_xpath('//*[@id="js-domainSettingWrap"]/div/form/div/div[3]/div[2]/div/div[2]/a/span' ).click( )
                    obj2 = driver.find_elements_by_class_name( 'item-value' )
                    for item2 in obj2:
                        if item2.text==address2:
                            item2.click()
                            break
                    else:
                        obj2[34].click( )

                    address = self.repo.GetMaterial( scaleCount, 0, 1 )
                    if len( address ) == 0:
                        address = self.repo.GetMaterial( scaleCount, 0, 1 )
                        if len( address ) == 0:
                            print u"%s号仓库为空，没有取到消息" % scaleCount
                            time.sleep( 100 )
                            return
                    scale = address[0]['name']  # 类型
                    count = address[0]['content']  # 规模
                    driver.find_element_by_xpath('//*[@id="js-domainSettingWrap"]/div/form/div/div[4]/div[2]/div/a/span').click()
                    obj3 = driver.find_elements_by_class_name( 'item-value' )
                    for item3 in obj3:
                        if item3.text==scale:
                            item3.click()
                            break
                    driver.find_element_by_xpath(
                        '//*[@id="js-domainSettingWrap"]/div/form/div/div[5]/div[2]/div/a/span' ).click( )
                    obj4 = driver.find_elements_by_class_name( 'item-value' )
                    for item4 in obj4:
                        if item4.text == count:
                            item4.click( )
                            break


                    driver.find_element_by_xpath('//*[@id="js-domainSettingWrap"]/div/form/div/div[6]/div[2]/div[1]/a/span').click()
                    time.sleep(2)

                    username = self.repo.GetMaterial( username_cate_id, 0, 1 )
                    if len( username ) == 0:
                        username = self.repo.GetMaterial( username_cate_id, 0, 1 )
                        if len( username ) == 0:
                            print u"%s号仓库为空，没有取到消息" % username_cate_id
                            time.sleep( 100 )
                            return
                    username = username[0]['content']
                    driver.find_element_by_xpath('//*[@id="js-adminSettingWrap"]/div/form/div/div[1]/div[2]/div[2]/div/div[1]/div/input').send_keys(username)

                    manageAccount = self.repo.GetMaterial( manageAccount_cate_id, 0, 1 )
                    if len( manageAccount ) == 0:
                        manageAccount = self.repo.GetMaterial( manageAccount_cate_id, 0, 1 )
                        if len( manageAccount ) == 0:
                            print u"%s号仓库为空，没有取到消息" % manageAccount_cate_id
                            time.sleep( 100 )
                            return
                    manageAccount = manageAccount[0]['content']

                    driver.find_element_by_xpath('//*[@id="js-adminSettingWrap"]/div/form/div/div[1]/div[3]/div[2]/div[1]/div[1]/div/input').send_keys(manageAccount)
                    passwprd = "13141314Abc"
                    driver.find_element_by_xpath('//*[@id="js-adminSettingWrap"]/div/form/div/div[1]/div[4]/div[2]/div/div[1]/div/input').send_keys(passwprd)
                    driver.find_element_by_xpath('//*[@id="js-adminSettingWrap"]/div/form/div/div[1]/div[5]/div[2]/div/div[1]/div/input').send_keys(passwprd)
                    flag2 = False
                if flag3:
                    token = self.GetToken( )
                    flag3 = False
                for i in range( 0, 12 ):
                    phone = self.GetPhoneNumber( xunma_itemId, token )
                    if phone is None or phone == '' or phone == []:
                        continue
                    elif phone=="False":
                        flag3 = True
                        break
                    else:
                        print phone
                        break
                else:
                    print u"没有获取到手机号"
                    continue
                if flag3:
                    continue
                driver.find_element_by_xpath('//*[@id="js-adminSettingWrap"]/div/form/div/div[2]/div[2]/div[2]/div/div[1]/div/input').send_keys(phone)
                mailNumbers = self.repo.GetAccount( "normal",mail_cate_id, 90, 1 )
                if len( mailNumbers ) == 0:
                    mailNumbers = self.repo.GetAccount( "normal", mail_cate_id, 90, 1 )
                    if len( mailNumbers ) == 0:
                        print u"%s号仓库没有数据,等待5分钟" % mail_cate_id
                        time.sleep( 300 )
                        return
                account = mailNumbers[0]['number']
                if "@" not in account:
                    account = account + "@qq.com"
                driver.find_element_by_xpath('//*[@id="js-adminSettingWrap"]/div/form/div/div[2]/div[3]/div[2]/div/div[1]/div/input').send_keys(account)
                driver.find_element_by_xpath('//*[@id="js-adminSettingWrap"]/div/form/div/div[3]/div[2]/div/div[2]/a/span').click()
                time.sleep(2)

                for i in range(0,15):
                    imgcode = self.getImgCode(driver)
                    driver.find_element_by_xpath('//*[@id="js-mobileSettingWrap"]/div/form/div/div[2]/div[2]/div/div[1]/div/input').send_keys(imgcode)
                    driver.find_element_by_xpath('//*[@id="js-mobileSettingWrap"]/div/form/div/div[3]/div[2]/div[2]/a[1]/span').click()
                    time.sleep(1)
                    if "请输入图形验证码" in driver.page_source or "请输入图形验证码" in driver.page_source and "免费获取验证码(" not in driver.page_source :
                        print u"图片验证码错误或未输入"
                        driver.find_element_by_xpath('//*[@id="js-mobileSettingWrap"]/div/form/div/div[2]/div[2]/div/div[1]/div/input' ).clear()
                    else:
                        break
                else:
                    print u"图片验证码输入错误15次,本次注册失败，重新注册"
                    return

                if "一分钟只允许发送一次验证码" in driver.page_source:
                    print u"一分钟只允许发送一次验证码"
                    try:
                        driver.close()
                        driver.quit()
                    except:
                        pass
                    return
                for i in range( 0, 12 ):
                    code = self.GetCode( token, phone,xunma_itemId )
                    if code is None or code == '' or code == []:
                        continue
                    elif code=="False":
                        flag3 = True
                        break
                    else:
                        print code
                        break
                else:
                    print u"没有获取到验证码"
                    driver.find_element_by_xpath('//*[@id="js-mobileSettingWrap"]/div/form/div/div[5]/div[2]/div/div[1]/a/span').click()
                    driver.find_element_by_xpath(
                        '//*[@id="js-adminSettingWrap"]/div/form/div/div[2]/div[2]/div[2]/div/div[1]/div/input' ).clear()
                    continue
                if flag3:
                    continue
                driver.find_element_by_xpath('//*[@id="js-mobileSettingWrap"]/div/form/div/div[4]/div[2]/div/div[1]/div/input').send_keys(code)
                driver.find_element_by_xpath('//*[@id="js-mobileSettingWrap"]/div/form/div/div[5]/div[2]/div/div[2]/a/span').click()
                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="js-mxSettingWrap"]/div/div[4]/div[2]/a/span').click()
                if "管理帐号注册成功" in driver.page_source:
                    print u"管理帐号注册成功"

                driver.get( r'https://qiye.163.com/login/?from=ym' )
                time.sleep( 2 )
                myuser = manageAccount + "@" + ym
                cardId = self.repo.GetMaterial( cardId_id, 0, 1 )
                if len( address ) == 0:
                    address = self.repo.GetMaterial( address_cate_id, 0, 1 )
                    if len( address ) == 0:
                        print u"%s号仓库为空，没有取到消息" % address_cate_id
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

                try:
                    # 若帐号输入框有内容先清空
                    driver.find_element_by_id( "accname" ).clear( )
                    driver.find_element_by_id( "accpwd" ).clear( )
                except:
                    pass
                try:
                    # ///
                    # 输入框输入帐号和密码
                    # account = "02@vip.800130188.com"
                    # password = "13141314abc"
                    driver.find_element_by_id( "accname" ).send_keys( myuser )
                    driver.find_element_by_id( "accpwd" ).send_keys( passwprd )
                    # driver.save_screenshot( "222.png" )
                    time.sleep( 0.5 )
                    driver.find_element_by_id( "accpwd" ).send_keys( Keys.ENTER )
                    time.sleep( random.randint( 2, 4 ) )
                except:
                    pass

                if driver.current_url != "https://qiye.163.com/login/?from=ym":
                    # driver.find_element_by_xpath( '//*[@id="nav-mbox"]/div[1]/a[1]/div' )   #网易的logo

                    print u"%s  登陆成功" % account
                    # Repo( ).BackupInfo( repo_cate_id, 'normal', QQNumber, user_agent, '' )
                    startUrl = driver.current_url
                else:
                    print u"%s  登陆失败" % account

                #实名认证
                driver.find_element_by_xpath('//*[@id="js-submitSucWrap"]/div/div/div/div/div/div[3]/a/span').click()

                driver.find_element_by_xpath('//*[@id="domain_try"]/p[1]/a').click()
                driver.find_element_by_xpath('//*[@id="nickname"]').send_keys(name)
                driver.find_element_by_xpath( '//*[@id="id_code"]' ).send_keys( cardId )
                driver.find_element_by_xpath('//*[@id="info"]').click()
                driver.find_element_by_xpath('//*[@id="apply_form"]/table/tbody/tr[5]/td[2]/input').click()


                self.repo.RegisterAccount( myuser, passwprd, "", ymMail_cate_id)
                flag1 = True
                flag2 = True
                flag3 = True


                para = {"phoneNumber": myuser, 'x_01': "13141314Abc",
                        'x_03': organization, 'x_04': address1+address2, 'x_05': scale+count, 'x_06': "管理员姓名"+username,
                        'x_07': "管理帐号"+manageAccount, 'x_08': account,"x_09":name+cardId
                        }
                self.repo.PostInformation( ym_zlk_Id, para )
                #拨号
                pass

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
    return Email_Register

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