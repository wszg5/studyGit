# coding:utf-8
import colorsys
import os

import datetime
import random

from PIL import Image

from uiautomator import Device
import  time
from zservice import ZDevice

class MobilqqPicWall:

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)
        z.heartbeat()
        d(description='帐户及设置').click()
        z.sleep(1.5)
        d(descriptionContains='等级：').click()
        z.sleep( 5 )
        d(text='编辑资料').click()
        z.sleep( 1.5 )
        if d(text='编辑资料').exists:
            d.press.back()
            time.sleep(1)
            if d( text='编辑资料' ).exists:
                d( text='编辑资料' ).click( )
                time.sleep(2)
        obj = d( textContains="张", resourceId="com.tencent.mobileqq:id/name" )
        if d(textContains="张",resourceId="com.tencent.mobileqq:id/name").exists:
            num = int(obj.info['text'][:-1])

            d(text='照片墙').click()
            time.sleep(5)
            while self.getColor() != (30, 185, 242):
                time.sleep(3)
        obj = d(index=0,descriptionContains='照片墙').child(index=0, className="android.widget.ListView").child(index=0, className="android.view.View")
        if obj.exists:
            time.sleep(3)
        picList = [(111,276),( 348, 276 ),( 601, 276 ),
                   (111, 504), (348, 054), (601, 504),
                   (111, 750), (348, 750), (601, 750),
                   ( 111, 1004 ), (348, 1004), (601, 1004)]

        pls = picList[:num]
        for pl in pls:
            d.click(pl)

        # d(description='上传照片').click()
        # z.sleep(1.5)
        # d(text='从手机相册选择').click()
        # z.sleep(3)
        # for i in range(0,9):
        #     forclick = d(className='com.tencent.widget.GridView').child(className='android.widget.RelativeLayout',index=i).\
        #         child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.CheckBox')
        #     if forclick.exists:
        #         forclick.click()
        # z.heartbeat()
        #
        # d(textContains='确定').click()
        # while d(textContains='上传中').exists:
        #     z.sleep(2)
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def getColor(self):
        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        left = 128
        top = 1205
        right = 212
        bottom = 1244

        d.screenshot( sourcePng )  # 截取整个输入验证码时的屏幕

        img = Image.open( sourcePng )
        box = (left, top, right, bottom)  # left top right bottom
        region = img.crop( box )  # 截取验证码的图片
        # show(region)　　　　　　　#展示资料卡上的信息
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
                dominant_color = (r, g, b)
        z.heartbeat( )
        if None == dominant_color:
            # print('见鬼了')
            return
        return dominant_color

def getPluginClass():
    return MobilqqPicWall

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cc0e9474")
    z = ZDevice("cc0e9474")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)
    # obj = d( index=0, descriptionContains='照片墙' ).child( index=0,className="android.widget.ListView" ).child( index=0,className="android.view.View",descriptionContains='照片' )
    # if obj.exists:
    #     print "fdsfvsdfvs"
    # obj = d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.RelativeLayout' )
    # obj = d( index=0, descriptionContains='照片墙' ).child(className='android.widget.ListView').child(index=11)
    # if d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.RelativeLayout').exists:
    #     print "ok"
    #     obj.click()
    # color = o.getColor()
    # print color
