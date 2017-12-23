# coding:utf-8
from __future__ import division
import base64
import colorsys

import logging
import re

from PIL import Image

from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import os, time, datetime, random
import json

from zcache import cache
from zservice import ZDevice


class MMCTIMAddfriendsByCard:
    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )
    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def Gender(self, d, z):
        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        obj = d( resourceId='com.tencent.tim:id/name', className='android.widget.ImageView' )
        if obj.exists:
            z.heartbeat( )
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
                z.heartbeat( )
                score = (saturation + 0.1) * count
                if score > max_score:
                    max_score = score
                    dominant_color = (r, g, b)
            # print("---------------------------------------------------------------------------")
            # print(dominant_color)
            z.heartbeat( )
            if None == dominant_color:
                return '不限'
            red = dominant_color[0]
            blue = dominant_color[2]

            if red > blue:
                # print('女')
                return '女'
            else:
                # print('男')
                return '男'
        else:  # 没有基本资料的情况
            return '不限'

    def action(self, d, z,args):
        startTime = args["startTime"]
        endTime = args["endTime"]
        try:
            if self.repo.timeCompare( startTime, endTime ):
                z.toast( "该时间段不允许运行" )
                return
        except:
            z.toast( "输入的时间格式错误,请检查后再试" )
            return
        set_timeStart = int( args['set_timeStart'] )  # 得到设定的时间
        set_timeEnd = int( args["set_timeEnd"] )
        run_time = float( random.randint( set_timeStart, set_timeEnd ) )
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return
        z.toast( "准备执行MMS版TIM名片加好友模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM加好友(名片)" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text="消息", resourceId="com.tencent.tim:id/ivTitleName" ).exists and not d( text="马上绑定",className="android.widget.Button" ).exists:
            z.toast( "登录状态正常，继续执行" )
        else:
            if d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).exists:
                d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).click( )
                z.sleep( 1 )
            elif d( text="消息", className="android.widget.TextView" ).exists and d( text="马上绑定",className="android.widget.Button" ).exists:
                d( text="消息", className="android.widget.TextView" ).click( )
                z.sleep( 1 )
            elif d( text="返回" ).exists:
                d( text="返回" ).click( )
                z.sleep( 1 )

            else:
                z.toast( "登录状态异常，跳过此模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return

        gender1 = args['gender']
        cate_id1 = args["repo_material_cate_id"]
        add_count = int( args['add_count'] )  # 要添加多少人
        switch_card = args["switch_card"]
        switch = args["switch"]
        count = 1
        num = 0
        while True:  # 总人数
            Material = self.repo.GetMaterial( cate_id1, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id1 ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']  # 取出验证消息的内容

            repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号

            numbers = self.repo.GetNumber( repo_number_cate_id, 120, 1 )  # 取出add_count条两小时内没有用过的号码
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % repo_number_cate_id ).communicate( )
                z.sleep( 5 )
                return
            z.heartbeat( )
            QQnumber = numbers[0]['number']
            print(QQnumber)
            z.sleep( 1 )

            z.cmd( "shell",
                   'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"' % QQnumber )  # qq名片页面
            z.sleep( random.randint( 5, 7 ) )
            if d( text='TIM' ).exists:
                z.heartbeat( )
                d( text='TIM' ).click( )
                z.sleep( 2 )
                z.heartbeat( )
                while d( text='仅此一次' ).exists:
                    z.heartbeat( )
                    d( text='仅此一次' ).click( )
            z.sleep( 1 )
            if d( text="申请加群" ).exists:
                continue
            objtext = d( index=0, className="android.widget.LinearLayout" ).child( index=1,
                                                                                   className="android.widget.RelativeLayout" ).child(
                index=1, className="android.widget.TextView" )
            if objtext.exists:
                objtext = objtext.info['text']
                if objtext == "":
                    z.toast( "账号为空,继续唤醒" )
                    continue
            if gender1 != '不限':
                gender2 = self.Gender( d, z )
                z.heartbeat( )
                if gender1 == gender2:  # gender1是外界设定的，gender2是读取到的
                    z.sleep( 1 )
                else:
                    # d( text='返回', resourceId='com.tencent.tim:id/ivTitleBtnLeft' ).click( )
                    # add_count = add_count+1
                    continue
            z.sleep( 1 )
            n = 1
            # d.dump( compressed=False )
            if d( text='加好友', className="android.widget.Button" ).exists:
                d( text='加好友', className="android.widget.Button" ).click( )
                z.toast( "点了一次" )
                z.sleep( 6 )
            d.dump( compressed=False )
            if d( text='加好友', className="android.widget.Button" ).exists:
                d( text='加好友', className="android.widget.Button" ).click( )
                z.toast( "点了二次" )
                z.sleep( 6 )
            d.dump( compressed=False )
            if d( text='加好友', className="android.widget.Button" ).exists:
                d( text='加好友', className="android.widget.Button" ).click( )
                z.toast( "点了三次" )
                z.sleep( 6 )
            z.heartbeat( )
            d.dump( compressed=False )
            if d( text='加好友', className="android.widget.Button" ).exists:  # 拒绝被添加的轻况
                z.toast( "无法加好友,重新唤醒" )
                z.sleep( 2 )
                continue

            if d( text='必填', resourceId='com.tencent.tim:id/name' ).exists:  # 要回答问题的情况
                z.heartbeat( )
                continue
            d.dump( compressed=False )
            if d( text="风险提示" ).exists:  # 风险提示
                z.heartbeat( )
                continue
            obj = d( text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText' )  # 不需要验证可直接添加为好友的情况
            if obj.exists:
                z.sleep( 2 )
                obj.click( )
                if d( text='添加失败，请勿频繁操作', resourceId='com.tencent.tim:id/name' ).exists:
                    z.heartbeat( )
                    z.toast( "频繁操作,跳出模块" )
                    return
                else:
                    count = count + 1
                    print(QQnumber + "请求发送成功")
                continue

            if switch == "是":
                d.dump( compressed=False )
                obj = d( index=3, className='android.widget.EditText',
                         resourceId='com.tencent.tim:id/name' ).info  # 将之前消息框的内容删除        需要发送验证信息
                obj = obj['text']
                lenth = len( obj )
                t = 0
                while t < lenth:
                    d.press.delete( )
                    t = t + 1
                time.sleep( 2 )
                # z.input(message)
            # d(index=2,className="android.widget.CompoundButton",resourceId="com.tencent.tim:id/name").click()
            if "是" in switch_card:
                if d( index=2, className="android.widget.CompoundButton", resourceId="com.tencent.tim:id/name" ).exists:
                    d( index=2, className="android.widget.CompoundButton",
                       resourceId="com.tencent.tim:id/name" ).click( )
                else:
                    if d( text="设置我的名片" ).exists:
                        d( text="设置我的名片" ).click( )
                        while True:
                            z.sleep( 3 )
                            z.heartbeat( )
                            d.dump( compressed=False )
                            if d( text="添加我的名片" ).exists:
                                d( text="添加我的名片" ).click( )
                            d( index=3, resourceId="com.tencent.tim:id/name",
                               className="android.widget.Button" ).click( )
                            z.sleep( 2 )
                            obj = d( index=0, className="com.tencent.widget.GridView",
                                     resourceId="com.tencent.tim:id/photo_list_gv" ).child(
                                index=0, className="android.widget.RelativeLayout" )
                            if obj.exists:
                                z.sleep( 1 )
                                z.heartbeat( )
                                obj.click( )
                                z.sleep( 3 )
                                d( text='确定', resourceId='com.tencent.tim:id/name' ).click( )
                                time.sleep( 3 )
                                z.heartbeat( )
                                d( text="完成" ).click( )
                                z.sleep( 1 )
                                z.heartbeat( )
                                d( text="返回" ).click( )
                                break
                            if d( index=0, resourceId="com.tencent.tim:id/name",
                                  className="android.widget.ImageButton" ).exists:
                                d( index=0, resourceId="com.tencent.tim:id/name",
                                   className="android.widget.ImageButton" ).click( )
                                d( text="退出" ).click( )
            z.sleep( 3 )
            z.heartbeat( )
            d.dump( compressed=False )
            if d( text='下一步', resourceId='com.tencent.tim:id/ivTitleBtnRightText' ).exists:
                z.heartbeat( )
                d( text='下一步', resourceId='com.tencent.tim:id/ivTitleBtnRightText' ).click( )
            z.sleep( 2 )
            if d( text='发送' ).exists:
                z.heartbeat( )
                d( text='发送' ).click( )
                z.sleep( 3 )
            if d( resourceId='com.tencent.tim:id/name', text='添加失败，请勿频繁操作' ).exists:  # 操作过于频繁的情况
                z.toast( "频繁操作,跳出模块" )
                return
            print(QQnumber + "请求发送成功")
            z.heartbeat( )
            if count == add_count:
                break
            count = count + 1
        z.sleep( 1 )
        z.toast( "模块完成" )
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCTIMAddfriendsByCard

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"time_delay":"3","set_timeStart":"1","set_timeEnd":"1","startTime":"0","endTime":"8",
            "repo_number_cate_id":"119","repo_material_cate_id":"39",'gender':"不限","add_count":"5","switch_card":"N","switch":"是"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
