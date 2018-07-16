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


class EmailInternet_Chrome:
    def __init__(self):

        self.repo = Repo( )
        # self.ipChange = IPChange()

    def delete(self):
        path = "C:\Users\Administrator\AppData\Local\Temp"
        g = os.listdir( path )
        import shutil
        for i in g:
            x = path + "\\%s" % i
            try:
                shutil.rmtree( x )
            except:
                pass

    def updateNumberStatus(self, emailnumber, repo_number_cate_id):
        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
            emailnumber, repo_number_cate_id, "normal")
        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
        conn.request( "GET", path )
        time.sleep( 3 )

    def updateAccountStatus(self, repo_cate_id, account, status):
        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
            repo_cate_id, status, account, "", "")
        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
        conn.request( "GET", path )
        time.sleep( 3 )

    def lockAccount(self, account, repo_cate_id, QQType):
        path = "/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
            account, repo_cate_id, QQType)
        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
        conn.request( "GET", path )
        time.sleep( 3 )

    def GetUnique(self):
        num = ""
        for i in range( 0, random.randint( 1, 8 ) ):
            n = random.choice( "qwertyuiopasdfghjklzxcvbnm" )
            num = n + num
        for i in range( 0, random.randint( 1, 5 ) ):
            n = random.choice( "0123456789" )
            num = num + n

        return num

    def getImg(self, driver):
        imgName = self.GetUnique( )
        # imgpath = r"C:\PIC"
        imgpath = "/home/zunyun/text/img"
        if not os.path.exists( imgpath ):
            return
        g = os.listdir( imgpath )

        for i in g:
            name = i.split( "." )
            os.rename( imgpath + "/%s" % i, imgpath + "/%s.%s" % (imgName, name[1]) )
            imgpath = imgpath + "/%s.%s" % (imgName, name[1])
            # os.rename(imgpath + "\%s" % i, imgpath + "\%s.%s" % (imgName, name[1]))
            # imgpath = imgpath + "\%s.%s" % (imgName,name[1])
            try:
                driver.find_element_by_xpath( '//*[@id="attachUpload"]/a/input' ).send_keys( imgpath )
                time.sleep( 2 )
                return
            except:
                pass

        return imgpath

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
                    "user_agent_id": user_agent_id, "phonenumber": phonenumber, "cateId": cateId,
                    "my_userCount": my_userCount, "bccCount": bccCount}  # cate_id是仓库号，length是数量
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
                args = self.getArgs( )
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
                numbers = self.repo.GetAccount( "normal", repo_cate_id, 0, 1 )
                if len( numbers ) == 0:
                    print u"%s号仓库没有数据" % repo_cate_id
                    time.sleep( 300 )
                    try:
                        driver.close( )
                        driver.quit( )
                    except:
                        pass
                    return
                QQNumber = numbers[0]['number']  # 即将登陆的QQ号
                QQPassword = numbers[0]['password']
                # user_agent = numbers[0]['imei']
                user_agent = ""
                if user_agent is None or user_agent == '':
                    user_agentList = self.repo.GetMaterial( user_agent_id, 0, 1 )
                    if len( user_agentList ) == 0:
                        print u"%s号仓库为空，没有取到消息" % user_agent_id
                        try:
                            driver.close( )
                            driver.quit( )
                        except:
                            pass
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
                # user_agent = "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
                # user_agent = "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;"
                # cap["phantomjs.page.settings.userAgent"] = user_agent
                # cap["phantomjs.page.customHeaders.User-Agent"] = user_agent
                # driver = webdriver.PhantomJS( desired_capabilities=cap,
                #                               executable_path=r"/usr/local/phantomjs/bin/phantomjs" )
                time.sleep( 2 )
                options = webdriver.ChromeOptions( )
                options.add_argument( 'disable-infobars' )
                options.add_argument( 'lang=zh_CN.UTF-8' )
                # options.add_argument( 'headless' )
                # 更换头部
                # options.add_argument(user_agent)
                options.add_argument( 'user-agent="%s' % user_agent )
                try:
                    driver = webdriver.Chrome( chrome_options=options,
                                               executable_path="/opt/google/chrome/chromedriver" )
                except:
                    if not os.path.exists( "C:\Users\Administrator\AppData\Local\Temp" ):
                        os.mkdir( "C:\Users\Administrator\AppData\Local\Temp" )


                # 检查是否连接网络
                # driver.get("https://www.baidu.com/")
                # if "百度一下" in driver.page_source.encode("utf-8"):
                #     print "Internet OK"
                # else:
                #     print "Internet NO"
                #     return

                # 打开QQ邮箱登陆界面
                driver.delete_all_cookies( )
                driver.get( r'https://mail.qq.com/' )
                time.sleep( 3 )
                try:
                    driver.switch_to_frame( 'login_frame' )  # 需先跳转到iframe框架
                except:
                    driver.get( r'https://mail.qq.com/' )
                    time.sleep( 3 )
                    try:
                        driver.switch_to_frame( 'login_frame' )  # 需先跳转到iframe框架
                    except:
                        print u"https://mail.qq.com/ 不支持手机版头信息"
                        time.sleep( 100 )
                        return
                # driver.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
                time.sleep( 1 )

                try:
                    # 若帐号输入框有内容先清空
                    driver.find_element_by_id( "u" ).clear( )
                    driver.find_element_by_id( "p" ).clear( )
                except:
                    pass
                try:
                    # ///
                    # 输入框输入帐号和密码
                    # account = "2351382894"
                    # password = "wuzhou455854284"
                    driver.find_element_by_id( "u" ).send_keys( QQNumber )
                    driver.find_element_by_id( "p" ).send_keys( QQPassword )
                    # driver.save_screenshot( "222.png" )
                    time.sleep( 0.5 )
                    driver.find_element_by_id( "p" ).send_keys( Keys.ENTER )
                    time.sleep( random.randint( time_delayStart, time_delayEnd ) )
                except:
                    pass

                try:
                    driver.find_element_by_xpath( '//*[@id="composebtn"]' )
                    print u"%s  登陆成功" % QQNumber
                    # Repo( ).BackupInfo( repo_cate_id, 'normal', QQNumber, user_agent, '' )
                    startUrl = driver.current_url
                except:
                    print u"%s  登陆失败" % QQNumber
                    driver.save_screenshot( "002.png" )
                    time.sleep( 2 )
                    # 登陆出现异常状况
                    errorPage = driver.page_source.encode( "utf-8" )

                    if "拖动下方滑块完成拼图" in errorPage:
                        print u"%s  拖动下方滑块完成拼图" % QQNumber
                    elif "帐号或密码不正确" in errorPage:
                        print u"%s  帐号或密码不正确" % QQNumber
                    elif "你的帐号存在安全隐患" in errorPage:
                        print u"你的帐号存在安全隐患"
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "frozen", QQNumber, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    elif "冻结" in errorPage:
                        print u"%s  冻结" % QQNumber
                        # self.repo.BackupInfo(repo_cate_id, 'frozen', QQNumber, '', '')
                        # driver.get(
                        #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #         repo_cate_id, "frozen", QQNumber, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "frozen", QQNumber, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )

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
                    continue

                url = driver.current_url.encode( "utf-8" )
                sid = url.split( "sid=" )[1].split( "&" )[0]
                # for i in range(0,10):
                #     if driver.current_url == url:
                #         time.sleep(2)
                #         print "mei jin qu"
                #         try:
                #             driver.refresh()
                #         except:
                #             pass
                # else:
                #     continue

                driver.find_element_by_xpath( '//*[@id="folder_card"]' ).click( )
                driver.switch_to_frame('mainFrame')
                time.sleep(1)

                xpath = ["",'//*[@id="tab_yy"]/a','//*[@id="tab_aq"]/a','//*[@id="tab_zf"]/a','//*[@id="tab_sr"]/a','//*[@id="tab_jr"]/a']
                for path in xpath:
                    if path !="":
                        driver.find_element_by_xpath(path).click()
                    cards2 = driver.find_elements_by_xpath( '//*[@class="pic"]/a' )
                    for card in cards2:
                        print card.get_attribute( "cardid" )
                    if path == '//*[@id="tab_jr"]/a':
                        a = 9
                    elif path == "":
                        a = 0
                    else:
                        a = 1
                    if a>0:
                        for i in range(0,a):
                            time.sleep(2)
                            cards2 = driver.find_elements_by_xpath( '//*[@class="pic"]/a' )
                            for card in cards2:
                                print card.get_attribute( "cardid" )
                # # #漂流瓶
                # for i in range(0,6):
                #     driver.find_element_by_xpath('/html/body/div/section[1]/div/ul/li[4]/a/span[2]/span[1]').click()
                #     driver.find_element_by_xpath('//*[@id="ct"]/div[2]/a[1]/span[1]').click()
                #     driver.find_element_by_xpath('//*[@id="bottlelist"]/ul/li[1]/a/div/span').click()
                #     driver.find_element_by_xpath('//*[@id="multy_select"]').click()
                #     driver.find_element_by_xpath('//*[@id="multy_select"]').send_keys(Keys.SHIFT, Keys.TAB, Keys.SHIFT,message2)
                #     driver.find_element_by_xpath( '//*[@id="multy_select"]' ).click( )
                #     driver.find_element_by_xpath('//*[@id="postform"]/div[2]/div/div[3]/div/div/input').click()
                #     if "您的漂流瓶已漂向大海！" in driver.page_source.encode("utf-8"):
                #         continue
                #     else:
                #         break

                import shutil
                deletepath = "C:\Users\Administrator\AppData\Local\Temp"
                # shutil.rmtree(deletepath)
                try:
                    g = os.walk( deletepath )
                    for path, d, filelist in g:
                        try:
                            shutil.rmtree( path )
                        except:
                            pass
                except:
                    pass
        except Exception, e:
            print e
            command = 'taskkill /F /IM chromedriver.exe'
            os.system( command )
            try:
                driver.close( )
                driver.quit( )
            except:
                pass
            self.delete( )
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
        self.delete( )
        args = self.getArgs( )
        phonenumber = args["phonenumber"]
        cateId = args["cateId"]
        para = {"phoneNumber": phonenumber, "x_04": sta}
        self.repo.PostInformation( cateId, para )


def getPluginClass():
    return EmailInternet_Chrome


if __name__ == "__main__":

    reload( sys )
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass( )
    o = clazz( )
    # o.delete()
    # time.sleep(150)
    while True:
        try:
            o.action( )
        except Exception, e:
            print e




