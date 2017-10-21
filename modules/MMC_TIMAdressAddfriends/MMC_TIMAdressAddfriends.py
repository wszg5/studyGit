# coding:utf-8
from __future__ import division
import base64

import logging
import re

from slot import Slot
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import os, time, datetime, random
import json

from zcache import cache
from zservice import ZDevice


class MMCTIMAdressAddfriends:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def timeinterval(self, z, args):
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        d1 = datetime.datetime.strptime( nowtime, '%Y-%m-%d %H:%M:%S' )
        logging.info( '现在的时间%s' % nowtime )
        gettime = cache.get( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ) )
        logging.info( '以前的时间%s' % gettime )
        if gettime != None:
            d2 = datetime.datetime.strptime( gettime, '%Y-%m-%d %H:%M:%S' )
            delta1 = (d1 - d2)
            # print( delta1 )
            delta = re.findall( r"\d+\.?\d*", str( delta1 ) )  # 将天小时等数字拆开
            day1 = int( delta[0] )
            hours1 = int( delta[1] )
            minutes1 = 0
            if 'days' in str( delta1 ):
                minutes1 = int( delta[2] )
                allminutes = day1 * 24 * 60 + hours1 * 60 + minutes1
            else:
                allminutes = day1 * 60 + hours1  # 当时间不超过天时此时天数变量成为小时变量
            logging.info( "day=%s,hours=%s,minutes=%s" % (day1, hours1, minutes1) )

            logging.info( '两个时间的时间差%s' % allminutes )
            set_time = int( args['set_time'] )  # 得到设定的时间
            if allminutes < set_time:  # 由外界设定
                z.toast( '该模块未满足指定时间间隔,程序结束' )
                return 'end'
        else:
            z.toast( '尚未保存时间' )

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
        circle = 0
        self.scode = smsCode( d.server.adb.device_serial( ) )
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )
            print(GetBindNumber)
            z.sleep( 2 )
            z.heartbeat( )
            obj = d( className="android.view.View", description="删除 按钮" )
            if obj.exists:
                z.heartbeat( )
                z.sleep( 1 )
                obj.click( )
            z.sleep( 2 )
            d( resourceId='com.tencent.tim:id/name', className='android.widget.EditText' ).set_text(
                GetBindNumber )  # GetBindNumber
            z.heartbeat( )
            z.sleep( 1 )
            d( text='下一步' ).click( )
            z.sleep( 3 )
            if d( text='下一步' ).exists:  # 操作过于频繁的情况
                return 'false'
            if d( text='确定' ).exists:  # 提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d( text='确定', ).click( )
            z.heartbeat( )
            code = self.scode.GetVertifyCode( GetBindNumber, self.scode.QQ_CONTACT_BIND, '4' )
            d( resourceId='com.tencent.tim:id/name', className='android.widget.EditText' ).set_text( code )
            print(code)
            newStart = 0
            if d( text='请输入短信验证码' ).exists:
                if circle < 4:
                    z.toast( '没有接收到验证码' )
                    d( textContains='返回' ).click( )
                    if d( text='确定' ).exists:
                        d( text='返回' ).click( )
                        z.sleep( 1 )
                    d( description='删除 按钮' ).click( )
                    circle = circle + 1
                    newStart = 1
                    continue
                else:
                    z.toast( '程序结束' )
                    print(circle)
                    return 'false'
            z.heartbeat( )
            d( text='完成', resourceId='com.tencent.tim:id/name' ).click( )
            z.sleep( 10 )
            if d( textContains='没有可匹配的' ).exists:
                return 'false'
        return 'true'

    def bindPhoneNumber(self, z, d):
        z.toast( "点击开始绑定" )
        self.scode = smsCode( d.server.adb.device_serial( ) )
        d( text='马上绑定' ).click( )
        while d( text='验证手机号码' ).exists:
            PhoneNumber = None
            j = 0
            while PhoneNumber is None:
                j += 1
                PhoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )  # 获取接码平台手机号码
                z.heartbeat( )
                if j > 20:
                    z.toast( '取不到手机号码' )
                    return "nothing"
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
            obj = d( className="android.view.View", description="删除 按钮" )
            if obj.exists:
                z.heartbeat( )
                z.sleep( 1 )
                obj.click( )
            z.sleep( 2 )
            z.input( PhoneNumber )
            z.sleep( 1.5 )
            if d( text='下一步' ).exists:
                d( text='下一步' ).click( )
                z.sleep( 3 )
            if d( text='确定' ).exists:
                d( text='确定' ).click( )
                z.sleep( 2 )
            code = self.scode.GetVertifyCode( PhoneNumber, self.scode.QQ_CONTACT_BIND, '4' )  # 获取接码验证码
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_CONTACT_BIND )
            if code == '':
                z.toast( PhoneNumber + '手机号,获取不到验证码' )
                if d( text='返回' ).exists:
                    d( text='返回' ).click( )
                if not d( textContains='中国' ).exists:
                    if d( text='返回' ).exists:
                        d( text='返回' ).click( )
                if d( className='android.view.View', descriptionContains='删除' ).exists:
                    d( className='android.view.View', descriptionContains='删除' ).click( )
                continue
            z.heartbeat( )
            z.input( code )
            if d( text='完成' ).exists:
                d( text='完成' ).click( )
            z.sleep( 5 )
            break
        z.sleep( 1 )

    def action(self,d,z,args):
        condition = self.timeinterval( z, args )
        if condition == 'end':
            z.sleep( 2 )
            return
        z.heartbeat( )
        z.toast( "准备执行TIM通讯录加好友+导入通讯录 MMS版" )
        z.toast("开始导入通讯录")
        self.getAddressList(d,z,args)
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM通讯录加好友" )
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
        cate_id1 = args["repo_material_id"]
        Material = self.repo.GetMaterial( cate_id1, 0, 1 )
        message = Material[0]['content']  # 取出验证消息的内容
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
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
                cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                           None )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
        if d( text='马上绑定' ).exists:
            result = self.bindPhoneNumber( z, d )
            if result == "nothing":
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                           None )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
        if d( text='通讯录' ).exists:
            d( text='关闭' ).click( )
        d( description='快捷入口' ).click( )
        d( textContains='加好友' ).click( )
        d( text='添加手机联系人' ).click( )
        z.heartbeat( )
        while d( text='验证手机号码' ).exists:
            PhoneNumber = None
            j = 0
            while PhoneNumber is None:
                j += 1
                PhoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )  # 获取接码平台手机号码
                z.heartbeat( )
                if j > 2:
                    z.toast( '取不到手机号码' )
                    if (args["time_delay"]):
                        z.sleep( int( args["time_delay"] ) )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                               None )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
            obj = d( className="android.view.View", description="删除 按钮" )
            if obj.exists:
                z.heartbeat( )
                z.sleep( 1 )
                obj.click( )
            z.sleep( 2 )
            z.input( PhoneNumber )
            z.sleep( 1.5 )
            if d( text='下一步' ).exists:
                d( text='下一步' ).click( )
                z.sleep( 3 )
            if d( text='确定' ).exists:
                d( text='确定' ).click( )
                z.sleep( 2 )
            code = self.scode.GetVertifyCode( PhoneNumber, self.scode.QQ_CONTACT_BIND, '4' )  # 获取接码验证码
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_CONTACT_BIND )
            if code == '':
                z.toast( PhoneNumber + '手机号,获取不到验证码' )
                if d( text='返回' ).exists:
                    d( text='返回' ).click( )
                if not d( textContains='中国' ).exists:
                    if d( text='返回' ).exists:
                        d( text='返回' ).click( )
                if d( className='android.view.View', descriptionContains='删除' ).exists:
                    d( className='android.view.View', descriptionContains='删除' ).click( )
                continue
            z.heartbeat( )
            z.input( code )
            if d( text='完成' ).exists:
                d( text='完成' ).click( )
            z.sleep( 5 )
            break
        # if d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',
        #       index=2 ).exists:  # 检查到尚未 启用通讯录
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
                cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                           None )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            z.sleep( 7 )
        if d( textContains='没有可匹配的' ).exists:
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                       None )
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
            d( text='返回' ).click( )
            z.sleep( 1.5 )
            d( text='添加手机联系人' ).click( )
            if not obj1.exists:
                z.toast( "该手机上没有联系人" )
                if (args["time_delay"]):
                    z.sleep( int( args["time_delay"] ) )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                           None )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
        count = 0
        index = 2
        EndIndex = int( args['EndIndex'] )
        switch_card = args["switch_card"]
        # while index < EndIndex + 1:
        # for index in range(2,EndIndex+3):
        #     cate_id = args["repo_material_id"]
        #     time.sleep(2)
        num = 0
        obj = d( index=0, resourceId='com.tencent.tim:id/name', className='android.widget.AbsListView' ).child(
            className="android.widget.LinearLayout", index=index ).child( text="添加", index=2 )
        while obj.exists:

            obj.click( )

            # if gender != '不限':
            #     gender2 = self.Gender(d)
            #     if gender == gender2:               # gender是外界设定的，gender2是读取到的
            #         time.sleep(1)
            #     else:
            #         d(textContains='返回').click()
            #         i = i + 1
            z.sleep( 1 )
            z.heartbeat( )
            if obj.exists:  # 拒绝被添加的轻况或请求失败
                num = num + 1
                index = index + 1
                obj = d( index=0, resourceId='com.tencent.tim:id/name', className='android.widget.AbsListView' ).child(
                    className="android.widget.LinearLayout", index=index ).child( text="添加", index=2 )
                continue
            if d( text='必填', resourceId='com.tencent.tim:id/name' ).exists:  # 要回答问题的情况
                z.heartbeat( )
                objtext = d( textContains="问题", index=0, resourceId="com.tencent.tim:id/textView1",
                             className="android.widget.TextView" )
                objnum = d( index=1, resourceId="com.tencent.tim:id/name",
                            className="android.widget.FrameLayout" ).child(
                    index=0, className="android.widget.RelativeLayout", resourceId="com.tencent.tim:id/name" ).child(
                    index=2, resourceId="com.tencent.tim:id/name", className="android.widget.TextView" )
                if objtext.exists:
                    objtext = objtext.info["text"]
                    if "电话" in objtext or "手机" in objtext or "号码" in objtext:
                        if objnum.exists:
                            objnum = objnum.info["text"][3:]
                            z.input( objnum )
                            z.sleep( 1 )
                            z.heartbeat( )
                            d( text="下一步" ).click( )
                            z.sleep( 1 )
                            z.heartbeat( )
                            if d( text="下一步" ).exists:
                                z.sleep( 1 )
                                z.heartbeat( )
                                d( text="手机联系人" ).click( )
                                z.sleep( 1 )
                                z.heartbeat( )
                            else:
                                z.sleep( 1 )
                                z.heartbeat( )
                                if d( text="发送" ).exists:
                                    d( text="发送" ).click( )
                                    z.sleep(3)
                                    if d( text="发送" ).exists:
                                        now = datetime.datetime.now( )
                                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                                        cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                                                   None )
                                        z.toast( '模块结束，保存的时间是%s' % nowtime )
                                        return
                                if d( text='添加失败，请勿频繁操作' ).exists:
                                    z.heartbeat( )
                                    z.toast( "频繁操作,跳出模块" )
                                    now = datetime.datetime.now( )
                                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                                    cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ),
                                               nowtime,
                                               None )
                                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                                    return

                    else:
                        d( text="手机联系人", resourceId="com.tencent.tim:id/ivTitleBtnLeft",
                           className="android.widget.TextView" ).click( )
                index = index + 1
                obj = d( index=0, resourceId='com.tencent.tim:id/name', className='android.widget.AbsListView' ).child(
                    className="android.widget.LinearLayout", index=index ).child( text="添加", index=2 )
                num = 0
                continue
            d.dump( compressed=False )
            if d( text="风险提示" ).exists:  # 风险提示
                d( text="取消" ).click( )
                z.sleep( 1 )
                d( text="手机联系人", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click( )
                index = index + 1
                obj = d( index=0, resourceId='com.tencent.tim:id/name', className='android.widget.AbsListView' ).child(
                    className="android.widget.LinearLayout", index=index ).child( text="添加", index=2 )
                z.heartbeat( )
                num = 0
                continue
            obj = d( text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText' )  # 不需要验证可直接添加为好友的情况
            if obj.exists:
                z.sleep( 2 )
                obj.click( )
                if d( text='添加失败，请勿频繁操作', resourceId='com.tencent.tim:id/name' ).exists:
                    z.heartbeat( )
                    z.toast( "频繁操作,跳出模块" )
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                               None )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                else:
                    count = count + 1
                    print("请求发送成功")
                num = 0
                continue
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
            z.input( message )
            z.sleep( 1 )
            # d(index=2,className="android.widget.CompoundButton",resourceId="com.tencent.tim:id/name").click()
            if "是" in switch_card:
                if d( index=2, className="android.widget.CompoundButton", resourceId="com.tencent.tim:id/name" ).exists:
                    d( index=2, className="android.widget.CompoundButton",
                       resourceId="com.tencent.tim:id/name" ).click( )
                else:
                    if d( text="设置我的名片" ).exists:
                        d( text="设置我的名片" ).click( )
                        while True:
                            z.sleep( 1 )
                            z.heartbeat( )
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
            z.sleep( 1 )
            z.heartbeat( )
            d( text='下一步', resourceId='com.tencent.tim:id/ivTitleBtnRightText',
               className="android.widget.TextView" ).click( )
            z.sleep( 1 )
            if d( text='发送' ).exists:
                d( text='发送' ).click( )
                z.sleep(3)
                if d( text='发送' ).exists:
                    z.toast("无法添加")
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                               None )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
            if d( resourceId='com.tencent.tim:id/name', text='添加失败，请勿频繁操作' ).exists:  # 操作过于频繁的情况
                z.toast( "频繁操作,跳出模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                           None )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            # print( QQnumber + "请求发送成功" )
            num = 0
            z.heartbeat( )
            obj = d( index=0, resourceId='com.tencent.tim:id/name', className='android.widget.AbsListView' ).child(
                className="android.widget.LinearLayout", index=index ).child( text="添加", index=2 )
            count = count + 1
            if count == EndIndex:
                z.toast( "添加数量好友达到需求数量,停止模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                           None )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
            if num > 3:
                z.toast( "请求失败，无法添加，退出模块" )
                now = datetime.datetime.now( )
                nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                           None )
                z.toast( '模块结束，保存的时间是%s' % nowtime )
                return
        z.toast( "已无好友可加,停止模块！" )
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        cache.set( '%s_MMCTIMAdressAddfriends_time' % d.server.adb.device_serial( ), nowtime,
                   None )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        if (args["time_delay"]):
            time.sleep( int( args["time_delay"] ) )


def getPluginClass():
    return MMCTIMAdressAddfriends

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("HT524SK00685")
    z = ZDevice("HT524SK00685")
    nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )  # 当前时间
    thistimeH = int( nowTime[8:10] )
    thistimeM = int( nowTime[10:12] )
    thistimeH = thistimeH + thistimeM / 60
#     name = z.phoneToName('12345678910')
#     phone = z.nameToPhone(name)
#     pkg = 'com.tencent.mobileqq'
#     z.server.install()
#
#
#     slot = Slot('cda0ae8d', 'mobileqq')
#     print (slot.getSlots())
#     #slot.backup('1', 'slot_1')
#     #slot.restore('1')
#     print z.qq_getLoginStatus(d)
#     z.generate_serial('com.tencent.mobileqq')
#     print(z.get_serial(pkg))
#     info = '{"buildManufacturer":"ZTE","buildModel":"ZTE G720C","buildSerial":"ytz0fad63hkensm","buildVersionRelease":"Android 2.2.3","empty":false,"settingsSecureAndroidId":"wwx31wo6hhxbkrw","telephonyGetDeviceId":"864948416091531","telephonyGetLine1Number":"+8615015541026","telephonyGetNetworkType":"12","telephonyGetSimSerialNumber":"84508614357292636763","telephonyGetSubscriberId":"48313995020377949279","wifiInfoGetMacAddress":"00:03:6C:6B:B2:EA","wifiInfoGetSSID":"TP-ZPBZEBM7"}'
#     z.set_serial(pkg, info)
#     source = '/tmp/xxx.png'
#     d.screenshot(source)
#     width = 540.0
#     height = 960.0
#     p =  { "x1":37/width, "y1":380/height, "x2":502/width, "y2":473/height}
#     z.img_crop(source, p)
#
#     out = d.server.adb.run_cmd('shell', 'ls')
#     z.input("xxx")
# #    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").communicate()
#     z.server.install()
#
#     slot = Slot('cda0ae8d', 'mobileqq')
#     print (slot.getSlots())
#     slot.backup('21', '22221111')
#
#     print (slot.getSlots())
#     slot.clear('21')
#
#     z.generateSerial();
    #z.input("6565wv=1027&k=48KHKLm")


    #d.server.adb.cmd("shell", "am", "start", "-a", "zime.clear.contacts").communicate()
    # d.server.adb.cmd("shell", "pm clear com.android.providers.contacts").communicate()
    # #d.server.adb.cmd("push", filename, "/data/local/tmp/contacts.txt").communicate()
    # d.server.adb.cmd("shell", "am", "start", "-n", "com.zunyun.zime/.ImportActivity", "-t", "text/plain", "-d",
    #                  "/data/local/tmp/contacts.txt").communicate()

    # d.dump(compressed=False)

    args = {"repo_cate_id":"113",'number_count':'50',"random_name":"是","clear":"是","time_delay":"3","repo_material_id":"39","switch_card":"否",
            "EndIndex": "2","set_time":"100","startTime":"16","endTime":"10"}    #cate_id是仓库号，length是数量
    startTime = float( args["startTime"] )
    endTime = float( args["endTime"] )
    flag = True
    try:
        startTime = float( args["startTime"] )
        endTime = float( args["endTime"] )
        if startTime > endTime:
            if (thistimeH >= startTime and thistimeM<24) or thistimeH <= endTime:
                z.toast( "不在指定的时间内,不运行" )
                flag = False
        else:
            if thistimeH >= startTime and thistimeH <= endTime:
                z.toast( "不在指定的时间内,不运行" )
                flag = False
    except:
        z.toast( "设置的时间格式错误" )
        flag = False
    if flag:
        o.action( d, z, args )
