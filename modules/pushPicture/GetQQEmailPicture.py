# coding:utf-8
import os
import uuid

import requests
from PIL import Image

from imageCode import imageCode
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
import string


class GetQQEmailPicture:
    def __init__(self):
        self.repo = Repo()

    def get_pic(self,d,z,args):
        Str = d.info  # 获取屏幕大小等信息
        height = int( Str["displayHeight"] )
        width = int( Str["displayWidth"] )
        z.heartbeat( )
        z.heartbeat( )
        z.generate_serial( "com.tencent.androidqqmail" )  # 随机生成手机特征码
        d.server.adb.cmd( "shell",
                          "su -c 'rm -r -f /storage/emulated/0/tencent/QQmail'" )  # 删除/storage/emulated/0/tencent/QQmail文件夹
        time.sleep( 2 )
        d.server.adb.cmd( "shell", "pm clear com.tencent.androidqqmail" ).communicate( )  # 清除QQ邮箱缓存
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
        z.sleep( 15 )
        z.heartbeat( )
        try:
            for x in range( 2 ):
                if d( resourceId='com.tencent.androidqqmail:id/ea' ).exists:  # 选择QQ邮箱点击进入登陆页面
                    d( resourceId='com.tencent.androidqqmail:id/ea' ).click( )
                    z.sleep( 1 )
                    break
                # if d(resourceId='com.tencent.androidqqmail:id/ea').exists:  # 选择QQ邮箱点击进入登陆页面
                #     d(resourceId='com.tencent.androidqqmail:id/ea').click()
                #     z.sleep(1)
                #     break
                else:
                    d.server.adb.cmd( "shell",
                                      "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                    time.sleep( 25 )
                    continue

            if d( text='帐号密码登录' ).exists:
                d( text='帐号密码登录' ).click( )

            # random_code = args['random_code']
            if d( resourceId='com.tencent.androidqqmail:id/bi' ).exists:  # 输入邮箱帐号
                accounts = self.repo.GetAccount( args['repo_account_id'], int( args['account_time_limit'] ),
                                                 1 )  # 去仓库获取QQ邮箱帐号
                # accounts = self.repo.GetAccount( args['repo_account_id'], int( args['account_time_limit'] ),
                #                                  1 )  # 去仓库获取QQ邮箱帐号
                if len( accounts ) == 0:
                    z.toast( u"帐号库为空" )
                    return

                account = accounts[0]['number']
                password = accounts[0]['password']

                # account = '1006329641'
                # password = '13141314AAb'


                d( resourceId='com.tencent.androidqqmail:id/bi' ).set_text( account )
                # self.input( z,height,account )
            else:
                z.toast( "判断不出来界面" )
                return

            if d( resourceId='com.tencent.androidqqmail:id/bs' ).exists:  # 输入邮箱密码
                d( resourceId='com.tencent.androidqqmail:id/bs' ).set_text( password )
                # self.input(random_code,z,password)

            if d( resourceId='com.tencent.androidqqmail:id/a_' ).exists:  # 点击登录按钮
                d( resourceId='com.tencent.androidqqmail:id/a_' ).click( )

            z.sleep( 8 )
            while True:
                if d( textContains="验证中" ):
                    time.sleep( 3 )
                else:
                    break
            if d( resourceId='com.tencent.androidqqmail:id/h' ).exists:  # 判断是否要填写独立密码
                # self.input(random_code,z,"Abc" + account)
                d( resourceId='com.tencent.androidqqmail:id/h' ).set_text( "Abc" + account )
                z.sleep( 1 )
                if d( text='确定' ).exists:
                    d( text='确定' ).click( )
                z.sleep( 5 )

            if d( resourceId='com.tencent.androidqqmail:id/a16' ).exists:  # 出现验证码
                num = int( args['num'] )
                for nu in range( 0, num ):
                    z.heartbeat()
                    picObj = d( resourceId='com.tencent.androidqqmail:id/a19', index=0 )
                    base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
                    if not os.path.isdir( base_dir ):
                        os.mkdir( base_dir )
                    sourcePng = os.path.join( base_dir, "%s_s.png" % (
                    ''.join( random.sample( string.ascii_letters + string.digits, random.randint( 1, 11 ) ) )) )
                    codePng = os.path.join( base_dir, "%s_c.png" % (
                    ''.join( random.sample( string.ascii_letters + string.digits, random.randint( 1, 11 ) ) )) )
                    obj = picObj.info
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
                    time.sleep( 1 )
                    with open( codePng, 'rb' ) as f:
                        salt = ''.join( random.sample( string.ascii_letters + string.digits, random.randint( 1, 11 ) ) )
                        # print salt
                        form = 'png'
                        path = '/tmp/%s.%s' % (uuid.uuid1( ), form)
                        fp = open( path, 'wb' )
                        fp.write( f.read( ) )
                        fp.close( )
                        imgTarget = "/sdcard/Android/%s.%s" % (salt, form)
                        d.server.adb.cmd( "push", path, imgTarget ).wait( )
                        d.server.adb.cmd( "shell",
                                          "am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://%s" % imgTarget ).communicate( )

                    os.remove( sourcePng )
                    os.remove( codePng )
                    z.heartbeat( )
                    picObj.click( )
                    time.sleep( 0.5 )
            else:
                z.toast( "没出验证码,跳出" )

            z.heartbeat( )
            if d( textContains='你有多个应用同时收到' ).exists:
                d( text='确定' ).click( )
                z.sleep( 2 )

            if d( text='收件箱​' ).exists:
                z.toast( u"登录成功。退出模块" )
                # d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
                return True
            else:
                if d( textContains='帐号或密码错误' ).exists:
                    z.toast( u"帐号或密码错误" )
                    againCount = int( args["againCount"] )
                    for ac in range( againCount ):
                        result = self.againLogin( account, password, d, z, height )
                        if result is True:
                            z.toast( "跳出模块" )
                            return
                    else:
                        z.toast( u"一直登陆出现密码错误,跳出该帐号" )

                        # self.repo.BackupInfo(args["repo_account_id"], 'frozen', account, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                elif d( textContains="未开启IMAP服务" ).exists:
                    z.toast( u"未开启IMAP服务，标记为异常" )
                    self.repo.BackupInfo( args["repo_account_id"], 'exception', account, '',
                                          '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                elif d( text='当前网络不可用' ).exists:
                    z.toast( '当前网络不可用,跳出模块' )
                    return True
                self.action( d, z, args )


        except:
            z.toast( "出错了" )
            return


    def againLogin(self,account,password,d,z,height):
        if d(text="确定",className="android.widget.Button").exists or d(text="重新输入",className="android.widget.Button").exists:
            if d(text="确定",className="android.widget.Button").exists:
                d( text="确定", className="android.widget.Button" ).click()
            else:
                d( text="重新输入", className="android.widget.Button" ).click()
            time.sleep(1)
            z.input( password)
            time.sleep(1)
            if d(resourceId="com.tencent.androidqqmail:id/a_").exists:
                d( resourceId="com.tencent.androidqqmail:id/a_" ).click()
                time.sleep(5)
            while True:
                if d(textContains="验证中"):
                    time.sleep(3)
                else:
                    break
            if d( resourceId='com.tencent.androidqqmail:id/h' ).exists:  # 判断是否要填写独立密码
                z.input("Abc" + account )
                z.sleep( 1 )
                if d( text='确定' ).exists:
                    d( text='确定' ).click( )
                z.sleep( 5 )

            while d( resourceId='com.tencent.androidqqmail:id/a16' ).exists:  # 出现验证码
                picObj = d( resourceId='com.tencent.androidqqmail:id/a19', index=0 )
                num = int( args['num'] )
                for nu in range( 0, num ):
                    picObj = d( resourceId='com.tencent.androidqqmail:id/a19', index=0 )
                    base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
                    if not os.path.isdir( base_dir ):
                        os.mkdir( base_dir )
                    sourcePng = os.path.join( base_dir, "%s_s.png" % (
                        ''.join( random.sample( string.ascii_letters + string.digits, random.randint( 1, 11 ) ) )) )
                    codePng = os.path.join( base_dir, "%s_c.png" % (
                        ''.join( random.sample( string.ascii_letters + string.digits, random.randint( 1, 11 ) ) )) )
                    obj = picObj.info
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
                    time.sleep( 1 )
                    with open( codePng, 'rb' ) as f:
                        salt = ''.join( random.sample( string.ascii_letters + string.digits, random.randint( 1, 11 ) ) )
                        # print salt
                        form = 'png'
                        path = '/tmp/%s.%s' % (uuid.uuid1( ), form)
                        fp = open( path, 'wb' )
                        fp.write( f.read( ) )
                        fp.close( )
                        imgTarget = "/sdcard/Android/%s.%s" % (salt, form)
                        d.server.adb.cmd( "push", path, imgTarget ).wait( )
                        d.server.adb.cmd( "shell",
                                          "am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://%s" % imgTarget ).communicate( )

                    os.remove( sourcePng )
                    os.remove( codePng )
                    z.heartbeat( )
                    picObj.click( )
                    time.sleep( 0.5 )

            if d( resourceId='com.tencent.androidqqmail:id/h' ).exists:  # 判断是否要填写独立密码
                z.input("Abc" + account )
                z.sleep( 1 )
                if d( text='确定' ).exists:
                    d( text='确定' ).click( )

            if d(textContains='你有多个应用同时收到').exists:
                d(text='确定').click()
                z.sleep(2)

            if d(text='收件箱​').exists:
                z.toast(u"登录成功。退出模块")
                # d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
                return True
            else:
                if d(textContains='帐号或密码错误').exists:
                    z.toast(u"帐号或密码错误")
                    return False
                elif d(textContains="未开启IMAP服务").exists:
                    z.toast( u"未开启IMAP服务，标记为异常" )
                    self.repo.BackupInfo( args["repo_account_id"], 'exception', account, '','' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                    return False
                elif d(text='当前网络不可用').exists:
                    z.toast('当前网络不可用,跳出模块')
                    return True


    def action(self, d,z, args):
        againCount = int(args['againCount'])
        for i in range(againCount):
            self.get_pic(d,z,args)



def getPluginClass():
    return GetQQEmailPicture

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("3eed4e7b")
    z = ZDevice("3eed4e7b")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "413", "account_time_limit": "15",'num':'100','againCount':20}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
