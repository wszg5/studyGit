# coding:utf-8
import colorsys
import os

# from reportlab.graphics.shapes import Image
from PIL import Image

from smsCode import smsCode
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class MobilqqCardParise:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z,args):
        z.toast( "准备执行QQ名片点赞" )
        z.sleep(1)
        z.heartbeat( )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ名片点赞" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text='消息' ).exists:  # 到了通讯录这步后看号有没有被冻结
            z.toast( "卡槽QQ状态正常，继续执行" )
        else:
            z.toast( "卡槽QQ状态异常，跳过此模块" )
            return
        z.heartbeat()

        count = int(args['count'])  # 要添加多少人
        i = 0
        time_limit1 = int(args["time_limit1"])
        repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
        click_count = int(args["click_count"])
        for i in range( 0, count ):           #总人数
            numbers = self.repo.GetAccount( repo_number_cate_id, time_limit1, 1 )


            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % repo_number_cate_id ).communicate( )
                z.sleep( 5 )
                return
            z.heartbeat( )
            QQnumber = numbers[0]['number']  # 即将点赞的QQ号
            print(QQnumber)
            z.sleep(1)

            z.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"'%445564338)  # qq名片页面
            z.sleep(3)
            if d(text='QQ',resourceId="android:id/text1").exists:
                z.heartbeat( )
                d( text='QQ', resourceId="android:id/text1" ).click()
                z.sleep(2)
                z.heartbeat()
                while d(text='仅此一次').exists:
                    z.heartbeat( )
                    d(text='仅此一次').click()
            z.sleep(1)
            flag = True
            obj = d(descriptionContains="当前有").child(index=0,className='android.widget.LinearLayout').child(index=1,className="android.widget.TextView")
            if obj.exists:
                objtext = obj.info["text"]
                for j in range(0,click_count):
                    if d(descriptionContains="当前有").exists:
                        d( descriptionContains="当前有" ).click()
                        d.dump( compressed=False )
                        if flag:
                            if objtext == d(descriptionContains="当前有").child(index=0,className='android.widget.LinearLayout').child(index=1,className="android.widget.TextView").info["text"]:
                                z.toast("今天无法继续赞了，停止模块")
                                return
                            flag = False
            else:
                z.toast("对方拒绝赞")
                count = count+1

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqCardParise

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A6SK01638")
    z = ZDevice("HT4A6SK01638")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_cate_id":"217",'time_limit1':"60","count":"5","time_delay":"3","click_count":"2"}    #cate_id是仓库号，length是数量

    o.action(d, z, args)