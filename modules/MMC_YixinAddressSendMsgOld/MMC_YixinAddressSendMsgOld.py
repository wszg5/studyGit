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


class MMCYixinAddressSendMsgOld:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def getAddressList(self, d,z, args,msgNum):
        z.heartbeat()
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        filename = os.path.join(base_dir, "%s.txt"%(self.GetUnique()) )

        number_count = msgNum
        cate_id = args["repo_cate_id"]
        while True:
            exist_numbers = self.repo.GetNumber(cate_id, 60, number_count, 'exist')
            print(exist_numbers)
            remain = number_count - len(exist_numbers)
            normal_numbers = self.repo.GetNumber(cate_id, 60, remain, 'normal',"NO")
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

            listNum = []
            for item in numbers:
                print item["number"]
                listNum.append(item["number"])

            out = d.server.adb.cmd("shell",
                               "dumpsys activity top  | grep ACTIVITY").communicate()[0].decode('utf-8')
            while out.find("com.zunyun.zime/.ImportActivity") > -1:
                z.heartbeat()
                out = d.server.adb.cmd("shell",
                                   "dumpsys activity top  | grep ACTIVITY").communicate()[0].decode('utf-8')
                z.sleep(5)

            return listNum
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

    def action(self, d, z,args):
        z.toast( "准备执行MMS版易信通讯录发短信旧版本" )
        # z.toast("先导入通信录")
        # numList = self.getAddressList(d,z,args)    #导入的通讯录
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：易信通讯录发短信旧版本" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop im.yixin" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell","am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        if d(textContains="停止运行").exists:
            if d(text="确定").exists:
                d( text="确定" ).click()
                d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
                z.sleep(5)
        z.heartbeat( )
        if d( text="我", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
            d( text="我", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
        else:
            if d(text="立即更新",resourceId="im.yixin:id/easy_dialog_positive_btn").exists:
                d( text="下次再说", resourceId="im.yixin:id/easy_dialog_negative_btn" ).click()
                z.toast( "登录状态正常" )
            else:
                z.toast( "登录状态异常" )
                return
        if d( text="立即更新", resourceId="im.yixin:id/easy_dialog_positive_btn" ).exists:
            d( text="下次再说", resourceId="im.yixin:id/easy_dialog_negative_btn" ).click( )
        if d(text="立即体验").exists:
            d( text="立即体验").click()
            z.sleep(1)

        msg = d( resourceId="im.yixin:id/my_free_services_root", className="android.widget.LinearLayout" ).child(index=2,className="android.widget.LinearLayout").child(
            index=1, resourceId="im.yixin:id/free_service_item_free_message" ).child( index=0,resourceId="im.yixin:id/root" ).child(
            index=0, resourceId="im.yixin:id/content_layout" ).child(
            index=1, resourceId="im.yixin:id/quotaTV" )

        msgNum = 0
        if msg.exists:
            try:
                msgNum = msg.info["text"].encode( "utf-8" )
                msgNum = int(msgNum)
                if msgNum == 0:
                    z.toast( "可能没有短信可发" )
                    return
            except:
                z.toast("可能没有短信可发")
                return
        if d(text="免费短信",resourceId="im.yixin:id/titleTV").exists:
            d( text="免费短信", resourceId="im.yixin:id/titleTV" ).click()
            if d( textContains="剩余", resourceId="im.yixin:id/quotaTV" ).exists:
                msgNum0 = d( textContains="剩余", resourceId="im.yixin:id/quotaTV" ).info["text"].encode( "utf-8" )
                msgNum = ""
                for i in msgNum0:
                    try:
                        b = int( i )
                    except:
                        continue
                    msgNum = msgNum + i
        try:
            msgNum = int( msgNum )
            if msgNum == 0:
                z.toast( "可能没有短信可发" )
                return
        except:
            z.toast( "可能没有短信可发" )
            return
        if d(text="好的",resourceId="im.yixin:id/free_service_detail_fineBtn").exists:
            d( text="好的", resourceId="im.yixin:id/free_service_detail_fineBtn" ).click()

        number_count  = int(args["number_count"])
        z.toast( "有短信可发消息" )
        if number_count > msgNum:
            z.toast( "今日短信还剩 %d ,所以只需导入%d 个到通信录"%(msgNum,msgNum) )
        else:
            z.toast("导入通讯录")
        numList = self.getAddressList( d, z, args,msgNum )  # 导入的通讯录
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        z.sleep(1)
        # if d( text="易信", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
        #     d( text="易信", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
        # z.sleep(1)
        if d(className="android.widget.TextView",resourceId="im.yixin:id/action_search").exists:
            d( className="android.widget.TextView", resourceId="im.yixin:id/action_search" ).click()
            if d(description="搜索查询",resourceId="im.yixin:id/search_src_text").exists:
                d( description="搜索查询", resourceId="im.yixin:id/search_src_text" ).click()
        num = 0
        for item in numList:
            if num == msgNum:
                z.toast("短信发完了")
                break
            z.heartbeat()
            if d(description="清除查询",resourceId="im.yixin:id/search_close_btn").exists:
                d( description="清除查询", resourceId="im.yixin:id/search_close_btn" ).click()
                z.sleep(1)
            else:
                if d( className="android.widget.TextView", resourceId="im.yixin:id/action_search" ).exists:
                    d( className="android.widget.TextView", resourceId="im.yixin:id/action_search" ).click( )
                    if d( description="搜索查询", resourceId="im.yixin:id/search_src_text" ).exists:
                        d( description="搜索查询", resourceId="im.yixin:id/search_src_text" ).click( )
            z.input( item )
            z.heartbeat()
            # if d( text="查找手机号", resourceId="im.yixin:id/lblNickname" ).exists:
                # d( text="查找手机号", resourceId="im.yixin:id/lblNickname" ).click( )
                # z.sleep( 3 )
                # if d( text="查找手机号", resourceId="im.yixin:id/lblNickname" ).exists:
            if d(text="本地通讯录",resourceId="im.yixin:id/lblNickname").exists:
                if d(index=2,className="android.widget.RelativeLayout").child(index=0,className="android.widget.RelativeLayout",resourceId="im.yixin:id/name_layout").child(text=item,resourceId="im.yixin:id/lblMaintel").exists:
                    d( index=2, className="android.widget.RelativeLayout" ).child( index=0,
                                                                                   className="android.widget.RelativeLayout",
                                                                                   resourceId="im.yixin:id/name_layout" ).child(
                        text=item, resourceId="im.yixin:id/lblMaintel" ).click()
                    z.heartbeat()
                    if d( text="加为好友", resourceId="im.yixin:id/yixin_profile_add" ).exists or d(text="发消息",resourceId="im.yixin:id/yixin_profile_buddy_talk_btn").exists:
                        if d(resourceId="im.yixin:id/mobile_entry_more",className="android.widget.ImageView").exists:
                            d( resourceId="im.yixin:id/mobile_entry_more", className="android.widget.ImageView" ).click()
                            if d(text="免费短信",resourceId='im.yixin:id/custom_dialog_text_view').exists:
                                d( text="免费短信", resourceId='im.yixin:id/custom_dialog_text_view' ).click()
                                if d( text="发送免费短信", resourceId='im.yixin:id/easy_dialog_positive_btn' ).exists:
                                    d( text="发送免费短信", resourceId='im.yixin:id/easy_dialog_positive_btn' ).click( )
                            if d(text="知道了",className="android.widget.Button").exists:
                                d( text="知道了", className="android.widget.Button" ).click()
                        else:
                            z.toast("无法发送短信给对方")
                            continue
            else:
                z.toast("没有导入通讯录")
                continue
            z.heartbeat()
            if d(resourceId="im.yixin:id/editTextSMS",textContains="发送到").exists:
                d( resourceId="im.yixin:id/editTextSMS", textContains="发送到" ).click()
                cate_id1 = args["repo_material_cate_id"]
                Material = self.repo.GetMaterial( cate_id1, 0, 1 )
                if len( Material ) == 0:
                    z.toast( "%s仓库为空" % cate_id1 )
                    return
                message = Material[0]['content']  # 取出验证消息的内容
                z.input( message )
                if d( text="发送", resourceId="im.yixin:id/buttonSendSMS" ).exists:
                    d( text="发送", resourceId="im.yixin:id/buttonSendSMS" ).click( )
                    z.sleep( 3 )
                    num = num + 1
                    # if d( text="发送", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).exists:
                    #     z.toast( "可能操作频繁了" )
                    #     break

                a = 0
                z.heartbeat()
                while not d(description="清除查询",resourceId="im.yixin:id/search_close_btn").exists and not d( text="消息", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
                    d.press.back()
                    z.sleep(2)
                    if a ==4:
                        z.toast("可能干猛了")
                        break
                    else:
                        a = a + 1
                # if d(description="清除查询",resourceId="im.yixin:id/search_close_btn").exists:
                #     d( description="清除查询", resourceId="im.yixin:id/search_close_btn" ).click()
                #     z.sleep(1)
                # else:
                #     if d( text="搜索", className="android.widget.TextView" ).exists:
                #         d( text="搜索", className="android.widget.TextView" ).click( )


        z.toast( "模块完成" )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCYixinAddressSendMsgOld

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("INNZL7YDLFPBNFN7")
    z = ZDevice("INNZL7YDLFPBNFN7")

    args = {"repo_cate_id":"104",'number_count':'20',"random_name":"否","clear":"是","time_delay":"3",
            "repo_material_cate_id":"255"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
