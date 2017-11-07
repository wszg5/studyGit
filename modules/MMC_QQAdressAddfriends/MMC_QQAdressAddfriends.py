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


class MMCQQAdressAddfriends:
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
        obj = d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.TextView',
                 descriptionContains='基本信息' )  # 当弹出选择QQ框的时候，定位不到验证码图片
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
            # print("---------------------------------------------------------------------------")
            # print(dominant_color)
            z.heartbeat( )
            if None == dominant_color:
                # print('见鬼了')
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

    def getAddressList(self, d,z, args):
        z.heartbeat()
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        filename = os.path.join(base_dir, "%s.txt"%(self.GetUnique()) )

        number_count = int(args['number_count'])
        cate_id = args["repo_cate_id"]
        while True:
            exist_numbers = self.repo.GetNumber(cate_id, 0, number_count, 'exist')
            print(exist_numbers)
            remain = number_count - len(exist_numbers)
            normal_numbers = self.repo.GetNumber(cate_id, 0, remain, 'normal')
            numbers = exist_numbers + normal_numbers
            if len(numbers)> 0:
                break

            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，等待中\""%cate_id).communicate()
            z.sleep(30)

        if numbers:
            file_object = open(filename, 'w')
            lines = ""
            pname = ""
            for number in numbers:
                if number["name"] is None:
                    random_name = args['random_name']
                    if random_name == '是':
                        pname = z.phoneToName(number["number"])
                    else:
                        pname = number["number"]
                else:
                    pname = number["name"]
                lines = "%s%s----%s\r" %(lines, pname, number["number"])

            file_object.writelines(lines)
            file_object.close()
            isclear = args['clear']
            if isclear=='是':
                d.server.adb.cmd("shell", "pm clear com.android.providers.contacts").communicate()

            #d.server.adb.cmd("shell", "am", "start", "-a", "zime.clear.contacts").communicate()
            d.server.adb.cmd("push", filename, "/data/local/tmp/contacts.txt").communicate()
            d.server.adb.cmd("shell", "am", "start", "-n", "com.zunyun.zime/.ImportActivity", "-t", "text/plain", "-d",
                             "file:////data/local/tmp/contacts.txt").communicate()


            #d.server.adb.cmd("shell", "am broadcast -a com.zunyun.import.contact --es file \"file:///data/local/tmp/contacts.txt\"").communicate()
            os.remove(filename)

            out = d.server.adb.cmd("shell",
                               "dumpsys activity top  | grep ACTIVITY").communicate()[0].decode('utf-8')
            while out.find("com.zunyun.zime/.ImportActivity") > -1:
                z.heartbeat()
                out = d.server.adb.cmd("shell",
                                   "dumpsys activity top  | grep ACTIVITY").communicate()[0].decode('utf-8')
                z.sleep(5)


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

    def Bind(self, d, z):
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )
            print(GetBindNumber)
            z.sleep( 2 )
            d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText' ).set_text(
                GetBindNumber )  # GetBindNumber
            z.heartbeat( )
            z.sleep( 1 )
            d( text='下一步' ).click( )
            z.sleep( 3 )
            if d( text='下一步', resourceId='com.tencent.mobileqq:id/name', index=2 ).exists:  # 操作过于频繁的情况
                return 'false'

            if d( text='确定', resourceId='com.tencent.mobileqq:id/name',
                  index='2' ).exists:  # 提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d( text='确定', resourceId='com.tencent.mobileqq:id/name', index='2' ).click( )
            z.heartbeat( )
            code = self.scode.GetVertifyCode( GetBindNumber, self.scode.QQ_CONTACT_BIND, '4' )
            newStart = 0

            d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText' ).set_text( code )
            d( text='完成', resourceId='com.tencent.mobileqq:id/name' ).click( )
            z.heartbeat( )
            z.sleep( 5 )
            if d( textContains='没有可匹配的' ).exists:
                return 'false'

        return 'true'

    def action(self,d,z,args):
        startTime = args["startTime"]
        endTime = args["endTime"]
        try:
            if self.repo.timeCompare(startTime,endTime):
                z.toast("该时间段不允许运行")
                return
        except:
            z.toast("输入的时间格式错误,请检查后再试")
            return
        set_timeStart = int( args['set_timeStart'] )  # 得到设定的时间
        set_timeEnd = int( args["set_timeEnd"] )
        run_time = float( random.randint( set_timeStart, set_timeEnd ) )
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return

        z.heartbeat( )
        z.toast( "准备执行QQ通讯录加好友+导入通讯录 MMS版" )
        z.toast("开始导入通讯录")
        self.getAddressList(d,z,args)
        z.heartbeat( )
        gender1 = args['gender']

        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ通讯录加好友+导入通讯录 MMS版" )
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
        cate_id1 = args["repo_material_id"]
        Material = self.repo.GetMaterial( cate_id1, 0, 1 )
        message = Material[0]['content']  # 取出验证消息的内容
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        # loginStatusList = z.qq_getLoginStatus( d )
        # if loginStatusList is None:
        #     z.toast( "登陆新场景，现无法判断登陆状态" )
        #     now = datetime.datetime.now( )
        #     nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        #     cache.set( '%s_MMCQQAddfriendsByNumber_time' % d.server.adb.device_serial( ), nowtime,
        #                None )
        #     z.toast( '模块结束，保存的时间是%s' % nowtime )
        #     return
        # loginStatus = loginStatusList['success']
        # if loginStatus:
        #     z.toast( "卡槽QQ状态正常，继续执行" )
        # else:
        #     z.toast( "卡槽QQ状态异常，跳过此模块" )
        #     now = datetime.datetime.now( )
        #     nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        #     cache.set( '%s_MMCQQAddfriendsByNumber_time' % d.server.adb.device_serial( ), nowtime,
        #                None )
        #     z.toast( '模块结束，保存的时间是%s' % nowtime )
        #     return
        if d(text="消息",resourceId="com.tencent.mobileqq:id/ivTitleName",className="android.widget.TextView").exists:
            z.toast("登录状态正常")
        elif d( text='绑定手机号码' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep(0.5)
            z.sleep( 1 )
        elif d( text='主题装扮' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep(0.5)
        elif d( text='马上绑定' ).exists:
            while d( text='关闭' ).exists:
                d( text='关闭' ).click( )
                z.sleep(0.5)
        else:
            z.toast("登录状态异常,停止模块")
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        # if d(text='通讯录').exists:
        #     d(text='关闭').click()

        if d(className="android.widget.ImageView",description="快捷入口").exists:
            d( className="android.widget.ImageView", description="快捷入口" ).click()
            z.heartbeat()
            if d(text="加好友/群",className="android.widget.TextView").exists:
                d( text="加好友/群", className="android.widget.TextView" ).click()
                z.sleep(1)
            if d(text="添加手机联系人",className="android.widget.TextView").exists:
                d( text="添加手机联系人", className="android.widget.TextView" ).click()
            if d(className="android.view.View",description="删除 按钮").exists:
                d( className="android.view.View", description="删除 按钮" ).click()
                z.sleep(1)
            if d(text="验证手机号码",resourceId="com.tencent.mobileqq:id/ivTitleName").exists:
                if not d( textContains='+86' ).exists:
                    d( description='点击选择国家和地区' ).click( )
                    if d( text='中国' ).exists:
                        d( text='中国' ).click( )
                    else:
                        str = d.info  # 获取屏幕大小等信息
                        height = str["displayHeight"]
                        width = str["displayWidth"]
                        d.click( width * 5 / 12, height * 5 / 32 )
                        z.sleep( 1.5 )
                        z.input( '中国' )
                        z.sleep( 2 )
                        d( text='+86' ).click( )
                console = self.Bind(d,z)
                if console is "false":
                    z.toast("绑定手机号失败")
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
            if d( text="启用" ).exists:  # 检查到尚未 启用通讯录
                d( text="启用" ).click( )
                if not d( textContains='+86' ).exists:
                    d( description='点击选择国家和地区' ).click( )
                    if d( text='中国' ).exists:
                        d( text='中国' ).click( )
                    else:
                        str = d.info  # 获取屏幕大小等信息
                        height = str["displayHeight"]
                        width = str["displayWidth"]
                        d.click( width * 5 / 12, height * 5 / 32 )
                        z.sleep( 1.5 )
                        z.input( '中国' )
                        z.sleep( 2 )
                        d( text='+86' ).click( )
                z.heartbeat( )
                text = self.Bind( d, z )  # 未开启通讯录的，现绑定通讯录
                z.heartbeat( )
                if text == 'false':  # 操作过于频繁的情况
                    if (args["time_delay"]):
                        z.sleep( int( args["time_delay"] ) )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                z.sleep( 7 )
            if d( textContains='没有可匹配的' ).exists:
                if d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).exists:
                    d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click( )
                    z.sleep( 1 )
                    if d( text='添加手机联系人' ).exists:
                        d( text='添加手机联系人' ).click( )
                        z.sleep( 1 )
                        if d( textContains='没有可匹配的' ).exists:
                            if d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).exists:
                                d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click( )
                                z.sleep( 1 )
                                if d( text='添加手机联系人' ).exists:
                                    d( text='添加手机联系人' ).click( )
                                    z.sleep( 1 )
                                    if d( textContains='没有可匹配的' ).exists:
                                        z.toast( "显示不出来" )
                                        now = datetime.datetime.now( )
                                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                                        z.setModuleLastRun( self.mid )
                                        z.toast( '模块结束，保存的时间是%s' % nowtime )
                                        return
            if d( text='匹配手机通讯录' ).exists:
                d( text='匹配手机通讯录' ).click( )
            z.heartbeat( )
            z.sleep( 5 )
            obj1 = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                      index=2 ) \
                .child( className='android.widget.ImageView', index=0 )  # 判断第一次进通讯录是否有人
            if not obj1.exists:
                if d( text='返回' ).exists:
                    d( text='返回' ).click( )
                z.sleep( 1.5 )
                if d( text='添加手机联系人' ).exists:
                    d( text='添加手机联系人' ).click( )
                if not obj1.exists:
                    z.toast( "该手机上没有联系人" )
                    if (args["time_delay"]):
                        z.sleep( int( args["time_delay"] ) )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return

        index = 2
        EndIndex = int( args['EndIndex'] )
        # while index < EndIndex + 1:
        # for index in range(2,EndIndex+3):
        #     cate_id = args["repo_material_id"]
        #     time.sleep(2)
        num = 0
        a = 0
        count = 0
        # obj = d( text="添加", index=0 )
        while True:
            if num ==4:
                z.toast("暂时可能操作频繁,停止模块")
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                z.setModuleLastRun( self.mid )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            obj = d( index=0, className='android.widget.AbsListView' ).child(
                className="android.widget.LinearLayout", index=index )

            if obj.exists:
                obj = obj.child( index=0,className="android.widget.RelativeLayout" ).child(index=2, resourceId="com.tencent.mobileqq:id/result_layout" )
                if obj.exists:
                    obj = obj.child( text="添加", index=0 )
                    if obj.exists:
                        obj.click()
                        z.sleep(1)
                    else:
                        index = index + 1
                        continue
                else:
                    index = index + 1
                    continue
            else:
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                index = index - 1
                obj = d( index=0, className='android.widget.AbsListView' ).child(
                    className="android.widget.LinearLayout", index=index ).child( index=0,
                                                                                  className="android.widget.RelativeLayout" )

                if obj.exists:
                    obj = d( index=0, className='android.widget.AbsListView' ).child(
                        className="android.widget.LinearLayout", index=index ).child( index=0,
                                                                                      className="android.widget.RelativeLayout" ).child(
                        index=2, resourceId="com.tencent.mobileqq:id/result_layout" ).child( text="等待验证",index=0 )
                    if obj.exists:
                        z.toast("到底了,模块结束")
                        now = datetime.datetime.now( )
                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                        z.setModuleLastRun( self.mid )
                        z.toast( '模块结束，保存的时间是%s' % nowtime )
                        return

                    else:
                        index = 2
                        continue

            z.sleep( 1 )
            z.heartbeat( )
            if obj.exists:  # 拒绝被添加的轻况或请求失败
                num = num + 1
                index = index + 1
                obj = d( index=0, className='android.widget.AbsListView' ).child(
                    className="android.widget.LinearLayout", index=index ).child( index=0,
                                                                                  className="android.widget.RelativeLayout" ).child(
                    index=2, resourceId="com.tencent.mobileqq:id/result_layout" ).child( text="添加", index=0 )
                continue
            if d( text='输入答案' ).exists or d(description="输入答案").exists:  # 要回答问题的情况
                if d(text="取消",resourceId="com.tencent.mobileqq:id/ivTitleBtnLeftButton").exists:
                    d( text="取消", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeftButton" ).click()
                num = 0
                continue
            d.dump( compressed=False )
            if d( text="风险提示" ).exists:  # 风险提示
                d( text="取消" ).click( )
                z.sleep( 1 )
                if d( text="取消", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeftButton" ).exists:
                    d( text="取消", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeftButton" ).click( )
                num = 0
                continue
            obj = d( text='发送', resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText' )  # 不需要验证可直接添加为好友的情况
            if obj.exists:
                z.sleep( 2 )
                obj = d( index=4, className='android.widget.EditText',
                        resourceId='com.tencent.mobileqq:id/name' )  # 将之前消息框的内容删除        需要发送验证信息
                if obj.exists:
                    obj.click()
                    z.sleep(0.5)
                    obj = obj.info
                    obj = obj['text']
                    lenth = len( obj )
                    t = 0
                    while t < lenth:
                        d.press.delete( )
                        t = t + 1
                    time.sleep( 2 )
                    z.input( message )
                    z.sleep( 1 )
                if d( text='发送', resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText' ).exists:
                    d( text='发送', resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText' ).click( )
                if d( text='添加失败，请勿频繁操作', resourceId='com.tencent.mobileqq:id/name' ).exists:
                    z.heartbeat( )
                    z.toast( "频繁操作,跳出模块" )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                else:
                    index = index + 1
                    count = count + 1
                    print("请求发送成功")
                if count == EndIndex:
                    z.toast("已发送添加请求至指定数目,结束模块")
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                num = 0


def getPluginClass():
    return MMCQQAdressAddfriends

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")

    args = {"repo_cate_id":"113",'number_count':'20',"random_name":"是","clear":"是","time_delay":"3","repo_material_id":"39",'gender':"不限",
            "EndIndex": "20","set_timeStart":"0","set_timeEnd":"1","startTime":"0","endTime":"8"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
