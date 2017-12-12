# coding:utf-8
from __future__ import division
import base64
import logging
import re
import urllib2

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs

from Repo import *
import os, time, datetime, random
import json

from zcache import cache
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains


class EmailInternet:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum



    def action(self, args):
        exit_code = os.system('ping www.baidu.com')
        if exit_code:
            print "网络不通"
            return
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = True
        cap["phantomjs.page.settings.disk-cache"] = True

        cap[
            "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0"

        cap[
            "phantomjs.page.customHeaders.User-Agent"] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0'
        driver = webdriver.PhantomJS( desired_capabilities=cap )
        count = int(args["count"])
        selectContent = args["selectContent"]
        emailType = args["emailType"]
        repo_material_cateId2 = args["repo_material_cateId2"]
        repo_material_cateId = args["repo_material_cateId"]
        sendCount = int(args["sendCount"])
        repo_cookies_id = args["repo_cookies_id"]

        for i in range(0,count):
            repo_cate_id = args["repo_cate_id"]
            time_limit1 = args['time_limit1']
            numbers = self.repo.GetAccount(repo_cate_id, time_limit1, 1)
            while len( numbers ) == 0:
                print "%s号仓库没有数据"%repo_cate_id
                return

            QQNumber = numbers[0]['number']  # 即将登陆的QQ号
            QQPassword = numbers[0]['password']
            para = {"x_key": "x_01", "x_value": QQNumber}
            totalList = Repo( ).GetTIMInfomation( repo_cookies_id, para )
            if len(totalList)==0:
                driver.get( "https://w.mail.qq.com/" )
            else:
                total = None
                for i in totalList:
                    if i["x_01"]==QQNumber:
                        total = i
                        break
                if not total is None:
                    geturl = totalList["x02"]
                    getcookie = totalList["phonenumber"]
                    driver.get( geturl )
                    time.sleep(2)
                    driver.add_cookie(getcookie)
                    driver.get( geturl )
                else:
                    driver.get( "https://w.mail.qq.com/" )
            # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled')
            time.sleep(3)
            # driver.save_screenshot( "xxx.png" )
            # # driver.close()
            # # driver.quit()
            #
            # cookie ={'domain': '.mail.qq.com', 'name': 'mpwd', 'expires': '\u5468\u4e09, 10 1\u6708 2018 09:23:39 GMT', 'value': '76B5754E4B5F180625366E729727C115A4084636BACFF7C8264C3BE4A5326BEF@2564855064@4',
            #          'expiry': 1515576219, 'path': '/', 'httponly': False, 'secure': False}
            # driver.add_cookie(cookie)
            # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled' )


            # print  driver.page_source
            # print driver.get_cookies()
            # print driver.current_url
            # print driver.title
            # cap_dict = driver.desired_capabilities
            # for key in cap_dict:
            #     print '%s: %s' % (key, cap_dict[key])

            # obj = driver.find_element_by_id('del_u')

            driver.save_screenshot( "111.png" )
            try:
                driver.find_element_by_id( "u" ).clear()

            except:
                pass
            try:
                #///
                driver.find_element_by_id( "u" ).send_keys( "2795657252" )
                driver.find_element_by_id( "p" ).send_keys( "pckl5225" )
                driver.save_screenshot( "222.png" )
                time.sleep(1)
                # driver.find_element_by_id( "p" ).send_keys( "444444444" )
                driver.find_element_by_id( "go" ).click( )
                time.sleep( 4 )
            except:
                pass
            while True:
                try:
                    driver.find_element_by_id( "go" ).click( )
                except:
                    break

            driver.save_screenshot( "333.png" )

            try:
                obj = driver.find_element_by_class_name( "qm_btnIcon" )

            except:
                time.sleep(2)
                errorPage = driver.page_source.encode("utf-8")
                if "拖动下方滑块完成拼图" in errorPage:
                    pass
                if "你输入的帐号或密码不正确，请重新输入。" in errorPage:
                    self.repo.BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )
                try:
                    obj = driver.find_element_by_class_name("content")
                    driver.save_screenshot("aaa.png")

                    self.repo.BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )
                except:
                    time.sleep(2)
                    driver.save_screenshot( "bbb.png" )
                continue


            getCoolies = driver.get_cookies( )
            url = driver.current_url
            value = ''
            name = ''
            cookie = None
            for item in getCoolies:
                # key = self.get_keys(item,QQNumber.encode("utf-8"))
                # for v in item:
                #     if QQNumber.encode("utf-8") in v["value"].encode("utf-8"):
                #
                if QQNumber.encode( "utf-8" ) in item["value"].encode( "Utf-8" ):
                    value = item["value"].encode( "Utf-8" )
                    name = item["name"]
                    cookie = item
                    break
            if cookie!=None:
                para = {"phoneNumber": cookie, 'x_01': QQNumber,"x_02":url}
                self.repo.PostInformation( repo_cookies_id, para )

            obj.click( )
            driver.save_screenshot( "444.png" )
            flag = True
            while flag:
                repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
                emailnumbers = self.repo.GetNumber( repo_number_cate_id, 0, sendCount )  # 取出add_count条两小时内没有用过的号码
                if len( emailnumbers ) == 0:
                    print "QQ号码库%s号仓库为空"%repo_number_cate_id
                    return
                # emailnumber = emailnumbers[0]['number']

                Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                if len( Material ) == 0:
                    print "%s号仓库为空，没有取到消息"%repo_material_cateId
                    return
                message = Material[0]['content']

                Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                if len( Material2 ) == 0:
                    print "%s号仓库为空，没有取到消息" % repo_material_cateId
                    return
                message2 = Material2[0]['content']

                # driver.find_element_by_id("showto").send_keys(emailnumber)
                for i in range( 0, sendCount ):
                    if i<len(emailnumbers):
                        emailnumber = emailnumbers[i]['number']
                        # QQEmail = numbers[i]['number'].encode( "utf-8" )
                        if emailType=="QQ邮箱":
                            driver.find_element_by_id( "showto" ).send_keys( emailnumber + "@qq.com " )
                            driver.find_element_by_id( "subject" ).click()
                        elif emailType=="189邮箱":
                            driver.find_element_by_id( "showto" ).send_keys( emailnumber + "@189.cn " )
                            driver.find_element_by_id( "subject" ).click( )
                        else:
                            driver.find_element_by_id( "showto" ).send_keys( emailnumber + "@qq.com " )
                            driver.find_element_by_id( "subject" ).click( )
                # driver.find_element_by_id( "showto" ).send_keys( "455854284" + "@qq.com " )
                if selectContent == "只发主题" or selectContent == "主题内容都发":
                    driver.find_element_by_id("subject").send_keys(message)
                if selectContent == "只发内容" or selectContent == "主题内容都发":
                    driver.find_element_by_id("content").send_keys(message2)
                time.sleep(3)
                driver.save_screenshot( "555.png" )

                obj = driver.find_element_by_name("RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__")
                obj.click()
                time.sleep(3)
                driver.save_screenshot("666.png" )
                page_source = driver.page_source
                if "发送成功" in page_source:
                    print "发送成功"
                elif "邮件中可能包含不合适的用语或内容" in page_source:
                    flag = False
                    print "邮件中可能包含不合适的用语或内容"
                    driver.save_screenshot( "%s%s.png" % (QQNumber, self.GetUnique( )) )
                elif "<html><head></head><body></body></html>":
                    flag = False
                    print "空"
                else:
                    flag = False
                    print page_source
                    driver.save_screenshot( "%s%s.png" % (QQNumber, self.GetUnique( )) )
                    print "error"
                # print  page_source
                page_source = driver.page_source.encode('utf-8')
                driver.get( url )
                if flag:
                    try:
                        driver.find_element_by_class_name( "qm_btnIcon" ).click()
                    except:
                        pass
                else:
                    try:
                        driver.find_element_by_link_text("退出").click()
                        time.sleep(2)
                        driver.save_screenshot("exit.png")
                    except:
                        print "error"
                        driver.save_screenshot( "exit2.png" )

        driver.quit( )

def getPluginClass():
    return EmailInternet

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()

    # d = Device("d99e4b99")
    # z = ZDevice("d99e4b99")

    args = {"time_delay":"3","time_limit1":"60","count":"10","repo_cate_id":"287","repo_number_cate_id":"119","repo_material_cateId": "255",
            "repo_material_cateId2":"255","selectContent":"主题内容都发","emailType":"QQ邮箱","sendCount":"5","repo_cookies_id":"286"}    #cate_id是仓库号，length是数量
    o.action( args )
