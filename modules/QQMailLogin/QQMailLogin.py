# coding:utf-8
import colorsys
import os
import random

from PIL import Image

from imageCode import imageCode
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class QQMailLogin:
    def __init__(self):
        self.repo = Repo()
        self.type = 'qqmail'

    def GetUnique(self):
        nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" );  # 生成当前时间
        randomNum = random.randint( 0, 1000 );  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str( 00 ) + str( randomNum );
        uniqueNum = str( nowTime ) + str( randomNum );
        return uniqueNum

    def WebViewBlankPages(self, d, z):
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

        if screenScale == 0.61:
            left = 55  # 验证码的位置信息
            top = 420
            right = 460
            bottom = 460

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

    def palyCode(self):
        print


    def login(self, d, z, args):
        z.heartbeat()
        cate_id = args["repo_account_id"]
        time_limit1 = args['time_limit1']
        numbers = self.repo.GetAccount( cate_id, time_limit1, 1 )
        if len( numbers ) == 0:
            z.heartbeat( )
            d.server.adb.cmd( "shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库无%s分钟未用,开始切换卡槽\"" % (
                cate_id, time_limit1) ).communicate( )
            z.sleep( 2 )
            return 0

        QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        QQPassword = numbers[0]['password']
        z.sleep( 1 )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "pm clear com.tencent.androidqqmail" ).communicate( )  # 清除缓存
        z.sleep(2)
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
        z.sleep( 5 )
        while d( textContains='正在更新数据' ).exists:
            z.sleep( 2 )

        z.sleep( 15 )
        z.heartbeat( )
        d.dump( compressed=False )
        if d(description='QQ邮箱').exists:
            d(description='QQ邮箱').click()
        z.sleep(5)

        z.heartbeat( )
        if not self.WebViewBlankPages(d, z) is None:
            if self.WebViewBlankPages( d, z )[2] > 200:
                d.click( 130, 280 )
                z.input( QQNumber )
                z.sleep( 1 )
                d.click( 130, 360 )
                z.input( QQPassword )
                z.sleep( 1 )
                d.click( 270, 443 )

                print('QQ号:%s,QQ密码：%s' % (QQNumber, QQPassword))
                z.sleep( int( args['time_delay2'] ) )

                z.heartbeat( )
                if d( text='收件箱​' ).exists or d( text='温馨提示​' ).exists:
                    z.toast( "登陆成功" )
                    return QQNumber

                elif d( description='安全验证' ).exists:
                    self.repo.BackupInfo( cate_id, 'frozen', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                    z.toast( "卡槽QQ状态异常，跳过此模块" )
                    return "nothing"

                elif self.WebViewBlankPages( d, z )[2] > 200:
                    self.repo.BackupInfo( cate_id, 'normal', QQNumber, '', '' )
                    return "nothing"

                else:
                    self.repo.BackupInfo( cate_id, 'normal', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                    z.toast( "卡槽QQ状态异常，跳过此模块" )
                    return "nothing"
            else:
                self.repo.BackupInfo( cate_id, 'normal', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                return "nothing"

        else:
            self.repo.BackupInfo( cate_id, 'normal', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
            return "nothing"

    def qiehuan(self, d, z, args):
        time_limit = int( args['time_limit'] )
        serial = d.server.adb.device_serial( )
        self.slot = Slot( serial, self.type )
        slotObj = self.slot.getAvailableSlot( time_limit )  # 没有空卡槽，取２小时没用过的卡槽

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
        d.server.adb.cmd( "shell", "pm clear com.tencent.androidqqmail" ).communicate( )  # 清除缓存

        obj = self.slot.getSlotInfo( slotnum )
        remark = obj['remark']
        remarkArr = remark.split( "_" )
        if len( remarkArr ) == 3:
            slotInfo = d.server.adb.device_serial( ) + '_' + self.type + '_' + slotnum
            cateId = remarkArr[2]
            numbers = self.repo.Getserial( cateId, slotInfo )
            if len( numbers ) != 0:
                featureCodeInfo = numbers[0]['imei']
                z.set_serial( "com.tencent.androidqqmail", featureCodeInfo )

        self.slot.restore( slotnum )  # 有time_limit分钟没用过的卡槽情况，切换卡槽
        z.sleep( 2 )

        d.server.adb.cmd( "shell",
                          "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + slotnum + "号\"" ).communicate( )
        z.sleep( 2 )
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
        z.sleep( 5 )
        while d( textContains='正在更新数据' ).exists:
            z.sleep( 2 )
        z.sleep( 20 )

        z.heartbeat( )
        d.dump( compressed=False )
        if d( text='密码错误，请重新输入' ).exists:
            QQnumber = remarkArr[1]
            self.repo.BackupInfo( cateId, 'normal', QQnumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber

            self.slot.clear( slotnum )  # 清空改卡槽，并补登
            z.toast( "卡槽易信号状态异常，补登陆卡槽" )
            self.action( d, z, args )

        else:
            z.toast( "邮箱登陆状态正常，切换完毕。" )
            return


    def action(self, d,z,args):
        z.toast( "正在ping网络是否通畅" )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：ＱＱ邮箱登录 有卡槽" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep(int(args["time_delay"]))
            return

        z.heartbeat( )
        z.generate_serial( "com.tencent.androidqqmail" )  # 随机生成手机特征码

        serial = d.server.adb.device_serial( )
        self.slot = Slot( serial, self.type )
        slotnum = self.slot.getEmpty( )  # 取空卡槽
        if slotnum == 0:  # 没有空卡槽的话
            self.qiehuan( d, z, args )

        else:  # 有空卡槽的情况
            QQnumber = self.login( d, z, args )

            if QQnumber == 'nothing':
                self.slot.clear( slotnum )  # 清空改卡槽，并补登
                self.action( d, z, args )
            if QQnumber == 0:
                z.toast( "仓库为空，无法登陆。开始切换卡槽" )
                self.qiehuan( d, z, args )

            z.heartbeat( )
            featureCodeInfo = z.get_serial( "com.tencent.androidqqmail" )
            self.slot.backup( slotnum, str( slotnum ) + '_' + QQnumber + '_' + args["repo_account_id"] )  # 设备信息，卡槽号，QQ号
            self.repo.BackupInfo( args["repo_account_id"], 'using', QQnumber, featureCodeInfo, '%s_%s_%s' % (
            d.server.adb.device_serial( ), self.type, slotnum) )  # 仓库号,使用中,QQ号,设备号_卡槽号


def getPluginClass():
    return QQMailLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "275", "time_limit": "1", "time_limit1": "120", "time_delay": "3" , "time_delay1": "30", "time_delay2": "30"};
    o.action(d, z, args)

    # slot = Slot(d.server.adb.device_serial(),'qqmail')
    # slot.clear(2)
    # d.server.adb.cmd( "shell", "pm clear com.tencent.androidqqmail" ).communicate( )  # 清除缓存
    # slot.restore( 1 )
    # d.server.adb.cmd( "shell",
    #                   "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱

