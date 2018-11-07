# coding:utf-8
from __future__ import division
import colorsys
import datetime
import os

from PIL import Image

from uiautomator import Device
import  time,threading
from zservice import ZDevice
import random
import re
from Repo import *

class MobilqqCheckPicture:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )  # 生成当前时间
        randomNum = random.randint( 0, 1000 )  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str( 00 ) + str( randomNum )
        uniqueNum = str( nowTime ) + str( randomNum )
        return uniqueNum

    def WebViewBlankPages(self, d,i):
        # z.toast( "判断图片是否正常" )
        Str = d.info  # 获取屏幕大小等信息
        height = float( Str["displayHeight"] )
        width = float( Str["displayWidth"] )

        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        if i>=0:
            getobj = d( index=2, className="android.widget.HorizontalScrollView" ).child(
                index=0,className="android.widget.LinearLayout",resourceId="com.tencent.mobileqq:id/name" ).child(
                index=i, className="android.widget.FrameLayout" )
        else:
            getobj = d( index=0, className="android.widget.LinearLayout" ).child( index=0,
                                                                                  resourceId="com.tencent.mobileqq:id/name",
                                                                                  className="android.widget.RelativeLayout" ).child(
                index=1, resourceId="com.tencent.mobileqq:id/name", className="android.widget.RelativeLayout" )
        if getobj.exists:
            getobj = getobj.info["bounds"]
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

    def action(self, d,z, args):
        z.toast( "准备执行QQ交友资料图片检测修改" )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        if d( text="消息", resourceId="com.tencent.mobileqq:id/ivTitleName", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
        elif d( text='绑定手机号码' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep( 0.5 )
            z.sleep( 1 )
        elif d( text='主题装扮' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep( 0.5 )
        elif d( text='马上绑定' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep( 0.5 )
        else:
            z.toast( "登录状态异常,停止模块" )
            return

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.heartbeat()
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
        if d(textContains='匹配').exists:
            d.press.back()
        z.heartbeat()
        z.heartbeat()
        if d( text="联系人", resourceId="com.tencent.mobileqq:id/name" ).exists:
            d( text="联系人", resourceId="com.tencent.mobileqq:id/name" ).click( )
            time.sleep( 1 )
            d( text="添加", resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText" ).click( )
            time.sleep(1)
            d(text='查看附近的人').click()
            time.sleep(10)
        # while not d(text='附近的人',className="android.widget.TextView").exists:
        #     d(index=2,text="动态",className="android.widget.TextView").click()
        #     z.sleep(1)
        #     if d(index=1,text="附近",className="android.widget.TextView").exists:
        #         d(index=1,text="附近",className="android.widget.TextView").click()
        #         continue
        # d(text='附近的人',className="android.widget.TextView").click()
        while d(textContains='附近内容正在加载中').exists:
            z.sleep(2)
        # d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=2).click()
        d( textContains='我的',resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText' ).click()
        time.sleep(3)
        forwait = 0
        while True:
            if d(text='附近点赞升级啦').exists:
                d( text='知道了' ).click( )
                break
            else:
                z.sleep(2)
                if forwait == 4:
                    break
                else:
                    forwait = forwait+1
        d.click(500,230)
        time.sleep(3)
        z.heartbeat( )
        while d(textContains="正在加载").exists:
            time.sleep(2)
        d(text="资料",resourceId="com.tencent.mobileqq:id/name").click()
        while not d(text='编辑交友资料').exists:
            time.sleep(1)
        z.sleep(1)
        z.heartbeat()
        d( text='编辑交友资料', className="android.widget.Button" ).click( )
        if d( text='立即编辑' ).exists:
            d( text='立即编辑' ).click( )
            z.sleep( 1 )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        obj = d(className="com.tencent.widget.GridView",index=0).child(index=0,className="android.widget.RelativeLayout").child(index=0,className='android.widget.FrameLayout')
        flag = False
        while obj.exists:
            obj.click( )
            if d( text="删除照片" ).exists:
                d( text="删除照片" ).click( )
            else:
                flag = True
                d(text="取消").click()
                break
        d(text="添加照片",resourceId="com.tencent.mobileqq:id/name").click()
        time.sleep(1)
        d(text="手机相册").click()
        time.sleep(4)
        z.heartbeat( )
        for index in range(12):
            obj = d( className="com.tencent.widget.GridView", index=0 ).child( index=index,
                                                                               className="android.widget.RelativeLayout" ).child(
                index=0, className='android.widget.ImageView' )
            if obj.exists:
                obj.click( )
                time.sleep( 1 )
                d( text="完成" ).click( )
                if flag:
                    flag = False
                    obj = d( className="com.tencent.widget.GridView", index=0 ).child( index=0,
                                                                                       className="android.widget.RelativeLayout" ).child(
                        index=0, className='android.widget.FrameLayout' )
                    if obj.exists:
                        obj.click()
                        if d( text="删除照片" ).exists:
                            d( text="删除照片" ).click( )
                        else:
                            d( text="取消" ).click( )
                d( text="添加照片", resourceId="com.tencent.mobileqq:id/name" ).click( )
                time.sleep( 1 )
                d( text="手机相册" ).click( )
                time.sleep( 4 )
                z.heartbeat( )
            else:
                d(text="取消").click()
                time.sleep(1)
                break
        z.heartbeat( )
        d(resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText",text="完成").click()
        time.sleep(3)
        while d(textContains="正在上传照片").exists:
            time.sleep(3)



        # topobj = d(index=0,className="android.widget.LinearLayout").child(index=0,resourceId="com.tencent.mobileqq:id/name",className="android.widget.RelativeLayout").child(index=1,resourceId="com.tencent.mobileqq:id/name",className="android.widget.RelativeLayout")
        # obj1 = d( index=1, className="android.widget.RelativeLayout" ).child( index=0,
        #                                                                       className="android.widget.AbsListView",
        #                                                                       resourceId="com.tencent.mobileqq:id/name" )
        # if obj1.exists:
        #     obj1 = obj1.info["bounds"]
        #     top = obj1["top"]
        #     left = obj1["left"]
        #     right = obj1["right"]
        #     bottom = obj1["bottom"]
        #     x = (394 - 271)/540
        # objnum = d( index=3, className="android.widget.LinearLayout" ).child( index=1, className="android.widget.TextView",
        #                                                          textContains="/12" )
        # if objnum.exists:
        #     objnum = objnum.info["text"]
        #     objnum = int( objnum[:len( objnum ) - 3] )
        #     i = objnum - 1
        # while True:
        #     if not d( index=1, className="android.widget.RelativeLayout" ).child( index=0,
        #                                                                       className="android.widget.AbsListView",
        #                                                                       resourceId="com.tencent.mobileqq:id/name" ).exists:
        #         break
        #     obj = d( index=2, className="android.widget.HorizontalScrollView" ).child( index=0,className="android.widget.LinearLayout",resourceId="com.tencent.mobileqq:id/name" ).child(
        #         index=i, className="android.widget.FrameLayout" )
        #     if i<0:
        #         if topobj.exists:
        #             z.sleep( 1 )
        #             z.heartbeat( )
        #             color = self.WebViewBlankPages( d, i )
        #             if color == (212, 212, 212) or color == (213, 213, 213) :
        #                 z.sleep( 1 )
        #                 z.heartbeat( )
        #                 while not d( text="删除头像" ).exists:
        #                     topobj.click( )
        #                 z.sleep( 1 )
        #                 z.heartbeat( )
        #                 if d( text="删除头像" ).exists:
        #                     d( text="删除头像" ).click( )
        #                     z.toast( "图片检测完成" )
        #             break
        #
        #     else:
        #         if obj.exists:
        #             z.sleep(1)
        #             z.heartbeat()
        #             color = self.WebViewBlankPages( d,i)
        #             if color == (212, 212, 212)or color == (213, 213, 213):
        #                 z.sleep( 1 )
        #                 z.heartbeat( )
        #                 obj.click( )
        #                 z.sleep( 1 )
        #                 z.heartbeat( )
        #                 if d( text="删除照片" ).exists:
        #                     d( text="删除照片" ).click( )
        #             z.sleep(1)
        #             z.heartbeat()
        #             i = i - 1
        #             d.swipe( (right - left) / 2, (bottom - top) + top, (right - left) / 2 + width * x,(bottom - top) + top )
        #             z.sleep( 1 )
        #         else:
        #             i = i -1
        #             # d.swipe( (right - left) / 2, (bottom - top) + top, (right - left) / 2 + width * x,
        #             #          (bottom - top) + top )
        #             continue

        # z.sleep(1)
        # z.heartbeat()
        # d( text='完成' ).click( )
        # z.sleep( 2 )
        # if d( text='发布资料' ).exists:
        #     d( text='发布资料' ).click( )
        #
        # seconds = 30
        # while seconds > 0:
        #     seconds = seconds - 5
        #     z.heartbeat( )
        #     z.sleep( 5 )
        #     z.toast( "等待资料上传完成" )
        #     if d( textContains='编辑交友资料' ).exists:
        #         z.sleep( 1 )
        #         z.heartbeat( )
        #         break
        #     if d( textContains='资料完整度' ).exists:
        #         z.sleep( 1 )
        #         z.heartbeat( )
        #         d( description="关闭", className="android.widget.ImageButton" ).click( )
        #         break
        # if d( text="完成" ).exists:
        #     d( text="完成" ).click( )
        # d( text='编辑交友资料', className="android.widget.Button" ).click( )
        # if d( text='立即编辑' ).exists:
        #     d( text='立即编辑' ).click( )
        #     z.sleep( 2 )
        # if topobj.exists:
        #     z.heartbeat( )
        #     topobj.click( )
        #     if d(text="查看大图").exists:
        # for m in range( 0, 12 ):
        #     if d(className='android.widget.FrameLayout', index=3).child(className='android.widget.ImageView', index=1).exists or d(className="android.widget.FrameLayout",description="添加图片").exists:
        #         if d(className="android.widget.FrameLayout",description="添加图片").exists:
        #             z.heartbeat()
        #             d( className="android.widget.FrameLayout", description="添加图片" ).click()
        #         else:
        #             d( className='android.widget.FrameLayout', index=3 ).child( className='android.widget.ImageView',index=1 ).click()
        #             z.sleep(1)
        #             z.heartbeat()
        #             if d(text="查看大图").exists:
        #                 continue
        #         z.heartbeat()
        #         d(text='从手机相册选择图片',className="android.widget.TextView").click()
        #         time.sleep(2)
        #         if d(className='com.tencent.widget.GridView').child(className='android.widget.RelativeLayout',index=m).exists:
        #             d(className='com.tencent.widget.GridView').child(className='android.widget.RelativeLayout', index=m).click()
        #         else:
        #             z.toast('手机不足12张图片')
        #             break
        #         rangee = d(className='android.widget.RelativeLayout', index=0).child(className='android.widget.RelativeLayout',index=1).child(className='android.view.View').info['bounds']
        #         x1 = rangee['left']     #缩小图片
        #         y1 = rangee['top']
        #         x2 = rangee['right']
        #         y2 = rangee['bottom']
        #         print(rangee)
        #         d(className='android.view.View').gesture((x1, y1), (x1, y1)).to((x2, y2), (x2, y2))
        #         d(text='完成').click()
        #         z.sleep(2)
        #         z.heartbeat()
        #         if not d(description='添加图片').exists:
        #            break
        #         z.heartbeat()
        #     else:
        #         picnum = d( textContains='上传真实照片' ).right( className='android.widget.TextView', index=1 )
        #         if picnum.exists:
        #             picnum = picnum.info["text"]
        #             picnum = re.findall( r"\d+\.?\d*", picnum )
        #             if int(picnum[0])<12:
        #                 d( description='添加图片' ).click( )
        #                 d( textContains='从手机相册选择图片' ).click( )
        #             capic = int(picnum[0])
        #             for a in (12,capic,-1):
        #                 if d( className='com.tencent.widget.GridView' ).child( className='android.widget.RelativeLayout',index=a ).exists:
        #                     d( className='com.tencent.widget.GridView' ).child( className='android.widget.RelativeLayout',index=a ).click()
        #                 else:
        #                     z.toast( '手机不足12张图片' )
        #                     break

        # z.sleep( 1 )
        z.heartbeat( )
        # if d( text='完成' ).exists:
        #     d( text='完成' ).click( )
        # z.sleep( 2 )
        # if d( text='发布资料' ).exists:
        #     d( text='发布资料' ).click( )
        #
        # seconds = 30
        # while seconds > 0:
        #     seconds = seconds - 5
        #     z.heartbeat( )
        #     z.sleep( 5 )
        #     z.toast( "等待资料上传完成" )
        #     if d( textContains='编辑交友资料' ).exists:
        #         z.sleep( 1 )
        #         z.heartbeat( )
        #         break
        #     if d( textContains='资料完整度' ).exists:
        #         z.sleep( 1 )
        #         z.heartbeat( )
        #         d( description="关闭", className="android.widget.ImageButton" ).click( )
        #         break

def getPluginClass():
    return MobilqqCheckPicture

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cc0e9474")
    z = ZDevice("cc0e9474")
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").communicate()

    args = {"time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)
    # obj = d( className="com.tencent.widget.GridView", index=0 ).child( index=1,
    #                                                                    className="android.widget.RelativeLayout" ).child(
    #     index=0, className='android.widget.ImageView' )
    # if obj.exists:
    #     obj.click()
    #     time.sleep(1)
    #     d(text="完成").click()

    #     if d( text="删除照片" ).exists:
    #         d( text="删除照片" ).click( )
    #     else:
    #         break