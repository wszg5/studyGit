# coding:utf-8
from __future__ import division
import base64
import logging
import re
import socket
import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs


import os, time, datetime, random
import json





class Baidu:
    def __init__(self):
        # Repo() = Repo()
        pass
    # def GetUnique(self):
    #     nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
    #     randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
    #     if randomNum <= 10:
    #         randomNum = str(00) + str(randomNum);
    #     uniqueNum = str(nowTime) + str(randomNum);
    #     return uniqueNum

    def action(self, args):
        while True:
            user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Mobile Safari/537.36"
            print user_agent
            cap = webdriver.DesiredCapabilities.PHANTOMJS
            cap["phantomjs.page.settings.resourceTimeout"] = 1000
            cap["phantomjs.page.settings.loadImages"] = True
            cap["phantomjs.page.settings.disk-cache"] = True
            cap["phantomjs.page.settings.userAgent"] = user_agent

            cap["phantomjs.page.customHeaders.User-Agent"] = user_agent
            driver = webdriver.PhantomJS( desired_capabilities=cap,executable_path="/usr/local/phantomjs/bin/phantomjs" )

            #访问邮箱
            # driver.get( "https://w.mail.qq.com/" )

            driver.get( "https://www.baidu.com/" )
            # driver.execute_script( "window.location.href='http://www.baidu.com';" )
            time.sleep( 3 )
            print driver.current_url
            print driver.page_source
            driver.save_screenshot("0.png")
            # 点 进入网页版QQ邮箱 (模拟手机版会有这个)
            try:
                obj = driver.find_element_by_xpath( "//td[@class='enter_mail_button_td']/a" )
                obj.click( )

            except:
                print "error"

            driver.save_screenshot( "111.png" )
            try:
                # 若帐号输入框有内容先清空
                driver.find_element_by_id( "u" ).clear( )
            except:
                pass

            driver.get( "https://www.baidu.com" )
            driver.save_screenshot("2.png")
            if "百度一下" in driver.page_source.encode("utf-8"):
                driver.save_screenshot("baidu.png")
            else:
                # print "网络不通"
                driver.save_screenshot("baidu2.png")
                driver.quit( )
                return

            obj = driver.find_element_by_id("kw")
            obj.send_keys("java")
            driver.find_element_by_id( "su" ).click()
            driver.save_screenshot("1.png")




        driver.quit( )

def getPluginClass():
    return Baidu

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()

    # print taskList
    # print paramList
    args = {"user_agent_id":"292"}    #cate_id是仓库号，length是数量
    o.action( args )

    #拨号换ip
    # a = os.system("echo 1 | sudo -S poff")
    # print a
    # b = os.system("echo 1 | sudo -S pon dsl-provider")
    # print b