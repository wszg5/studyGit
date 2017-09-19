# coding:utf-8
import colorsys
import datetime
import os
import random

from PIL import Image

from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice

class TIMSpaceParise:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )  # 生成当前时间
        randomNum = random.randint( 0, 1000 )  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str( 00 ) + str( randomNum )
        uniqueNum = str( nowTime ) + str( randomNum )
        return uniqueNum

    def WebViewBlankPages(self, d, obj):
        # z.toast( "判断图片是否正常" )
        Str = d.info  # 获取屏幕大小等信息
        height = float( Str["displayHeight"] )
        width = float( Str["displayWidth"] )

        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        if obj.exists:
            getobj = obj.info["bounds"]
            top = getobj["top"]
            left = getobj["left"]
            right = getobj["right"]
            bottom = getobj["bottom"]
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
        else:
            dominant_color = None
        return dominant_color

    def action(self, d,z,args):
        z.toast( "TIM空间点赞" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM空间点赞" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
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
        count = int( args["count"] )
        while True:
            if d( index=1, className='android.widget.ImageView' ).exists:
                z.heartbeat( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            if d( text="加好友" ).exists:  # 由于网速慢或手机卡可能误点
                d( text="加好友" ).click( )
                z.heartbeat( )
                d( text="返回", className="android.widget.TextView" ).click( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            z.sleep( 3 )
            if d( text='邮件' ).exists:
                z.heartbeat( )
                # d( text='邮件' ).click( )
                break
        if d(text="好友动态").exists:
            z.sleep(1)
            z.heartbeat()
            d( text="好友动态" ).click()
            z.sleep(2)
        else:
            z.sleep(1)
            z.heartbeat()
            d(index=1,className='android.widget.RelativeLayout').child(index=1,className="android.widget.RelativeLayout").child(index=1,className="android.widget.ImageView").click()
            z.sleep(2)
            z.heartbeat()
            d(index=0,text="功能",className="android.widget.TextView").click()
            z.sleep(2)
            z.heartbeat()
            if d(text="好友动态",resourceId="com.tencent.tim:id/letsTextView").exists:
                d( text="好友动态", resourceId="com.tencent.tim:id/letsTextView" ).click()
            if d(text="启用",className="android.widget.Button").exists:
                z.sleep(1)
                z.heartbeat()
                d( text="启用", className="android.widget.Button" ).click()
            z.sleep(1)
            z.heartbeat()
            d(text="功能",resourceId="com.tencent.tim:id/ivTitleBtnLeft").click()
            z.sleep(1)
            z.heartbeat()
            d( text="设置", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click( )
            z.sleep( 1 )
            z.heartbeat( )
            d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click( )
            z.sleep(1)
            z.heartbeat()
            d( text="好友动态" ).click( )
            z.sleep(2)
        while not d(text="说说",className="android.widget.TextView").exists:
            z.sleep(1)

        i=0
        num = 0
        objlist = []
        flag = True
        # for i in range(0,count):
        while i<count:
            obj = d(index=i,className="android.widget.LinearLayout").child(index=6,className="android.widget.RelativeLayout").child(index=1,className='android.widget.FrameLayout').child(index=0,className="android.widget.ImageView")
            if obj.exists:
                objtemp = d( index=i - 1, className="android.widget.LinearLayout" )
                if objtemp.exists:
                    objinfo = objtemp.info
                    if objinfo not in objlist:
                        objlist.append( objinfo )
                z.sleep(1)
                z.heartbeat()
                color = self.WebViewBlankPages(d,obj)
                if color == (118,120,134):
                    z.sleep(2)
                    obj.click()
                    num = num +1
                    if num ==count:
                        z.toast("点赞数达到要求,停止模块")
                        print("点赞数达到要求,停止模块")
                        break
                z.sleep(1)
                i = i +1
                continue
            else:
                obj2 = d(index=i+1,className="android.widget.LinearLayout").child(index=6,className="android.widget.RelativeLayout").child(
                        index=1,className='android.widget.FrameLayout').child(index=0,className="android.widget.ImageView")
                if obj2.exists:
                    z.sleep(1)
                    z.heartbeat()
                    obj2.click()
                    continue
                z.sleep(1)
                z.heartbeat()
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                z.sleep(1)
                objtemp = d(index=i-1,className="android.widget.LinearLayout")
                if objtemp.exists:
                    objinfo = objtemp.info
                    if objinfo in objlist:
                        z.toast("到底了,没有说说可赞了,停止模块")
                        print("到底了,没有说说可赞了,停止模块")
                        return
                    else:
                        objlist.append(objinfo)
                if flag:
                    i = 0
                    flag =False
                else:
                    i = 1

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMSpaceParise

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT524SK00685")
    z = ZDevice("HT524SK00685")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"count":"5","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
