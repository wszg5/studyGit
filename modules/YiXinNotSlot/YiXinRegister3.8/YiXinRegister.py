# coding:utf-8
import colorsys
import os
import random
import string

from PIL import Image

from imageCode import imageCode
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class YiXinRegister:
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

    def register(self, d, z, args, password):
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.toast("开始注册")
        d.server.adb.cmd( "shell", "pm clear im.yixin" ).communicate( )  # 清除缓存
        d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起易信
        z.sleep( 10 )
        z.heartbeat( )
        if d( text='很抱歉，“易信”已停止运行。' ).exists:
            d( text='确定' ).click( )
            return 'fail'

        if d( text='注册' ).exists:
            d( text='注册' ).click()
            z.sleep( 2 )

        self.scode = smsCode(d.server.adb.device_serial())
        while True:
            material_cate_id = args['repo_material_id']
            # material_time_limit = args['material_time_limit']
            nicknameLsit = self.repo.GetMaterial(material_cate_id, 0, 1)
            if len( nicknameLsit ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"素材库%s号仓库为空\"" % material_cate_id ).communicate( )
            else:
                break

        nickname = nicknameLsit[0]['content']

        while True:
            z.heartbeat()

            z.toast(u'开始获取手机号')
            while True:
                if d(resourceId='im.yixin:id/register_phone_number_edittext').exists:
                    d(resourceId='im.yixin:id/register_phone_number_edittext').click.bottomright()

                number_cate_id = args['repo_number_id']
                # number_time_limit = int(args['number_time_limit'])  # 号码提取时间间隔
                exist_numbers = self.repo.GetNumber(number_cate_id, 0, 1, 'exist')
                remain = 1 - len(exist_numbers)
                normal_numbers = self.repo.GetNumber(number_cate_id, 0, remain, 'normal')
                numbers = exist_numbers + normal_numbers
                if len(numbers) == 0:
                    d.server.adb.cmd("shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空\"" % number_cate_id).communicate()
                else:
                    break

            number = numbers[0]["number"]

            if d(resourceId='im.yixin:id/register_phone_number_edittext').exists:
                d(resourceId='im.yixin:id/register_phone_number_edittext').click()


            try:
                PhoneNumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER, number)  # 获取接码平台手机号码
            except:
                PhoneNumber = None

            # PhoneNumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER)  # 获取接码平台手机号码

            if PhoneNumber is None:
                z.toast(u'讯码查不无此号,重新获取')
                continue
            else:
                z.toast(u'成功获取到手机号')

            z.input(PhoneNumber)

            if not d( text='中国', resourceId='im.yixin:id/tv_register_country' ).exists:
                d( resourceId='im.yixin:id/tv_register_country' ).click( )
                z.sleep( 1 )
                while True:
                    if d( text='中国' ).exists:
                        d( text='中国' ).click( )
                        break
                    else:
                        d.swipe( width / 2, height * 6 / 7, width / 2, height / 7 )

            if d(text='下一步').exists:
                d(text='下一步').click()
                z.sleep(8)

            z.heartbeat()
            if d(text='为了验证身份，我们将会发送短信验证码到你的手机').exists:
                d(resourceId='im.yixin:id/register_phone_number_edittext').click.bottomright()  # 清空输入框
                self.scode.defriendPhoneNumber(PhoneNumber, self.scode.WECHAT_REGISTER)
                continue

            if d(textContains='验证码短信已发送至').exists:
                break

        try:
            code = self.scode.GetVertifyCode(PhoneNumber, self.scode.WECHAT_REGISTER, 4)  # 获取接码验证码
            self.scode.defriendPhoneNumber(PhoneNumber, self.scode.WECHAT_REGISTER)
        except:
            self.scode.defriendPhoneNumber(PhoneNumber, self.scode.WECHAT_REGISTER)
            code = ''

        if code == '':
            z.toast( PhoneNumber + '手机号,获取不到验证码' )
            return "fail"

        z.input(code[0])
        z.input(code[1])
        z.input(code[2])
        z.input(code[3])

        if d(resourceId='im.yixin:id/register_username_edittext').exists:
            d(resourceId='im.yixin:id/register_username_edittext').click()
            z.input(nickname)

        if d(resourceId='im.yixin:id/register_password_edittext').exists:
            d( resourceId='im.yixin:id/register_password_edittext' ).click()
            z.input(password)

        if d(text='下一步').exists:
            d(text='下一步').click()
            z.sleep(3)

        if d(text='进入易信',resourceId='im.yixin:id/btn_register_start').exists:
            d(text='进入易信',resourceId='im.yixin:id/btn_register_start').click()
            z.sleep(20)

        # d.server.adb.cmd( "shell", "am force-stop im.yixin" ).communicate( )  # 强制停止
        # d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起易信

        z.heartbeat()
        if d( text='立即更新' ).exists:
            d(text='下次再说').click()

        if d(text='消息').exists and d(text='电话').exists and d(text='发现').exists:
            z.toast( u'注册成功' )
            return PhoneNumber

        else:
            z.toast( u'注册失败，重新注册' )
            return "fail"


    def action(self, d, z, args):

        while True:
            z.toast( "正在ping网络是否通畅" )
            while True:
                ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
                print(ping)
                if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                    z.toast( "开始执行：易信注册模块　有卡槽" )
                    break
                z.sleep( 2 )

            z.generate_serial( "im.yixin" )  # 随机生成手机特征码
            z.toast( "随机生成手机特征码" )

            saveCate = args['repo_account_id']
            password = self.GenPassword( )

            register_result = self.register( d, z, args, password )
            if register_result == "fail":
                continue

            else:
                # 入库
                featureCodeInfo = z.get_serial( "im.yixin" )
                self.repo.RegisterAccount( register_result, password, "", saveCate, "using", featureCodeInfo )
                break

        if (args['time_delay']):
            z.sleep( int( args['time_delay'] ) )







def getPluginClass():
    return YiXinRegister

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "279", "repo_number_id": "123", "repo_material_id": "139", "slot_time_limit": "2", "time_delay": "3"};
    o.action(d, z, args)
    # slot = Slot(d.server.adb.device_serial(),'yixin')
    # slot.clear(1)
    # slot.clear(2)
    # d.server.adb.cmd( "shell", "pm clear im.yixin" ).communicate( )  # 清除缓存
    # slot.restore( 1 )
    # d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate()  # 拉起易信

