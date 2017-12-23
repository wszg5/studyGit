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


class MMCYixinAppiontFriendsChatOld:
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

    def getAddressList(self, d,z, args):
        time_lock = int(args["time_lock"])
        z.heartbeat()
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        filename = os.path.join(base_dir, "%s.txt"%(self.GetUnique()) )

        number_count = int(args['number_count'])
        cate_id = args["repo_cate_id"]
        while True:
            exist_numbers = self.repo.GetNumber(cate_id, time_lock, number_count, 'exist')
            print(exist_numbers)
            remain = number_count - len(exist_numbers)
            normal_numbers = self.repo.GetNumber(cate_id, time_lock, remain, 'normal',"NO")
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

        sendTime = args["sendTime"]
        sendTime = sendTime.split( "-" )
        try:
            sendTimeStart = int( sendTime[0] )
            sendTimeEnd = int( sendTime[1] )
        except:
            z.toast( "发送时间间隔的参数格式有误" )
            return
        z.toast( "准备执行易信指定好友互聊旧版本" )
        z.toast("导入需要添加的好友至通讯录")
        numbers = self.getAddressList( d, z, args )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：易信指定好友互聊旧版本" )
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
        if d( text="消息", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
            # d( text="消息", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
        else:
            if d(text="立即更新",resourceId="im.yixin:id/easy_dialog_positive_btn").exists:
                d( text="下次再说", resourceId="im.yixin:id/easy_dialog_negative_btn" ).click()
                z.toast( "登录状态正常" )
            else:
                z.toast( "登录状态异常" )
                return
        if d( text="立即更新", resourceId="im.yixin:id/easy_dialog_positive_btn" ).exists:
            d( text="下次再说", resourceId="im.yixin:id/easy_dialog_negative_btn" ).click( )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        number_count = int(args["number_count"])
        megcount = int(args["megcount"])
        repo_cate_id = args["repo_cate_id"]
        repo_material_cate_id = args["repo_material_cate_id"]
        if d(className="android.widget.TextView",resourceId="im.yixin:id/action_search").exists:
            d( className="android.widget.TextView", resourceId="im.yixin:id/action_search" ).click()
            if d(description="搜索查询",resourceId="im.yixin:id/search_src_text").exists:
                d( description="搜索查询", resourceId="im.yixin:id/search_src_text" ).click()
        i = 0
        num = 0
        nameList = []
        random.shuffle( numbers )
        print numbers
        for item in numbers:
            if num == number_count:
                z.toast("数量达到设定的值了")
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

            if d(text="本地通讯录",resourceId="im.yixin:id/lblNickname").exists:
                if d( text="查找手机号", resourceId="im.yixin:id/lblNickname" ).exists:
                    d( text="查找手机号", resourceId="im.yixin:id/lblNickname" ).click( )
                    z.sleep( 3 )
                    if d( text="查找手机号", resourceId="im.yixin:id/lblNickname" ).exists:
                        z.toast( "用户不存在" )
                        continue
            else:
                z.toast("没有导入通讯录")
                continue
            z.heartbeat()
            # if d( text="本地通讯录", resourceId="im.yixin:id/lblNickname" ).exists:
            #     z.toast("对方没有开通易信")
            #     continue
            if d( text="加为好友", resourceId="im.yixin:id/yixin_profile_add" ).exists:
                d( text="加为好友", resourceId="im.yixin:id/yixin_profile_add" ).click( )
                z.sleep( 3 )
                if d( text="加为好友", resourceId="im.yixin:id/yixin_profile_add" ).exists:
                    z.toast("添加失败")
                    if not d( description="清除查询", resourceId="im.yixin:id/search_close_btn" ).exists:
                        d.press.back( )
                    continue
                if d( text="对方开启了好友验证，需要通过验证才能添加其为好友。", resourceId="im.yixin:id/easy_dialog_message_text_view" ).exists:
                    if d(text="取消",resourceId="im.yixin:id/easy_dialog_negative_btn").exists:
                        d( text="取消", resourceId="im.yixin:id/easy_dialog_negative_btn" ).click()
                        z.sleep(1)
                        d.press.back()
                        z.sleep(1)
                        if not d(description="清除查询",resourceId="im.yixin:id/search_close_btn").exists:
                            d.press.back()
                        continue

            z.heartbeat()
            if d(text="发消息",resourceId="im.yixin:id/yixin_profile_buddy_talk_btn").exists:
                d( text="发消息", resourceId="im.yixin:id/yixin_profile_buddy_talk_btn" ).click()
                if d(index=1,resourceId="im.yixin:id/editTextMessage",className="android.widget.EditText").exists:
                    d( index=1, resourceId="im.yixin:id/editTextMessage", className="android.widget.EditText" ).click()
                    for j in range( 0, random.randint( 1, megcount ) ):
                        Material = self.repo.GetMaterial( repo_material_cate_id, 0, 1 )
                        if len( Material ) == 0:
                            d.server.adb.cmd( "shell",
                                              "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % repo_material_cate_id ).communicate( )
                            z.sleep( 10 )
                            return
                        message = Material[0]['content']  # 取出发送消息的内容
                        z.input( message )
                        z.sleep( 1 )
                        if d(text="发送",resourceId="im.yixin:id/buttonSendMessage").exists:
                            d( text="发送", resourceId="im.yixin:id/buttonSendMessage" ).click()
                            z.sleep( random.randint( sendTimeStart, sendTimeEnd ) )
            else:
                z.toast("没有添加或发送按钮")

            a = 0
            z.heartbeat()
            while not d( description="清除查询", resourceId="im.yixin:id/search_close_btn" ).exists and not d(
                    text="消息", resourceId="im.yixin:id/tab_title_label",
                    className="android.widget.TextView" ).exists:
                d.press.back( )
                z.sleep( 2 )
                if a == 4:
                    z.toast( "可能干猛了" )
                    break
                else:
                    a = a + 1
            num = num + 1

        z.toast( "模块完成" )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCYixinAppiontFriendsChatOld

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")

    args = {"repo_cate_id":"278",'number_count':'8',"random_name":"否","clear":"是","time_delay":"3","set_timeStart":"0","set_timeEnd":"0","startTime":"0","endTime":"8",
            "repo_material_cate_id":"255","megcount":"1","sendTime":"2-3","time_lock":"60"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
