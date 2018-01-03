# coding:utf-8
from __future__ import division

import base64
import logging
import re
import socket
import urllib2

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs
import os, time, datetime, random
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from IPChange import *


class EmailInternet:
    def __init__(self):
        # Repo() = Repo()
        pass

    def GetUnique(self):
        nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )  # 生成当前时间
        randomNum = random.randint( 0, 1000 )  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str( 00 ) + str( randomNum )
        uniqueNum = str( nowTime ) + str( randomNum )
        return uniqueNum

    def action(self, args):
        emailType = args["emailType"]
        repo_material_cateId2 = args["repo_material_cateId2"]
        repo_material_cateId = args["repo_material_cateId"]
        sendTime = args["sendTime"]
        sendTime = sendTime.split( "-" )
        try:
            sendTimeStart = int( sendTime[0] )
            sendTimeEnd = int( sendTime[1] )
        except:
            print  "    发送时间间隔的参数格式有误"
            sendTimeStart = 3
            sendTimeEnd = 5

        time_delay = args["time_delay"]
        time_delay = time_delay.split( "-" )
        try:
            time_delayStart = int( time_delay[0] )
            time_delayEnd = int( time_delay[1] )
        except:
            print  "    参数格式有误"
            time_delayStart = 3
            time_delayEnd = 5
        user_agentid = args["user_agent_id"]
        count = 0
        while True:
            repo_cate_id = args["repo_cate_id"]
            numbers = Repo( ).GetAccount( repo_cate_id, 5, 1 )
            while len( numbers ) == 0:
                print "%s号仓库没有数据" % repo_cate_id
                return

            QQNumber = numbers[0]['number']  # 即将登陆的QQ号
            QQPassword = numbers[0]['password']
            user_agent = numbers[0]['imei']
            if user_agent is None or user_agent == '':
                user_agentList = Repo( ).GetMaterial( user_agent_id, 0, 1 )
                if len( user_agentList ) == 0:
                    # print "%s号仓库为空，没有取到消息"%repo_material_cateId
                    return
                user_agent = user_agentList[0]['content']
            print user_agent
            cap = webdriver.DesiredCapabilities.PHANTOMJS
            cap["phantomjs.page.settings.resourceTimeout"] = 1000
            cap["phantomjs.page.settings.loadImages"] = True
            cap["phantomjs.page.settings.disk-cache"] = True
            cap["phantomjs.page.settings.userAgent"] = user_agent

            cap["phantomjs.page.customHeaders.User-Agent"] = user_agent
            driver = webdriver.PhantomJS( desired_capabilities=cap )
            # driver.close()
            # driver.quit( )
            # 检查是否连接网络
            driver.get( "https://www.baidu.com/" )
            if "百度一下" in driver.page_source.encode( "utf-8" ):
                print "Internet OK"
            else:
                print "Internet NO"
                driver.quit( )
                return

                # driver.save_screenshot( "5.png" )
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
            # driver.save_screenshot("0.png")
            # 点 进入网页版QQ邮箱 (模拟手机版会有这个)
            try:
                obj = driver.find_element_by_xpath( "//td[@class='enter_mail_button_td']/a" )
                obj.click( )

            except:
                print "error"

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
                driver.find_element_by_id( "go" ).click( )
                time.sleep( random.randint( time_delayStart, time_delayEnd ) )
            except:
                pass

            # while True:
            #     try:
            #         # 点击登陆
            #         driver.find_element_by_id( "go" ).click( )
            #     except:
            #         break

            driver.save_screenshot( "333.png" )

            try:
                obj = driver.find_element_by_class_name( "qm_btnIcon" )
                print "%s  登陆成功" % QQNumber
                Repo( ).BackupInfo( repo_cate_id, 'normal', QQNumber, user_agent, '' )

            except:
                print "%s  登陆失败" % QQNumber

                time.sleep( 2 )
                # 登陆出现异常状况
                errorPage = driver.page_source.encode( "utf-8" )
                if "拖动下方滑块完成拼图" in errorPage:
                    print "%s  拖动下方滑块完成拼图" % QQNumber
                    continue
                if "帐号或密码不正确" in errorPage:
                    print "%s  帐号或密码不正确" % QQNumber
                    continue
                if "冻结" in errorPage:
                    print "%s  冻结" % QQNumber
                    Repo( ).BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )
                    continue
                else:
                    try:
                        obj = driver.find_element_by_id( "p" )
                        text = obj.get_attribute( "text" )

                        driver.find_element_by_id( "p" ).send_keys( QQPassword )

                        driver.find_element_by_id( "go" ).click( )
                        try:
                            driver.find_element_by_id( "go" )
                            print "%s  冻结" % QQNumber
                            Repo( ).BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )
                        except:
                            pass
                        Repo( ).BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )
                    except:
                        pass
                try:
                    obj = driver.find_element_by_class_name( "content" )
                    # driver.save_screenshot( "aaa.png" )

                    # Repo().BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )
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


            # 一起删除
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

            url = driver.current_url.encode( "utf-8" )
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
            #     Repo().PostInformation( repo_cookies_id, para )

            obj.click( )
            # driver.save_screenshot( "444.png" )
            flag = True
            while flag:
                repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
                emailnumbers = Repo( ).GetNumber( repo_number_cate_id, 0, 1 )  # 取出add_count条两小时内没有用过的号码
                if len( emailnumbers ) == 0:
                    print u"QQ号码库%s  号仓库为空" % repo_number_cate_id
                    driver.quit( )
                    return
                # emailnumber = emailnumbers[0]['number']
                if repo_material_cateId == "" or repo_material_cateId is None:
                    selectContent1 = ""
                else:
                    selectContent1 = "只发主题"
                    Material = Repo( ).GetMaterial( repo_material_cateId, 0, 1 )
                    while len( Material ) == 0:
                        print u"%s  号仓库为空，没有取到消息,等五分钟再试" % repo_material_cateId
                        time.sleep(300)

                    message = Material[0]['content']
                if repo_material_cateId2 == "" or repo_material_cateId2 is None:
                    selectContent2 = ""
                else:
                    selectContent2 = "只发内容"
                    Material2 = Repo( ).GetMaterial( repo_material_cateId2, 0, 1 )
                    if len( Material2 ) == 0:
                        print u"%s  号仓库为空，没有取到消息,等五分钟再试" % repo_material_cateId2
                        time.sleep( 300 )
                    message2 = Material2[0]['content']

                # driver.find_element_by_id("showto").send_keys(emailnumber)
                # for i in range( 0, sendCount ):
                #     if i<len(emailnumbers):
                emailnumber = emailnumbers[0]['number']
                # QQEmail = numbers[i]['number'].encode( "utf-8" )
                try:
                    emailnumberObj = driver.find_element_by_id( "to" )
                except:
                    emailnumberObj = driver.find_element_by_id( "showto" )

                if "@" not in emailnumber:
                    if emailType == "QQ邮箱":
                        emailnumberObj.send_keys( emailnumber + "@qq.com" )
                    elif emailType == "189邮箱":
                        emailnumberObj.send_keys( emailnumber + "@189.cn" )
                    elif emailType == "139邮箱":
                        emailnumberObj.send_keys( emailnumber + "@139.com" )
                    elif emailType == "163邮箱":
                        emailnumberObj.send_keys( emailnumber + "@163.com" )
                    elif emailType == "wo邮箱":
                        emailnumberObj.send_keys( emailnumber + "@wo.cn" )
                    else:
                        emailnumberObj.send_keys( emailnumber + "@qq.com" )
                else:
                    emailnumberObj.send_keys( emailnumber )

                # if emailType=="QQ邮箱":
                #     emailnumberObj.send_keys( emailnumber + "@qq.com " )
                #     driver.find_element_by_id( "subject" ).click()
                # elif emailType=="189邮箱":
                #     emailnumberObj.send_keys( emailnumber + "@189.cn " )
                #     driver.find_element_by_id( "subject" ).click( )
                # else:
                #     emailnumberObj.send_keys( emailnumber + "@qq.com " )
                #     driver.find_element_by_id( "subject" ).click( )
                # driver.save_screenshot("mmm.png")
                # driver.find_element_by_id( "showto" ).send_keys( "455854284" + "@qq.com " )
                if selectContent1 == "只发主题":
                    driver.find_element_by_id( "subject" ).send_keys( message )
                if selectContent2 == "只发内容":
                    driver.find_element_by_id( "content" ).send_keys( message2 )
                time.sleep( 3 )
                # driver.save_screenshot( "555.png" )

                try:
                    # windows
                    driver.find_element_by_name( "RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__" ).click( )
                except:
                    driver.find_element_by_id( "composeSend" ).click( )
                time.sleep( random.randint( sendTimeStart, sendTimeEnd ) )
                # driver.save_screenshot("666.png" )
                page_source = driver.page_source

                if "发送成功" in page_source and "验证码" not in page_source:
                    print "%s  发送成功" % QQNumber
                else:
                    print "%s  发送不成功" % QQNumber
                    flag = False
                    if "邮件中可能包含不合适的用语或内容" in page_source:
                        # 需要解锁
                        print "%s  邮件中可能包含不合适的用语或内容" % QQNumber
                        # driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                        Repo( ).BackupInfo( repo_cate_id, 'exception', QQNumber, '', '' )

                    elif "<html><head></head><body></body></html>" in page_source:
                        # driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                        print "%s  空" % QQNumber
                        IPChange( ).ooo( )
                        IPChange( ).ooo( )
                    elif "验证码" in page_source:
                        print "%s  需要验证码" % QQNumber
                        count = count + 1
                        # driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                    elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                        print "%s  您发送的邮件已经达到上限，请稍候再发" % QQNumber
                        # driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                    else:
                        # print page_source
                        driver.save_screenshot( "%s-%s.png" % (QQNumber, self.GetUnique( )) )
                        print "%s  该情况没判断出来" % QQNumber
                        # print  page_source
                page_source = driver.page_source.encode( 'utf-8' )
                driver.get( url )
                if flag:
                    try:
                        driver.find_element_by_class_name( "qm_btnIcon" ).click( )
                    except:
                        pass
                else:
                    pass
                    # replace1 = "#list,1__"  # 收件箱
                    # url1 = url.replace( "#today", replace1 )
                    #
                    # replace2 = "#list,3__"  #已发送
                    # url2 = url.replace( "#today", replace2 )
                    #
                    # replace3 = "#list,4__"
                    # url3 = url.replace( "#today", replace3 )
                    #
                    # replace4 = "#list,6__"
                    # url4 = url.replace( "#today", replace4 )
                    #
                    # # replace5 = "#list,5__"
                    # # url4 = url.replace( "#today", replace5 )
                    #
                    #
                    # urlList = [url1,url2,url3,url4]
                    #
                    # print driver.current_url
                    #
                    # for needurl in urlList:
                    # driver.save_screenshot("000.png")

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
                    # flag2 = False
                    # while True:
                    #       点击全选按钮删除
                    #     driver.get( needurl )
                    #     try:
                    #         obj = driver.find_element_by_xpath("//label[@class='qm_actionBar_listItem qm_actionBar_listItem_SelectAll']/input[@class='qm_chkb']")
                    #         obj.click()
                    #         driver.save_screenshot( "df.png" )
                    #     except:
                    #         print "没有数据邮件可删除"
                    #         time.sleep(0.5)
                    #         driver.save_screenshot("qw.png")
                    #         flag2 = True
                    #         break
                    #     try:
                    #         deleteObj = driver.find_element_by_xpath("//div[@class='qm_actionBar_listItem qm_btnGroup func_posRelative']/a[@class='qm_btn']" )
                    #         text = deleteObj.get_attribute("text")
                    #         if "删除" in text.encode("utf-8"):
                    #             deleteObj.click()
                    #             flag2 = True
                    #         driver.save_screenshot( "er.png" )
                    #     except:
                    #         print "error"
                    #         driver.save_screenshot("as.png")
                    #     break
                    #
                    # if flag2:
                    #     continue
                    # if needurl == url5:
                    #     while True:
                    #         #点击全选按钮删除
                    #         driver.get( needurl )
                    #         try:
                    #             obj = driver.find_element_by_xpath(
                    #                 "//label[@class='qm_actionBar_listItem qm_actionBar_listItem_SelectAll']/input[@class='qm_chkb']" )
                    #             obj.click( )
                    #             driver.save_screenshot( "df.png" )
                    #         except:
                    #             print "没有数据邮件可删除"
                    #             time.sleep( 0.5 )
                    #             driver.save_screenshot( "qw.png" )
                    #             flag2 = True
                    #             break
                    #         try:
                    #             deleteObj = driver.find_element_by_xpath(
                    #                 "//div[@class='qm_actionBar_listItem qm_btnGroup func_posRelative']/a[@class='qm_btn']" )
                    #             text = deleteObj.get_attribute( "text" )
                    #             if "删除" in text.encode( "utf-8" ):
                    #                 deleteObj.click( )
                    #                 flag2 = True
                    #             driver.save_screenshot( "er.png" )
                    #         except:
                    #             print "error"
                    #             driver.save_screenshot( "as.png" )
                    #         break
                    #
                    #     # 下面操作 防止出现点击全选按钮删除不见了
                    #     flag2 = False
                    #     while True:
                    #         deleteList = []
                    #         driver.get( needurl )
                    #         print needurl
                    #         time.sleep( 3 )
                    #         # driver.save_screenshot( "888.png" )
                    #
                    #         # driver.refresh( )
                    #         # time.sleep(2)
                    #         # driver.save_screenshot( "999.png" )
                    #         page = driver.page_source.encode( "utf-8" )
                    #
                    #         for j in range( 0, 10 ):
                    #             try:
                    #                 searchObj = re.search( r'id="Z.*?"', page, re.M | re.I )
                    #                 # if needurl==url3:
                    #                 #     searchObj = re.search( r'id="ZD.*?"', page, re.M | re.I )
                    #                 # else:
                    #                 #     if needurl==url5:
                    #                 #         searchObj = re.search( r'id="ZC.*?"', page, re.M | re.I )
                    #                 #     else:
                    #                 #         searchObj = re.search( r'id="Z.*?"', page, re.M | re.I )
                    #
                    #                 id = searchObj.group( )[4:][:-1]
                    #                 if id not in deleteList:
                    #                     deleteList.append( id )
                    #                 else:
                    #                     flag2 = True
                    #                 print id
                    #                 page = page.replace( id, "xx" )
                    #             except:
                    #                 if len(deleteList)==0:
                    #                     flag2 = True
                    #                 break
                    #
                    #         if flag2:
                    #             print "没刷新出来或者没有邮件可删除"
                    #             break
                    #
                    #         print deleteList
                    #
                    #         current = driver.current_url
                    #         for item in deleteList:
                    #
                    #             try:
                    #                 driver.find_element_by_class_name( "qm_icon_Delete" )
                    #             except:
                    #                 driver.find_element_by_id( item ).find_element_by_class_name( "maillist_listItemRight" ).click( )
                    #                 time.sleep( 2 )
                    #             # driver.save_screenshot( "q.png" )
                    #             try:
                    #                 # obj = driver.find_element_by_class_name("qm_icon_Delete")
                    #                 # driver.find_element_by_xpath( "//span[@class='qm_icon qm_icon_Delete']/parent::*" ).click( )
                    #                 obj =driver.find_element_by_class_name( "qm_icon_Delete" )
                    #                 obj.click()
                    #                 # obj = driver.find_element_by_xpath("//a[@class='qm_btnIcon']/following::*")
                    #                 # obj.click()
                    #                 # href = obj.get_attribute("href")
                    #                 # driver.get(href)
                    #                 time.sleep( 2 )
                    #                 # driver.save_screenshot( "333.png" )
                    #                 try:
                    #                     driver.find_element_by_class_name( "qm_icon_Delete" )
                    #                     continue
                    #                 except:
                    #                     driver.get( current )
                    #                     time.sleep( 2 )
                    #
                    #             except:
                    #                 pass

                    # driver.refresh( )
                    # time.sleep( 2 )

            try:
                driver.find_element_by_link_text( "退出" ).click( )
                time.sleep( 2 )
                # driver.save_screenshot( "exit.png" )
                IPChange( ).ooo( )
                IPChange( ).ooo( )
            except:
                print "error"
                # driver.save_screenshot( "exit2.png" )

        driver.quit( )


def getPluginClass():
    return EmailInternet


if __name__ == "__main__":
    # global args

    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass( )
    o = clazz( )

    sys.path.append( "D:\TaskConsole-master" )

    from Repo import *

    from IPChange import *

    data = IPChange( ).Check_for_Broadband( )
    # if exist running broadband connection, disconnected it.
    if data != None:
        print u"网络已连接宽带"
    else:
        print u"网络未连接宽带"
        IPChange( ).ooo( )


    repo = Repo( )
    while True:
        taskList = repo.GetPhantomJSTaskInfo( )
        if len( taskList ) == 0:
            print "please check http://data.zunyun.net/repo/phantomjs/list"
            time.sleep( 30 )
            continue

        task = taskList[random.randint( 0, len( taskList ) ) - 1]
        phonenumber = task["phonenumber"]
        cateId = task["cateId"]
        repo_material_cateId = task["x01"]
        repo_material_cateId2 = task["x07"]
        repo_number_cate_id = task["x03"]
        user_agent_id = task["x02"]

        while True:
            paramList = repo.GetPhantomJSParamInfo( )
            if len( paramList ) == 0:
                time.sleep( 30 )
                continue
            else:
                break

        param = paramList[random.randint( 0, len( paramList ) ) - 1]
        repo_cate_id = param["phonenumber"]
        time_delay = param["x01"]
        sendTime = param["x02"]
        emailType = param["x03"]

        # print taskList
        # print paramList
        args = {"time_delay": time_delay, "sendTime": sendTime, "repo_cate_id": repo_cate_id,
                "repo_number_cate_id": repo_number_cate_id, "repo_material_cateId": repo_material_cateId,
                "repo_material_cateId2": repo_material_cateId2, "emailType": emailType,
                "user_agent_id": user_agent_id}  # cate_id是仓库号，length是数量
        try:
            o.action( args )
        except:
            pass
        para = {"phoneNumber": phonenumber, "x_04": "stopped"}
        repo.PostInformation( cateId, para )
        # a = os.system("echo 1 | sudo -S poff")
        # print a
        # b = os.system("echo 1 | sudo -S pon dsl-provider")
        # print b
