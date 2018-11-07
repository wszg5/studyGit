# coding:utf-8
import base64
import colorsys
import os
import random

from PIL import Image

from imageCode import imageCode
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from util import logger
from zservice import ZDevice


class QQMailLogin:
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

    def againLogin(self,account,password,d,z,height):
        if d(text="确定",className="android.widget.Button").exists or d(text="重新输入",className="android.widget.Button").exists:
            if d(text="确定",className="android.widget.Button").exists:
                d( text="确定", className="android.widget.Button" ).click()
            else:
                d( text="重新输入", className="android.widget.Button" ).click()
            time.sleep(1)
            self.input( z, height, password)
            time.sleep(1)
            if d(resourceId="com.tencent.androidqqmail:id/a_").exists:
                d( resourceId="com.tencent.androidqqmail:id/a_" ).click()
                time.sleep(8)
            while True:
                if d(textContains="验证中"):
                    time.sleep(3)
                else:
                    break
            if d( resourceId='com.tencent.androidqqmail:id/h' ).exists:  # 判断是否要填写独立密码
                self.input( z, height, "Abc" + account )
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
                self.input( z, height, code )
                if d( resourceId='com.tencent.androidqqmail:id/a_' ).exists:  # 点击登陆
                    d( resourceId='com.tencent.androidqqmail:id/a_' ).click( )
                z.sleep( 8 )

            if d( resourceId='com.tencent.androidqqmail:id/h' ).exists:  # 判断是否要填写独立密码
                self.input( z, height, "Abc" + account )
                z.sleep( 1 )
                if d( text='确定' ).exists:
                    d( text='确定' ).click( )
            while True:
                if d(textContains="验证中"):
                    time.sleep(3)
                else:
                    break
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
            # if i > 0:
            #     icode.reportError(im_id)
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
                else:
                    continue
            os.remove(sourcePng)
            os.remove(codePng)
            z.heartbeat()
            if code.isalpha() or code.isisdigitv() or code.isalnum():
                break
            else:
                continue

        return code

    def login(self, d, z, args, accounts):
        try:
            d.server.adb.cmd( "shell", "pm clear com.tencent.androidqqmail" ).communicate( )  # 清除QQ邮箱缓存
            d.server.adb.cmd( "shell",
                              "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
            z.sleep( 15 )
            z.heartbeat( )
            Str = d.info  # 获取屏幕大小等信息
            height = int( Str["displayHeight"] )
            width = int( Str["displayWidth"] )
            for x in range(2):



                if args['mail_type'] == '163邮箱登录':
                    if d(resourceId='com.tencent.androidqqmail:id/ee').exists:  # 选择163邮箱点击进入登陆页面
                        d(resourceId='com.tencent.androidqqmail:id/ee').click()
                        z.sleep(1)
                        break
                    else:
                        d.server.adb.cmd( "shell",
                                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        z.sleep( 25 )
                        continue

                if args['mail_type'] == 'QQ邮箱登录':
                    if d(resourceId='com.tencent.androidqqmail:id/ea').exists:  # 选择QQ邮箱点击进入登陆页面
                        d(resourceId='com.tencent.androidqqmail:id/ea').click()
                        z.sleep(1)
                        break
                    else:
                        d.server.adb.cmd( "shell",
                                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        z.sleep( 25 )
                        continue

                if args['mail_type'] == '腾讯企业邮箱登录':
                    if d(resourceId='com.tencent.androidqqmail:id/eb').exists:  # 选择腾讯企业邮箱登录点击进入登陆页面
                        d(resourceId='com.tencent.androidqqmail:id/eb').click()
                        z.sleep(1)
                        break
                    else:
                        d.server.adb.cmd( "shell",
                                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        z.sleep( 25 )
                        continue

            account = accounts[0]['number']
            password = accounts[0]['password']

            if d(text='帐号密码登录').exists:
                d(text='帐号密码登录').click()


            if d(resourceId='com.tencent.androidqqmail:id/bi').exists:  # 输入邮箱帐号
                d(resourceId='com.tencent.androidqqmail:id/bi').click()
                # self.input(z,height,account)
                self.input(z,height,account )
            else:
                return

            if d(resourceId='com.tencent.androidqqmail:id/bs').exists:  # 输入邮箱密码
                d(resourceId='com.tencent.androidqqmail:id/bs').click()
                self.input(z,height,password)

            if d(resourceId='com.tencent.androidqqmail:id/a_').exists:  # 点击登录按钮
                d(resourceId='com.tencent.androidqqmail:id/a_').click()

            z.sleep(20)
            while True:
                if d(textContains="验证中"):
                    time.sleep(3)
                else:
                    break
            if args['mail_type'] == 'QQ邮箱登录':
                if d(resourceId='com.tencent.androidqqmail:id/h').exists:  # 判断是否要填写独立密码
                    self.input(z,height,"Abc" + account)
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
                    self.input(z,height,code)
                    if d(resourceId='com.tencent.androidqqmail:id/a_').exists:  # 点击登陆
                        d(resourceId='com.tencent.androidqqmail:id/a_').click()
                    z.sleep(8)

                if d(resourceId='com.tencent.androidqqmail:id/h').exists:  # 判断是否要填写独立密码
                    self.input(z,height,"Abc" + account)
                    z.sleep(1)
                    if d(text='确定').exists:
                        d(text='确定').click()

            if args['mail_type'] == '163邮箱登录':
                if d(resourceId='com.tencent.androidqqmail:id/a_').exists:   # 点击完成按钮
                    d(resourceId='com.tencent.androidqqmail:id/a_').click()
                    time.sleep(3)
                    d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
                    d.server.adb.cmd( "shell",
                                      "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                    # z.sleep(3)
                    # z.heartbeat()

                # d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止163邮箱
                # d.server.adb.cmd("shell", "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail").communicate()  # 拉起163邮箱

            if args['mail_type'] == '腾讯企业邮箱登录':
                if d(resourceId='com.tencent.androidqqmail:id/a_').exists:   # 点击登录按钮
                    d(resourceId='com.tencent.androidqqmail:id/a_').click()
                    z.sleep(3)
                    z.heartbeat()
                    d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
                    d.server.adb.cmd( "shell",
                                      "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱

                if d( text='收件箱​' ).exists:
                    z.toast( u"登录成功。退出模块" )
                    # d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).wait( )  # 强制停止
                    return True
                else:
                    return False
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
                return False
        except:
            logging.exception("exception")
            z.toast(u"程序出现异常，模块退出")
            d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
            return False

    def qiehuan(self, d, z, args):
        Str = d.info  # 获取屏幕大小等信息
        height = int( Str["displayHeight"] )
        width = int( Str["displayWidth"] )
        if args['mail_type'] == '163邮箱登录':
            self.type = '163mail'
        time_limit = int(args['slot_time_limit'])
        serial = d.server.adb.device_serial()
        self.slot = Slot(serial, self.type)
        slotObj = self.slot.getAvailableSlot(time_limit)  # 没有空卡槽，取２小时没用过的卡槽

        slotnum = None
        if not slotObj is None:
            slotnum = slotObj['id']

        while slotObj is None:  # 2小时没用过的卡槽也为没有的情况
            d.server.adb.cmd("shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"").communicate()
            z.heartbeat()
            z.sleep(30)
            slotObj = self.slot.getAvailableSlot(time_limit)
            if not slotObj is None:
                slotnum = slotObj['id']
                break

        z.heartbeat()
        d.server.adb.cmd("shell", "pm clear com.tencent.androidqqmail").communicate()  # 清除缓存

        obj = self.slot.getSlotInfo(slotnum)
        remark = obj['remark']
        remarkArr = remark.split("_")
        cateId = args['repo_account_id']
        if len(remarkArr) == 3:
            slotInfo = d.server.adb.device_serial() + '_' + self.type + '_' + slotnum
            cateId = remarkArr[2]
            numbers = self.repo.Getserial(cateId, slotInfo)
            if len(numbers) != 0:
                featureCodeInfo = numbers[0]['imei']
                z.set_serial("com.tencent.androidqqmail", featureCodeInfo)

        self.slot.restore(slotnum)  # 有time_limit分钟没用过的卡槽情况，切换卡槽
        z.sleep(2)

        d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + slotnum + "号\"").communicate()
        z.sleep(2)
        d.server.adb.cmd("shell", "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail").communicate()  # 拉起QQ邮箱
        z.sleep(5)
        while d(textContains='正在更新数据').exists:
            z.sleep(2)
        z.sleep(20)

        z.heartbeat()
        d.dump(compressed=False)
        if d(text='密码错误，请重新输入').exists or d(description='QQ邮箱').exists:
            QQnumber = remarkArr[1]
            self.repo.BackupInfo(cateId, 'normal', QQnumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber

            self.slot.clear(slotnum)  # 清空改卡槽，并补登
            z.toast("卡槽邮箱号状态异常，补登陆卡槽")
            return False

        else:
            z.toast("邮箱登陆状态正常，切换完毕。")
            return True

    def action(self, d, z, args):

        while True:
            # z.toast("正在ping网络是否通畅")
            # i = 0
            # while i < 200:
            #     i += 1
            #     ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
            #     # print(ping)
            #     if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
            #         z.toast(u"网络通畅。开始执行：" + args['mail_type'] + u" 有卡槽")
            #         break
            #     z.sleep(2)
            # if i > 200:
            #     z.toast(u"网络不通，请检查网络状态")
            #     return
            Str = d.info  # 获取屏幕大小等信息
            height = int( Str["displayHeight"] )
            width = int( Str["displayWidth"] )
            z.heartbeat()
            z.generate_serial("com.tencent.androidqqmail")  # 随机生成手机特征码
            d.server.adb.cmd( "shell",
                              "su -c 'rm -r -f /storage/emulated/0/tencent/QQmail'" )  # 删除/storage/emulated/0/tencent/QQmail文件夹
            time.sleep( 2 )
            if args['mail_type'] == '163邮箱登录':
                self.type = '163mail'

            accounts = self.repo.GetAccount(args['repo_account_id'], int(args['account_time_limit']), 1)  # 去仓库获取QQ邮箱帐号
            if len(accounts) == 0:
                z.toast(u"帐号库为空")

            # self.qiehuan( d, z, args )
            serial = d.server.adb.device_serial()
            self.slot = Slot(serial, self.type)
            slotnum = self.slot.getEmpty()  # 取空卡槽
            if slotnum == 0 or len(accounts) == 0:  # 没有空卡槽的话或者仓库没有可登陆的帐号，进行卡槽切换。
                if self.qiehuan(d, z, args):
                    break
                else:
                    continue
            else:  # 有空卡槽的情况

                QQnumber = accounts[0]['number']
                password = accounts[0]['password']
                # print QQnumber
                if self.login(d, z, args, accounts):
                    z.heartbeat()
                    featureCodeInfo = z.get_serial("com.tencent.androidqqmail")
                    self.slot.backup(slotnum, str(slotnum) + '_' + QQnumber + '_' + args["repo_account_id"])  # 设备信息，卡槽号，QQ号
                    self.repo.BackupInfo(args["repo_account_id"], 'using', QQnumber, featureCodeInfo, '%s_%s_%s' % (
                        d.server.adb.device_serial(), self.type, slotnum))  # 仓库号,使用中,QQ号,设备号_卡槽号
                    break

                else:
                    self.slot.clear(slotnum)  # 清空改卡槽，并补登
                    if d(text='本次登录存在异常，如需帮助请前往安全中心').exists:
                        z.toast(u"登录失败。重新登录")
                        self.repo.BackupInfo(args["repo_account_id"], 'frozen', QQnumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                    elif d(textContains='帐号或密码错误').exists:
                        z.toast(u"帐号或密码错误")
                        againCount = int(args["againCount"])
                        for ac in range( againCount ):
                            result = self.againLogin( QQnumber, password, d, z, height )
                            if result is True:
                                # z.toast( "跳出模块" )
                                return
                        else:
                            z.toast( u"一直登陆出现密码错误,跳出该帐号" )
                        # self.repo.BackupInfo(args["repo_account_id"], 'frozen', QQnumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber

                    elif d( textContains="未开启IMAP服务" ).exists:
                        z.toast( u"未开启IMAP服务，标记为异常" )
                        self.repo.BackupInfo( args["repo_account_id"], 'exception', QQnumber, '',
                                              '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                    else:
                        self.repo.BackupInfo(args["repo_account_id"], 'normal', QQnumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                    continue



def getPluginClass():
    return QQMailLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT51DSK01490")
    z = ZDevice("HT51DSK01490")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "358", "mail_type": "QQ邮箱登录", "account_time_limit": "120", "slot_time_limit": "1","againCount":"4"}
    # print o.repo.GetAccount("345","120",1,"","1")
    # o.repo.UpdateNumberStauts("","104","normal")
    o.action( d, z, args )
    # d.server.adb.cmd( "shell",
    #                   "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
    # Repo().BackupInfo( args["account_cateId"], 'exception', account, '' , '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
    # while True:
    #     # o.action(d, z, args)
    #     o.qiehuan(d,z,args)
    # slot = Slot(d.server.adb.device_serial(),'qqmail')
    # slot.clear(1)
    # d.server.adb.cmd("shell", "pm clear com.tencent.androidqqmail").communicate()  # 清除缓存
    # slot.restore(1)
    # d.server.adb.cmd("shell",
    #                    "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail").communicate()  # 拉起QQ邮箱
    # picObj = d(resourceId='com.tencent.androidqqmail:id/a19', className='android.widget.ImageView')
    # if picObj.exists:
    #     code = o.palyCode(d, z, picObj)
    # if d(description='QQ邮箱').exists:
    #     d(description='QQ邮箱').click()
    #
    # if d(resourceId='com.tencent.androidqqmail:id/ea').exists:
    #     d(resourceId='com.tencent.androidqqmail:id/ea').click()

