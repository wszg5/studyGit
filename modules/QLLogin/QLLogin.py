# coding:utf-8

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

class QLLogin:

    def __init__(self):
        self.repo = Repo()
        self.type = 'qqlite'

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def LoginPlayCode(self, d, z):
        self.scode = smsCode( d.server.adb.device_serial( ) )
        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        codePng = os.path.join( base_dir, "%s_c.png" % (self.GetUnique( )) )
        detection_robot = d( index='3', className="android.widget.EditText" )
        not_detection_robot = d( index='2', className="android.widget.EditText" )
        if detection_robot.exists or not_detection_robot.exists:  # 需要验证码的情况
            icode = imageCode( )
            im_id = ""
            for i in range( 0, 4 ):  # 打码循环
                if i > 0:
                    icode.reportError( im_id )
                obj = d( resourceId='com.tencent.qqlite:id/0',
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
                if not_detection_robot.exists:
                    d( resourceId='com.tencent.qqlite:id/0', index='2',
                       className="android.widget.EditText" ).set_text( code )
                else:
                    detection_robot.set_text( code )
                z.sleep( 3 )
                if d( descriptionContains='验证', className='android.view.View' ).exists:
                    d( descriptionContains='验证', className='android.view.View' ).click( )
                else:
                    d( text='完成', resourceId='com.tencent.qqlite:id/ivTitleBtnRightText' ).click( )
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

    def BindAddressBook(self, z, d, args):
        z.toast( "点击启用" )
        self.scode = smsCode( d.server.adb.device_serial( ) )
        d( text='启用' ).click( )
        while d( text='验证手机号码' ).exists:

            PhoneNumber = None
            j = 0
            while PhoneNumber is None:
                j += 1
                if j == 2:
                    z.toast( '取不到手机号码' )
                    if (args["time_delay"]):
                        z.sleep( int( args["time_delay"] ) )
                    return
                PhoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )  # 获取接码平台手机号码
                z.heartbeat( )


            if not d( textContains='+86' ).exists:
                d( description='点击选择国家和地区' ).click( )
                if d( text='中国' ).exists:
                    d( text='中国' ).click( )
                else:
                    str = d.info  # 获取屏幕大小等信息
                    height = str["displayHeight"]
                    width = str["displayWidth"]
                    d.click(width * 5 / 12, height * 5 / 32)
                    z.sleep(1.5)
                    z.input('中国')
                    z.sleep(2)
                    d(text='+86').click()

            z.input(PhoneNumber)
            z.sleep(1.5)
            if d(text='下一步').exists:
                d(text='下一步').click()
                z.sleep(3)

            while d( text='正在发送请求' ).exists:
                z.sleep( 2 )
            z.sleep(2)
            z.heartbeat( )
            if d( text='确定' ).exists:
                d( text='确定' ).click( )
                z.sleep( 2 )
            code = self.scode.GetVertifyCode( PhoneNumber, self.scode.QQ_CONTACT_BIND, '4' )  # 获取接码验证码
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_CONTACT_BIND )
            if code == '':
                z.toast( PhoneNumber + '手机号,获取不到验证码' )
                if d( text='返回' ).exists:
                    d( text='返回' ).click( )
                if not d( textContains='中国' ).exists:
                    if d( text='返回' ).exists:
                        d( text='返回' ).click( )
                if d( className='android.view.View', descriptionContains='删除' ).exists:
                    d( className='android.view.View', descriptionContains='删除' ).click( )
                continue
            z.heartbeat( )
            z.input( code )
            if d( text='下一步' ).exists:
                d( text='下一步' ).click( )
                z.sleep(1.5)
            if d(text='好').exists:
                d(text='好').click()
            z.sleep(5)
            break

    def login(self,d,args,z):
        z.heartbeat()
        Str = d.info  # 获取屏幕大小等信息
        height = float( Str["displayHeight"] )
        width = float( Str["displayWidth"] )
        W_H = width / height
        screenScale = round( W_H, 2 )

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
        d.server.adb.cmd("shell", "pm clear com.tencent.qqlite").communicate( )  # 清除缓存

        # d.server.adb.cmd("shell",
        #                   "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.server.adb.run_cmd( "shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity" )
        z.sleep(5)
        while d( textContains='正在更新数据' ).exists:
            z.sleep( 2 )
        z.sleep(3)
        z.heartbeat( )
        d.dump(compressed=False)
        if d(text='登 录',resourceId='com.tencent.qqlite:id/btn_login').exists:
            z.toast("控件点击")
            d( text='登 录' ).click()
        else:
            if screenScale == 0.61:
                d.click(140, 788)
            if screenScale == 0.56:
                d.click(186, 1128)
        z.sleep( 1 )
        # d(className='android.widget.EditText', index=0).set_text(QQNumber)  # ﻿1918697054----xiake1234.  QQNumber
        d(className='android.widget.EditText', index=0).click()  # ﻿1918697054----xiake1234.  QQNumber
        z.input( QQNumber )

        z.sleep( 1 )
        # d(resourceId='com.tencent.mobileqq:id/password').set_text(QQPassword)  # Bn2kJq5l     QQPassword
        d(resourceId='com.tencent.qqlite:id/password').click()  # Bn2kJq5l     QQPassword
        z.input( QQPassword )
        z.heartbeat()
        logger = util.logger
        print('QQ号:%s,QQ密码：%s' % (QQNumber, QQPassword))
        d.dump(compressed=False )
        d( text='登 录', resourceId='com.tencent.qqlite:id/login' ).click( )
        z.sleep(1)
        while d(text='登录中').exists:
            z.sleep(2)
        z.sleep(5)
        z.heartbeat()

        detection_robot = d(index='3', className="android.widget.EditText" )
        not_detection_robot = d(resourceId='com.tencent.qqlite:id/0',index='2', className="android.widget.EditText" )
        if detection_robot.exists or not_detection_robot.exists:
            playCodeResult = self.LoginPlayCode( d, z )  # 打验证码
        elif d( text='QQ轻聊版', resourceId='com.tencent.qqlite:id/0',className='android.widget.TextView').exists or d( text='启用' ).exists:
            return QQNumber
        else:
            self.repo.BackupInfo( cate_id, 'frozen', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
            z.toast( "卡槽QQ状态异常，跳过此模块" )
            return "nothing"

        if playCodeResult == "no":
            return "nothing"

        z.sleep(5)
        z.heartbeat()
        if d( text='启用' ).exists:
            # self.BindAddressBook(z, d, args)
            return QQNumber

        if d(text='QQ轻聊版', resourceId='com.tencent.qqlite:id/0',className='android.widget.TextView').exists:
            z.toast("卡槽QQ状态正常，继续执行")
            return QQNumber
        else:
            self.repo.BackupInfo( cate_id, 'frozen', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
            z.toast( "卡槽QQ状态异常，跳过此模块" )
            return "nothing"


    def qiehuan(self,d,z,args):
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
        d.server.adb.cmd("shell", "pm clear com.tencent.qqlite").communicate()  # 清除缓存

        d.server.adb.cmd("shell", "settings put global airplane_mode_on 1").communicate()
        d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true").communicate()
        z.sleep(6)
        z.heartbeat()
        self.slot.restore(slotnum)  # 有time_limit分钟没用过的卡槽情况，切换卡槽
        d.server.adb.cmd("shell", "settings put global airplane_mode_on 0").communicate()
        d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false").communicate()
        z.heartbeat()
        z.toast( "正在ping网络是否通畅" )
        while True:
            ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                break
            z.sleep(2)

        d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + str(slotnum) + "号\"").communicate()
        z.sleep(2)
        # d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.server.adb.run_cmd( "shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity" )

        z.sleep( 5 )
        while d( textContains='正在更新数据' ).exists:
            z.sleep( 2 )
        z.sleep( 3 )
        z.heartbeat()
        if d(text='QQ轻聊版', resourceId='com.tencent.qqlite:id/0',className='android.widget.TextView').exists.exists or d( text='启用' ).exists:
            z.toast( "卡槽QQ切换成功，继续执行" )
        else:
            obj = self.slot.getSlotInfo( slotnum )
            remark = obj['remark']
            remarkArr = remark.split( "_" )
            QQnumber = remarkArr[1]
            self.repo.BackupInfo( cate_id, 'frozen', QQnumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
            self.slot.clear( slotnum )  # 清空改卡槽，并补登
            z.toast( "卡槽QQ状态异常，补登陆卡槽" )
            self.action( d, z, args )


    def action(self,d,z,args):
        z.generate_serial("com.tencent.qqlite")  # 随机生成手机特征码
        z.toast("随机生成手机特征码")


        time_limit = int( args['time_limit'] )
        cate_id = args["repo_cate_id"]
        serial = d.server.adb.device_serial( )
        self.slot = Slot( serial, self.type )
        slotnum = self.slot.getEmpty( )  # 取空卡槽
        if slotnum == 0:  # 没有空卡槽的话
            slotObj = self.slot.getAvailableSlot( time_limit )  # 取空卡槽，取２小时没用过的卡槽
            if not slotObj is None:
                slotnum = slotObj['id']
            print( slotnum )
            while slotObj is None:  # 2小时没用过的卡槽也为没有的情况
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"" ).communicate( )
                z.heartbeat( )
                z.sleep( 10 )
                slotObj = self.slot.getAvailableSlot( time_limit )
                if not slotObj is None:
                    slotnum = slotObj['id']
            z.heartbeat( )
            d.server.adb.cmd( "shell", "pm clear com.tencent.qqlite" ).communicate( )  # 清除缓存

            d.server.adb.cmd("shell", "settings put global airplane_mode_on 1").communicate() #开数据流量
            d.server.adb.cmd("shell","am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true").communicate()#开飞行模式
            z.sleep( 6 )
            z.heartbeat( )
            self.slot.restore( slotnum )  # 有time_limit分钟没用过的卡槽情况，切换卡槽
            d.server.adb.cmd("shell", "settings put global airplane_mode_on 0").communicate() # 关数据流量
            d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false").communicate()#开飞行模式

            z.heartbeat( )
            z.toast( "正在ping网络是否通畅" )
            while True:
                ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
                print( ping )
                if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                    break
                z.sleep( 2 )

            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + slotnum + "号\"" ).communicate( )

            z.sleep( 2 )
            # d.server.adb.cmd( "shell",
            #                   "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
            z.server.adb.run_cmd( "shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity" )

            z.sleep(5)
            while d( textContains='正在更新数据' ).exists:
                z.sleep( 2 )
            z.sleep( 3 )
            z.heartbeat()
            if d(text='QQ轻聊版', resourceId='com.tencent.qqlite:id/0',className='android.widget.TextView').exists or d( text='启用' ).exists:
                z.toast("卡槽QQ切换成功，继续执行")
            else:
                obj = self.slot.getSlotInfo( slotnum )
                remark = obj['remark']
                remarkArr = remark.split( "_" )
                QQnumber = remarkArr[1]
                self.repo.BackupInfo( cate_id, 'frozen', QQnumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                self.slot.clear( slotnum )  # 清空改卡槽，并补登
                z.toast( "卡槽QQ状态异常，补登陆卡槽" )
                self.action( d, z, args )

        else:  # 有空卡槽的情况
            d.server.adb.cmd( "shell", "pm clear com.tencent.qqlite" ).communicate( )  # 清除缓存

            d.server.adb.cmd("shell", "settings put global airplane_mode_on 1").communicate()
            d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true").communicate()
            z.sleep(3)
            d.server.adb.cmd("shell", "settings put global airplane_mode_on 0").communicate()
            d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false").communicate()
            z.heartbeat( )
            z.toast( "正在ping网络是否通畅" )
            while True:
                ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
                print( ping )
                if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                    break
                z.sleep( 2 )
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
                self.slot.backup( slotnum, str( slotnum ) + '_' + QQnumber )  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo( cate_id, 'using', QQnumber, serialinfo, '%s_%s_%s' % (
                    d.server.adb.device_serial( ), self.type, slotnum) )  # 仓库号,使用中,QQ号,设备号_卡槽号


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return QLLogin

if __name__ == "__main__":
    import sys
    reload( sys )
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT49YSK00272")
    z = ZDevice("HT49YSK00272")

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_cate_id": "216", "time_limit": "120", "time_limit1": "120","time_delay": "3"};  # cate_id是仓库号，length是数量
    o.action(d, z, args)
    # d.server.adb.cmd( "shell", "pm clear com.tencent.tim" ).communicate( )  # 清除缓存
    # repo = Repo()
    # serial = d.server.adb.device_serial( )
    # type = 'qqlite'
    # slot = Slot( serial, type )
    # d.server.adb.cmd( "shell", "pm clear com.tencent.mobileqq" ).communicate( )  # 清除缓存
    # slot.clear( "1" )
    # for i in range(1,10):
    #     slot.clear(i)
    #     print('已经清除')
    # print('全部清除')
