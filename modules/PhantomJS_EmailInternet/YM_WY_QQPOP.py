# coding:utf-8
from __future__ import division
import base64
import httplib
import logging
import poplib
import re
import socket
import urllib2

import win32api
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import phantomjs


import os, time, datetime, random
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


sys.path.append("C:\TaskConsole-master")
from IPChange import IPChange
from Repo import Repo
from WaterMark import WaterMark
import win32clipboard as w
import win32con

#网易发信，QQ POP收信
class YM_WY_QQPOP:
    def __init__(self):
        self.repo = Repo()
        self.ipChange = IPChange()
        self.wateMark = WaterMark()
        self.ipChangeFlag = True
        self.ipCount = int(self.getArgs()["ipCount"])

    def GetUnique(self):
        num = ""
        for i in range(0, random.randint(1, 8)):
            n = random.choice("qwertyuiopasdfghjklzxcvbnm")
            num = n + num
        for i in range(0, random.randint(1, 5)):
            n = random.choice("0123456789")
            num = num + n

        return num

    def getTime(self, timeType):
        path = "/cgi-bin/cgi_svrtime"
        conn = httplib.HTTPConnection("cgi.im.qq.com", None, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        data = response.read().replace("\n", "")
        #if response.status == 200:
         #   data = response.read()
        #else:
         #   print u"http://cgi.im.qq.com/cgi-bin/cgi_svrtime 失效了"
          #  return ""
        timea = datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        if timeType == "EnTime":
            return timea.strftime("%a, %b %d,  %Y %I:%M %p")
        elif timeType == "CnTime":
            nt = timea
            w = ""
            weekday = nt.weekday()
            if weekday == 0:
                w = "星期一"
            elif weekday == 1:
                w = "星期二"
            elif weekday == 2:
                w = "星期三"
            elif weekday == 3:
                w = "星期四"
            elif weekday == 4:
                w = "星期五"
            elif weekday == 5:
                w = "星期六"
            elif weekday == 6:
                w = "星期日"
            p = nt.strftime("%p")
            if p == "PM" or p == "pm":
                p = "下午"
            else:
                p = "上午"

            nowtime = nt.strftime('%Y年%m月%d日%I:%M')
            nowtime = nowtime.replace("日", "日 (%s) %s" % (w, p))
            return nowtime
        else:
            return timea.strftime("%a, %b %d,  %Y %I:%M %p")

    #附件
    def getImg(self,driver):
        imgName = self.GetUnique()
        imgpath = r"C:\water"
        if not os.path.exists(imgpath ):
            return
        g = os.listdir(imgpath)

        for i in g:
            name = i.split(".")
            os.rename(imgpath + "\%s" % i, imgpath + "\%s.%s" % (imgName, name[1]))
            imgpath = imgpath + "\%s.%s" % (imgName,name[1])
            try:
                fileInputs = driver.find_elements_by_xpath('//input[@class="js-attach-native"]')
                for fileInput in fileInputs:
                    if fileInput.get_attribute("type")== "file":
                        fileInput.send_keys(imgpath)
                time.sleep(5)
                return
            except:
                pass

        return imgpath

    # 写入剪切板内容
    def settext(self,aString):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_TEXT, aString)
        w.CloseClipboard()

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

    def getArgs(self):
        # asdlFile = open( r"/home/zunyun/text/asdl.txt", "r" )
        asdlFile = open( r"c:\asdl.txt", "r" )
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
            sendCount = task["x11"]
            enailLoop = task["x12"]
            auto_rp_cate_id = task["x13"]
            auto_loop = task["x14"]
            if my_userCount is None or my_userCount == "" or my_userCount == 0 or my_userCount == "0":
                my_userCount = 0
            else:
                my_userCount = int(my_userCount)

            if bccCount is None or bccCount == "":
                bccCount = 0
            else:
                bccCount = int(bccCount)
            fj = ""
            trainCateId = ''
            name_cate_id = ''
            ipCount = 1
            popFlag = True
            accountLockTime= "130"
            if sendCount is None or sendCount == "" or sendCount=="0":
                sendCount = 0
                print u"发信个数为0，默认为3"
            else:
                try:
                    sendCount = int(sendCount)
                except:
                    sendCountArr = sendCount.split("-")
                    if len(sendCountArr)>=8:
                        sendCount = sendCountArr[0]
                        name_cate_id = sendCountArr[1]
                        fj = sendCountArr[2]
                        trainCateId = sendCountArr[3]
                        msgCateId = sendCountArr[4]
                        ipCount = int(sendCountArr[5])
                        if sendCountArr[6]:
                            if sendCountArr[6].upper()=="Y":
                                popFlag = True
                            else:
                                popFlag = False
                        else:
                            popFlag = True
                        accountLockTime = sendCountArr[7]
                    else:
                        print u"参数错误"
                        time.sleep(60)
                        return
            if fj == "" or fj.upper()=="Y":
                flFlag = True
            else:
                flFlag = False

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
            lockTimes = param["x05"]
            if sleepTime is None or sleepTime == '':
                sleepTime = "10-15"
            lockTime = 1440
            sendSleep = 60
            if lockTimes:
                try:
                    lockTimeArr = lockTimes.split("-")
                    if len(lockTimeArr)>1:
                        lockTime = int(lockTimeArr[0])
                        sendSleep = int(lockTimeArr[1])
                except:
                    pass

            args = {"time_delay": time_delay, "sendTime": sendTime, "repo_cate_id": repo_cate_id,
                    "repo_number_cate_id": repo_number_cate_id, "repo_material_cateId": repo_material_cateId,
                    "repo_material_cateId2": repo_material_cateId2, "emailType": emailType,
                    "user_agent_id": user_agent_id,"phonenumber":phonenumber,"cateId":cateId,"my_userCount":my_userCount,
                    "bccCount":bccCount,"sleepTime":sleepTime,"sendCount":sendCount,"name_cate_id":name_cate_id,"flFlag":flFlag,"lockTime":lockTime,"sendSleep":sendSleep,"enailLoop":enailLoop
                    ,"auto_rp_cate_id":auto_rp_cate_id,"auto_loop":auto_loop,"trainCateId":trainCateId,"msgCateId":msgCateId,"ipCount":ipCount,"popFlag":popFlag,"accountLockTime":accountLockTime}  # cate_id是仓库号，length是数量
            return args

    def getAccount(self,status,cateId, interval, limit, condition,lockTime):
        domain = "data.161998.com"
        port = None
        path = "/repo_api/account/pick?status=%s&cate_id=%s&interval=%s&limit=%s&condition=%s&recover=%s" % (
        status, cateId, interval, limit, condition,"1")
        conn = httplib.HTTPConnection(domain, port, timeout=30)
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            numbers = json.loads(data)
            if len(numbers)>0:
                account = numbers[0]['number']  # 即将登陆的QQ号
                password = numbers[0]['password']
                ym = "@" + account.split("@")[1]
                path = "/repo_api/account/updateTime?cateId=%s&number=%s" % (cateId, ym)
                conn = httplib.HTTPConnection(domain, port, timeout=30)
                conn.request("GET", path)
                time.sleep(3)
                path = "/repo_api/account/timeDelay?cate_id=%s&number=%s&numberType=PT_QQ&status=&QQTimeDelay=%s" % (cateId, account, lockTime)
                conn = httplib.HTTPConnection(domain, port, timeout=30)
                conn.request("GET", path)
                time.sleep(3)
                return numbers
            else:
                return []

        else:
            return []

    def getFilePath(self,path):
        if not os.path.exists(path):
            return
        g = os.listdir(path)
        if len(g) > 0:
            b = random.randint(0, len(g) - 1)
            path = path + "\\" + g[b]
        else:
            print u"没有图片或视频"
            return
        return path

    def sendImg(self,driver,fileType):
        if fileType == "img":
            path = self.getFilePath(r"C:\water")
        else:
            path  = self.getFilePath(r"C:\waterVideo")
        if path != None and path != r"C:\water":
            #video = driver.find_element_by_xpath('//*[@id="AttachFrame"]/span')
            #video.send_keys(imgpath)
            self.settext(path)
            #video.send_keys(Keys.CONTROL, 'a')  # selenium的send_keys（ctrl+a）
            #video.send_keys(Keys.CONTROL, 'x')  # (ctrl+x)
            try:
                driver.find_element_by_xpath('//*[@title="添加图片"]').click()
                time.sleep(0.5)
                driver.find_elements_by_xpath('//div[@class="edui-box edui-label edui-menuitem-label  edui-default"]')[0].click()
                time.sleep(5)
            except:
                logging.exception("a")

            # 粘贴（ctrl + v）
            try:
                win32api.keybd_event(17, 0, 0, 0)  # 按下按键 ctrl
                # time.sleep(3)
                win32api.keybd_event(86, 0, 0, 0)  # 按下按键 v
                # time.sleep(3)
                win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 升起按键 v
                # time.sleep(3)
                win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 升起按键 ctrl
                time.sleep(1)

                # 回车（enter）
                win32api.keybd_event(13, 0, 0, 0)  # 按下按键 enter
                win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)  # 升起按键 enter
            except:
                pass

    def sendMsg(self,driver,account,accountCateId,repo_number_cate_id,bccCount,my_userCount,loop,msgCateFlag=False):
        args = self.getArgs()
        emailType = args["emailType"]
        repo_material_cateId2 = args["repo_material_cateId2"]
        repo_material_cateId = args["repo_material_cateId"]
        sendTime = args["sendTime"]
        sendTime = sendTime.split("-")
        try:
            sendTimeStart = int(sendTime[0])
            sendTimeEnd = int(sendTime[1])
        except:
            print  u"发送时间间隔的参数格式有误"
            sendTimeStart = 3
            sendTimeEnd = 5
        sleepTime = args["sleepTime"]
        sleepTime = sleepTime.split("-")
        try:
            sleepTime_Start = int(sleepTime[0])
            sleepTime_delayEnd = int(sleepTime[1])
        except:
            print  u"参数格式有误"
            sleepTime_Start = 10
            sleepTime_delayEnd = 15
        if "@" not in repo_number_cate_id:
            emailnumbers = Repo().GetNumber(repo_number_cate_id, 0, my_userCount)  # 取出add_count条两小时内没有用过的号码
            emailnumberArr = []
            if len(emailnumbers) == 0 and my_userCount > 0:
                while len(emailnumbers) == 0:
                    if loop == "true" or loop is True:
                        print u"%s 号仓库没有数据可用,自动恢复循环取" % repo_number_cate_id
                        path = "/repo_api/receive/emptyCate?cate_id=%s" % (
                            repo_number_cate_id)
                        conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                        conn.request("GET", path)
                        time.sleep(20)
                        emailnumbers = self.repo.GetNumber(repo_number_cate_id, 0, my_userCount)
                    else:
                        print u"%s号仓库没有数据" % repo_number_cate_id
                        break
            else:
                for item in emailnumbers:
                    emailnumberArr.append(item['number'])

            # emailnumber = emailnumbers[0]['number']

            bccnumbers = self.repo.GetNumber(repo_number_cate_id, 0, bccCount)  # 取出add_count条两小时内没有用过的号码
            bccnumberArr = []
            if len(bccnumbers) == 0 and bccCount > 0:
                while len(bccnumbers) == 0:
                    if loop == "true" or loop is True:
                        print u"%s 号仓库没有数据可用,自动恢复循环取" % repo_number_cate_id
                        path = "/repo_api/receive/emptyCate?cate_id=%s" % (
                            repo_number_cate_id)
                        conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                        conn.request("GET", path)
                        time.sleep(20)
                        bccnumbers = self.repo.GetNumber(repo_number_cate_id, 0, bccCount)
                    else:
                        print u"%s号仓库没有数据" % repo_number_cate_id
                        break
            else:
                for item in bccnumbers:
                    bccnumberArr.append(item['number'])

        else:
            emailnumberArr = [repo_number_cate_id]
            bccnumberArr = []

        if repo_material_cateId == "" or repo_material_cateId is None:
            selectContent1 = ""
        else:
            selectContent1 = "只发主题"
            Material = self.repo.GetMaterial(repo_material_cateId, 0, 1)
            if len(Material) == 0:
                print u"%s  号仓库为空，没有取到消息" % repo_material_cateId
                try:
                    driver.close()
                    driver.quit()
                except:
                    pass
                return
            message = Material[0]['content']
        if msgCateFlag:
            repo_material_cateId2 = args["msgCateId"]
        if repo_material_cateId2 == "" or repo_material_cateId2 is None:
            selectContent2 = ""
        else:
            selectContent2 = "只发内容"
            Material2 = self.repo.GetMaterial(repo_material_cateId2, 0, 1)
            if len(Material2) == 0:
                # print "%s号仓库为空，没有取到消息" % repo_material_cateId
                try:
                    driver.close()
                    driver.quit()
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
            time.sleep(2)
            # driver.switch_to_default_content()
            # driver.switch_to_frame( 'foldmain' )  # 需先跳转到iframe框架
            # time.sleep(1)
            # emailnumberObj = driver.find_element_by_xpath( '//*[@id="subject"]' )   #定位到主题
            emailnumberObj = driver.find_element_by_xpath('//input[@name="subject"]')
        except:
            pass

        if selectContent1 == "只发主题":
            try:
                # emailnumberObj.send_keys( Keys.TAB )
                emailnumberObj.send_keys(message)
                time.sleep(0.5)
            except:
                pass

        # bccObj = driver.find_element_by_xpath( '//*[@id="bccHref"]' )
        try:
            bccObj = driver.find_element_by_xpath('//a[@name="bcc"]')
            text = bccObj.get_attribute("text").encode("utf-8")
            if text == "删除密送":
                bccObj.click()
        except:
            pass

        j = 2
        # emailnumberArr = ['33367718@qq.com']
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
        # emailnumberObj.click()
        try:
            driver.find_element_by_xpath('//div[@name="to"]/div[1]/input').send_keys(eArr)
        except:
            pass
        # eArrInput = driver.find_element_by_css_selector('right.input-focus').find_element_by_xpath("//div[@class='right-inner']")
        # driver.find_element_by_xpath('//*[@id="module_compose_1521875647544"]/div[2]/div/div/div[3]/div/div[1]/div[2]/div[2]/div/div/div[1]/input')
        # emailnumberObj.send_keys(Keys.SHIFT, Keys.TAB, Keys.SHIFT,eArr)
        time.sleep(2)
        emailnumberObj.click()
        time.sleep(1)
        bccstr = ""
        if bccnumberArr != []:
            # if count_Y == 0:
            bccObj.click()
            time.sleep(2)
            j = 2

            for bcc in bccnumberArr:
                if "@" not in bcc:
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
            emailnumberObj.click()
            driver.find_element_by_xpath('//div[@name="bcc"]/div[1]/input').send_keys(bccstr)
            # emailnumberObj.send_keys( Keys.SHIFT, Keys.TAB, Keys.SHIFT, bccstr )
            time.sleep(2)

        time.sleep(0.5)
        driver.find_element_by_xpath('//a[@name="seprate"]').click()
        time.sleep(1)

        # message2 = 'dsf <video src="+videoUrl+"/>dfdsf'
        if "+imgUrl+" in message2 or "+videoUrl+" in message2:

            if "+imgUrl+" in message2:
                base64 = self.wateMark.getWatermarkBase64()
                self.sendImg(driver, "img")
            else:
                self.wateMark.getWatermarkVideo()
                self.sendImg(driver, "video")

            try:
                driver.switch_to_frame('ueditor_0')
            except:
                driver.switch_to_frame('ueditor_1')
            time.sleep(2)
            ps = driver.page_source
            try:
                srcArr = ps.split("/jy5/s?func=mbox:")[1]
            except:
                time.sleep(10)
                ps = driver.page_source
                srcArr = ps.split("/jy5/s?func=mbox:")[1]
            src = "/jy5/s?func=mbox:" + srcArr.split("\"")[0]
            if "+imgUrl+" in message2:
                message2 = message2.replace("+imgUrl+", src)
            else:
                message2 = message2.replace("+videoUrl+", src)
            driver.switch_to_default_content()
            time.sleep(2)
        driver.find_element_by_xpath('//*[@id="edui68_body"]/div').click()

        if selectContent2 == "只发内容":
            if "@" not in account:
                account2 = account + "@qq.com"
            else:
                account2 = account
            message2 = message2.replace("+FromMail+", account2)
            email = emailnumberArr[0]
            if "@" not in email:
                # emailnumber = "455854284"
                if emailType == "QQ邮箱":
                    email = email + "@qq.com "
                elif emailType == "189邮箱":
                    email = email + "@189.cn "
                elif emailType == "139邮箱":
                    email = email + "@139.com "
                elif emailType == "163邮箱":
                    email = email + "@163.com "
                elif emailType == "wo邮箱":
                    email = email + "@wo.cn "
                else:
                    email = email + "@qq.com "
            message2 = message2.replace("+ToMail+", email)
            message2 = message2.replace("+Subject+", message)
            while True:
                try:
                    message2 = message2.replace("+CnTime+", self.getTime("CnTime"))
                    break
                except:
                    pass
            while True:
                try:
                    message2 = message2.replace("+EnTime+", self.getTime("EnTime"))
                    break
                except:
                    pass
            # if imgpath != None and imgpath != "":
            if "+base64+" in message2:
                waterMark = self.wateMark.getWatermarkBase64()
                if waterMark != None:
                    message2 = message2.replace("+base64+", waterMark)

            message2 = message2.encode('GB18030')
            self.settext(message2)
            driver.find_element_by_xpath('//*[@id="edui1_iframeholder"]/textarea').clear()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="edui1_iframeholder"]/textarea').send_keys(Keys.CONTROL, 'v')
            # driver.find_element_by_xpath('//*[@id="edui1_iframeholder"]/textarea').send_keys(message2)
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="edui68_body"]/div').click()
            # time.sleep(300)
            # while "正在上传第" in driver.page_source:
            #     time.sleep(5)
            # 附件
            flFlag = args["flFlag"]
            if flFlag:
                watermarkBase64 = self.wateMark.getWatermarkBase64()
                self.getImg(driver)

            sendBtns = driver.find_elements_by_class_name("js-txt")
            for sendBtn in sendBtns:
                if sendBtn.text == "发送":
                    sendBtn.click()
                    break

                time.sleep(1)
        time.sleep(random.randint(sendTimeStart, sendTimeEnd))

        page_source = driver.page_source.encode("utf-8")
        if "邮件发送成功!" in page_source and "验证码" not in page_source:
            try:
                driver.find_element_by_xpath('//input[@name="subject"]').click()
                for it in emailnumberArr:
                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                        it, repo_number_cate_id, "normal")
                    conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                    conn.request("GET", path)
                    time.sleep(1)
                for it2 in bccnumberArr:
                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                        it2, repo_number_cate_id, "normal")
                    conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                    conn.request("GET", path)
                    time.sleep(1)
                print "点击发送还在原界面"
                errorHtml = driver.page_source
                if "验证码" in errorHtml:
                    print u'验证码'
                    time.sleep(random.randint(5, 10))
                if "您的帐号因频繁发送广告或垃圾邮件，已被禁止发信。" in errorHtml:
                    print u'您的帐号因频繁发送广告或垃圾邮件，已被禁止发信'
                    flag = False
                    flagFirst2 = True
                else:
                    time.sleep(random.randint(5, 10))
            except:
                count_Y = 0
                print u"%s发送成功给%s,%s" % (account, eArr, bccstr)
                if eArr == "":
                    return "True"
                return eArr.replace(";","")

        else:
            path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                emailnumber, repo_number_cate_id, "normal")
            conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
            conn.request("GET", path)
            try:
                if "验证码" in page_source:
                    print u"需要验证码"
                    flagFirst = True
                    sc = 0
                elif "邮件中可能包含不合适的用语或内容" in page_source:
                    sc = 0
                    flag = False

                    print u"%s  邮件中可能包含不合适的用语或内容" % account
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
                    # driver.get("http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                    #     repo_cate_id, "exception", account, "", ""))
                    path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        accountCateId, "exception", account, "", "")
                    conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                    conn.request("GET", path)
                    time.sleep(3)
                elif "您的帐号存在安全隐患" in page_source:
                    sc = 0
                    flag = False
                    print u"您的帐号存在安全隐患"
                    # self.repo.BackupInfo(repo_cate_id, 'frozen', account, '', '')
                    # driver.get(
                    #     "http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                    #         repo_cate_id, "frozen", account, "", ""))
                    path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        accountCateId, "exception", account, "", "")
                    conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                    conn.request("GET", path)
                    time.sleep(3)
                else:
                    driver.find_element_by_class_name("qm_icon_Compose")
                    print u"%s发送成功2" % account
                    if eArr=="":
                        return "True"
                    return eArr
            except:

                try:
                    # self.repo.UpdateNumberStauts(emailnumber, repo_number_cate_id, "normal")
                    # driver.get(
                    #     "http://data.161998.com/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                    #     emailnumber, repo_number_cate_id, "normal"))
                    path = "/repo_api/number/updateNumberStatus?number=%s&cateId=%s&status=%s" % (
                        emailnumber, repo_number_cate_id, "normal")
                    conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                    conn.request("GET", path)
                    time.sleep(1)
                except:
                    pass
                print u"%s  发送不成功" % account
                sc = 0
                flag = False
                if "验证码" in page_source:
                    print u"需要验证码"
                    flagFirst = False
                if "邮件中可能包含不合适的用语或内容" in page_source:
                    print u"%s  邮件中可能包含不合适的用语或内容" % account
                elif "<html><head></head><body></body></html>" in page_source:
                    print "空"
                    time.sleep(3)
                elif "您发送的邮件已经达到上限，请稍候再发" in page_source:
                    flagFirst2 = True
                    print u"您发送的邮件已经达到上限，请稍候再发"
                elif "您的域名邮箱账号存在异常行为" in page_source:
                    print u"您的域名邮箱账号存在异常行为"
                    # self.repo.BackupInfo(repo_cate_id, 'exception', account, '', '')
                    # driver.get(
                    #     "http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                    #     repo_cate_id, "exception", account, "", ""))
                    path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        accountCateId, "exception", account, "", "")
                    conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                    conn.request("GET", path)
                    time.sleep(3)
                elif "您的帐号存在安全隐患" in page_source:
                    print u"您的帐号存在安全隐患"
                    # self.repo.BackupInfo(repo_cate_id, 'exception', account, '', '')
                    # driver.get(
                    #     "http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                    #         repo_cate_id, "frozen", account, "", ""))
                    path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        accountCateId, "frozen", account, "", "")
                    conn = httplib.HTTPConnection("data.161998.com", None, timeout=30)
                    conn.request("GET", path)
                    time.sleep(3)
                else:
                    # print page_source
                    # driver.save_screenshot( "%s-%s.png" % (account, self.GetUnique( )) )
                    print "error"

    def sendProcess(self):
        try:
            sc = 0
            flagFirst = False
            flagFirst2 = False
            count = 0
            changeCount = 0
            # try:
            #     self.ipCount = int(self.getArgs()["ipCount"])
            # except:
            #     self.ipCount = 1
            args = self.getArgs()
            popFlag = args["popFlag"]
            if popFlag:
                try:
                    with open(r"C:\qqpop.txt") as f:
                        qqPopList =  f.readlines()
                except:
                    print u"c盘没有qqpop.txt"
                    time.sleep(60)
                    return
            else:
                qqPopList = ["3506587283----zykm9436----aeovbwroudnkchec","3506587283----zykm9436----aeovbwroudnkchec","3506587283----zykm9436----aeovbwroudnkchec","3506587283----zykm9436----aeovbwroudnkchec","3506587283----zykm9436----aeovbwroudnkchec","3506587283----zykm9436----aeovbwroudnkchec","3506587283----zykm9436----aeovbwroudnkchec","3506587283----zykm9436----aeovbwroudnkchec"]

            for qqPop in qqPopList:
                args = self.getArgs()
                # user_agentid = args["user_agent_id"]
                user_agent_id = args["user_agent_id"]
                repo_cate_id = args["repo_cate_id"]
                time_delay = args["time_delay"]
                time_delay = time_delay.split( "-" )
                qqPop = qqPop.replace("\n","")
                arr = qqPop.split("----")
                if len(arr)>=3:
                    qq = arr[0]
                    pwd = arr[2]
                elif len(arr)==2:
                    qq = arr[0]
                    pwd = arr[1]
                else:
                    print u"c盘qqpop.txt内容错误"
                    time.sleep(60)
                    return
                if "@" not in qq:
                    qq = qq + "@qq.com"
                try:
                    time_delayStart = int( time_delay[0] )
                    time_delayEnd = int( time_delay[1] )
                except:
                    print  u"参数格式有误"
                    time_delayStart = 3
                    time_delayEnd = 5
                # numbers = Repo( ).GetAccount( "normal",repo_cate_id, 90, 1 )
                # if len( numbers ) == 0:
                #     print u"%s号仓库没有数据,等待5分钟" % repo_cate_id
                #     time.sleep(300)
                #     return

                accountId = ""
                accountNum = 1
                lockTime = args["lockTime"]
                accountLockTime = int(args["accountLockTime"])
                numbers = self.getAccount("normal", repo_cate_id, accountLockTime, 1,"",lockTime)
                if len(numbers) == 0:
                    print u"%s号仓库没有数据,等待2分钟" % repo_cate_id
                    time.sleep(120)
                    return
                account = numbers[0]['number']  # 即将登陆的QQ号
                password = numbers[0]['password']
                self.ipCount = self.ipCount - 1
                # if changeCount >= 5:
                #     self.ipChange.ooo()
                #     self.ipChange.ooo()
                #     time.sleep(3)
                #     changeCount = 0
                # accountArr = account.split("@")
                # account2 = accountArr[0] + "%40" + accountArr[1]
                # user_agent = numbers[0]['imei']
                # changeCount = changeCount + 1
                # if user_agent is None or user_agent == '':
                user_agentList = Repo( ).GetMaterial( user_agent_id, 0, 1 )
                if len( user_agentList ) == 0:
                    print u"%s号仓库为空" %user_agent_id
                    return
                user_agent = user_agentList[0]['content']
                # user_agent = "	Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
                print user_agent
                command = 'taskkill /F /IM chromedriver.exe'
                os.system(command)
                try:
                    command = 'taskkill /F /IM chrome.exe'
                    os.system(command)
                    # print u'close02'
                except:
                    pass
                # try:
                #     driver.close()
                #     driver.quit()
                # except:
                #     pass
                # display = Display( visible=0, size=(800, 600) )
                # display.start( )
                # user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0"
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

                time.sleep(3)
                driver.get(r'https://qiye.163.com/login/?from=ym')
                time.sleep(2)

                try:
                    # 若帐号输入框有内容先清空
                    driver.find_element_by_id("accname").clear()
                    driver.find_element_by_id("accpwd").clear()
                except:
                    pass
                try:
                    # ///
                    # 输入框输入帐号和密码
                    # account = "xst030@888.jianli58.com"
                    # password = "13141314abc"
                    driver.find_element_by_id("accname").send_keys(account)
                    driver.find_element_by_id("accpwd").send_keys(password)
                    # driver.save_screenshot( "222.png" )
                    time.sleep(0.5)
                    driver.find_element_by_id("accpwd").send_keys(Keys.ENTER)
                    time.sleep(random.randint(2, 4))
                except:
                    pass

                try:
                    driver.find_element_by_xpath('/html/body/div/div[2]/div/form/div[2]/input').send_keys(password)
                    time.sleep(2)
                    driver.find_element_by_xpath('/html/body/div/div[2]/div/form/div[3]/input').send_keys(password)
                    time.sleep(2)
                    driver.find_element_by_xpath('/html/body/div/div[2]/div/form/div[6]/p[1]/label/input').click()
                    time.sleep(2)
                    driver.find_element_by_xpath('/html/body/div/div[2]/div/form/div[6]/p[2]/button').click()
                    time.sleep(2)
                except:
                    pass
                if "管理员信息" in driver.page_source:
                    try:
                        startUrl = driver.current_url
                        if "aid" in startUrl:
                            aid = startUrl.split("aid=")[1]
                            driver.get("https://entry.ym.163.com/entry/hmaildoor?app=web&aid="+aid)
                            time.sleep(3)
                        # driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/a[1]').click()
                    except:
                        pass


                if driver.current_url != "https://qiye.163.com/login/?from=ym" and "邮箱帐号和密码不匹配" not in driver.page_source:
                    # driver.find_element_by_xpath( '//*[@id="nav-mbox"]/div[1]/a[1]/div' )   #网易的logo

                    print u"%s  登陆成功" % account
                    # Repo( ).BackupInfo( repo_cate_id, 'normal', QQNumber, user_agent, '' )
                    startUrl = driver.current_url
                else:
                    # print driver.page_source
                    print u"%s  登陆失败" % account
                    time.sleep( 2 )
                    # 登陆出现异常状况
                    errorPage = driver.page_source.encode( "utf-8" )
                    if "拖动下方滑块完成拼图" in errorPage:
                        print u"拖动下方滑块完成拼图"
                    elif "看不清" in errorPage:
                        print u"需要验证码"
                    elif "验证码" in errorPage and (not "邮箱帐号和密码不匹配" in errorPage):
                        print u"验证码"
                    elif "你的帐号存在安全隐患" in errorPage:
                        print u"你的帐号存在安全隐患"
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "exception", account, "", "")
                        conn = httplib.HTTPConnection( "data.161998.com", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    elif "邮箱帐号和密码不匹配" in errorPage:
                        print u"邮箱帐号和密码不匹配"
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "frozen", account, "", "")
                        conn = httplib.HTTPConnection( "data.161998.com", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep( 3 )
                    elif "冻结" in errorPage:
                        print u"冻结"
                        self.repo.BackupInfo( repo_cate_id, 'frozen', account, '', '' )
                        # driver.get(
                        #     "http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                        #         repo_cate_id, "frozen", account, "", ""))
                        path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            repo_cate_id, "frozen", account, "", "")
                        conn = httplib.HTTPConnection( "data.161998.com", None, timeout=30 )
                        conn.request( "GET", path )
                        time.sleep(3)
                    elif "请输入完整的成员帐号，包括域名。" in errorPage:
                        print  u"%s 冻结" % account
                        try:
                            # self.repo.BackupInfo(repo_cate_id, 'frozen', account, '', '')
                            # driver.get(
                            #     "http://data.161998.com/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                            #         repo_cate_id, "frozen", account, "", ""))
                            path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (
                                repo_cate_id, "exception", account, "", "")
                            conn = httplib.HTTPConnection( "data.161998.com", None, timeout=30 )
                            conn.request( "GET", path )
                        except:
                            pass
                    else:
                        print u"没判断出来"
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
                startUrl2 = driver.current_url.replace("/jy3/","/jy5/")
                driver.get(startUrl2)
                time.sleep(3)

                try:
                    driver.switch_to_default_content()
                except:
                    pass
                #弹窗
                try:
                    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div/a[1]').click()
                except:
                    pass
                url = driver.current_url
                sid = driver.current_url.split("sid=")[1].split('&')[0]
                driver.get('http://mail.ym.163.com/jy5/main.jsp?sid=%s&hl=zh_CN#module=settingaccount'%sid)
                time.sleep(3)
                # driver.switch_to_frame('settingpersonal')
                # time.sleep(2)
                driver.find_element_by_xpath('//*[@class="link js-edit-nickname"]').click()
                obj = driver.find_element_by_xpath('//*[@name="nickname"]')
                name_cate_id = args["name_cate_id"]
                names = self.repo.GetMaterial(name_cate_id, 0, 1)
                if len(names) == 0:
                    names = self.repo.GetMaterial(name_cate_id, 0, 1)
                    if len(names) == 0:
                        print u"%s  号仓库为空，没有取到消息" % name_cate_id
                        # print u'close09'
                        try:
                            driver.close()
                            driver.quit()
                        except:
                            pass
                        return "a"
                name = names[0]['content']
                obj.clear()
                time.sleep(0.5)
                obj.send_keys(name)
                time.sleep(1)
                subs = driver.find_elements_by_xpath('//span[@class="value"]')
                for sub in subs:
                    if sub.text == "确定":
                        sub.click()
                        time.sleep(1)
                        break

                time.sleep(5)


                driver.get(startUrl)
                time.sleep(4)
                try:
                    driver.switch_to_frame('folder')
                    time.sleep(1)
                except:
                    print "dsad"

                # '//*[@id="folder_1"]/div/div/span[1]'
                # '//*[@id="folder_2"]/div/div/span[1]'
                floder = '//*[@id="lnk1"]'

                driver.find_element_by_xpath('//*[@id="lnk1"]').click()
                driver.switch_to_default_content()
                driver.switch_to_frame('foldmain')  # 需先跳转到iframe框架
                time.sleep(1)
                while True:
                    try:
                        if "没有 任何邮件" in driver.page_source.encode("utf-8"):
                            break
                        driver.find_element_by_xpath('//*[@id="oFormCheckAll"]').click()
                        time.sleep(2)
                        # driver.find_element_by_xpath( '//*[@id="oFormMessage"]/div/div/div[2]/input[1]' ).click()
                        try:
                            driver.find_element_by_xpath(
                                '//*[@id="oFormMessage"]/div/div/div[2]/input[1]').send_keys(Keys.ENTER, Keys.ENTER)
                        except:
                            pass
                        # driver.find_element_by_xpath('// *[ @ id = "quick_completelydel"]').click()
                        # time.sleep(0.5)
                        # # driver.switch_to_frame( 'actionFrame' )  # 需先跳转到iframe框架
                        # driver.find_element_by_xpath( '//*[@id="QMconfirm_QMDialog_confirm"]' ).click()
                        time.sleep(2)
                        # driver.find_element_by_xpath(floder ).send_keys( Keys.CONTROL, 'a' )
                        # driver.find_element_by_xpath( floder).send_keys(Keys.DELETE)
                    except:
                        break

                driver.get(url)
                time.sleep(4)
                try:
                    driver.find_element_by_xpath('//*[@id="nav-mbox"]/div[1]/a[1]').click()
                except:
                    continue

                # try:
                #     driver.switch_to_frame('folder')
                #     driver.find_element_by_xpath('/html/body/div/div/div/table/tbody/tr[1]/td/h1/a[2]/b[2]').click()
                #     time.sleep(1)
                # except:
                #     driver.refresh()
                #     driver.switch_to_frame('folder')
                #     driver.find_element_by_xpath('/html/body/div/div/div/table/tbody/tr[1]/td/h1/a[2]/b[2]').click()
                #     pass

                count_Y = 0
                flag = True
                sendCounts = int(args["sendCount"])
                sendCount = 0
                repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
                bccCount = args["bccCount"]
                my_userCount = args["my_userCount"]
                auto_rp_cate_id = qq
                sendSleep = args["sendSleep"]
                auto_loop = args["auto_loop"]
                enailLoop = args["enailLoop"]

                f = True
                train = False
                popFlag = args["popFlag"]
                if popFlag:
                    for i in range(2):
                        print u"给QQ邮箱发消息"
                        if i>0:
                            msgCateFlag = True
                            try:
                                driver.get(url)
                                time.sleep(4)
                                driver.find_element_by_xpath('//*[@id="nav-mbox"]/div[1]/a[1]').click()
                                time.sleep(2)
                                driver.refresh()
                                time.sleep(3)
                            except:
                                pass
                        else:
                            msgCateFlag = False
                        result = self.sendMsg(driver,account,repo_cate_id,qq,0,1,True,msgCateFlag)
                        # sendCounts = sendCounts - 1
                        if result:
                            # time.sleep(sendSleep)
                            pop3_server = "pop.qq.com"
                            # account = "20003280444@wo.cn"
                            # password = 'tidTID505TI'
                            sendMailArr = []
                            try:
                                # 连接到POP3服务器:
                                server = poplib.POP3_SSL(pop3_server, 995)
                                # 可以打开或关闭调试信息:
                                # server.set_debuglevel(1)
                                # 可选:打印POP3服务器的欢迎文字:
                                # print(account, server.getwelcome())
                                # 身份认证:
                                server.user(qq)
                                server.pass_(pwd)
                                # stat()返回邮件数量和占用空间:
                                # print('Messages: %s. Size: %s' % server.stat())
                                # list()返回所有邮件的编号:
                                resp, mails, octets = server.list()
                                # 可以查看返回的列表类似['1 82923', '2 2184', ...]
                                print(mails)
                                # 获取最新一封邮件, 注意索引号从1开始:
                                index = len(mails)

                            except Exception, e:
                                print u"%s pop收信登录失败" % qq
                                print e
                                try:
                                    server.quit()
                                except:
                                    pass
                                return
                            for num in range(1, index + 1):
                                try:
                                    time.sleep(1)
                                    resp, lines, octets = server.retr(num)

                                except:
                                    continue
                                for item in lines:
                                    if "From:" in item:
                                        try:
                                            if "= " in item and "<" not in item:
                                                a = item.split("= ")[1]
                                                sendMailArr.append(a)
                                                break
                                            elif "<" in item:
                                                a = item.split("<")[1]
                                            # print a.split(">")[0]
                                                sendMailArr.append(a.split(">")[0])
                                                break
                                            else:
                                                if item not in "From: ":
                                                    sendMailArr.append(item.split("From: ")[1])
                                                else:
                                                    continue
                                            if result in sendMailArr:
                                                break
                                        except:
                                            try:
                                                print item.split("From: ")[1]
                                                sendMailArr.append(item.split("From: ")[1])
                                                if result in sendMailArr:
                                                    break
                                            except:
                                                pass
                                    elif "Received: from " in item and "@" in item:
                                        a = item.split("Received: from ")[1].split("(")[0]
                                        if a not in sendMailArr:
                                            sendMailArr.append(a.split(">")[0])
                                            break
                            for num in range(1, index + 1):
                                server.dele(num)
                            server.quit()
                            print sendMailArr
                            if account in sendMailArr:
                                print u"进了收件箱"
                                f = True
                                try:
                                    driver.get(url)
                                    time.sleep(3)
                                    driver.find_element_by_xpath('//*[@id="nav-mbox"]/div[1]/a[1]').click()
                                    time.sleep(2)
                                    driver.refresh()
                                    time.sleep(3)
                                except:
                                    pass
                                break
                            else:
                                f = False
                                print u"没进收件箱"
                                # try:
                                #     driver.get(url)
                                #     time.sleep(3)
                                #     driver.find_element_by_xpath('//*[@id="nav-mbox"]/div[1]/a[1]').click()
                                #     time.sleep(2)
                                #     driver.refresh()
                                #     time.sleep(3)
                                # except:
                                #     continue
                                if i==0:
                                    driver.find_element_by_xpath('//*[@id="folder_1"]/div/div/span[1]').click()
                                    time.sleep(1)
                                    try:
                                        driver.find_element_by_xpath('//*[@class="link js-do-it"]').click()
                                    except:
                                        pass
                                    time.sleep(1)
                                    mailObj = driver.find_elements_by_xpath('//span[contains( @ d, "@")]')
                                    time.sleep(1)
                                    mailArr = []
                                    if len(mailObj) == 0:
                                        # print u"邮箱没有邮件"
                                        continue
                                    else:
                                        for mail in mailObj:
                                            try:
                                                address = mail.get_attribute("d")
                                                if address:
                                                    if address not in mailArr:
                                                        mailArr.append(address)
                                            except:
                                                print "d:获取不到该属性"
                                        for item in mailArr:
                                            if "Postmaster@" in item:
                                                print u"退信了"
                                                self.deleteMail(driver, startUrl)
                                                self.ipChangeFlag = False
                                                try:
                                                    data = self.ipChange.Check_for_Broadband()
                                                    if data != None:
                                                        self.ipChange.ooo("10000", "AB")
                                                        time.sleep(5)
                                                        data = self.ipChange.Check_for_Broadband()
                                                        if data != None:
                                                            pass
                                                        else:
                                                            self.ipChange.ooo("10000", "AB")
                                                            time.sleep(10)
                                                            data = self.ipChange.Check_for_Broadband()
                                                            if data != None:
                                                                print u"宽带确认已连接"
                                                    else:
                                                        self.ipChange.ooo("10000", "AB")
                                                        time.sleep(10)
                                                        data = self.ipChange.Check_for_Broadband()
                                                        if data != None:
                                                            print u"宽带确认已连接"
                                                        else:
                                                            self.ipChange.ooo("10000", "AB")
                                                            time.sleep(10)
                                                except:
                                                    pass
                                                return






                        else:
                            f = False
                            break
                    else:
                        train = True
                if f:
                    args = self.getArgs()
                    if train:
                       pass
                    else:
                        repo_number_cate_id = args["repo_number_cate_id"]
                        my_userCount = args["my_userCount"]
                        bccCount = args["bccCount"]
                        enailLoop = args["enailLoop"]
                        for i in range(sendCounts):
                            result = self.sendMsg(driver, account, repo_cate_id, repo_number_cate_id, bccCount, my_userCount, enailLoop)
                            if result:
                                try:
                                    driver.get(url)
                                    time.sleep(3)
                                    driver.find_element_by_xpath('//*[@id="nav-mbox"]/div[1]/a[1]').click()
                                    time.sleep(2)
                                    driver.refresh()
                                    time.sleep(3)
                                except:
                                    continue
                            else:
                                break

                # 删除邮件
                self.deleteMail(driver,startUrl)

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
                #     obj = driver.find_elements_by_xpath( '//*[@id="SetInfo"]/div[1]/a[3]' )
                #     obj[0].click( )
                # for handle in driver.window_handles:  # 方法二，始终获得当前最后的窗口
                #     driver.switch_to_window( handle )
                #     driver.close()
                if self.ipCount==0 and self.ipChangeFlag:
                    try:
                        data = self.ipChange.Check_for_Broadband()
                        if data != None:
                            self.ipChange.ooo("10000", "AB")
                            time.sleep(5)
                            data = self.ipChange.Check_for_Broadband()
                            if data != None:
                                pass
                            else:
                                self.ipChange.ooo("10000", "AB")
                                time.sleep(10)
                                data = self.ipChange.Check_for_Broadband()
                                if data != None:
                                    print u"宽带确认已连接"
                        else:
                            self.ipChange.ooo("10000", "AB")
                            time.sleep(10)
                            data = self.ipChange.Check_for_Broadband()
                            if data != None:
                                print u"宽带确认已连接"
                            else:
                                self.ipChange.ooo("10000", "AB")
                                time.sleep(10)
                    except:
                        pass
                    try:
                        self.ipCount = int(self.getArgs()["ipCount"])
                    except:
                        self.ipCount = 1
                self.delete()

        except:
            # driver.save_screenshot(self.GetUnique()+".jpg")
            logging.exception( "Exception" )
            self.delete()
            return []

    def deleteMail(self,driver,startUrl):
        # 删除邮件
        driver.get(startUrl)
        try:
            driver.switch_to_frame('folder')
            time.sleep(1)
        except:
            print "dsad"

        # '//*[@id="folder_1"]/div/div/span[1]'
        # '//*[@id="folder_2"]/div/div/span[1]'
        floders = ['//*[@id="lnk1"]', '//*[@id="lnk2"]', '//*[@id="lnk3"]', '//*[@id="lnk4"]',
                   '//*[@id="lnk5"]']

        for floder in floders:
            driver.find_element_by_xpath(floder).click()
            driver.switch_to_default_content()
            driver.switch_to_frame('foldmain')  # 需先跳转到iframe框架
            time.sleep(1)
            PostmasterCount = 0
            while True:
                try:
                    if "没有 任何邮件" in driver.page_source.encode("utf-8"):
                        break
                    if floder=='//*[@id="lnk1"]':
                        mailObj = driver.find_elements_by_xpath('//td[contains( @ title, "@")]')
                        time.sleep(1)
                        mailArr = []
                        if len(mailObj) == 0:
                            # print u"邮箱没有邮件"
                            continue
                        else:
                            for mail in mailObj:
                                try:
                                    address = mail.get_attribute("title")
                                    if address:
                                        mailArr.append(address)
                                except:
                                    print "d:获取不到该属性"

                            for item in mailArr:
                                if "Postmaster@" in item:
                                    # print u"退信了"
                                    PostmasterCount = PostmasterCount + 1
                            if PostmasterCount>=2:
                                os.system('shutdown /r /f /t 0')

                    driver.find_element_by_xpath('//*[@id="oFormCheckAll"]').click()
                    time.sleep(2)
                    # driver.find_element_by_xpath( '//*[@id="oFormMessage"]/div/div/div[2]/input[1]' ).click()
                    try:
                        driver.find_element_by_xpath(
                            '//*[@id="oFormMessage"]/div/div/div[2]/input[1]').send_keys(Keys.ENTER, Keys.ENTER)
                    except:
                        pass
                    # driver.find_element_by_xpath('// *[ @ id = "quick_completelydel"]').click()
                    # time.sleep(0.5)
                    # # driver.switch_to_frame( 'actionFrame' )  # 需先跳转到iframe框架
                    # driver.find_element_by_xpath( '//*[@id="QMconfirm_QMDialog_confirm"]' ).click()
                    time.sleep(2)
                    # driver.find_element_by_xpath(floder ).send_keys( Keys.CONTROL, 'a' )
                    # driver.find_element_by_xpath( floder).send_keys(Keys.DELETE)
                except:
                    break
            driver.get(startUrl)
            time.sleep(1)
            try:
                driver.switch_to_frame('folder')
                time.sleep(1)
            except:
                print "dsad"

    def action(self):
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
        self.delete()
        args = self.getArgs( )
        phonenumber = args["phonenumber"]
        cateId = args["cateId"]
        para = {"phoneNumber": phonenumber, "x_04": sta}
        self.repo.PostInformation( cateId, para )

def getPluginClass():
    return YM_WY_QQPOP

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    # time.sleep(150)
    #o.getTime("CnTime")




    data = IPChange().Check_for_Broadband()
    if data != None:
        print u"宽带确认已连接,模块继续运行"
    else:
        print u"宽带未连接,连接宽带"
        time.sleep(150)
        IPChange().ooo("10000", "AB")
        time.sleep(5)
    clazz = getPluginClass()
    o = clazz()
    # os.system('shutdown /r /f /t 0')

    while True:
        try:
            o.action()
        except Exception,e:
            print e
    # numbers = Repo().GetAccount("303", 5, 1)
    # if len(numbers) == 0:
    #     print u"%s号仓库没有数据,等待5分钟" % "303"
    #     time.sleep(300)
    #
    #
    # account = numbers[0]['number']  # 即将登陆的QQ号
    #
    # accountArr = account.split("@")
    # account = accountArr[0] + "%40" + accountArr[1]
    # cap = webdriver.DesiredCapabilities.PHANTOMJS
    # cap["phantomjs.page.settings.resourceTimeout"] = 1000
    # cap["phantomjs.page.settings.loadImages"] = True
    # cap["phantomjs.page.settings.disk-cache"] = True
    #
    # driver = webdriver.PhantomJS(desired_capabilities=cap, executable_path=r"C:\phantomjs\bin\phantomjs.exe")
    # driver.get(
    #     "http://data.161998.com/repo_api/account/timeDelay?number=%s&cate_id=%s&numberType=%s" % (
    #         account, "303", "PT_QQ"))
