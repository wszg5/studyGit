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


    def Login(self, d, z, args):
        z.heartbeat()
        d.server.adb.cmd( "shell", "pm clear com.tencent.token" ).communicate( )  # 清除缓存
        d.server.adb.cmd( "shell", "am start -n com.tencent.token/.ui.LogoActivity" ).communicate( )  # 拉起来
        z.sleep(6)

        z.heartbeat()
        if d( text='登录QQ,开启安全之旅 >' ).exists:
            d( resourceId='com.tencent.token:id/account_bind_eval_level' ).click( )
            z.sleep( 0.5 )

        if d( text='QQ登录' ).exists:
            d( text='QQ登录' ).click( )
            z.sleep(8)

        z.heartbeat()
        cate_id = args["repo_cate_id"]
        time_limit = args['time_limit']
        numbers = self.repo.GetAccount(cate_id, time_limit, 1)
        while len(numbers) == 0:
            z.heartbeat()
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库无%s分钟未用\"" % (
                                  cate_id, time_limit)).communicate()
            z.sleep(2)
            return "none"

        sendSMS_URL = args["sms_url"]
        QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        QQPassword = numbers[0]['password']
        z.sleep(1)

        d.click(120, 360)  # 点击输入帐号文本框
        z.input(QQNumber)
        z.sleep(1)

        d.click(120, 480)  # 点击输入密码文本框
        z.input(QQPassword)
        z.sleep(1)

        d.click(363, 593)  # 点击登陆按钮
        z.sleep(6)

        z.heartbeat()
        if d(description='请向右拖动滑块完成拼图').exists:
            z.toast("遇到安全验证，重新开始")
            return "again"

        while d( text='身份验证' ).exists:
            d( text='下一步' ).click()
            z.sleep(3)

            z.heartbeat()
            if d( text='请填写您收到的短信验证码:' ).exists:
                z.sleep(65)

                z.heartbeat()
                if d(text='请填写您收到的短信验证码:').exists:
                    return "again"

            if d(text='开启安全之旅').exists:
                d(text='开启安全之旅').click()
                z.sleep(3)

            if d(text='重试').exists:
                d(text='重试').click()
                return "again"

            if d(text='您的帐号安全有待加强').exists:
                return QQNumber




    def action(self, d, z, args):
        z.toast(u"开始：ping网络是否通畅")
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast(u"网络通畅。开始执行：QQ安全中心登陆备份模块")
                break
            z.sleep(2)

        if i > 200:
            z.toast(u"网络不通，请检查网络状态")
            return

        while True:
            z.heartbeat()
            z.generate_serial("com.tencent.token")  # 随机生成手机特征码
            z.toast(u"随机生成手机特征码")

            serial = d.server.adb.device_serial()
            self.slot = Slot(serial, self.type)
            self.slot.backupToDisk("132132132")  # 设备信息，卡槽号，QQ号
            print "ok"
            break

            # Login_Result = self.Login(d, z, args)
            # if Login_Result == "again":
            #     continue
            #
            # elif Login_Result == "none":  # 有空卡槽，单仓库无帐号可登，继续继续切换卡槽
            #     return
            #
            # else:
            #     QQnumber = Login_Result
                # self.slot.backup(QQnumber, QQnumber)  # 设备信息，卡槽号，QQ号

def getPluginClass():
    return QQSafetyCenter

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("465b4e4b")
    z = ZDevice("465b4e4b")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # d.server.adb.cmd("shell", "am start -a android.intent.action.MAIN -n com.android.settings/.Settings").communicate()    #打开android设置页面
    args = {"repo_cate_id": "335", "time_limit": "120", "sms_url": "http://192.168.1.107:5555/send?callee=phoneNumber&sms=smsContent"};
    o.action(d, z, args)
    # repo = Repo()
    # cate_id = args["repo_cate_id"]
    # time_limit = args['time_limit']
    # numbers = repo.GetAccount( cate_id, time_limit, 1 )
    # info = numbers[0]['qqtoken']
    # infoArray = info.split( '----' )
    # print(infoArray)
    # d.server.adb.cmd("shell", "am start -n com.tencent.token/com.tencent.token.MainActivity").communicate()  # 拉起来
    # d.server.adb.cmd("shell", "am start -n com.tencent.token/com.tencent.token.MainActivity").communicate()  # 拉起来
    # d.server.adb.cmd("shell", "am start -n com.tencent.token/.ui.LogoActivity").communicate()  # 拉起来
