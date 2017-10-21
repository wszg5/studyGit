# coding:utf-8
from PIL import Image

from imageCode import imageCode
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from zservice import ZDevice
import logging
import os
import util
import time, datetime, random
from slot import Slot



class QQSafetyCenter:
    def __init__(self):
        self.repo = Repo()
        self.type = 'token'

    def GetUnique(self):
        nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" );  # 生成当前时间
        randomNum = random.randint( 0, 1000 );  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str( 00 ) + str( randomNum );
        uniqueNum = str( nowTime ) + str( randomNum );
        return uniqueNum

    def LoginPlayCode(self, d, z):
        self.scode = smsCode( d.server.adb.device_serial( ) )
        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        codePng = os.path.join( base_dir, "%s_c.png" % (self.GetUnique( )) )
        codeEditTextObj = d( resourceId='com.tencent.mobileqq:id/name', index='2',
                                 className="android.widget.EditText" )
        if codeEditTextObj.exists:  # 需要验证码的情况
            icode = imageCode( )
            im_id = ""
            for i in range( 0, 4 ):  # 打码循环
                if i > 0:
                    icode.reportError( im_id )
                obj = d( resourceId='com.tencent.mobileqq:id/name',
                         className='android.widget.ImageView' )  # 当弹出选择QQ框的时候，定位不到验证码图片
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

        return code


    def CaseOne(self, d, z, QQNumber,QQPassword):  # 登录情况一：手机上有ｑｑ登录或提示历史登陆过的帐号直接登陆

        if d(text='切换帐号').exists and d(text='添加帐号').exists:
            if d(resourceId='com.tencent.mobileqq:id/name',index=0).exists:
                obj = d( resourceId='com.tencent.mobileqq:id/name', index=0, className='android.widget.RelativeLayout').child(
                    className='android.widget.LinearLayout',index=1).child(
                    resourceId='com.tencent.mobileqq:id/name', index=0, className='android.widget.LinearLayout').child(
                    resourceId='com.tencent.mobileqq:id/name', index=0, className='android.widget.RelativeLayout')
                Str = obj.info["bounds"] # 获取该控件大小等信息
                height = int(Str["bottom"]) - int(Str["top"])
                d.swipe(int(Str["right"]) - 10,int(Str["bottom"]) - height / 2, int(Str["left"]) + 10,int(Str["bottom"]) - height / 2, 5)
                z.sleep(1.5)
                if d(text='删除').exists:
                    d(text='删除').click()
                    z.sleep(1)
            d(text='添加帐号').click()

        d( resourceId='com.tencent.mobileqq:id/account' ).click( )
        z.input( QQNumber )

        d( resourceId='com.tencent.mobileqq:id/password' ).click( )
        z.input( QQPassword )

        if d( text='登 录' ).exists:
            d( text='登 录' ).click( )
            z.sleep(5)

        if d(text='输入验证码').exists:
            code = self.LoginPlayCode(d, z)
            z.input(code)
            z.sleep(1)

            if d(text='完成').exists:
                d(text='完成').click()


    def CaseTwo(self, d, z, QQNumber,QQPassword): #登录情况二：手机上没有登陆ｑｑ也没有登录过安全中心

        d( className='android.view.View', index=1 ).click( )
        z.input( QQNumber )

        d( className='android.view.View', index=2 ).click( )
        z.input( QQPassword )

        if d( description='登 录' ).exists:
            d( description='登 录' ).click( )

    def Login(self, d, z, args): #登录方法
        self.scode = smsCode( d.server.adb.device_serial( ) )
        d.server.adb.cmd( "shell", "pm clear com.tencent.token" ).communicate( )  # 清除缓存
        d.server.adb.cmd( "shell", "am start -n com.tencent.token/.ui.LogoActivity" ).communicate( )  # 拉起来
        z.sleep(6)

        if d( resourceId='com.tencent.token:id/account_bind_qqface' ).exists:
            d( resourceId='com.tencent.token:id/account_bind_qqface' ).click( )
            z.sleep( 1 )

        if d( text='登录' ).exists:
            d( text='登录' ).click( )
            z.sleep( 0.5 )

        if d( text='QQ登录' ).exists:
            d( text='QQ登录' ).click( )
            z.sleep(1)

        cate_id = args["repo_cate_id"]
        time_limit = args['time_limit']
        numbers = self.repo.GetAccount( cate_id, time_limit, 1 )
        print( numbers )
        while len( numbers ) == 0:
            z.heartbeat( )
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库无%s分钟未用,开始切换卡槽\"" % (
                                  cate_id, time_limit) ).communicate( )
            z.sleep( 2 )
            return "none"

        QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        QQPassword = numbers[0]['password']
        # QQNumber = '3518608471'
        # QQPassword = 'uxpm6521'
        z.sleep( 1 )

        if d( text='切换帐号' ).exists:
            d(text='切换帐号').click()
            z.sleep( 1 )
            self.CaseOne( d, z, QQNumber, QQPassword )
            z.sleep( 5 )
        else:
            self.CaseTwo( d, z, QQNumber, QQPassword )
            z.sleep( 5 )

        if d(description='请向右拖动滑块完成拼图').exists:
            z.toast("遇到安全验证，重新开始")
            return "again"

        if d( text='身份验证' ).exists:
            d( text='下一步' ).click( )

        if d( text='请填写您收到的短信验证码:' ).exists:
            info = numbers[0]['qqtoken']
            infoArray = info.split( '----' )
            number = infoArray[6]
            # number = "14773454349"
            try:
                PhoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_TOKEN_BIND, number )  # 获取接码平台手机号码
            except:
                logging.exception("exception")
                PhoneNumber = None

            if PhoneNumber is None:
                self.repo.BackupInfo( cate_id, 'frozen', QQNumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                z.toast( '查不无此号' )
                return "again"

            try:
                code = self.scode.GetVertifyCode( PhoneNumber, self.scode.QQ_TOKEN_BIND )  # 获取接码验证码
                self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_TOKEN_BIND )
            except:
                logging.exception("exception")
                code = ''

            if code == '':
                z.toast( PhoneNumber + '手机号,获取不到验证码' )
                self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_TOKEN_BIND )
                return "again"

            if d(resourceId='com.tencent.token:id/sms_code').exists: #点击输入框输入验证码
                d( resourceId='com.tencent.token:id/sms_code' ).click()
                z.input( code )

            if d( text='下一步' ).exists:
                d( text='下一步' ).click( )
                z.sleep(5)

            if d(text='开启安全之旅').exists:
                d(text='开启安全之旅').click()
                return QQNumber

            if d(textContains='绑定QQ失败').exists:
                return "again"

        elif d(text='登录失败').exists:
            return "again"



    def QieHuanSolt(self, d, z, args): # 卡槽切换方法
        time_limit_slot = int(args['time_limit_slot'])
        slotObj = self.slot.getAvailableSlot(time_limit_slot)  # 取空卡槽，取２小时没用过的卡槽
        if not slotObj is None:
            slotnum = slotObj['id']
        print( slotnum )
        while slotObj is None:  # 2小时没用过的卡槽也为没有的情况
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"" ).communicate( )
            z.heartbeat( )
            z.sleep( 10 )
            slotObj = self.slot.getAvailableSlot( time_limit_slot )
            if not slotObj is None:
                slotnum = slotObj['id']

        d.server.adb.cmd( "shell", "pm clear com.tencent.token" ).communicate( )  # 清除缓存
        d.server.adb.cmd( "shell", "am broadcast -a com.zunyun.zime.toast --es msg \"正在切换到" + slotnum + "号卡槽...\"" ).communicate( )

        self.slot.restore( slotnum )  # 有time_limit分钟没用过的卡槽情况，切换卡槽

        d.server.adb.cmd( "shell", "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + slotnum + "号\"" ).communicate( )
        d.server.adb.cmd( "shell", "am start -n com.tencent.token/.ui.LogoActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )

        if d(text='欢迎来到安全中心').exists:
            return "fail"

        return "success"

    def action(self, d, z, args):
        z.generate_serial( "com.tencent.tim" )  # 随机生成手机特征码
        z.toast( "随机生成手机特征码" )

        serial = d.server.adb.device_serial()
        cate_id = args["repo_cate_id"]
        self.slot = Slot( serial, self.type )
        slotnum = self.slot.getEmpty()  # 取空卡槽

        if slotnum == 0:
            QieHuanSolt_Result = self.QieHuanSolt( d, z, args )
            if QieHuanSolt_Result == "fail":
                obj = self.slot.getSlotInfo( slotnum )
                remark = obj['remark']
                remarkArr = remark.split("_")
                QQnumber = remarkArr[1]
                self.repo.BackupInfo(cate_id, 'frozen', QQnumber, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                self.slot.clear( slotnum )  # 清空改卡槽，并补登
                z.toast( "卡槽恢复失败,进行补登" )
                self.action( d, z, args )

            else:
                z.toast( "卡槽恢复成功，帐号正常" )

        else:
            Login_Result = self.Login( d, z, args )
            if Login_Result == "again":
                self.action( d, z, args )

            elif Login_Result == "none": # 有空卡槽，单仓库无帐号可登，继续继续切换卡槽
                QieHuanSolt_Result = self.QieHuanSolt( d, z, args )
                if QieHuanSolt_Result == "fail":
                    obj = self.slot.getSlotInfo( slotnum )
                    remark = obj['remark']
                    remarkArr = remark.split( "_" )
                    QQnumber = remarkArr[1]
                    self.repo.BackupInfo( cate_id, 'frozen', QQnumber, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                    self.slot.clear( slotnum )  # 清空改卡槽，并补登
                    z.toast( "卡槽恢复失败,进行补登" )
                    self.action( d, z, args )

                else:
                    z.toast( "卡槽恢复成功，帐号正常" )

            else:
                QQnumber = Login_Result
                self.slot.backup( slotnum, str( slotnum ) + '_' + QQnumber )  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo( cate_id, 'using', QQnumber, serial, '%s_%s_%s' % (
                    d.server.adb.device_serial( ), self.type, slotnum) )  # 仓库号,使用中,QQ号,设备号_卡槽号


def getPluginClass():
    return QQSafetyCenter

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("c0e5994f")
    z = ZDevice("c0e5994f")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # d.server.adb.cmd("shell", "am start -a android.intent.action.MAIN -n com.android.settings/.Settings").communicate()    #打开android设置页面
    args = {"repo_cate_id": "261","time_limit":"120", "time_limit_slot":"2", "time_delay": "3"};
    o.action(d, z, args)
    # repo = Repo()
    # cate_id = args["repo_cate_id"]
    # time_limit = args['time_limit']
    # numbers = repo.GetAccount( cate_id, time_limit, 1 )
    # info = numbers[0]['qqtoken']
    # infoArray = info.split( '----' )
    # print(infoArray)
    # d.server.adb.cmd("shell", "am start -n com.tencent.token/com.tencent.token.MainActivity").communicate()  # 拉起来
    # d.server.adb.cmd("shell", "am start -n com.tencent.token/.ui.LogoActivity").communicate()  # 拉起来