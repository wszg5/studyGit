# coding:utf-8
import random
import string
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class YiXinLogin:
    def __init__(self):
        self.repo = Repo()
        self.type = 'yixin'

    def GenPassword(self, numOfNum=4, numOfLetter=4):
        # 选中numOfNum个数字
        slcNum = [random.choice( string.digits ) for i in range( numOfNum )]
        # 选中numOfLetter个字母
        slcLetter = [random.choice( string.lowercase ) for i in range( numOfLetter )]
        slcChar = slcLetter + slcNum
        genPwd = ''.join( [i for i in slcChar] )
        return genPwd


    def login(self, d, z, args, password):
        z.toast("开始登录")
        d.server.adb.cmd("shell", "pm clear im.yixin" ).communicate( )  # 清除缓存
        d.server.adb.cmd("shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起易信
        z.sleep(10)
        z.heartbeat()
        if d(text='很抱歉，“易信”已停止运行。').exists:
            d(text='确定')
            return 'fail'

        d.server.adb.cmd( "shell", "am force-stop im.yixin" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起易信
        z.sleep(5)
        z.heartbeat()
        if d( text='很抱歉，“易信”已停止运行。' ).exists:
            d( text='确定' )
            return 'fail'

        if d( text='接受', resourceId='im.yixin:id/easy_dialog_positive_btn' ).exists:
            d( text='接受', resourceId='im.yixin:id/easy_dialog_positive_btn' ).click( )
            z.sleep( 2 )

        if d( text='登 录' ).exists:
            d( text='登 录' ).click()
            z.sleep( 2 )

        while True:
            z.heartbeat()
            z.toast(u"开始获取手机号码")
            self.scode = smsCode( d.server.adb.device_serial( ) )

            str = d.info  # 获取屏幕大小等信息
            height = str["displayHeight"]
            width = str["displayWidth"]

            if d( resourceId='im.yixin:id/register_phone_number_edittext' ).exists:
                d( resourceId='im.yixin:id/register_phone_number_edittext' ).click.bottomright( )


            number_cate_id = args['repo_number_id']
            # number_time_limit = int(args['number_time_limit'])  # 号码提取时间间隔
            exist_numbers = self.repo.GetNumber( number_cate_id, 0, 1, 'exist' )
            remain = 1 - len( exist_numbers )
            normal_numbers = self.repo.GetNumber( number_cate_id, 0, remain, 'normal' )
            numbers = exist_numbers + normal_numbers
            if len( numbers ) == 0:
                d.server.adb.cmd("shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空\"" % number_cate_id).communicate()
                return None

            number = numbers[0]["number"]

            if d(resourceId='im.yixin:id/editUserid').exists:
                d(resourceId='im.yixin:id/editUserid').click()

            try:
                PhoneNumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER, number)  # 获取接码平台手机号码
            except:
                PhoneNumber = None

            # PhoneNumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER)  # 获取接码平台手机号码

            if PhoneNumber is None:
                z.toast(u'讯码查不无此号,重新获取')
                continue
            else:
                z.toast(u"成功获取手机号")
                break

        z.input(PhoneNumber)

        if d(text='找回密码').exists:
            d(text='找回密码').click()
            z.sleep(3)

        if not d(text='中国',resourceId='im.yixin:id/country_name').exists:
            d( resourceId='im.yixin:id/country_name' ).click()
            z.sleep(1)
            while True:
                if d( text='中国').exists:
                    d( text='中国' ).click()
                    break
                else:
                    d.swipe( width / 2, height * 6 / 7, width / 2, height / 7 )

        if d(text='下一步').exists:
            d(text='下一步').click()
            z.sleep(8)

        z.heartbeat()
        if d(text='注册',resourceId='im.yixin:id/easy_dialog_positive_btn').exists:
            return "fail"

        if d(text='输入收到的验证码').exists:
            d(text='输入收到的验证码').click()

        try:
            code = self.scode.GetVertifyCode( PhoneNumber, self.scode.WECHAT_REGISTER, 4)  # 获取接码验证码
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.WECHAT_REGISTER )
        except:
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.WECHAT_REGISTER )
            code = ''

        if code == '':
            z.toast( PhoneNumber + '手机号,获取不到验证码' )
            return "fail"

        z.input(code)
        if d(text='下一步').exists:
            d(text='下一步').click()
            z.sleep(8)

        if d(resourceId='im.yixin:id/password_edittext').exists:
            z.input(password)
            z.sleep(1)
            d(text='完成').click()
            z.sleep(15)
            z.heartbeat()

        if d(text='立即更新').exists and d(text='下次再说').exists:
            d(text='下次再说').click()

        if d(text='消息').exists and d(text='电话').exists and d(text='发现').exists and d(text='通讯录').exists:
            z.toast(u'登录成功')
            return PhoneNumber
        else:
            z.toast(u'登录失败，重新登录')
            return "fail"


    def qiehuan(self, d, z, args):
        z.toast("开始切换卡槽")
        slot_time_limit = int( args['slot_time_limit'] )  # 卡槽提取时间间隔
        slotObj = self.slot.getAvailableSlot(slot_time_limit)  # 取空卡槽，取N小时没用过的卡槽

        if not slotObj is None:
            slotnum = slotObj['id']

        while slotObj is None:  # 2小时没用过的卡槽也为没有的情况
            d.server.adb.cmd("shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"").communicate()
            z.heartbeat()
            z.sleep(10)
            slotObj = self.slot.getAvailableSlot(slot_time_limit)
            if not slotObj is None:
                slotnum = slotObj['id']

        z.heartbeat()
        print(slotnum)

        obj = self.slot.getSlotInfo( slotnum )
        remark = obj['remark']
        remarkArr = remark.split( "_" )
        if len( remarkArr ) == 3:
            slotInfo = d.server.adb.device_serial( ) + '_' + self.type + '_' + slotnum
            cateId = remarkArr[2]
            numbers = self.repo.Getserial( cateId, slotInfo )
            if len(numbers) > 0:
                featureCodeInfo = numbers[0]['imei']
                z.set_serial( "im.yixin", featureCodeInfo )

        self.slot.restore( slotnum )  # 有time_limit分钟没用过的卡槽情况，切换卡槽

        d.server.adb.cmd( "shell",
                          "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + slotnum + "号\"" ).communicate( )
        z.sleep( 2 )

        d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起易信
        z.sleep(10)
        z.heartbeat()
        if d( text='很抱歉，“易信”已停止运行。' ).exists:
            d( text='确定' )
            return 'fail'

        if d( text='立即更新' ).exists and d( text='下次再说' ).exists:
            d( text='下次再说' ).click( )

        if d( text='消息' ).exists and d( text='电话' ).exists and d( text='发现' ).exists and d( text='通讯录' ).exists:
            z.toast( u'切换成功' )
            return "success"
        else:
            z.toast( u'切换失败，重新补登' )
            self.repo.BackupInfo( cateId, 'exception', remarkArr[1], featureCodeInfo, '')  # 仓库号,使用中,QQ号,设备号_卡槽号
            return "fail"



    def action(self, d, z, args):
        z.toast( "正在ping网络是否通畅" )
        while True:
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast("开始执行：易信登录模块　有卡槽")
                break
            z.sleep( 2 )

        z.generate_serial( "im.yixin" )  # 随机生成手机特征码
        z.toast( "随机生成手机特征码" )

        saveCate = args['repo_account_id']
        password = self.GenPassword()

        serial = d.server.adb.device_serial()
        self.slot = Slot(serial, self.type)
        slotnum = self.slot.getEmpty()  # 取空卡槽

        if slotnum == 0:  # 没有空卡槽的话
            qiehuan_result = self.qiehuan(d, z, args)
            if qiehuan_result == "fail":
                self.action(d, z, args)
        else:
            login_result = self.login(d, z, args, password)
            if login_result == "fail":
                self.action(d, z, args)

            elif login_result is None:
                self.qiehuan(d, z, args)

            else:
                # 入库
                featureCodeInfo = z.get_serial("im.yixin")
                self.repo.RegisterAccount(login_result, password, "", saveCate, "using", featureCodeInfo, '%s_%s_%s' % (
                        d.server.adb.device_serial(), self.type, slotnum))
                # 入卡槽
                self.slot.backup(slotnum, str(slotnum) + '_' + login_result + '_' + saveCate)  # 设备信息，卡槽号，QQ号

        if (args['time_delay']):
            z.sleep(int(args['time_delay']))



def getPluginClass():
    return YiXinLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("25424f9")
    z = ZDevice("25424f9")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "279", "repo_number_id": "123", "slot_time_limit": "2", "time_delay": "3"};
    o.action(d, z, args)

    # slot = Slot(d.server.adb.device_serial(),'yixin')
    # slot.clear(1)
    # slot.clear(2)
    # d.server.adb.cmd( "shell", "pm clear im.yixin" ).communicate( )  # 清除缓存
    # slot.restore( 1 )
    # d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate()  # 拉起易信

