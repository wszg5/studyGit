# coding:utf-8
from __future__ import division
import base64
import httplib
import logging
import re
import socket
import urllib2
from pyvirtualdisplay import Display
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs
# import virtkey

import os, time, datetime, random
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
sys.path.append("/home/zunyun/workspace/TaskConsole")
# sys.path.append("C:\TaskConsole-master")
# from IPChange import IPChange
from Repo import Repo
class YM_WY:
    def __init__(self):
        self.repo = Repo()
        # self.ipChange = IPChange()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 1000)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

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
            my_userCount= task["x09"]
            bccCount = task["x10"]
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
            sleepTime = param["x04"]
            if sleepTime is None or sleepTime == '':
                sleepTime = "10-15"

            args = {"time_delay": time_delay, "sendTime": sendTime, "repo_cate_id": repo_cate_id,
                    "repo_number_cate_id": repo_number_cate_id, "repo_material_cateId": repo_material_cateId,
                    "repo_material_cateId2": repo_material_cateId2, "emailType": emailType,
                    "user_agent_id": user_agent_id,"phonenumber":phonenumber,"cateId":cateId,"my_userCount":my_userCount,"bccCount":bccCount,"sleepTime":sleepTime}  # cate_id是仓库号，length是数量
            return args

    def sendProcess(self):
        try:
            sc = 0
            flagFirst = False
            flagFirst2 = False

            count = 0
            changeCount = 0
            while True:
                args = self.getArgs()
                # user_agentid = args["user_agent_id"]
                user_agent_id = args["user_agent_id"]
                repo_cate_id = args["repo_cate_id"]
                time_delay = args["time_delay"]
                time_delay = time_delay.split( "-" )
                try:
                    time_delayStart = int( time_delay[0] )
                    time_delayEnd = int( time_delay[1] )
                except:
                    print  u"参数格式有误"
                    time_delayStart = 3
                    time_delayEnd = 5

                #测试
                # repo_cate_id = "337"
                numbers = Repo( ).GetAccount( "normal",repo_cate_id, 0, 1 )
                if len( numbers ) == 0:
                    print u"%s号仓库没有数据,等待5分钟" % repo_cate_id
                    time.sleep(300)
                    return


                account = numbers[0]['number']  # 即将登陆的QQ号
                password = numbers[0]['password']
                # accountArr = account.split("@")
                # account2 = accountArr[0] + "%40" + accountArr[1]
                # user_agent = numbers[0]['imei']
                # if user_agent!=u"":
                #     print "user_agent%s"%user_agent
                changeCount = changeCount + 1
                # if user_agent is None or user_agent == '':
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
                    driver.close()
                    driver.quit()
                except:
                    pass
                # display = Display( visible=0, size=(800, 600) )
                # display.start( )
                options = webdriver.ChromeOptions( )
                options.add_argument( 'disable-infobars' )
                options.add_argument( 'lang=zh_CN.UTF-8' )
                # options.add_argument( 'headless' )
                # 更换头部
                # options.add_argument(user_agent)
                options.add_argument('user-agent="%s'%user_agent )
                driver = webdriver.Chrome( chrome_options=options,executable_path="/opt/google/chrome/chromedriver")

                driver.get( r'https://qiye.163.com/login/?from=ym' )
                time.sleep(2)

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
                    driver.find_element_by_id( "accname" ).send_keys( account )
                    driver.find_element_by_id( "accpwd" ).send_keys( password )
                    # driver.save_screenshot( "222.png" )
                    time.sleep( 0.5 )
                    driver.find_element_by_id( "accpwd" ).send_keys( Keys.ENTER )
                    time.sleep( random.randint( time_delayStart, time_delayEnd ) )
                except:
                    pass

                if driver.current_url != "https://qiye.163.com/login/?from=ym":
                    # driver.find_element_by_xpath( '//*[@id="nav-mbox"]/div[1]/a[1]/div' )   #网易的logo

                    print u"%s  登陆成功" % account
                    # Repo( ).BackupInfo( repo_cate_id, 'normal', QQNumber, user_agent, '' )
                    startUrl = driver.current_url
                else:
                    print driver.page_source
                    print u"%s  登陆失败" % account

                    time.sleep( 2 )
                    # 登陆出现异常状况
                    errorPage = driver.page_source.encode( "utf-8" )
                    if "拖动下方滑块完成拼图" in errorPage:
                        print u"拖动下方滑块完成拼图"
                    elif "看不清" in errorPage:
                        print u"需要验证码"
                    elif "验证码" in errorPage:
                        print u"验证码"
                    elif "你的帐号存在安全隐患" in errorPage:
                        print u"你的帐号存在安全隐患"
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    elif "帐号或密码不正确" in errorPage:
                        print u"帐号或密码不正确"
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "frozen", account, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    elif "冻结" in errorPage:
                        print u"冻结"
                        self.repo.BackupInfo( repo_cate_id, 'frozen', account, '', '' )
                        # driver.get(
                        #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #         repo_cate_id, "frozen", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                repo_cate_id, "frozen", account, "", "")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep(3)
                    elif "请输入完整的成员帐号，包括域名。" in errorPage:
                        print  u"%s 冻结" % account
                        try:
                            # self.repo.BackupInfo(repo_cate_id, 'frozen', account, '', '')
                            # driver.get(
                            #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            #         repo_cate_id, "frozen", account, "", ""))
                            path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                repo_cate_id, "frozen", account, "", "")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                        except:
                            pass
                    else:
                        driver.save_screenshot("%s-%s.png"%(account,self.GetUnique()))
                    try:
                        obj = driver.find_element_by_class_name( "content" )
                        #driver.save_screenshot( "aaa.png" )

                        # Repo().BackupInfo( repo_cate_id, 'frozen', QQNumber, '', '' )
                    except:
                        time.sleep( 2 )
                        #driver.save_screenshot( "%s.png"%(account) )
                    continue

                # driver.get( startUrl )
                # time.sleep(1)
                startUrl = startUrl.replace("http://mail.ym.163.com/jy5","http://mail.ym.163.com/jy3")
                driver.get(startUrl)
                try:
                    driver.switch_to_frame('folder')
                    driver.find_element_by_xpath('/html/body/div/div/div/table/tbody/tr[1]/td/h1/a[2]/b[2]').click()
                    time.sleep(1)
                except:
                    pass

                # flag = False
                flag = True
                count_Y = 0
                while flag:
                # for i in  range(0,17):
                    args = self.getArgs( )
                    emailType = args["emailType"]
                    repo_material_cateId2 = args["repo_material_cateId2"]
                    repo_material_cateId = args["repo_material_cateId"]
                    sendTime = args["sendTime"]
                    sendTime = sendTime.split( "-" )
                    try:
                        sendTimeStart = int( sendTime[0] )
                        sendTimeEnd = int( sendTime[1] )
                    except:
                        print  u"发送时间间隔的参数格式有误"
                        sendTimeStart = 3
                        sendTimeEnd = 5
                    sleepTime = args["sleepTime"]
                    sleepTime = sleepTime.split( "-" )
                    try:
                        sleepTime_Start = int( sleepTime[0] )
                        sleepTime_delayEnd = int( sleepTime[1] )
                    except:
                        print  u"参数格式有误"
                        sleepTime_Start = 10
                        sleepTime_delayEnd = 15
                    repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
                    bccCount = args["bccCount"]
                    my_userCount = args["my_userCount"]
                    emailnumbers = Repo( ).GetNumber( repo_number_cate_id, 0, my_userCount )  # 取出add_count条两小时内没有用过的号码
                    emailnumberArr = []
                    if len( emailnumbers ) == 0 and my_userCount > 0:
                        print u"QQ号码库%s号仓库为空" % repo_number_cate_id
                        time.sleep( 100 )
                        try:
                            driver.close( )
                            driver.quit( )
                        except:
                            pass
                        return
                    else:
                        for item in emailnumbers:
                            emailnumberArr.append( item['number'] )

                    # emailnumber = emailnumbers[0]['number']

                    bccnumbers = self.repo.GetNumber( repo_number_cate_id, 0, bccCount )  # 取出add_count条两小时内没有用过的号码
                    bccnumberArr = []
                    if len( bccnumbers ) == 0 and bccCount > 0:
                        print u"QQ号码库%s号仓库为空" % repo_number_cate_id
                        if my_userCount == 0:
                            time.sleep( 100 )
                            try:
                                driver.close( )
                                driver.quit( )
                            except:
                                pass
                            return
                    else:
                        for item in bccnumbers:
                            bccnumberArr.append( item['number'] )

                    if repo_material_cateId == "" or repo_material_cateId is None:
                        selectContent1 = ""
                    else:
                        selectContent1 = "只发主题"
                        Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                        if len( Material ) == 0:
                            print u"%s  号仓库为空，没有取到消息" % repo_material_cateId
                            try:
                                driver.close( )
                                driver.quit( )
                            except:
                                pass
                            return
                        message = Material[0]['content']
                    if repo_material_cateId2 == "" or repo_material_cateId2 is None:
                        selectContent2 = ""
                    else:
                        selectContent2 = "只发内容"
                        Material2 = self.repo.GetMaterial( repo_material_cateId2, 0, 1 )
                        if len( Material2 ) == 0:
                            # print "%s号仓库为空，没有取到消息" % repo_material_cateId
                            try:
                                driver.close( )
                                driver.quit( )
                            except:
                                pass
                            return
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
                        time.sleep( 2 )
                        driver.switch_to_default_content( )
                        driver.switch_to_frame( 'foldmain' )  # 需先跳转到iframe框架
                        time.sleep( 1 )
                        emailnumberObj = driver.find_element_by_xpath( '//*[@id="subject"]' )  # 定位到主题
                        # emailnumberObj = driver.find_element_by_xpath( '//*[@id="toAreaCtrl"]' )
                    except:
                        pass

                    if selectContent1 == "只发主题":
                        try:
                            # emailnumberObj.send_keys( Keys.TAB )
                            emailnumberObj.send_keys( message )
                            time.sleep( 0.5 )
                        except:
                            pass

                    bccObj = driver.find_element_by_xpath( '//*[@id="bccHref"]' )
                    text = bccObj.get_attribute( "text" ).encode( "utf-8" )
                    if text == "删除密送":
                        bccObj.click( )

                    j = 2
                    emailnumberArr = ['2351382894@qq.com']
                    eArr = ""
                    for emailnumber in emailnumberArr:
                        if "@" not in emailnumber:
                            # emailnumber = "455854284"
                            if emailType == "QQ邮箱":
                                eArr = eArr + emailnumber + "@qq.com;"
                                # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input'%j).send_keys( emailnumber + "@qq.com;" )
                            elif emailType == "189邮箱":
                                eArr = eArr + emailnumber + "@189.cn;"
                                # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input' % j).send_keys( emailnumber + "@189.cn;" )
                            elif emailType == "139邮箱":
                                eArr = eArr + emailnumber + "@139.com;"
                                # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input' % j).send_keys( emailnumber + "@139.com;" )
                            elif emailType == "163邮箱":
                                eArr = eArr + emailnumber + "@163.com;"
                                # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input' % j).send_keys( emailnumber + "@163.com;" )
                            elif emailType == "wo邮箱":
                                eArr = eArr + emailnumber + "@wo.cn;"
                                # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input' % j).send_keys( emailnumber + "@wo.cn;" )
                            else:
                                eArr = eArr + emailnumber + "@qq.com;"
                                # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input' % j).send_keys( emailnumber + "@qq.com;" )
                        else:
                            eArr = eArr + emailnumber + ";"
                            # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input' % j).send_keys( emailnumber + ";"  )
                        j = j + 1
                    # driver.save_screenshot( "mmm.png" )
                    emailnumberObj.click( )
                    emailnumberObj.send_keys( Keys.SHIFT, Keys.TAB, Keys.SHIFT, eArr )
                    # time.sleep( 2 )
                    emailnumberObj.click( )
                    # time.sleep( 1 )
                    bccstr = ""
                    if bccnumberArr != []:
                        # if count_Y == 0:
                        bccObj.click( )
                        time.sleep( 0.5 )
                        j = 2

                        for bcc in bccnumberArr:
                            if "@" not in emailnumber:
                                # emailnumber = "455854284"
                                if emailType == "QQ邮箱":
                                    bccstr = bccstr + bcc + "@qq.com;"
                                    # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input'%j).send_keys( emailnumber + "@qq.com;" )
                                elif emailType == "189邮箱":
                                    bccstr = bccstr + bcc + "@189.cn;"
                                    # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input' % j).send_keys( emailnumber + "@189.cn;" )
                                elif emailType == "139邮箱":
                                    bccstr = bccstr + bcc + "@139.com;"
                                    # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input' % j).send_keys( emailnumber + "@139.com;" )
                                elif emailType == "163邮箱":
                                    bccstr = bccstr + bcc + "@163.com;"
                                    # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input' % j).send_keys( emailnumber + "@163.com;" )
                                elif emailType == "wo邮箱":
                                    bccstr = bccstr + bcc + "@wo.cn;"
                                    # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input' % j).send_keys( emailnumber + "@wo.cn;" )
                                else:
                                    bccstr = bccstr + bcc + "@qq.com;"
                                    # driver.find_element_by_xpath('//*[@id="oDivTo"]/div[%s]/input' % j).send_keys( emailnumber + "@qq.com;" )
                            else:
                                bccstr = bccstr + bcc + ";"
                            j = j + 1
                    emailnumberObj.click( )
                    emailnumberObj.send_keys( Keys.SHIFT, Keys.TAB, Keys.SHIFT, bccstr )

                    # time.sleep(2)
                    driver.switch_to_frame( 'editor' )
                    driver.find_element_by_xpath('//*[@id="dvToobar"]/div[2]/a[2]').click()
                    # time.sleep(1.5)

                    driver.find_element_by_xpath( '//*[@id="dvToobarFull"]/div[1]/div[7]/a' ).click( )
                    if selectContent2 == "只发内容":

                        # # frame = driver.find_element_by_xpath()
                        # # driver.switch_to_frame(frame)
                        # driver.switch_to_frame( 'HtmlEditor' )
                        # time.sleep(2)
                        # js = "setMailEditorContentHtml('%s') ;" % message2.encode("utf-8")
                        # # js = "var x = setMailEditorContentHtml(\"<h1>Hi</h1> <sapn id='s'></sapn>\");"
                        # # js = "setMailEditorContentHtml('<h1>Hi</h1> <span style=\"font-size:1px\">乓</span>ｖ<span>乓</span>的发<v>sdfs</v>送ｖ发财<sapn id=\"s\"></sapn>');"
                        # # js = "setMailEditorContentHtml('<h1>Hi</h1> <sapn style="font-size:0px">456825</sapn>');"
                        #
                        # try:
                        #     driver.execute_script( js )
                        # except Exception,e:
                        #     print e
                        # time.sleep(2)
                        driver.switch_to_default_content( )
                        driver.switch_to_frame( 'foldmain' )  # 需先跳转到iframe框架
                        # time.sleep( 1 )
                        emailnumberObj.click()
                        emailnumberObj.send_keys(Keys.TAB,Keys.CONTROL,'a',Keys.CONTROL,message2)
                        # emailnumberObj.send_keys(Keys.TAB,Keys.CONTROL,'v')
                        # time.sleep(2)
                        # emailnumberObj.click( )
                        # emailnumberObj.send_keys( Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,
                        #                           Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,
                        #                           Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,Keys.TAB,message2 )
                        # time.sleep(0.5)
                    driver.switch_to_frame( 'editor' )
                    driver.find_element_by_xpath('//*[@id="dvToobarFull"]/div[1]/div[7]/a').click()
                    time.sleep(0.5)

                    # time.sleep( 1 )
                    try:
                        driver.switch_to_default_content( )
                        driver.switch_to_frame( 'foldmain' )  # 需先跳转到iframe框架
                        driver.find_element_by_xpath('//*[@id="oSendButton1"]').click()
                    except:
                        emailnumberObj.send_keys( Keys.TAB )
                        emailnumberObj.send_keys( Keys.ENTER )
                    time.sleep( random.randint( sendTimeStart, sendTimeEnd ) )

                    # try:
                    #     try:
                    #         driver.find_element_by_id("composeSend")
                    #     except:
                    #         driver.find_element_by_name("RedirectY29tcG9zZV9zZW5kP21vYmlsZXNlbmQ9MSZzPQ__")
                    #     time.sleep(3)
                    #
                    # except:
                    #     pass

                    try:
                        driver.switch_to_frame('iframeForSave')
                    except:
                        pass
                    page_source = driver.page_source.encode("utf-8")
                    if "邮件已成功发送！" in page_source and "验证码" not in page_source:
                        try:
                            emailnumberObj = driver.find_element_by_xpath( '//*[@id="subject"]' )
                            try:
                                driver.switch_to_frame('leftFrame')
                            except:
                                pass
                            path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                            emailnumber, repo_number_cate_id, "normal")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                            time.sleep( 1 )
                            path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                repo_cate_id, "using", account, "", "")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                            time.sleep( 3 )
                            errorHtml = driver.page_source
                            if "验证码" in errorHtml:
                                print u'验证码'
                                time.sleep(random.randint(5,10))
                            if "您的帐号因频繁发送广告或垃圾邮件，已被禁止发信。" in errorHtml:
                                print u'您的帐号因频繁发送广告或垃圾邮件，已被禁止发信'
                                flag = False
                                print "点击发送还在原界面"
                                path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                    emailnumber, repo_number_cate_id, "normal")
                                conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                conn.request( "GET", path )
                                time.sleep(1)
                                flagFirst2 = True
                            else:
                                count_Y = count_Y + 1
                                if count_Y>=2:
                                    flag = False
                                else:
                                    time.sleep( random.randint( 5, 10 ) )
                        except:
                            count_Y = 0
                            print u"%s发送成功给%s,%s" % (account, eArr, bccstr)
                            flagFirst = False
                            flagFirst2 = False
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
                        #             "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                        #             emailnumber, repo_number_cate_id, "normal"))
                        #     except:
                        #         pass
                        #
                        # except:
                        #     print u"发送成功"
                        #     flagFirst = False
                        #     count = 0
                    else:

                        path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                            emailnumber, repo_number_cate_id, "normal")
                        conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                        conn.request( "GET", path )
                        try:
                            if "验证码" in page_source:
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
                            elif "操作过于频繁，请求被拒绝" in page_source:
                                print u"操作过于频繁，请求被拒绝"
                                flag = False
                            elif "对不起，您今天发送邮件数量超过限制，请明日再试" in page_source:
                                print u"对不起，您今天发送邮件数量超过限制，请明日再试"
                                flag = False
                            elif "邮件中可能包含不合适的用语或内容" in page_source:
                                sc = 0
                                flag = False

                                print u"%s  邮件中可能包含不合适的用语或内容"%account
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
                                # driver.get("http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                #     repo_cate_id, "exception", account, "", ""))
                                path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                    repo_cate_id, "exception", account, "", "")
                                conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                conn.request( "GET", path )
                                time.sleep( 3 )
                            elif "您的帐号存在安全隐患" in page_source:
                                sc = 0
                                flag = False
                                print u"您的帐号存在安全隐患"
                                # self.repo.BackupInfo(repo_cate_id, 'frozen', account, '', '')
                                # driver.get(
                                #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                #         repo_cate_id, "frozen", account, "", ""))
                                path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                        repo_cate_id, "frozen", account, "", "")
                                conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                conn.request( "GET", path )
                                time.sleep( 3 )
                            else:
                                driver.find_element_by_class_name( "qm_icon_Compose" )
                                sc = sc + 1
                                if sc >= 20:
                                    flag = False
                                    sc = 0
                                print u"%s发送成功2"%account
                                flagFirst = False
                                flagFirst2 = False
                        except:

                            try:
                                # self.repo.UpdateNumberStauts(emailnumber, repo_number_cate_id, "normal")
                                # driver.get(
                                #     "http://data.zunyun.net/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                #     emailnumber, repo_number_cate_id, "normal"))
                                path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                                    emailnumber, repo_number_cate_id, "normal")
                                conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                conn.request( "GET", path )
                                time.sleep( 1 )
                            except:
                                pass
                                print u"%s发送失败给%s,%s" % (account, eArr, bccstr)
                            sc = 0
                            flag = False
                            if "验证码" in page_source:
                                print u"需要验证码"
                                flagFirst = False
                                count = count + 1
                                if count >= 2:
                                    # self.ipChange.ooo()
                                    # self.ipChange.ooo()
                                    time.sleep(3)
                                    count = 0
                            if "邮件中可能包含不合适的用语或内容" in page_source:
                                print u"%s  邮件中可能包含不合适的用语或内容"%account
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
                                #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                #     repo_cate_id, "exception", account, "", ""))
                                path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                    repo_cate_id, "exception", account, "", "")
                                conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                conn.request( "GET", path )
                                time.sleep(3)
                            elif "您的帐号存在安全隐患" in page_source:
                                print u"您的帐号存在安全隐患"
                                # self.repo.BackupInfo(repo_cate_id, 'exception', account, '', '')
                                # driver.get(
                                #     "http://data.zunyun.net/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                #         repo_cate_id, "frozen", account, "", ""))
                                path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                        repo_cate_id, "frozen", account, "", "")
                                conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                                conn.request( "GET", path )
                                time.sleep(3)
                            else:
                                print page_source
                                # driver.save_screenshot( "%s-%s.png" % (account, self.GetUnique( )) )
                                print "error"
                    if flagFirst:
                        try:
                            # self.repo.AccountFrozenTimeDelay(account, repo_cate_id)
                            # driver.get(
                            #     "http://data.zunyun.net/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                            #         account, repo_cate_id,"PT_QQ"))
                            path = "/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                                    account, repo_cate_id,"PT_QQ")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                            time.sleep(1)
                        except:
                            pass
                    if flagFirst2:
                        try:
                            # driver.get("http://data.zunyun.net/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                            #         account, repo_cate_id, "PT_QQ") )
                            path = "/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
                                account, repo_cate_id, "PT_QQ")
                            conn = httplib.HTTPConnection( "data.zunyun.net", None, timeout=30 )
                            conn.request( "GET", path )
                        except:
                            pass
                    driver.get( startUrl )
                    time.sleep(2)
                    try:
                        driver.switch_to_frame( 'folder' )
                        driver.find_element_by_xpath(
                            '/html/body/div/div/div/table/tbody/tr[1]/td/h1/a[2]/b[2]' ).click( )
                        time.sleep( 1 )
                    except:
                        pass

                # 删除邮件
                driver.get( startUrl )
                try:
                    driver.switch_to_frame('folder')
                    time.sleep(1)
                except:
                    print "dsad"
                floders = ['//*[@id="lnk1"]','//*[@id="lnk2"]','//*[@id="lnk3"]','//*[@id="lnk4"]','//*[@id="lnk5"]']
                for floder in floders:
                    driver.find_element_by_xpath( floder ).click( )
                    driver.switch_to_default_content( )
                    driver.switch_to_frame( 'foldmain' )  # 需先跳转到iframe框架
                    time.sleep( 1 )
                    while True:
                        try:
                            if "没有 任何邮件" in driver.page_source.encode("utf-8"):
                                break
                            driver.find_element_by_xpath( '//*[@id="oFormCheckAll"]' ).click()
                            time.sleep(2)
                            # driver.find_element_by_xpath( '//*[@id="oFormMessage"]/div/div/div[2]/input[1]' ).click()
                            try:
                                driver.find_element_by_xpath( '//*[@id="oFormMessage"]/div/div/div[2]/input[1]' ).send_keys(Keys.ENTER,Keys.ENTER)
                            except:
                                pass
                            # driver.find_element_by_xpath('// *[ @ id = "quick_completelydel"]').click()
                            # time.sleep(0.5)
                            # # driver.switch_to_frame( 'actionFrame' )  # 需先跳转到iframe框架
                            # driver.find_element_by_xpath( '//*[@id="QMconfirm_QMDialog_confirm"]' ).click()
                            time.sleep( 2 )
                            # driver.find_element_by_xpath(floder ).send_keys( Keys.CONTROL, 'a' )
                            # driver.find_element_by_xpath( floder).send_keys(Keys.DELETE)
                        except:
                            break
                    driver.get( startUrl )
                    time.sleep(1)
                    try:
                        driver.switch_to_frame( 'folder' )
                        time.sleep( 1 )
                    except:
                        print "dsad"

                # if not flag:
                #     try:
                #         driver.delete_all_cookies()
                #     except:
                #         pass
                #     if changeCount >= 5:
                #         # self.ipChange.ooo()
                #         # self.ipChange.ooo()
                #         time.sleep(3)
                #         changeCount = 0


                # 退出帐号重新登陆
                try:
                    # for handle in driver.window_handles:  # 方法二，始终获得当前最后的窗口
                    #     driver.switch_to_window( handle )
                    #     driver.close()
                    time.sleep( 2 )
                    if changeCount >= 5:
                        # self.ipChange.ooo()
                        # self.ipChange.ooo()
                        time.sleep(3)
                        changeCount = 0
                    # IPChange().ooo()
                    # IPChange().ooo()
                    # time.sleep(3)
                    # driver.save_screenshot( "exit.png" )
                    driver.delete_all_cookies()
                except:
                    if changeCount >= 5:
                        # self.ipChange.ooo()
                        # self.ipChange.ooo()
                        time.sleep(3)
                        changeCount = 0
                    # driver.save_screenshot("exceptionError.png")
                    # driver.save_screenshot("444.png")
                    print "error"


        except:
            logging.exception( "Exception" )
            try:
                driver.close( )
                driver.quit( )
            except:
                pass

            return []

    def action(self):
        # data = self.ipChange.Check_for_Broadband()
        # if data != None:
        #     print u"宽带确认已连接,模块继续运行"
        # else:
        #     print u"宽带未连接,连接宽带"
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
        args = self.getArgs( )
        phonenumber = args["phonenumber"]
        cateId = args["cateId"]
        para = {"phoneNumber": phonenumber, "x_04": sta}
        self.repo.PostInformation( cateId, para )


def getPluginClass():
    return YM_WY

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()
    # time.sleep(150)
    import socket

    while True:
        try:
            o.action()
        except:
            logging.exception("Exception")