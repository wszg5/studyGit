# coding:utf-8
import base64
import os
import random
from uiautomator import Device
from Repo import *
from util import logger
from zservice import ZDevice
from PIL import Image

from imageCode import imageCode
from smsCode import smsCode


class QQMailLoginNZ:
    def __init__(self):
        self.repo = Repo()
        self.type = 'qqmail'

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 1000)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

    def input(self,z,height,text):
        if height>888:
            z.input(text)
        else:
            z.cmd( "shell", "am broadcast -a ZY_INPUT_TEXT --es text \\\"%s\\\"" % text )

    def palyCode(self, d, z, picObj):
        self.scode = smsCode(d.server.adb.device_serial())
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))
        icode = imageCode()
        im_id = ""
        code = ""
        for i in range(0, 2):  # 打码循环
            if i > 0:
                icode.reportError(im_id)
            obj = picObj.info
            obj = obj['bounds']  # 验证码处的信息
            left = obj["left"]  # 验证码的位置信息
            top = obj['top']
            right = obj['right']
            bottom = obj['bottom']

            d.screenshot(sourcePng)  # 截取整个输入验证码时的屏幕

            img = Image.open(sourcePng)
            box = (left, top, right, bottom)  # left top right bottom
            region = img.crop(box)  # 截取验证码的图片

            img = Image.new('RGBA', (right - left, bottom - top))
            img.paste(region, (0, 0))

            img.save(codePng)
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
                    break
                else:
                    continue
                # print data
            # im = open(codePng, 'rb')
            #
            # codeResult = icode.getCode(im, icode.CODE_TYPE_4_NUMBER_CHAR, 60)
            #
            # code = codeResult["Result"]
            # im_id = codeResult["Id"]
            os.remove(sourcePng)
            os.remove(codePng)
            z.heartbeat()
            break
            # if code.isalpha() or code.isisdigitv() or code.isalnum():
            #     break
            # else:
            #     continue

        return code

    def action(self, d,z,args):
        # z.toast("正在ping网络是否通畅")
        # i = 0
        # while i < 200:
        #     i += 1
        #     ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
        #     print(ping)
        #     if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
        #         z.toast(u"网络通畅。开始执行：QQ邮箱登录 无卡槽" )
        #         break
        #     z.sleep(2)
        # if i > 200:
        #     z.toast(u"网络不通，请检查网络状态" )
        #     return
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
            for x in range(2):
                if args['mail_type'] == '163邮箱登录':
                    if d(resourceId='com.tencent.androidqqmail:id/ee').exists:  # 选择163邮箱点击进入登陆页面
                        d(resourceId='com.tencent.androidqqmail:id/ee').click()
                        z.sleep(1)
                        break
                    else:
                        d.server.adb.cmd( "shell",
                                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        time.sleep(25)
                        continue

                if args['mail_type'] == 'QQ邮箱登录':
                    if d(resourceId='com.tencent.androidqqmail:id/ea').exists:  # 选择QQ邮箱点击进入登陆页面
                        d(resourceId='com.tencent.androidqqmail:id/ea').click()
                        z.sleep(1)
                        break
                    else:
                        d.server.adb.cmd( "shell",
                                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        time.sleep( 25 )
                        continue

                if args['mail_type'] == '腾讯企业邮箱登录':
                    if d(resourceId='com.tencent.androidqqmail:id/eb').exists:  # 选择腾讯企业邮箱登录点击进入登陆页面
                        d(resourceId='com.tencent.androidqqmail:id/eb').click()
                        z.sleep(1)
                        break
                    else:
                        d.server.adb.cmd( "shell",
                                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        time.sleep( 25 )
                        continue



            if d(text='帐号密码登录').exists:
                d(text='帐号密码登录').click()

            if d(resourceId='com.tencent.androidqqmail:id/bi').exists:  # 输入邮箱帐号
                accounts = self.repo.GetAccount( args['repo_account_id'], int( args['account_time_limit'] ),
                                                 1 )  # 去仓库获取QQ邮箱帐号
                if len( accounts ) == 0:
                    z.toast( u"帐号库为空" )
                    return

                account = accounts[0]['number']
                password = accounts[0]['password']
                # account = "17094558161"
                # password = "tifo5456"
                d(resourceId='com.tencent.androidqqmail:id/bi').set_text(account)
                # z.input(account )
            else:
                z.toast("判断不出来界面")
                return

            if d(resourceId='com.tencent.androidqqmail:id/bs').exists:  # 输入邮箱密码
                d(resourceId='com.tencent.androidqqmail:id/bs').click()
                z.input(password)

            if d(resourceId='com.tencent.androidqqmail:id/a_').exists:  # 点击登录按钮
                d(resourceId='com.tencent.androidqqmail:id/a_').click()

            z.sleep(8)
            while True:
                if d(textContains="验证中"):
                    time.sleep(3)
                else:
                    break
            if args['mail_type'] == 'QQ邮箱登录':
                if d(resourceId='com.tencent.androidqqmail:id/h').exists:  # 判断是否要填写独立密码
                    z.input("Abc" + account)
                    z.sleep(1)
                    if d(text='确定').exists:
                        d(text='确定').click()
                    z.sleep(5)

                while d(resourceId='com.tencent.androidqqmail:id/a16').exists:  # 出现验证码
                    picObj = d(resourceId='com.tencent.androidqqmail:id/a19', index=0)
                    code = self.palyCode(d, z, picObj)
                    if code == "":
                        return False
                    if d(resourceId='com.tencent.androidqqmail:id/a17').exists:
                        d(resourceId='com.tencent.androidqqmail:id/a17').click()
                    z.input(code)
                    if d(resourceId='com.tencent.androidqqmail:id/a_').exists:  # 点击登陆
                        d(resourceId='com.tencent.androidqqmail:id/a_').click()
                    z.sleep(8)

                if d(resourceId='com.tencent.androidqqmail:id/h').exists:  # 判断是否要填写独立密码
                    z.input("Abc" + account)
                    z.sleep(1)
                    if d(text='确定').exists:
                        d(text='确定').click()

            if args['mail_type'] == '163邮箱登录' or args['mail_type'] == '腾讯企业邮箱登录':
                if d(resourceId='com.tencent.androidqqmail:id/a_').exists:   # 点击登录按钮
                    obj = d(resourceId="com.tencent.androidqqmail:id/e4",className="android.widget.EditText")
                    repo_name_cateId = args["repo_name_cateId"]
                    Material = self.repo.GetMaterial( repo_name_cateId, 0, 1 )
                    if len( Material ) == 0:
                        d.server.adb.cmd( "shell",
                                          "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_name_cateId ).communicate( )
                        z.sleep( 10 )
                        return
                    message = Material[0]['content']
                    name = ""
                    if obj.exists:
                        name = obj.info["text"]
                        if len(name)>1:
                            obj.click()
                            for nameL in range( len( name ) ):
                                d.press.right()
                            time.sleep(1)
                            for nameL in range(len(name)):
                                d.press.delete()
                            time.sleep(1)
                            z.input(message)
                        else:
                            z.input( message )
                    else:
                        if d(textContains="发信昵称",resourceId="com.tencent.androidqqmail:id/e3").exists:
                            d( textContains="发信昵称", resourceId="com.tencent.androidqqmail:id/e3" ).click()
                            time.sleep(1)
                            z.input( message )
                            time.sleep(1)

                    d(resourceId='com.tencent.androidqqmail:id/a_').click()
                    z.sleep(1)
                    z.heartbeat()
                    z.toast("登陆成功")
                    d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
                    return True
                else:
                    while True:
                        if not d( text='收件箱​',resourceId="com.tencent.androidqqmail:id/t0" ).exists and d(textContains=account,resourceId="com.tencent.androidqqmail:id/ac").exists:
                            time.sleep(5)
                        else:
                            break
                    if d( text='收件箱​' ).exists:
                        if d( description="写邮件和设置等功能" ).exists:
                            d( description="写邮件和设置等功能" ).click( )
                            z.sleep( 0.5 )
                            if d( text="设置", resourceId="com.tencent.androidqqmail:id/w1" ).exists:
                                d( text="设置", resourceId="com.tencent.androidqqmail:id/w1" ).click( )
                                z.sleep( 0.5 )

                        if d( textContains=account, className="android.widget.TextView" ).exists:
                            d( textContains=account, className="android.widget.TextView" ).click( )
                            z.sleep( 1 )

                        objName = d( index=1, className="android.widget.LinearLayout" ).child( index=1,
                                                                                               className="android.widget.TextView" )
                        name = ""
                        if objName.exists:
                            name = objName.info["text"]

                        if d( index=1, className="android.widget.LinearLayout" ).child( index=2,
                                                                                        className="android.widget.ImageView" ).exists:
                            d( index=1, className="android.widget.LinearLayout" ).child( index=2,
                                                                                         className="android.widget.ImageView" ).click( )
                            z.sleep( 2 )
                            z.heartbeat( )
                            nameLen = len( name )
                            repo_name_cateId = args["repo_name_cateId"]
                            Material = self.repo.GetMaterial( repo_name_cateId, 0, 1 )
                            if len( Material ) == 0:
                                d.server.adb.cmd( "shell",
                                                  "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_name_cateId ).communicate( )
                                z.sleep( 10 )
                                return
                            message = Material[0]['content']
                            if nameLen == 1:
                                if d( text="默认发信昵称​", className="android.widget.TextView" ).exists:
                                    d( text="默认发信昵称​", className="android.widget.TextView" ).click( )
                                    time.sleep( 0.5 )
                                    z.input( message.encode( "utf-8" ) )
                                    time.sleep( 0.5 )
                                    if d( index=0, resourceId="com.tencent.androidqqmail:id/a6",
                                          className="android.widget.ImageButton" ).exists:
                                        d( index=0, resourceId="com.tencent.androidqqmail:id/a6",
                                           className="android.widget.ImageButton" ).click( )
                                        z.sleep( 1 )
                            else:
                                if d( text=name, className="android.widget.TextView" ).exists:
                                    d( text=name, className="android.widget.TextView" ).click( )
                                    for i in range( 0, nameLen ):
                                        d.press.delete( )
                                    z.input( message.encode( "utf-8" ) )
                                    if d( index=0, resourceId="com.tencent.androidqqmail:id/a6",
                                          className="android.widget.ImageButton" ).exists:
                                        d( index=0, resourceId="com.tencent.androidqqmail:id/a6",
                                           className="android.widget.ImageButton" ).click( )
                                        z.sleep( 1 )
                        z.toast("登陆成功")
                        return True

                    # d.server.adb.cmd( "shell",
                    #                   "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱


            # if args['mail_type'] == '腾讯企业邮箱登录':
            #     if d(resourceId='com.tencent.androidqqmail:id/a_').exists:   # 点击登录按钮
            #         d(resourceId='com.tencent.androidqqmail:id/a_').click()
            #         z.sleep(3)
            #         z.heartbeat()
            #         d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
            #         d.server.adb.cmd( "shell",
            #                           "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
            #
            #     if d( text='收件箱​' ).exists:
            #         z.toast( u"登录成功。退出模块" )
            #         # d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).wait( )  # 强制停止
            #         return True
            #     else:
            #         return False
            # d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止163邮箱
            # d.server.adb.cmd("shell", "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail").communicate()  # 拉起163邮箱

            z.sleep(12)
            z.heartbeat()
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
                    againCount = int(args["againCount"])
                    for ac in range(againCount):
                        result = self.againLogin(account,password,d,z,height)
                        if result is True:
                            z.toast("跳出模块")
                            return
                    else:
                        z.toast( u"一直登陆出现密码错误,跳出该帐号")

                    # self.repo.BackupInfo(args["repo_account_id"], 'frozen', account, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                elif d(textContains="未开启IMAP服务").exists:
                    z.toast( u"未开启IMAP服务，标记为异常" )
                    self.repo.BackupInfo( args["repo_account_id"], 'exception', account, '','' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                elif d(text='当前网络不可用').exists:
                    z.toast('当前网络不可用,跳出模块')
                    return True
                self.action(d,z,args)
        except:
            logging.exception("exception")
            z.toast(u"程序出现异常，模块退出")
            d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
            return False

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
                z.input( "Abc" + account )
                z.sleep( 1 )
                if d( text='确定' ).exists:
                    d( text='确定' ).click( )
                z.sleep( 5 )

            while d( resourceId='com.tencent.androidqqmail:id/a16' ).exists:  # 出现验证码
                picObj = d( resourceId='com.tencent.androidqqmail:id/a19', index=0 )
                code = self.palyCode( d, z, picObj )
                if code == "":
                    return False
                if d( resourceId='com.tencent.androidqqmail:id/a17' ).exists:
                    d( resourceId='com.tencent.androidqqmail:id/a17' ).click( )
                z.input( code )
                if d( resourceId='com.tencent.androidqqmail:id/a_' ).exists:  # 点击登陆
                    d( resourceId='com.tencent.androidqqmail:id/a_' ).click( )
                z.sleep( 8 )

            if d( resourceId='com.tencent.androidqqmail:id/h' ).exists:  # 判断是否要填写独立密码
                z.input( "Abc" + account )
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




def getPluginClass():
    return QQMailLoginNZ

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT51DSK01490")
    z = ZDevice("HT51DSK01490")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "250", "account_time_limit": "15","mail_type": "QQ邮箱登录","repo_name_cateId":"234","againCount":"10"}
    # d.dump( 'test.xml' )
    # o.palyCode(d,z,"dsa")
    o.action(d, z, args)

    # slot = Slot(d.server.adb.device_serial(),'qqmail')
    # slot.clear(2)
    # d.server.adb.cmd( "shell", "pm clear com.tencent.androidqqmail" ).communicate( )  # 清除缓存
    # slot.restore( 1 )
    # d.server.adb.cmd( "shell",
    #                   "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱