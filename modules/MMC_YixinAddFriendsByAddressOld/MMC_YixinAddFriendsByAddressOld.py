# coding:utf-8
from __future__ import division
import base64
import logging
import re

from uiautomator import Device
from Repo import *
import os, time, datetime, random
import json

from zcache import cache
from zservice import ZDevice


class MMCYixinAddFriendsByAddressOld:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

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


    def action(self, d, z,args):
        z.toast( "准备执行MMS版易信通讯录加好友模块旧版本" )
        z.sleep( 1 )
        z.toast( "开始导入通讯录" )
        self.getAddressList( d, z, args )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：易信加好友版模块(通讯录旧版本)" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        d.server.adb.cmd( "shell", "am force-stop im.yixin" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        if d(textContains="停止运行").exists:
            if d(text="确定").exists:
                d( text="确定" ).click()
                d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
                z.sleep(5)
        z.heartbeat( )
        if d( text="消息", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
            # d( text="消息", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
        else:
            if d( text="立即更新", resourceId="im.yixin:id/easy_dialog_positive_btn" ).exists:
                d( text="下次再说", resourceId="im.yixin:id/easy_dialog_negative_btn" ).click( )
                z.toast( "登录状态正常" )
            else:
                z.toast( "登录状态异常" )
                return
        if d( text="立即更新", resourceId="im.yixin:id/easy_dialog_positive_btn" ).exists:
            d( text="下次再说", resourceId="im.yixin:id/easy_dialog_negative_btn" ).click( )
            z.sleep(2)
        if d( text="通讯录", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            d( text="通讯录", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
            z.sleep(0.5)
        if d(text="立即体验").exists:
            d( text="立即体验").click()
            z.sleep(1)
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        if d(text="添加好友",resourceId="im.yixin:id/lblfuncname").exists:
            d( text="添加好友", resourceId="im.yixin:id/lblfuncname" ).click()
            z.sleep(1)
        else:
            if d( text="通讯录", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
                d( text="通讯录", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click( )
                z.sleep( 0.5 )
            if d( text="添加好友", resourceId="im.yixin:id/lblfuncname" ).exists:
                d( text="添加好友", resourceId="im.yixin:id/lblfuncname" ).click( )
                z.sleep( 1 )
        if d(text="从手机通讯录添加",className="android.widget.TextView").exists:
            d( text="从手机通讯录添加",className="android.widget.TextView" ).click()
            z.sleep(2)
        else:
            z.toast("不太正常,先跳出")

        add_count = int(args["add_count"])
        i = 0
        num = 0
        nameList = []
        while True:
            if num == add_count:
                z.toast("加的好友达到设定的值了")
                break

            obj = d( index=0, className="android.widget.ListView", resourceId="im.yixin:id/lvContacts" ).child( index=i,className="android.widget.LinearLayout",resourceId="im.yixin:id/listItemLayout" )

            objName = obj.child(index=0,className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(
                index=0,resourceId="im.yixin:id/contact_item_nick_name")
            z.heartbeat()
            if not obj.exists and d( index=0, className="android.widget.ListView", resourceId="im.yixin:id/lvContacts" ).child( index=i,className="android.widget.RelativeLayout" ).exists:
                i = i + 1
                continue
            elif obj.exists:
                if objName.exists:
                    name = objName.info["text"].encode("utf-8")
                    if name in nameList:
                        i = i + 1
                        continue
                    else:
                        nameList.append( name )
                        print name
                z.heartbeat( )
                if obj.child(index=0,className="android.widget.RelativeLayout").child(index=1,className="android.widget.LinearLayout",resourceId="im.yixin:id/invite_layout_id").child(text="添加",resourceId="im.yixin:id/contact_item_function_btn").exists:
                    obj.child( index=0, className="android.widget.RelativeLayout" ).child( index=1,
                                                                                           className="android.widget.LinearLayout",
                                                                                           resourceId="im.yixin:id/invite_layout_id" ).child(
                        text="添加", resourceId="im.yixin:id/contact_item_function_btn" ).click()
                    z.sleep( 5 )
                    if d( text="发送验证申请等待对方通过", resourceId="im.yixin:id/add_friend_verify_content" ).exists:
                        d( text="发送验证申请等待对方通过", resourceId="im.yixin:id/add_friend_verify_content" ).click( )
                        cate_id1 = args["repo_material_cate_id"]
                        Material = self.repo.GetMaterial( cate_id1, 0, 1 )
                        if len( Material ) == 0:
                            z.toast( "%s仓库为空" % cate_id1 )
                            return
                        message = Material[0]['content']  # 取出验证消息的内容
                        z.input( message )
                        if d( text="发送", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).exists:
                            d( text="发送", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).click( )
                            z.sleep( 3 )
                            if d( text="发送", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).exists:
                                z.toast( "可能操作频繁了" )
                                break
                        i = i + 1

                    num = num + 1


                # elif obj.child(index=0,className="android.widget.RelativeLayout").child(index=1,className="android.widget.LinearLayout",resourceId="im.yixin:id/invite_layout_id").child(text="邀请",resourceId="im.yixin:id/contact_item_tip_view").exists:
                #     i = i + 1
                #     continue
                else:
                    z.heartbeat( )
                    if obj.child(index=0,className="android.widget.RelativeLayout").child(index=1,className="android.widget.LinearLayout",resourceId="im.yixin:id/invite_layout_id").child(text="邀请",resourceId="im.yixin:id/contact_item_tip_view").exists:
                        z.toast("底下的都是邀请,没有添加了")
                        break
                    if obj.child( index=0, className="android.widget.RelativeLayout" ).child( index=1,className="android.widget.LinearLayout",resourceId="im.yixin:id/invite_layout_id" ).child(
                            text="已添加", resourceId="im.yixin:id/contact_item_tip_view" ).exists:
                        z.toast( "底下的都是已添加,没有添加了" )
                        break
                    i = i + 1
                    continue
            else:
                z.heartbeat( )
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                # if d( index=0, className="android.widget.ListView", resourceId="im.yixin:id/lvContacts" ).child( index=i,className="android.widget.LinearLayout",resourceId="im.yixin:id/listItemLayout" ).child(index=0,className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(
                # index=0,resourceId="im.yixin:id/contact_item_nick_name").exists:
                #     name = d( index=0, className="android.widget.ListView", resourceId="im.yixin:id/lvContacts" ).child( index=i,className="android.widget.LinearLayout",resourceId="im.yixin:id/listItemLayout" ).child(index=0,className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(
                # index=0,resourceId="im.yixin:id/contact_item_nick_name").info["text"].encode( "utf-8" )
                #     if name in nameList:
                #         z.toast( "到底了" )
                #         break
                # else:
                #     if d( index=0, className="android.widget.ListView", resourceId="im.yixin:id/lvContacts" ).child( index=i-1,className="android.widget.LinearLayout",resourceId="im.yixin:id/listItemLayout" ).child(index=0,className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(
                # index=0,resourceId="im.yixin:id/contact_item_nick_name").exists:
                #         name = d( index=0, className="android.widget.ListView", resourceId="im.yixin:id/lvContacts" ).child( index=i-1,className="android.widget.LinearLayout",resourceId="im.yixin:id/listItemLayout" ).child(index=0,className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(
                # index=0,resourceId="im.yixin:id/contact_item_nick_name").info["text"].encode( "utf-8" )
                #         if name in nameList:
                #             z.toast( "到底了" )
                #             break
                #     else:
                #         if d( index=0, className="android.widget.ListView", resourceId="im.yixin:id/lvContacts" ).child( index=i-2,className="android.widget.LinearLayout",resourceId="im.yixin:id/listItemLayout" ).child(index=0,className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(
                # index=0,resourceId="im.yixin:id/contact_item_nick_name").exists:
                #             name = d( index=0, className="android.widget.ListView", resourceId="im.yixin:id/lvContacts" ).child( index=i-2,className="android.widget.LinearLayout",resourceId="im.yixin:id/listItemLayout" ).child(index=0,className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(
                # index=0,resourceId="im.yixin:id/contact_item_nick_name").info["text"].encode(
                #                 "utf-8" )
                #             if name in nameList:
                #                 z.toast( "到底了" )
                #                 break
                i = 1
        z.toast("模块完成")
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCYixinAddFriendsByAddressOld

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("INNZL7YDLFPBNFN7")
    z = ZDevice("INNZL7YDLFPBNFN7")

    args = {"repo_cate_id":"104",'number_count':'30',"random_name":"否","clear":"是","time_delay":"3",
            "repo_material_cate_id":"255","add_count":"30"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
