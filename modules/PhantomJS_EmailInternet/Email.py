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



class Email:
    def __init__(self):
        # Repo() = Repo()
        pass

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def action(self, args):
        selectContent = args["selectContent"]
        emailType = args["emailType"]
        repo_material_cateId2 = args["repo_material_cateId2"]
        repo_material_cateId = args["repo_material_cateId"]
        sendTime = args["sendTime"]
        sendTime = sendTime.split( "-" )
        try:
            sendTimeStart = int( sendTime[0] )
            sendTimeEnd = int( sendTime[1] )
        except:
            print  "发送时间间隔的参数格式有误"
            sendTimeStart = 3
            sendTimeEnd = 5

        time_delay = args["time_delay"]
        time_delay = time_delay.split( "-" )
        try:
            time_delayStart = int( time_delay[0] )
            time_delayEnd = int( time_delay[1] )
        except:
            print  "参数格式有误"
            time_delayStart = 3
            time_delayEnd = 5

        while True:
            user_agentid = args["user_agent_id"]
            repo_cate_id = args["repo_cate_id"]
            numbers = Repo( ).GetAccount( repo_cate_id, 5, 1 )
            while len( numbers ) == 0:
                print "%s号仓库没有数据" % repo_cate_id
                return

            account = numbers[0]['number']  # 即将登陆的QQ号
            password = numbers[0]['password']
            user_agent = numbers[0]['imei']
            if user_agent is None or user_agent == '':
                user_agentList = Repo( ).GetMaterial( user_agent_id, 0, 1 )
                if len( user_agentList ) == 0:
                    print "%s号仓库为空，没有取到消息" % repo_material_cateId
                    return
                user_agent = user_agentList[0]['content']
            print user_agent
            cap = webdriver.DesiredCapabilities.PHANTOMJS
            cap["phantomjs.page.settings.resourceTimeout"] = 1000
            cap["phantomjs.page.settings.loadImages"] = True
            cap["phantomjs.page.settings.disk-cache"] = True
            cap["phantomjs.page.settings.userAgent"] = user_agent

            cap["phantomjs.page.customHeaders.User-Agent"] = user_agent
            driver = webdriver.PhantomJS( desired_capabilities=cap,
                                          executable_path="/usr/local/phantomjs/bin/phantomjs" )
            driver.get( "https://m.exmail.qq.com/cgi-bin/loginpage" )
            # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled')
            time.sleep( 3 )

            driver.save_screenshot( "111.png" )
            try:
                driver.find_element_by_id( "uin" ).clear( )
            except:
                pass
            try:
                driver.find_element_by_id( "uin" ).send_keys( account )
                time.sleep( 0.5 )
                driver.find_element_by_id( "pwd" ).send_keys( password )
                driver.save_screenshot( "222.png" )
                time.sleep( 1 )
                driver.find_element_by_id( "pwd" ).send_keys( Keys.ENTER )
                time.sleep( random.randint( time_delayStart, time_delayEnd ) )
                driver.save_screenshot( "333.png" )
            except:
                pass

            try:
                obj = driver.find_element_by_class_name( "qm_icon_Compose" )
                print "%s  登陆成功" % account
                # Repo( ).BackupInfo( repo_cate_id, 'normal', QQNumber, user_agent, '' )
                startUrl = driver.current_url
            except:
                print "%s  登陆失败" % account

                time.sleep( 2 )
                # 登陆出现异常状况
                errorPage = driver.page_source.encode( "utf-8" )
                if "拖动下方滑块完成拼图" in errorPage:
                    print "拖动下方滑块完成拼图"
                if "看不清" in errorPage:
                    print "需要验证码"
                if "帐号或密码不正确" in errorPage:
                    print "帐号或密码不正确"
                if "冻结" in errorPage:
                    print "冻结"
                    Repo( ).BackupInfo( repo_cate_id, 'frozen', account, '', '' )
                else:
                    pass
                try:
                    obj = driver.find_element_by_class_name( "content" )
                    driver.save_screenshot( "aaa.png" )

                    # Repo().BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )
                except:
                    time.sleep( 2 )
                    driver.save_screenshot( "%s.png"%(account) )
                continue

            url = driver.current_url.encode( "utf-8" )
            obj.click( )
            time.sleep(2)
            driver.save_screenshot( "444.png" )
            flag = True
            while flag:
                repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
                emailnumbers = Repo( ).GetNumber( repo_number_cate_id, 0, 1 )  # 取出add_count条两小时内没有用过的号码
                if len( emailnumbers ) == 0:
                    print "QQ号码库%s号仓库为空" % repo_number_cate_id
                    driver.quit( )
                    return
                # emailnumber = emailnumbers[0]['number']

                Material = Repo( ).GetMaterial( repo_material_cateId, 0, 1 )
                if len( Material ) == 0:
                    print "%s号仓库为空，没有取到消息" % repo_material_cateId
                    driver.quit( )
                    return
                message = Material[0]['content']

                Material2 = Repo( ).GetMaterial( repo_material_cateId2, 0, 1 )
                if len( Material2 ) == 0:
                    print "%s号仓库为空，没有取到消息" % repo_material_cateId
                    driver.quit( )
                    return
                message2 = Material2[0]['content']
                emailnumber = emailnumbers[0]['number']
                driver.save_screenshot("test01.png")
                # try:
                #     emailnumberObj = driver.find_element_by_id( "to" )
                #     emailnumberObj.click()
                # except:
                #     emailnumberObj = driver.find_element_by_id( "showto" )
                try:
                    emailnumberObj = driver.find_element_by_id( "showto" )
                except:
                    driver.save_screenshot("to.png")
                    try:
                        emailnumberObj = driver.find_element_by_id( "to" )
                    except:
                        driver.get( url )
                        time.sleep( 2 )
                        continue
                if emailType == "QQ邮箱":
                    emailnumberObj.send_keys( emailnumber + "@qq.com " )
                    driver.save_screenshot( "555.png" )
                    driver.find_element_by_id( "subject" ).click( )
                elif emailType == "189邮箱":
                    emailnumberObj.send_keys( emailnumber + "@189.cn " )
                    driver.find_element_by_id( "subject" ).click( )
                else:
                    emailnumberObj.send_keys( emailnumber + "@qq.com " )
                    driver.find_element_by_id( "subject" ).click( )
                driver.save_screenshot( "mmm.png" )

                if selectContent == "只发主题" or selectContent == "主题内容都发":
                    driver.find_element_by_id( "subject" ).send_keys( message )
                if selectContent == "只发内容" or selectContent == "主题内容都发":
                    driver.find_element_by_class_name( "compose_form_item_textarea" ).send_keys( message2 )
                time.sleep( 3 )
                driver.save_screenshot( "555.png" )
                driver.save_screenshot( "test02.png" )
                try:
                    driver.find_element_by_id( "composeSend" ).click( )
                except:
                    driver.find_element_by_name( "RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__" ).click( )
                time.sleep( random.randint( sendTimeStart, sendTimeEnd ) )
                driver.save_screenshot( "666.png" )
                try:
                    try:
                        driver.find_element_by_id( "composeSend" )
                    except:
                        driver.find_element_by_name( "RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__" )
                    print "发送失败"
                    flag = False
                    driver.get( url )
                    time.sleep( 2 )
                    continue
                except:
                    pass
                page_source = driver.page_source.encode( "utf-8" )

                if "发送成功" in page_source and "验证码" not in page_source:
                    print "发送成功"

                else:
                    try:
                        driver.find_element_by_class_name( "qm_icon_Compose" )
                        print "发送成功"
                    except:
                        print "发送不成功"
                        flag = False
                        if "邮件中可能包含不合适的用语或内容" in page_source:
                            print "邮件中可能包含不合适的用语或内容"
                        elif "<html><head></head><body></body></html>" in page_source:
                            print "空"
                        elif "验证码" in page_source:
                            print "需要验证码"
                        elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                            print "您发送的邮件已经达到上限，请稍候再发"
                        else:
                            print page_source
                            driver.save_screenshot( "%s-%s.png" % (account, self.GetUnique( )) )
                            print "error"
                driver.get( url )
                time.sleep(2)
                try:
                    driver.find_element_by_class_name( "qm_icon_Compose" ).click()
                except:
                    pass

            # 删除邮件
            driver.get( startUrl )
            folder = driver.find_elements_by_xpath( "//span[@class='qm_list_item_title']" )[7]
            folder.click( )
            driver.save_screenshot( "folder.png" )
            folderUrl = driver.current_url
            driver.find_elements_by_xpath( "//span[@class='qm_list_item_title']" )[6].click( )
            i = 0
            while True:
                try:
                    driver.find_element_by_id( "selectall" ).click( )
                except:
                    if "没有邮件" in driver.page_source.encode( "utf-8" ):
                        print "没有邮件可删除"
                        if i == 2:
                            break
                        print "没有邮件可删除"
                        i = i + 1
                        driver.get( folderUrl )
                        if i == 1:
                            driver.find_elements_by_xpath( "//span[@class='qm_list_item_title']" )[9].click( )
                        else:
                            driver.find_elements_by_xpath( "//span[@class='qm_list_item_title']" )[10].click( )
                        time.sleep( 1 )
                        continue
                driver.save_screenshot( "delete.png" )
                if i == 1:
                    deleteObj = driver.find_element_by_xpath("//div[@class='qm_actionBar_listItem qm_btnGroup func_posRelative']/input[@class='qm_btn']" )
                else:
                    try:
                        deleteObj = driver.find_elements_by_xpath("//div[@class='qm_actionBar_listItem qm_btnGroup func_posRelative']/input[@class='qm_btn']" )[1]
                    except:
                        deleteObj = driver.find_element_by_xpath("//div[@class='qm_actionBar_listItem qm_btnGroup func_posRelative']/input[@class='qm_btn']" )
                deleteObj.click( )
                driver.save_screenshot( "delete2.png" )
                if "没有邮件" in driver.page_source.encode( "utf-8" ):
                    if i == 2:
                        break
                    print "没有邮件可删除"
                    i = i + 1
                    driver.get( folderUrl )
                    if i == 1:
                        driver.find_elements_by_xpath( "//span[@class='qm_list_item_title']" )[9].click( )
                    else:
                        driver.find_elements_by_xpath( "//span[@class='qm_list_item_title']" )[10].click( )

                    time.sleep( 1 )
                driver.save_screenshot( "get.png" )

            # 退出帐号重新登陆
            try:
                obj = driver.find_elements_by_xpath( "//p[@class='qm_footer_userInfo']/a" )
                obj[0].click( )
                time.sleep( 2 )
                driver.save_screenshot( "exit.png" )
            except:
                print "error"


        driver.quit( )

def getPluginClass():
    return Email

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()

    sys.path.append("/home/zunyun/workspace/TaskConsole")

    from Repo import *

    repo = Repo()
    while True:
        taskList = repo.GetPhantomJSTaskInfo()
        if len(taskList)==0:
            time.sleep(30)
            continue
        else:
            break
        #get random task
    task = taskList[random.randint(0,len(taskList))-1]
    phonenumber = task["phonenumber"]
    cateId = task["cateId"]
    repo_material_cateId =task["x01"]
    repo_material_cateId2 =task["x07"]
    repo_number_cate_id = task["x03"]
    user_agent_id = task["x02"]


    while True:
        paramList = repo.GetPhantomJSParamInfo( )
        if len(paramList)==0:
            time.sleep(30)
            continue
        else:
            break

    param = paramList[random.randint( 0, len( paramList ) ) - 1]
    repo_cate_id = param["phonenumber"]
    time_delay = param["x01"]
    sendTime = param["x02"]
    selectContent = param["x03"]
    emailType = param["x04"]

    # print taskList
    # print paramList
    args = {"time_delay":time_delay,"sendTime":sendTime,"repo_cate_id":repo_cate_id,"repo_number_cate_id":repo_number_cate_id,"repo_material_cateId": repo_material_cateId,
            "repo_material_cateId2":repo_material_cateId2,"selectContent":selectContent,"emailType":emailType,"user_agent_id":user_agent_id}    #cate_id是仓库号，length是数量
    # try:
    #     o.action( args )
    # except:
    #     pass
    o.action( args )
    para = {"phoneNumber": phonenumber, "x_04": "stopped"}
    repo.PostInformation( cateId, para )

    #拨号换ip
    # a = os.system("echo 1 | sudo -S poff")
    # print a
    # b = os.system("echo 1 | sudo -S pon dsl-provider")
    # print b