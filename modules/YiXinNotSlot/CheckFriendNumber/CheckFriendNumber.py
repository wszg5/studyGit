# coding:utf-8
import random
import string
from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class CheckFriendNumber:
    def __init__(self):
        self.repo = Repo()
        self.type = 'yixin'

    def action(self, d, z, args):
        Str = d.info  # 获取屏幕大小等信息
        height = float( Str["displayHeight"] )
        width = float( Str["displayWidth"] )

        z.toast( "正在ping网络是否通畅" )
        while True:
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast("开始执行：易信检测免费短信数量模块")
                break
            z.sleep( 2 )

        d.server.adb.cmd( "shell", "am force-stop im.yixin" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起易信
        z.sleep(15)

        if d(text='我',resourceId='im.yixin:id/tab_title_label').exists:
            d(text='我').click()
            if d( text='我', resourceId='im.yixin:id/tab_title_label' ).exists:
                d( text='我' ).click( )
            z.sleep(8)

        if d( text='立即体验' ).exists:
            d( text='立即体验' ).click( )
            if d( text='立即体验' ).exists:
                d( text='立即体验' ).click( )

        obj38 = d(className='android.widget.LinearLayout', resourceId='im.yixin:id/free_service_item_free_message', index=1).child(
            className='android.widget.RelativeLayout',resourceId='im.yixin:id/root').child(
            className='android.widget.RelativeLayout', resourceId='im.yixin:id/content_layout').child(
            className='android.widget.RelativeLayout', index=0)

        obj = d(className='android.widget.LinearLayout', resourceId='im.yixin:id/free_service_item_free_message').child(
            className='android.widget.RelativeLayout',resourceId='im.yixin:id/root')

        if obj38.exists:
            smsNumber = obj.child( resourceId='im.yixin:id/quotaTV' ).info['text']
            smslength = len( smsNumber )
            if smsNumber[smslength - 1] == "条":
                smsNumber = smsNumber[0:smslength - 1]

        if obj.exists:
            smsNumber = obj.child(resourceId='im.yixin:id/quotaTV').info['text']
            smslength = len(smsNumber)
            if smsNumber[smslength-1] == "条":
                smsNumber = smsNumber[0:smslength-1]

        d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)

        if d(text='设置').exists:
            d(text='设置').click()
            z.sleep(2)

        if d(text='帐号设置').exists:
            d(text='帐号设置').click()
            z.sleep(2)

        phoneNumber = d(resourceId='im.yixin:id/detail_label').info['text']

        cateId = args['repo_account_id']
        self.repo.UpdateYXsmsNumber(cateId,phoneNumber,smsNumber)

        if (args['time_delay']):
            z.sleep(int(args['time_delay']))



def getPluginClass():
    return CheckFriendNumber

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "279", "time_delay": "3"};
    o.action(d, z, args)



    # slot = Slot(d.server.adb.device_serial(),'yixin')
    # slot.clear(1)
    # slot.clear(2)
    # d.server.adb.cmd( "shell", "pm clear im.yixin" ).communicate( )  # 清除缓存
    # slot.restore( 1 )
    # d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate()  # 拉起易信
