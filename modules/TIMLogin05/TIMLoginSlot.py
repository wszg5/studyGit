# coding:utf-8
import base64
import logging
from PIL import Image
from imageCode import imageCode
from smsCode import smsCode
from uiautomator import Device
import os
import util
from Repo import *
import time, datetime, random
from slot import Slot
from zservice import ZDevice
import colorsys
from imageCode import imageCode

class TIMLoginSlot:

    def __init__(self):
        self.repo = Repo()
        self.type = 'tim'

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def WebViewBlankPages(self, d):
        z.toast( "判断是否是空白页" )
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
            left = 60  # 验证码的位置信息
            top = 655
            right = 290
            bottom = 680
        if screenScale == 0.61:
            left = 60  # 验证码的位置信息
            top = 490
            right = 210
            bottom = 510

        left = width * 7 / 135  # 验证码的位置信息
        top = height * 245 / 444
        right = width * 51 / 54
        bottom = height * 275 / 444

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
        z.toast( "开始截图打码" )

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
                p = {"x1": 30 / width, "y1": 283 / height, "x2": 271 / width, "y2": 379 / height}
            if screenScale == 0.56:
                p = {"x1": 40 / width, "y1": 375 / height, "x2": 362 / width, "y2": 505 / height}
            cropedImg = z.img_crop( sourcePng, p )
            im = open( cropedImg, 'rb' )
            codeResult = icode.getCode( im, icode.CODE_TYPE_4_NUMBER_CHAR, 60 )
            code = codeResult["Result"]
            im_id = codeResult["Id"]
            os.remove( sourcePng )
            z.heartbeat( )
            z.sleep( 5 )
            d.click( width * 300 / 540, height * 330 / 888 )
            self.input( z, height, code )
            z.sleep( 2 )
            d.click( width * 270 / 540, height * 525 / 888 )
            while d( className='android.widget.ProgressBar', index=0 ).exists:  # 网速不给力时，点击完成后仍然在加载时的状态
                z.sleep( 2 )
            z.sleep( 8 )
            z.toast( "机器人打码－－" )
            if not d( textContains='验证码' ).exists:
                z.toast( "机器人打码跳出－－" )
                break

    def LoginPlayCode(self, d, z):
        self.scode = smsCode( d.server.adb.device_serial( ) )
        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        codePng = os.path.join( base_dir, "%s_c.png" % (self.GetUnique( )) )
        detection_robot = d( index='3', className="android.widget.EditText" )
        not_detection_robot = d( resourceId='com.tencent.tim:id/name', index='2',
                                 className="android.widget.EditText" )
        if detection_robot.exists or not_detection_robot.exists:  # 需要验证码的情况
            icode = imageCode( )
            im_id = ""
            for i in range( 0, 4 ):  # 打码循环
                # if i > 0:
                #     icode.reportError( im_id )
                obj = d( resourceId='com.tencent.tim:id/name',
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
                with open( codePng, 'rb' ) as f:
                    # file = f.read()
                    file = "data:image/jpeg;base64," + base64.b64encode( f.read( ) )
                    da = {"IMAGES": file}
                    path = "/ocr.index"
                    headers = {"Content-Type": "application/x-www-form-urlencoded",
                               "Connection": "Keep-Alive"}
                    conn = httplib.HTTPConnection( "162626i1w0.51mypc.cn", 10082, timeout=30 )
                    params = urllib.urlencode( da )
                    conn.request( method="POST", url=path, body=params, headers=headers )
                    response = conn.getresponse( )
                    if response.status == 200:
                        code = response.read( )
                    else:
                        continue
                os.remove( sourcePng )
                os.remove( codePng )
                z.heartbeat( )
                z.sleep( 5 )
                if not_detection_robot.exists:
                    d( resourceId='com.tencent.tim:id/name', index='2',
                       className="android.widget.EditText" ).set_text( code )
                else:
                    detection_robot.set_text( code )
                z.sleep( 3 )
                if d( descriptionContains='验证', className='android.view.View' ).exists:
                    d( descriptionContains='验证', className='android.view.View' ).click( )
                else:
                    d( text='完成', resourceId='com.tencent.tim:id/ivTitleBtnRightText' ).click( )
                z.sleep( 5 )
                z.heartbeat( )
                while d( className='android.widget.ProgressBar', index=0 ).exists:  # 网速不给力时，点击完成后仍然在加载时的状态
                    z.sleep( 2 )
                z.heartbeat( )
                if detection_robot.exists or not_detection_robot.exists:
                    continue
                else:
                    break
            z.sleep( 5 )
            if d( textContains='验证码' ).exists:
                return "no"
            else:
                return "yes"
        else:
            return "no"

    def login(self,d,args,z):
        z.heartbeat()
        Str = d.info  # 获取屏幕大小等信息
        height = float( Str["displayHeight"] )
        width = float( Str["displayWidth"] )

        cate_id = args["repo_cate_id"]
        time_limit1 = args['time_limit1']
        numbers = self.repo.GetAccount( cate_id, time_limit1, 1 )
        while len( numbers ) == 0:
            z.heartbeat( )
            d.server.adb.cmd( "shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库无%s分钟未用,开始切换卡槽\"" % (
            cate_id, time_limit1) ).communicate( )
            z.sleep( 2 )
            return 0

        QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        QQPassword = numbers[0]['password']
        z.sleep( 1 )
        z.heartbeat( )
        d.server.adb.cmd("shell", "pm clear com.tencent.tim").communicate( )  # 清除缓存
        # d.server.adb.cmd("shell",
        #                   "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.server.adb.run_cmd( "shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" )
        z.sleep(10)
        while d( textContains='正在更新数据' ).exists:
            z.sleep( 2 )
        z.sleep(10)
        z.heartbeat()
        z.server.adb.run_cmd( "shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" )
        z.sleep( 5 )
        z.heartbeat( )
        if d(className='android.widget.ImageView',resourceId='com.tencent.tim:id/title',index=1).exists:
            for i in range(0,2):
                d.swipe( width - 20, height / 2, 0, height / 2, 5 )
                z.sleep(1.5)
            if d(text='立即体验').exists:
                d(text='立即体验').click()
        z.sleep(2)
        if d(text='登 录').exists:
            d(text='登 录').click()
        else:
           d( text='QQ号登录' ).click( )
        z.sleep( 1 )
        # d(className='android.widget.EditText', index=0).set_text(QQNumber)  # ﻿1918697054----xiake1234.  QQNumber
        d(className='android.widget.EditText', index=0).click()  # ﻿1918697054----xiake1234.  QQNumber
        self.input( z, height, QQNumber )

        z.sleep( 1 )
        # d(resourceId='com.tencent.mobileqq:id/password').set_text(QQPassword)  # Bn2kJq5l     QQPassword
        d(resourceId='com.tencent.tim:id/password').click()  # Bn2kJq5l     QQPassword
        self.input( z, height, QQPassword )
        z.heartbeat()
        logger = util.logger
        print('QQ号:%s,QQ密码：%s' % (QQNumber, QQPassword))
        d.dump(compressed=False )
        d( text='登 录', resourceId='com.tencent.tim:id/login' ).click( )
        z.sleep(1)
        while d(text='登录中').exists:
            z.sleep(2)

        z.sleep(int(args['time_delay1']))
        z.heartbeat()

        detection_robot = d( index='3', className="android.widget.EditText" )
        not_detection_robot = d( resourceId='com.tencent.tim:id/name', index='2',
                                 className="android.widget.EditText" )
        playCodeResult = ''
        if detection_robot.exists or not_detection_robot.exists:
            playCodeResult = self.LoginPlayCode( d, z )  # 打验证码
        else:
            if self.WebViewBlankPages( d )[2] > 200:
                z.toast( "不是空白页" )
                self.WebViewPlayCode( d, z )
            else:
                z.toast( "是空白页" )
                return "nothing"


        if playCodeResult == "no":
            return "nothing"

        z.sleep(10)
        z.heartbeat()
        if d( text='马上绑定' ).exists:
            return QQNumber

        if d(textContains="请在小米神隐模式中将TIM设置为“无限制”。").exists:
            z.toast("我是小米神隐")
            return QQNumber

        if d( text='匹配手机通讯录' ).exists:  # 登陆上后弹出t通讯录的情况
            d( text='匹配手机通讯录' ).click()
            z.sleep(1.5)
            if d(text='取消').exists:
                d(text='取消').child()
            return QQNumber

        if d(text='消息').exists and d(description='快捷入口').exists:
            z.toast("卡槽QQ状态正常，继续执行")
            return QQNumber

        if d( text='去安全中心' ).exists:
            self.repo.BackupInfo( cate_id, 'frozen', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
            z.toast( "登陆失败，重新登陆" )
            return "nothing"
        elif d(resourceId="com.tencent.tim:id/login",description="登录").exists:
            failCount = int(args["failCount"])
            for r in range(failCount):
                result = self.againLogin(d,z)
                if result is True:
                    return QQNumber
                elif result is False:
                    self.repo.BackupInfo( cate_id, 'frozen', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                    return "nothing"
                elif result is None:
                    return "nothing"
        else:
            self.repo.BackupInfo( cate_id, 'normal', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
            z.toast( "登陆失败，重新登陆" )
            return "nothing"

    def qiehuan(self, d, z, args):
        Str = d.info  # 获取屏幕大小等信息
        height = float( Str["displayHeight"] )
        width = float( Str["displayWidth"] )
        time_limit = int(args['time_limit'])
        cate_id = args["repo_cate_id"]
        serial = d.server.adb.device_serial( )
        self.slot = Slot( serial, self.type )
        slotObj = self.slot.getAvailableSlot(time_limit)  # 没有空卡槽，取２小时没用过的卡槽
        while slotObj is None:  # 2小时没有用过的卡槽也为空的情况
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"").communicate()
            z.heartbeat()
            z.sleep(10)
            slotObj = self.slot.getAvailableSlot( time_limit )  # 没有空卡槽，取２小时没用过的卡槽

        if not slotObj is None:
            slotnum = slotObj['id']
        z.heartbeat()
        d.server.adb.cmd("shell", "pm clear com.tencent.tim").communicate()  # 清除缓存

        # d.server.adb.cmd("shell", "settings put global airplane_mode_on 1").communicate()
        # d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true").communicate()
        # z.sleep(6)
        # z.heartbeat()
        # d.server.adb.cmd("shell", "settings put global airplane_mode_on 0").communicate()
        # d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false").communicate()
        z.heartbeat()
        z.toast( "正在ping网络是否通畅" )
        while True:
            ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                break
            z.sleep(2)

        obj = self.slot.getSlotInfo( slotnum )
        remark = obj['remark']
        remarkArr = remark.split( "_" )
        if len( remarkArr ) == 3:
            slotInfo = d.server.adb.device_serial( ) + '_' + self.type + '_' + slotnum
            cateId = remarkArr[2]
            numbers = self.repo.Getserial( cateId, slotInfo )
            if len( numbers ) != 0:
                featureCodeInfo = numbers[0]['imei']
                z.set_serial( "com.tencent.tim", featureCodeInfo )

        self.slot.restore( slotnum )  # 有time_limit分钟没用过的卡槽情况，切换卡槽

        d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + str(slotnum) + "号\"").communicate()
        z.sleep(2)
        # d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.server.adb.run_cmd( "shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" )

        z.sleep( 5 )
        while d( textContains='正在更新数据' ).exists:
            z.sleep( 2 )

        z.sleep( 3 )
        z.server.adb.run_cmd( "shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" )
        z.sleep(3)
        z.heartbeat()
        if d(className='android.widget.ImageView',resourceId='com.tencent.tim:id/title',index=1).exists:
            for i in range(0,2):
                d.swipe( width - 20, height / 2, 0, height / 2, 5 )
                z.sleep(1.5)
            if d(text='立即体验').exists:
                d(text='立即体验').click()
        z.sleep(3)

        if d( textContains="请在小米神隐模式中将TIM设置为“无限制”。" ).exists:
            z.toast( "我是小米神隐" )
            d( text='我知道了' ).click( )
            d( text='我知道了' ).click( )
        elif d( text='消息' ).exists or d( text='马上绑定' ).exists or d( text='匹配手机通讯录' ).exists:
            if d( text='匹配手机通讯录' ).exists:  # 登陆上后弹出t通讯录的情况
                d( text='匹配手机通讯录' ).click( )
                z.sleep( 1.5 )
                if d( text='取消' ).exists:
                    d( text='取消' ).child( )
            z.toast( "卡槽QQ切换成功，继续执行" )
        else:
            obj = self.slot.getSlotInfo( slotnum )
            remark = obj['remark']
            remarkArr = remark.split( "_" )
            QQnumber = remarkArr[1]
            if d( text='去安全中心' ).exists:
                self.repo.BackupInfo( cate_id, 'frozen', QQnumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber

            else:
                self.repo.BackupInfo( cate_id, 'normal', QQnumber, '', '' )
            self.slot.clear( slotnum )  # 清空改卡槽，并补登
            z.toast( "卡槽QQ状态异常，补登陆卡槽" )
            self.action( d, z, args )

    def againLogin(self, d , z):
        if d(resourceId="com.tencent.tim:id/login",description="登录").exists:
            d( resourceId="com.tencent.tim:id/login", description="登录" ).click()
            z.sleep( 1 )
            while d( text='登录中' ).exists:
                z.sleep( 2 )

            z.sleep( int( args['time_delay1'] ) )
            z.heartbeat( )

            detection_robot = d( index='3', className="android.widget.EditText" )
            not_detection_robot = d( resourceId='com.tencent.tim:id/name', index='2',
                                     className="android.widget.EditText" )
            playCodeResult = ''
            if detection_robot.exists or not_detection_robot.exists:
                playCodeResult = self.LoginPlayCode( d, z )  # 打验证码
            else:
                if self.WebViewBlankPages( d )[2] > 200:
                    z.toast( "不是空白页" )
                    self.WebViewPlayCode( d, z )
                else:
                    z.toast( "是空白页" )
                    return "nothing"

            if playCodeResult == "no":
                return "nothing"

            z.sleep( 10 )
            z.heartbeat( )
            if d( text='马上绑定' ).exists:
                return True

            if d( textContains="请在小米神隐模式中将TIM设置为“无限制”。" ).exists:
                z.toast( "我是小米神隐" )
                return True

            if d( text='匹配手机通讯录' ).exists:  # 登陆上后弹出t通讯录的情况
                d( text='匹配手机通讯录' ).click( )
                z.sleep( 1.5 )
                if d( text='取消' ).exists:
                    d( text='取消' ).child( )
                return True

            if d( text='消息' ).exists and d( description='快捷入口' ).exists:
                z.toast( "卡槽QQ状态正常，继续执行" )
                return True

            if d( text='去安全中心' ).exists:
                # self.repo.BackupInfo( cate_id, 'frozen', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                z.toast( "登陆失败，重新登陆" )
                return False
            if d( resourceId="com.tencent.tim:id/login", description="登录" ).exists:
                return "nothing"
            else:
                # self.repo.BackupInfo( cate_id, 'normal', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                z.toast( "登陆失败，重新登陆" )
                return

    def input(self, z, height, text):
        if height>888:
            z.input(text)
        else:
            z.cmd( "shell", "am broadcast -a ZY_INPUT_TEXT --es text \\\"%s\\\"" % text )

    def action(self,d,z,args):
        Str = d.info  # 获取屏幕大小等信息
        height = float( Str["displayHeight"] )
        width = float( Str["displayWidth"] )

        z.generate_serial("com.tencent.tim")  # 随机生成手机特征码
        z.toast("随机生成手机特征码")


        time_limit = int(args['time_limit'])
        cate_id = args["repo_cate_id"]
        serial = d.server.adb.device_serial()
        self.slot = Slot(serial, self.type)
        slotnum = self.slot.getEmpty()  # 取空卡槽
        if slotnum == 0:  # 没有空卡槽的话
            slotObj = self.slot.getAvailableSlot(time_limit)  # 取空卡槽，取２小时没用过的卡槽
            if not slotObj is None:
                slotnum = slotObj['id']
            print(slotnum)
            while slotObj is None:  # 2小时没用过的卡槽也为没有的情况
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"" ).communicate( )
                z.heartbeat()
                z.sleep(10)
                slotObj = self.slot.getAvailableSlot(time_limit)
                if not slotObj is None:
                    slotnum = slotObj['id']
            z.heartbeat()
            d.server.adb.cmd( "shell", "pm clear com.tencent.tim" ).communicate( )  # 清除缓存
            # d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止


            # d.server.adb.cmd("shell", "settings put global airplane_mode_on 1").communicate() #开数据流量
            # d.server.adb.cmd("shell","am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true").communicate()#开飞行模式
            # z.sleep( 6 )
            # z.heartbeat( )
            # d.server.adb.cmd("shell", "settings put global airplane_mode_on 0").communicate() # 关数据流量
            # d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false").communicate()#开飞行模式

            # z.heartbeat( )
            # z.toast( "正在ping网络是否通畅" )
            # while True:
            #     ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            #     print( ping )
            #     if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
            #         break
            #     z.sleep( 2 )
            obj = self.slot.getSlotInfo( slotnum )
            remark = obj['remark']
            remarkArr = remark.split( "_" )
            if len( remarkArr ) == 3:
                slotInfo = d.server.adb.device_serial() + '_' + self.type + '_' + slotnum
                cateId = remarkArr[2]
                numbers = self.repo.Getserial( cateId, slotInfo)
                if len(numbers) != 0:
                    featureCodeInfo = numbers[0]['imei']
                    z.set_serial( "com.tencent.tim", featureCodeInfo )

            self.slot.restore( slotnum )  # 有time_limit分钟没用过的卡槽情况，切换卡槽

            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + slotnum + "号\"" ).communicate( )
            z.sleep( 2 )
            # d.server.adb.cmd( "shell",
            #                   "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
            z.server.adb.run_cmd( "shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" )

            z.sleep(5)
            while d( textContains='正在更新数据' ).exists:
                z.sleep( 2 )
            z.sleep( 3 )
            z.server.adb.run_cmd( "shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" )
            z.sleep( 3 )

            if d( className='android.widget.ImageView', resourceId='com.tencent.tim:id/title', index=1 ).exists:
                for i in range( 0, 2 ):
                    d.swipe( width - 20, height / 2, 0, height / 2, 5 )
                    z.sleep( 1.5 )
                if d( text='立即体验' ).exists:
                    d( text='立即体验' ).click( )
            z.sleep( 2 )
            z.heartbeat()
            if d( textContains="请在小米神隐模式中将TIM设置为“无限制”。" ).exists:
                z.toast( "我是小米神隐" )
                d( text='我知道了' ).click( )
            elif d( text='消息' ).exists or d( text='马上绑定' ).exists or d( text='匹配手机通讯录' ).exists:
                if d( text='匹配手机通讯录' ).exists:  # 登陆上后弹出t通讯录的情况
                    d( text='匹配手机通讯录' ).click( )
                    z.sleep( 1.5 )
                    if d( text='取消' ).exists:
                        d( text='取消' ).child( )
                z.toast("卡槽QQ切换成功，继续执行")
            else:
                obj = self.slot.getSlotInfo( slotnum )
                remark = obj['remark']
                remarkArr = remark.split( "_" )
                QQnumber = remarkArr[1]
                if d(text='去安全中心').exists:
                    self.repo.BackupInfo(cate_id, 'frozen', QQnumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber

                else:
                    self.repo.BackupInfo(cate_id, 'normal', QQnumber, '', '')

                self.slot.clear( slotnum )  # 清空改卡槽，并补登
                z.toast("卡槽QQ状态异常，补登陆卡槽")
                self.action( d, z, args )

        else:  # 有空卡槽的情况
            d.server.adb.cmd( "shell", "pm clear com.tencent.tim" ).communicate( )  # 清除缓存

            # d.server.adb.cmd("shell", "settings put global airplane_mode_on 1").communicate()
            # d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true").communicate()
            # z.sleep(3)
            # d.server.adb.cmd("shell", "settings put global airplane_mode_on 0").communicate()
            # d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false").communicate()
            z.heartbeat( )
            # z.toast( "正在ping网络是否通畅" )
            # while True:
            #     ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            #     print( ping )
            #     if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
            #         break
            #     z.sleep( 2 )

            serialinfo = d.server.adb.device_serial( )
            # print('登陆时的serial%s'%serialinfo)
            z.heartbeat( )
            QQnumber = self.login( d, args, z )
            if QQnumber == 'nothing':
                self.slot.clear( slotnum )  # 清空改卡槽，并补登
                self.action( d, z, args )
            elif QQnumber == 0:
                z.toast( "仓库为空，无法登陆。开始切换卡槽" )
                self.qiehuan( d, z, args )
            elif QQnumber is None:
                return
            else:
                z.heartbeat()
                z.toast("登陆成功")
                featureCodeInfo = z.get_serial("com.tencent.tim")
                self.slot.backup( slotnum, str( slotnum ) + '_' + QQnumber + '_' + cate_id)  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo( cate_id, 'using', QQnumber, featureCodeInfo, '%s_%s_%s' % (
                    d.server.adb.device_serial( ), self.type, slotnum) )  # 仓库号,使用中,QQ号,设备号_卡槽号


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMLoginSlot


if __name__ == "__main__":
    import sys
    reload( sys )
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()

    d = Device("9cae944e")
    z = ZDevice("9cae944e")

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_cate_id": "358", "time_limit": "0", "time_limit1": "120","time_delay1":"10","time_delay": "3","failCount":"3"}  # cate_id是仓库号，length是数量
    # o.action(d, z, args)

    # d.server.adb.cmd( "shell","su -c 'rm -r -f /storage/emulated/0/tencent/QQmail'")


    # d.server.adb.cmd( "shell", "pm clear com.tencent.tim" ).communicate( )  # 清除缓存
    # d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
    # z.server.adb.run_cmd( "shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" )
    # serial = d.server.adb.device_serial( )
    # type = 'tim'
    # slot = Slot( serial, type )
    # d.server.adb.cmd( "shell", "pm clear com.tencent.mobileqq" ).communicate( )  # 清除缓存
    # slot.clear( "1" )
    # for i in range(2,20):
    #     slot.clear(i)
    #     print('已经清除')
    # print('全部清除')
    # o.repo.BackupInfo( "241", 'using', "2827519631", "dsa", '%s_%s_%s' % (
    #     d.server.adb.device_serial( ), "tim", "1") )  # 仓库号,使用中,QQ号,设备号_卡槽号