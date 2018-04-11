# coding:utf-8
import colorsys
import datetime
import os
import random
import time
import uuid

from PIL import Image

import util
from Repo import *
from imageCode import imageCode
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from zservice import ZDevice


class MobilqqLogin3:
    def __init__(self):
        self.type = 'mobileqq'
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def WebViewBlankPages(self, d, z):
        z.toast("判断是否是滑块")
        Str = d.info  # 获取屏幕大小等信息
        height = float( Str["displayHeight"] )
        width = float( Str["displayWidth"] )

        W_H = width / height
        screenScale = round( W_H, 2 )

        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )

        if screenScale == 0.56:
            left = 115  # 验证码的位置信息
            top = 670
            right = 185
            bottom = 720
        if screenScale == 0.61:
            left = 115  # 验证码的位置信息
            top = 670
            right = 185
            bottom = 720

        d.screenshot( sourcePng )  # 截取整个输入验证码时的屏幕

        img = Image.open( sourcePng )
        box = (left, top, right, bottom)  # left top right bottom
        region = img.crop( box )  # 截取验证码的图片
        # show(region)    #展示资料卡上的信息
        image = region.convert( 'RGBA' )
        # 生成缩略图，减少计算量，减小cpu压力
        image.thumbnail( (200, 200) )
        max_score = None
        dominant_color = None
        for count, (r, g, b, a) in image.getcolors( image.size[0] * image.size[1] ):
            # 跳过纯黑色
            if a == 0:
                continue
            saturation = colorsys.rgb_to_hsv( r / 255.0, g / 255.0, b / 255.0 )[1]
            y = min( abs( r * 2104 + g * 4130 + b * 802 + 4096 + 131072 ) >> 13, 235 )
            y = (y - 16.0) / (235 - 16)
            # 忽略高亮色
            if y > 0.9:
                continue

            score = (saturation + 0.1) * count
            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)  # 红绿蓝
        return dominant_color

    def WebViewPlayCode(self, d, z):
        z.toast( "非空白页，开始截图打码" )

        Str = d.info  # 获取屏幕大小等信息
        height = float( Str["displayHeight"] )
        width = float( Str["displayWidth"] )
        W_H = width / height
        screenScale = round( W_H, 2 )

        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        icode = imageCode( )
        im_id = ""
        for i in range( 0, 1 ):  # 打码循环
            if i > 0:
                icode.reportError( im_id )

            d.screenshot( sourcePng )  # 截取整个输入验证码时的屏幕
            if screenScale == 0.61:
                p = {"x1": 30 / width, "y1": 200 / height, "x2": 271 / width, "y2": 300 / height}
            if screenScale == 0.56:
                p = {"x1": 40 / width, "y1": 270 / height, "x2": 362 / width, "y2": 400 / height}
            cropedImg = z.img_crop( sourcePng, p )
            im = open( cropedImg, 'rb' )
            codeResult = icode.getCode( im, icode.CODE_TYPE_4_NUMBER_CHAR, 60 )
            code = codeResult["Result"]
            im_id = codeResult["Id"]
            os.remove( sourcePng )
            z.heartbeat( )
            z.sleep( 5 )
            if screenScale == 0.61:
                d.click( 360, 240 )
            if screenScale == 0.56:
                d.click( 500, 350 )
            z.input( code )
            z.sleep( 2 )
            if screenScale == 0.61:
                d.click( 270, 450 )
            if screenScale == 0.56:
                d.click( 360, 600 )

            while d( className='android.widget.ProgressBar', index=0 ).exists:  # 网速不给力时，点击完成后仍然在加载时的状态
                z.sleep( 2 )
            z.sleep( 8 )

            if not d( textContains='验证码' ).exists:
                z.toast( "机器人打码跳出－－" )
                break

    def playCode(self, codeImgObj, type):
        z.toast( "非网页视图打码" )
        self.scode = smsCode( d.server.adb.device_serial( ) )
        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        codePng = os.path.join( base_dir, "%s_c.png" % (self.GetUnique( )) )
        icode = imageCode( )
        im_id = ""
        for i in range( 0, 4 ):  # 打码循环
            if i > 0:
                icode.reportError( im_id )
            obj = d( resourceId='com.tencent.mobileqq:id/name',
                     className='android.widget.ImageView' )  # 当弹出选择QQ框的时候，定位不到验证码图片
            if not obj.exists:
                obj = d( index='2', className='android.widget.Image' )
            obj = obj.info
            obj = obj['bounds']  # 验证码处的信息
            left = obj["left"]  # 验证码的位置信息
            top = obj['top']
            right = obj['right']
            bottom = obj['bottom']

            d.screenshot( sourcePng )  # 截取整个输入验证码时的屏幕

            img = Image.open( sourcePng )
            box = (left, top, right, bottom)  # left top right bottom
            region = img.crop( box )  # 截取验证码的图片

            img = Image.new( 'RGBA', (right - left, bottom - top) )
            img.paste( region, (0, 0) )

            img.save( codePng )
            im = open( codePng, 'rb' )

            codeResult = icode.getCode( im, icode.CODE_TYPE_4_NUMBER_CHAR, 60 )

            code = codeResult["Result"]
            im_id = codeResult["Id"]
            os.remove( sourcePng )
            os.remove( codePng )
            z.heartbeat( )
            z.sleep( 5 )
            if type == 0:
                d( resourceId='com.tencent.mobileqq:id/name', index='2',
                   className="android.widget.EditText" ).set_text( code )
            else:
                codeImgObj.set_text(code)
            z.sleep( 3 )
            if d( descriptionContains='验证', className='android.view.View' ).exists:
                d( descriptionContains='验证', className='android.view.View' ).click( )
            else:
                d( text='完成', resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText' ).click( )
            z.sleep( 6 )
            z.heartbeat( )
            while d( className='android.widget.ProgressBar', index=0 ).exists:  # 网速不给力时，点击完成后仍然在加载时的状态
                z.sleep( 2 )
            z.sleep( 3 )
            z.heartbeat( )
            if codeImgObj.exists:
                continue
            else:
                break
        z.sleep( 5 )
        if d( textContains='验证码' ).exists:
            return False
        else:
            return True

    def login(self, d, args, z, numbers):

        QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        QQPassword = numbers[0]['password']

        z.heartbeat()
        d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存
        d.server.adb.cmd("shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep(5)
        while d( textContains='正在更新数据' ).exists:
            z.sleep( 2 )

        z.sleep(15)
        z.heartbeat( )
        d.dump(compressed=False)
        if d(text='登 录',resourceId='com.tencent.mobileqq:id/btn_login').exists:
            d( text='登 录' ).click()

        z.sleep(1)
        d( className='android.widget.EditText', index=0 ).click( )  # ﻿1918697054----xiake1234.  QQNumber
        z.input( QQNumber )

        z.sleep( 1 )
        d( resourceId='com.tencent.mobileqq:id/password' ).click( )  # Bn2kJq5l     QQPassword
        z.input( QQPassword )

        z.heartbeat( )
        print('QQ号:%s,QQ密码：%s' % (QQNumber, QQPassword))
        d.dump(compressed=False )
        d( text='登 录', resourceId='com.tencent.mobileqq:id/login' ).click( )
        z.sleep(3)
        while d(text='登录中').exists:
            z.sleep(2)
        z.sleep(20)

        z.heartbeat()
        detection_robot = d(index='3', className="android.widget.EditText")
        not_detection_robot = d( resourceId='com.tencent.mobileqq:id/name', index='2',
                                 className="android.widget.EditText" )
        if detection_robot.exists:  # 需要验证码的情况
            if not self.playCode(detection_robot, 1):
                return False

        if not_detection_robot.exists:
            if not self.playCode(not_detection_robot.exists, 0) == "nothing":
                return False

        if d(className='android.webkit.WebView').exists:
            if self.WebViewBlankPages(d, z)[2] < 200:
                self.WebViewPlayCode(d, z)
            else:
                d.swipe(155, 703, 550, 703)
                if d(text='验证码',resourceId='com.tencent.mobileqq:id/ivTitleName').exists:
                    return False

        z.sleep(5)
        z.heartbeat()
        loginStatusList = z.qq_getLoginStatus(d)
        if loginStatusList is None:
            if d( text='消息' ).exists and d( text='联系人' ).exists and d( text='动态' ).exists:
                loginStatusList = {'success': True}
            elif d( textContains="请在小米神隐模式中将TIM设置为“无限制”。" ).exists:
                z.toast( "我是小米神隐" )
                d( text='我知道了' ).click( )
            else:
                loginStatusList = {'success': False}

        loginStatus = loginStatusList['success']
        if loginStatus:
            z.toast( "卡槽QQ状态正常，继续执行" )
            return True
        else:
            if d( text='去安全中心' ).exists:
                self.repo.BackupInfo( args["repo_cate_id"], 'frozen', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber

            else:
                self.repo.BackupInfo( args["repo_cate_id"], 'normal', QQNumber, '', '' )

            z.toast( "卡槽QQ状态异常，跳过此模块" )
            return False

        # if d( text='马上绑定' ).exists:
        #     self.BindAddressBook(z, d, args)

    def qiehuan(self , d, z, args):
        time_limit = int(args['time_limit'])
        serial = d.server.adb.device_serial( )
        self.slot = Slot( serial, self.type )
        slotObj = self.slot.getAvailableSlot(time_limit)  # 没有空卡槽，取２小时没用过的卡槽
        slotnum = None
        if not slotObj is None:
            slotnum = slotObj['id']

        while slotObj is None:  # 2小时没用过的卡槽也为没有的情况
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"" ).communicate( )
            z.heartbeat( )
            z.sleep( 30 )
            slotObj = self.slot.getAvailableSlot( time_limit )
            if not slotObj is None:
                slotnum = slotObj['id']
                break

        z.heartbeat( )
        d.server.adb.cmd( "shell", "pm clear com.tencent.mobileqq" ).communicate( )  # 清除缓存

        d.server.adb.cmd( "shell", "settings put global airplane_mode_on 1" ).communicate( )  # 开飞行模式
        d.server.adb.cmd( "shell",
                          "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true" ).communicate( )
        z.sleep( 6 )
        z.heartbeat( )

        d.server.adb.cmd( "shell", "settings put global airplane_mode_on 0" ).communicate( )  # 关飞行模式
        d.server.adb.cmd( "shell",
                          "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false" ).communicate( )

        z.heartbeat( )
        while True:
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                break
            z.sleep( 2 )

        obj = self.slot.getSlotInfo(slotnum)
        remark = obj['remark']
        remarkArr = remark.split("_")
        cateId = ""
        if len(remarkArr) == 3:
            slotInfo = d.server.adb.device_serial() + '_' + self.type + '_' + slotnum
            cateId = remarkArr[2]
            numbers = self.repo.Getserial(cateId, slotInfo)
            if len( numbers ) != 0:
                featureCodeInfo = numbers[0]['imei']
                z.set_serial( "com.tencent.mobileqq", featureCodeInfo )

        self.slot.restore(slotnum)  # 有time_limit分钟没用过的卡槽情况，切换卡槽
        z.sleep(2)

        d.server.adb.cmd("shell",
                          "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + slotnum + "号\"").communicate()
        z.sleep(2)
        d.server.adb.cmd("shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate( )  # 拉起来
        z.sleep(5)
        while d(textContains='正在更新数据').exists:
            z.sleep( 2 )
        z.sleep( 15 )

        z.heartbeat( )
        loginStatusList = z.qq_getLoginStatus( d )
        if loginStatusList is None:
            if d( text='消息' ).exists and d( text='联系人' ).exists and d( text='动态' ).exists:
                loginStatusList = {'success': True}
            elif d( textContains="请在小米神隐模式中将TIM设置为“无限制”。" ).exists:
                z.toast( "我是小米神隐" )
                d( text='我知道了' ).click( )
                loginStatusList = {'success': True}
            else:
                z.toast( "登陆新场景，现无法判断登陆状态" )
                loginStatusList = {'success': False}

        loginStatus = loginStatusList['success']
        if loginStatus:
            z.toast("卡槽QQ状态正常，继续执行")
            return True
        else:
            QQnumber = remarkArr[1]
            if d(text='去安全中心').exists:
                self.repo.BackupInfo(cateId, 'frozen', QQnumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber

            else:
                self.repo.BackupInfo(cateId, 'normal', QQnumber, '', '')

            self.slot.clear(slotnum)  # 清空改卡槽，并补登
            z.toast("卡槽QQ状态异常，补登陆卡槽")
            return False

    def action(self, d, z, args):
        while True:
            z.toast("正在ping网络是否通畅")
            i = 0
            while i < 200:
                i += 1
                ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate()
                print(ping)
                if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                    z.toast("网络通畅。开始执行：普通ＱＱ登录有卡槽")
                    break
                z.sleep( 2 )
            if i > 200 :
                z.toast("网络不通，请检查网络状态")
                if (args["time_delay"]):
                    z.sleep(int(args["time_delay"]))
                return

            z.heartbeat()
            z.generate_serial("com.tencent.mobileqq") # 随机生成手机特征码
            cate_id = args["repo_cate_id"]

            time_limit1 = args['time_limit1']
            numbers = self.repo.GetAccount(cate_id, time_limit1, 1)
            if len(numbers) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库无%s分钟未用,开始切换卡槽\"" % (cate_id, time_limit1)).communicate()

            serial = d.server.adb.device_serial()
            self.slot = Slot(serial, self.type)
            slotnum = self.slot.getEmpty()  # 取空卡槽
            if slotnum == 0 or len(numbers) == 0:    #没有空卡槽的话
               if self.qiehuan(d, z, args):
                   break

            else:  # 有空卡槽的情况
                d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存

                d.server.adb.cmd("shell", "settings put global airplane_mode_on 1").communicate()
                d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true").communicate()
                z.sleep(6)
                d.server.adb.cmd("shell", "settings put global airplane_mode_on 0").communicate()
                d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false").communicate()
                z.heartbeat()
                while True:
                    ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
                    print(ping)
                    if 'icmp_seq'and 'bytes from'and'time' in ping[0]:
                        break
                    z.sleep(2)

                z.heartbeat()
                if self.login(d, args, z, numbers):
                    z.heartbeat()
                    featureCodeInfo = z.get_serial("com.tencent.mobileqq")
                    self.slot.backup(slotnum, str(slotnum ) + '_' + numbers[0]['number'] + '_' + cate_id )  # 设备信息，卡槽号，QQ号
                    self.repo.BackupInfo(cate_id, 'using', numbers[0]['number'], featureCodeInfo, '%s_%s_%s' % (
                    d.server.adb.device_serial(), self.type, slotnum) )  # 仓库号,使用中,QQ号,设备号_卡槽号
                else:
                    continue



        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))



def getPluginClass():
    return MobilqqLogin3

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("465b4e4b")
    z = ZDevice("465b4e4b")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_cate_id": "331", "time_limit": "2", "time_limit1": "120", "time_delay": "3"};    #cate_id是仓库号，length是数量
    # z.server.install( )
    o.action(d, z, args)
    # serial = d.server.adb.device_serial( )
    # type = 'qqmail'
    # slot = Slot( serial, type )
    # slot.clear( "1" )
    # for i in range(1,200):
    #     slot.clear(i)
    #     print('已经清除')
    # print('全部清除')
    # d.server.adb.cmd("shell", "pm clear com.tencent.androidqqmail").communicate( )  # 清除缓存

    # d.server.adb.cmd( "shell", "am start -n com.tencent.androidqqmail/com.tencent.qqmail.launcher.third.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱

    # d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( ) 拉起易信



