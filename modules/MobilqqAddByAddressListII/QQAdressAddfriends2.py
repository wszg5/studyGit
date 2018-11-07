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


class QQAdressAddfriends2:
    def __init__(self):
        self.repo = Repo()

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
            if isinstance(GetBindNumber, list) and GetBindNumber:
                GetBindNumber = GetBindNumber[0]
            elif GetBindNumber is None or GetBindNumber==[]:
                return 'false'
            if 'Session' in GetBindNumber:
                self.Bind(d, z)
            print(GetBindNumber)
            z.sleep( 2 )
            d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText' ).set_text(
                GetBindNumber )  # GetBindNumber
            z.heartbeat( )
            z.sleep( 1 )
            d( text='下一步' ).click( )
            z.sleep( 3 )
            while d(text="正在发送请求").exists:
                time.sleep(3)
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
        z.heartbeat( )
        z.toast( "准备执行QQ通讯录加好友+导入通讯录+多选" )
        z.toast("开始导入通讯录")
        self.getAddressList(d,z,args)
        z.heartbeat( )

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
        z.heartbeat( )
        cate_id = args["repo_material_id"]  # ------------------
        Material = self.repo.GetMaterial( cate_id, 0, 1 )
        if len( Material ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id ).communicate( )
            z.sleep( 10 )
            return
        message = Material[0]['content']  # 取出验证消息的内容

        z.heartbeat( )
        if d( text="联系人", resourceId="com.tencent.mobileqq:id/name" ).exists:
            d( text="联系人", resourceId="com.tencent.mobileqq:id/name" ).click( )
            time.sleep( 1 )
            d( text="添加", resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText" ).click( )
            time.sleep(1)
        d( text='添加手机联系人' ).click( )
        time.sleep(3)
        if d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',
              index=2 ).exists:  # 检查到尚未 启用通讯录
            if d( text=' +null', resourceId='com.tencent.mobileqq:id/name' ).exists:
                d( text=' +null', resourceId='com.tencent.mobileqq:id/name' ).click( )
                d( text='中国大陆', resourceId='com.tencent.mobileqq:id/name' ).click( )
            z.heartbeat( )
            text = self.Bind( d, z )  # 未开启通讯录的，现绑定通讯录
            z.heartbeat( )
            if text == 'false':  # 操作过于频繁的情况
                z.toast( '模块结束')
                return
            z.sleep( 7 )
        if d( textContains='没有可匹配的' ).exists:
            if d(text="返回",resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").exists:
                d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click()
                z.sleep(1)
                if d( text='添加手机联系人' ).exists:
                    d( text='添加手机联系人' ).click( )
                    z.sleep(1)
                    if d( textContains='没有可匹配的' ).exists:
                        if d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).exists:
                            d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click( )
                            z.sleep( 1 )
                            if d( text='添加手机联系人' ).exists:
                                d( text='添加手机联系人' ).click( )
                                z.sleep( 1 )
                                if d( textContains='没有可匹配的' ).exists:
                                    z.toast("显示不出来")
                                    return
        if d( text='匹配手机通讯录' ).exists:
            d( text='匹配手机通讯录' ).click( )
            while not d( text='多选' ).exists:
                z.sleep( 2 )
        z.heartbeat( )
        d( text='多选' ).click( )
        m = 0
        # while True:
            # if d( text='★' ).exists:
            #     z.heartbeat( )
            #     for m in range( 0, 12, +1 ):  # 快速加好友从#号下面的
            #         obj = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',index=m ).child(
            #             className='android.widget.TextView' ).info
            #         if obj['text'] == '★':
            #             break
            #         else:
            #             m = m + 1
            #             continue
            #
            #     break
            # else:  # 当前页没有找到＃时滑页
            #     d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
        z.heartbeat( )
        set1 = set( )
        i = m + 1
        t = 0
        EndIndex = int( args['EndIndex'] )  # ------------------
        while t < EndIndex:
            obj = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                     index=i )  # 滑动的条件
            if obj.exists:
                z.heartbeat( )
                obj1 = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                          index=i ) \
                    .child( className='android.widget.LinearLayout', index=2 ).child(
                    className='android.widget.TextView' )  # 第i个内容存在并且是人的情况
                if obj1.exists:
                    obj1 = obj1.info
                    phone = obj1['text']
                    if phone in set1:
                        i = i + 1
                        continue
                    else:
                        set1.add( phone )
                        print(phone)
                        obj5 = d( className='android.widget.AbsListView' ).child(
                            className='android.widget.LinearLayout', index=i ) \
                            .child( className='android.widget.FrameLayout' ).child( text='等待验证' )  # 验证已经发过的情况
                        if obj5.exists:
                            z.heartbeat( )
                            d( textContains='加好友' ).click( )
                            obj = d( className='android.widget.EditText' ).info  # 将之前消息框的内容删除
                            obj = obj['text']
                            lenth = len( obj )
                            mn = 0
                            while mn < lenth:
                                d.press.delete( )
                                mn = mn + 1
                            z.input( message )
                            d( text='发送' ).click( )
                            return
                        obj4 = d( className='android.widget.AbsListView' ).child(
                            className='android.widget.LinearLayout', index=i ).child(
                            className='android.widget.CheckBox' )  # 勾选框没被遮住的情况
                        if obj4.exists:
                            obj4.click( )
                        else:
                            d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                               index=i ).click( )
                        i = i + 1
                        t = t + 1
                        continue  # --------------------------------------------
                else:

                    i = i + 1
                    continue
            else:
                d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
                obj2 = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                          index=i ) \
                    .child( className='android.widget.LinearLayout', index=2 ).child(
                    className='android.widget.TextView' )  # 结束条件
                if obj2.exists:
                    obj2 = obj2.info
                else:
                    obj2 = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                              index=i-1 ) \
                        .child( className='android.widget.LinearLayout', index=2 ).child(
                        className='android.widget.TextView' )
                    if obj2.exists:
                        obj2 = obj2.info
                    else:
                        obj2 = d( className='android.widget.AbsListView' ).child(
                            className='android.widget.LinearLayout',
                            index=i - 2 ) \
                            .child( className='android.widget.LinearLayout', index=2 ).child(
                            className='android.widget.TextView' )
                        if obj2.exists:
                            obj2 = obj2.info
                        else:
                            i = 0
                            continue
                EndPhone = obj2['text']

                # obj2 = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                #                                                           index=i - 1 ) \
                #     .child( className='android.widget.LinearLayout', index=2 ).child(
                #     className='android.widget.TextView' )  # 结束条件
                # if obj2.exists:
                #     obj2 = obj2.info
                # else:
                #     obj2 = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                #                                                               index=i - 2 ) \
                #         .child( className='android.widget.LinearLayout', index=2 ).child(
                #         className='android.widget.TextView' ).info  # 结束条件
                # EndPhone = obj2['text']
                if EndPhone in set1:
                    z.heartbeat( )
                    d( textContains='加好友' ).click( )
                    obj = d( className='android.widget.EditText' ).info  # 将之前消息框的内容删除
                    obj = obj['text']
                    lenth = len( obj )
                    mn = 0
                    while mn < lenth:
                        d.press.delete( )
                        mn = mn + 1
                    z.input( message )
                    d( text='发送' ).click( )
                    return
                i = 0
                continue

        d( textContains='加好友' ).click( )
        obj = d( className='android.widget.EditText' ).info  # 将之前消息框的内容删除
        obj = obj['text']
        lenth = len( obj )
        mn = 0
        z.heartbeat( )
        while mn < lenth:
            d.press.delete( )
            mn = mn + 1
        z.input( message )
        d( text='发送' ).click( )
        while d( textContains='发送' ).exists:
            time.sleep( 2 )

        if (args["time_delay"]):
            z.sleep( int( args["time_delay"] ) )
        z.toast( "模块完成！" )


def getPluginClass():
    return QQAdressAddfriends2

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("cc0e9474")
    z = ZDevice("cc0e9474")

    args = {"repo_cate_id":"106",'number_count':'20',"random_name":"否","clear":"是","time_delay":"3","repo_material_id":"355",
            "EndIndex": "2"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
