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
from util import logger
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

    def palyCode(self, d, z, picObj):
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
            im = open( codePng, 'rb' )

            codeResult = icode.getCode( im, icode.CODE_TYPE_4_NUMBER_CHAR, 60 )

            code = codeResult["Result"]
            im_id = codeResult["Id"]
            os.remove( sourcePng )
            os.remove( codePng )
            z.heartbeat( )

        return code

    def judgmentBounced(self, d):

        if d(text='禁止登录​').exists:
            return "frozen"

        if d(text='登陆失败').exists:

            if d( text="帐号或密码错误" ).exists:
                return "exception"

            return "normal"

        return None


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
        # z.sleep( 5 )
        # while d( textContains='正在更新数据' ).exists:
        #     z.sleep( 2 )

        z.sleep(20)
        z.heartbeat()
        if d(description='QQ邮箱', index=0).exists:
            z.toast( "开始点击QQ邮箱" )
            d(description='QQ邮箱', index=0).click()
            z.sleep(3)

        if d(resourceId='com.tencent.androidqqmail:id/ea', index=0).exists:
            z.toast( "开始点击resourceId" )
            d(resourceId='com.tencent.androidqqmail:id/ea', index=0).click()
            z.sleep( 3 )

        if d(text='帐号密码登录').exists:
            d(text='帐号密码登录').click()
            z.sleep(3)


        d(resourceId='com.tencent.androidqqmail:id/bi').click()  # 输入帐号
        z.input( QQNumber )
        z.sleep(1)
        d(resourceId='com.tencent.androidqqmail:id/bs').click()  # 输入密码
        z.input( QQPassword )

        print('QQ号:%s,QQ密码：%s' % (QQNumber, QQPassword))
        d(text='登录​').click()
        z.sleep( int( args['time_delay1'] ) )

        z.heartbeat()
        if d(text='验证中…​').exists:
            z.sleep(20)
            z.heartbeat()

        result =  self.judgmentBounced(d)

        picObj = d(resourceId='com.tencent.androidqqmail:id/a19',className='android.widget.ImageView')
        if picObj.exists:
            code = self.palyCode(d, z, picObj)
            z.input(code)
            d( text='登录​' ).click( )
            z.sleep( int( args['time_delay2'] ) )

            z.heartbeat()
            if d(text='验证中…​').exists:
                z.sleep(20)
                z.heartbeat()

            result = self.judgmentBounced( d )

        if not result is None:
            if result == "normal":
                self.repo.BackupInfo( cate_id, 'normal', QQNumber, '', '' )
                z.toast( "登录异常，重新登录" )
                return "nothing"

            if result == "frozen":
                self.repo.BackupInfo( cate_id, 'frozen', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                z.toast( "登录异常，重新登录" )
                return "nothing"

            if result == "exception":
                self.repo.BackupInfo( cate_id, 'exception', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                z.toast( "登录异常，重新登录" )
                return "nothing"

        z.heartbeat( )
        if d( text='密码错误，请重新输入' ).exists:
            self.repo.BackupInfo( cate_id, 'frozen', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
            z.toast( "登录异常，重新登录" )
            return "nothing"

        if d( text='收件箱​' ).exists or d( text='温馨提示​' ).exists:
            z.toast( "登陆成功" )
            return QQNumber


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
        if d(text='密码错误，请重新输入').exists or d(description='QQ邮箱').exists:
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
                z.toast( "网络通畅。开始执行：QQ邮箱登录 有卡槽" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep(int(args["time_delay"]))
            return

        z.heartbeat()
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
    d = Device("HT4A1SK02114")
    z = ZDevice("HT4A1SK02114")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "275", "time_limit": "1", "time_limit1": "120", "time_delay": "3", "time_delay1": "15", "time_delay2": "15"};
    o.action(d, z, args)
    # slot = Slot(d.server.adb.device_serial(),'qqmail')
    # slot.clear(1)
    # d.server.adb.cmd( "shell", "pm clear com.tencent.androidqqmail" ).communicate( )  # 清除缓存
    # slot.restore( 1 )
    # d.server.adb.cmd( "shell",
    #                    "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
    # picObj = d( resourceId='com.tencent.androidqqmail:id/a19', className='android.widget.ImageView' )
    # if picObj.exists:
    #     code = o.palyCode( d, z, picObj )
    if d( description='QQ邮箱' ).exists:
        d( description='QQ邮箱' ).click( )

    if d( resourceId='com.tencent.androidqqmail:id/ea' ).exists:
        d( resourceId='com.tencent.androidqqmail:id/ea' ).click( )

