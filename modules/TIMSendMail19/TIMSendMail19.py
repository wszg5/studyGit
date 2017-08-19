# coding:utf-8
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice


class TIMSendMail19:
    def __init__(self):

        self.repo = Repo()


    def action(self, d, z, args):
        z.toast( "TIM邮件发消息" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TTIM邮件发消息" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        cate_id = args['repo_number_id']
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        if d( text="消息" ).exists:
            z.toast( "卡槽TIM状态正常，继续执行" )
        else:
            z.toast( "卡槽TIM状态异常，跳过此模块" )
            return

        d(index=2, className='android.widget.FrameLayout').click()
        d(text='邮件', className='android.widget.TextView').click()
        time.sleep(1)
        if d(text='开通QQ邮箱', className='android.widget.Button').exists:
            d(text='开通QQ邮箱', className='android.widget.Button').click()

        while 1:
            if d(text='写邮件', className='android.widget.TextView').exists:
                d(text='写邮件', className='android.widget.TextView').click()
                break
            else:
                time.sleep(1)

        # while 1:
        #     if d(text='发送', className='android.widget.Button').exists:


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMSendMail19

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52DSK00474")
    z = ZDevice("HT52DSK00474")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_mail_cateId": "121", "repo_material_cateId": "39", "time_delay": "3"};

    o.action(d, z, args)