# coding:utf-8
from __future__ import division
import base64
import logging
import re
import socket
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

        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = True
        cap["phantomjs.page.settings.disk-cache"] = True

        cap[
            "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0"

        cap[
            "phantomjs.page.customHeaders.User-Agent"] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0'
        driver = webdriver.PhantomJS( desired_capabilities=cap )
        # driver.close()
        # driver.quit( )
        #检查是否连接网络
        driver.get( "https://www.baidu.com/" )
        if "百度一下" in driver.page_source.encode("utf-8"):
            print "网络通畅"
        else:
            print "网络不通"
            return

        driver.save_screenshot( "5.png" )
        count = int(args["count"])
        selectContent = args["selectContent"]
        emailType = args["emailType"]
        repo_material_cateId2 = args["repo_material_cateId2"]
        repo_material_cateId = args["repo_material_cateId"]
        # sendCount = int(args["sendCount"])
        repo_cookies_id = args["repo_cookies_id"]

        for i in range(0,count):
            repo_cate_id = args["repo_cate_id"]
            time_limit1 = args['time_limit1']
            numbers = self.repo.GetAccount( repo_cate_id, time_limit1, 1 )
            while len( numbers ) == 0:
                print "%s号仓库没有数据" % repo_cate_id
                return

            QQNumber = numbers[0]['number']  # 即将登陆的QQ号
            QQPassword = numbers[0]['password']
            # QQNumber = "2179298964"
            # QQPassword = "sbkl2225"
            # para = {"x_key": "x_01", "x_value": QQNumber}
            # totalList = Repo( ).GetTIMInfomation( repo_cookies_id, para )
            # if len(totalList)==0:
            #     driver.get( "https://w.mail.qq.com/" )
            # else:
            #     total = None
            #     for i in totalList:
            #         if i["x_01"]==QQNumber:
            #             total = i
            #             break
            #     if not total is None:
            #         geturl = totalList["x02"]
            #         getcookie = totalList["phonenumber"]
            #         driver.get( geturl )
            #         time.sleep(2)
            #         driver.add_cookie(getcookie)
            #         driver.get( geturl )
            #     else:
            #         driver.get( "https://w.mail.qq.com/" )
            # 打开QQ邮箱登陆界面
            driver.get( "https://w.mail.qq.com/" )
            # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled')
            time.sleep( 3 )

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

            # driver.save_screenshot( "111.png" )
            try:
                # 若帐号输入框有内容先清空
                driver.find_element_by_id( "u" ).clear( )

            except:
                pass
            try:
                # ///
                # 输入框输入帐号和密码
                driver.find_element_by_id( "u" ).send_keys( QQNumber )
                driver.find_element_by_id( "p" ).send_keys( QQPassword )
                driver.save_screenshot( "222.png" )
                time.sleep( 1 )
                # driver.find_element_by_id( "p" ).send_keys( "444444444" )
                driver.find_element_by_id( "go" ).click( )
                time.sleep( 4 )
            except:
                pass
            while True:
                try:
                    # 点击登陆
                    driver.find_element_by_id( "go" ).click( )
                except:
                    break

            driver.save_screenshot( "333.png" )

            try:
                # 防止登陆点击一次没结果
                obj = driver.find_element_by_class_name( "qm_btnIcon" )
                print "登陆成功"

            except:
                print "登陆失败"
                time.sleep( 2 )
                # 登陆出现异常状况
                errorPage = driver.page_source.encode( "utf-8" )
                if "拖动下方滑块完成拼图" in errorPage:
                    pass
                if "你输入的帐号或密码不正确，请重新输入。" in errorPage:
                    pass
                if "冻结" in errorPage:
                    self.repo.BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )
                try:
                    obj = driver.find_element_by_class_name( "content" )
                    # driver.save_screenshot( "aaa.png" )

                    self.repo.BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )
                except:
                    time.sleep( 2 )
                    # driver.save_screenshot( "bbb.png" )
                continue
            # try:
            #     obj = driver.find_element_by_xpath(
            #         "//li[@class='folderlist_folder qm_list_item qm_list_item_Accessory'][1]/a[@class='qm_list_item_content' and @cmd='folder' ]")
            #     text = obj.get_attribute("class")
            #     obj.click()
            #
            #     driver.save_screenshot("aaaa.png")
            # except:
            #     pass


            #一起删除
            # try:
            #     js = "var q=document.documentElement.scrollTop=10000"
            #     driver.execute_script( js )
            #     time.sleep( 3 )
            #     driver.save_screenshot( "2.png" )
            #     # driver.find_element_by_class_name("qm_actionBar_listItem_SelectAll").click()
            #     # time.sleep( 3 )
            #     # driver.save_screenshot( "3.png" )
            #     time.sleep( 3 )
            #     print driver.page_source
            #
            #     while True:
            #         try:
            #             driver.find_element_by_class_name( "qm_actionBar_listItem_SelectAll" ).click( )
            #             driver.save_screenshot( "3.png" )
            #             obj = driver.find_element_by_class_name( "func_posRelative" )
            #             obj.click( )
            #             time.sleep( 3 )
            #             driver.save_screenshot( "4.png" )
            #         except:
            #             driver.save_screenshot( "5.png" )
            #             break
            #
            # except:
            #     driver.save_screenshot( "1.png" )
            #     pass

            url = driver.current_url.encode("utf-8")
            # getCoolies = driver.get_cookies( )
            # value = ''
            # name = ''
            # cookie = None
            # for item in getCoolies:
            #     # key = self.get_keys(item,QQNumber.encode("utf-8"))
            #     # for v in item:
            #     #     if QQNumber.encode("utf-8") in v["value"].encode("utf-8"):
            #     #
            #     if QQNumber.encode( "utf-8" ) in item["value"].encode( "Utf-8" ):
            #         value = item["value"].encode( "Utf-8" )
            #         name = item["name"]
            #         cookie = item
            #         break
            # if cookie!=None:
            #     para = {"phoneNumber": cookie, 'x_01': QQNumber,"x_02":url}
            #     self.repo.PostInformation( repo_cookies_id, para )

            obj.click( )
            driver.save_screenshot( "444.png" )
            flag = True
            while flag:
                repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
                emailnumbers = self.repo.GetNumber( repo_number_cate_id, 0, 1 )  # 取出add_count条两小时内没有用过的号码
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
                # for i in range( 0, sendCount ):
                #     if i<len(emailnumbers):
                emailnumber = emailnumbers[0]['number']
                        # QQEmail = numbers[i]['number'].encode( "utf-8" )
                try:
                    if emailType=="QQ邮箱":
                        driver.find_element_by_id( "showto" ).send_keys( emailnumber + "@qq.com " )
                        driver.find_element_by_id( "subject" ).click()
                    elif emailType=="189邮箱":
                        driver.find_element_by_id( "showto" ).send_keys( emailnumber + "@189.cn " )
                        driver.find_element_by_id( "subject" ).click( )
                    else:
                        driver.find_element_by_id( "showto" ).send_keys( emailnumber + "@qq.com " )
                        driver.find_element_by_id( "subject" ).click( )
                except:
                    continue
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
                else:
                    print "发送不成功"
                    flag = False
                    if "邮件中可能包含不合适的用语或内容" in page_source:
                        #需要解锁
                        print "邮件中可能包含不合适的用语或内容"
                        driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                        self.repo.BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )

                    elif "<html><head></head><body></body></html>" in page_source:
                        driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                        print "空"
                    elif "验证码" in page_source:
                        print "需要验证码"
                        driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                    elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                        print "您发送的邮件已经达到上限，请稍候再发"
                        driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                    else:
                        print page_source
                        driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
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
                   pass

            replace1 = "&t=phone#list,1__"  # 收件箱
            url1 = url.replace( "&mcookie=disabled", replace1 )

            replace2 = "&t=phone#list,3__"  #已发送
            url2 = url.replace( "&mcookie=disabled", replace2 )

            replace3 = "&t=phone#list,4__"
            url3 = url.replace( "&mcookie=disabled", replace3 )

            replace4 = "&t=phone#list,5__"
            url4 = url.replace( "&mcookie=disabled", replace4 )

            replace5 = "&t=phone#list,6__"
            url5 = url.replace( "&mcookie=disabled", replace5 )

            urlList = [url,url2,url3,url4,url5]

            print driver.current_url
            replace2 = "&t=phone#list,3__"
            url2 = driver.current_url.replace( "&mcookie=disabled", replace2 )

            for needurl in urlList:
                driver.save_screenshot("000.png")

                # try:
                #     obj = driver.find_element_by_xpath("qm_actionBar_listItem qm_actionBar_listItem_SelectAll")
                #     obj.click()
                #     driver.save_screenshot( "001.png" )
                #     obj = driver.find_element_by_xpath("//div[@class='qm_actionBar_listItem qm_btnGroup func_posRelative'][2]")
                #     obj.click()
                #
                # except:
                #     driver.save_screenshot("002.png")
                #     pass


                deleteList = []
                flag2 = False
                while True:
                    driver.get( needurl )
                    time.sleep( 3 )
                    driver.save_screenshot( "888.png" )

                    driver.refresh( )
                    time.sleep(2)
                    driver.save_screenshot( "999.png" )
                    page = driver.page_source.encode( "utf-8" )

                    for j in range( 0, 10 ):
                        try:
                            if needurl!=url3:
                                searchObj = re.search( r'id="ZC.*?"', page, re.M | re.I )
                            else:
                                searchObj = re.search( r'id="ZD.*?"', page, re.M | re.I )
                            id = searchObj.group( )[4:][:-1]
                            if id not in deleteList:
                                deleteList.append( id )
                            else:
                                flag2 = True
                            print id
                            page = page.replace( id, "xx" )
                        except:
                            flag2 = True
                            break

                    if flag2:
                        print "没刷新出来或者没有数据邮件可删除"
                        break

                    print deleteList
                    if len( deleteList ) == 0:
                        break

                    current = driver.current_url
                    for item in deleteList:
                        try:
                            driver.find_element_by_id( item ).find_element_by_class_name( "maillist_listItemRight" ).click( )
                        except:
                            pass
                        time.sleep( 2 )
                        driver.save_screenshot( "q.png" )
                        try:
                            # obj = driver.find_element_by_class_name("qm_icon_Delete")
                            # driver.find_element_by_xpath( "//span[@class='qm_icon qm_icon_Delete']/parent::*" ).click( )
                            driver.find_element_by_class_name( "qm_icon_Delete" ).click()
                            # obj = driver.find_element_by_xpath("//a[@class='qm_btnIcon']/following::*")
                            # obj.click()
                            # href = obj.get_attribute("href")
                            # driver.get(href)
                            time.sleep( 2 )
                            driver.save_screenshot( "333.png" )
                        except:
                            pass
                        driver.get( current )
                        time.sleep( 2 )
                        driver.refresh( )
                        time.sleep( 2 )

            try:
                driver.find_element_by_link_text( "退出" ).click( )
                time.sleep( 2 )
                driver.save_screenshot( "exit.png" )
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

    args = {"time_delay":"3","time_limit1":"60","count":"10","repo_cate_id":"275","repo_number_cate_id":"119","repo_material_cateId": "39",
            "repo_material_cateId2":"40","selectContent":"主题内容都发","emailType":"QQ邮箱","repo_cookies_id":"286"}    #cate_id是仓库号，length是数量
    o.action( args )

    # a = os.system("echo 1 | sudo -S poff")
    # print a
    # b = os.system("echo 1 | sudo -S pon dsl-provider")
    # print b