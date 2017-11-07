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


class MMCYixinAddNewFriends:
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
        z.toast( "准备执行MMS版易信加好友新朋友版模块" )
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
                z.toast( "网络通畅。开始执行：易信加好友版模块(新朋友)" )
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
        z.heartbeat( )
        if d( text="好友", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
            d( text="好友", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
        else:
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        if d(text="新的好友",resourceId="im.yixin:id/lblfuncname").exists:
            d( text="新的好友", resourceId="im.yixin:id/lblfuncname" ).click()
            z.sleep(1)
        add_count = int(args["add_count"])
        i = 0
        num = 0
        nameList = []
        while True:
            if num == add_count:
                z.toast("加的好友达到设定的值了")
                break
            obj = d(index=0,className="android.widget.ListView",resourceId="im.yixin:id/list").child(index=i,className="android.widget.RelativeLayout").child(
                index=2, className="android.widget.RelativeLayout", resourceId="im.yixin:id/add_states")
            objName =  d(index=0,className="android.widget.ListView",resourceId="im.yixin:id/list").child(index=i,className="android.widget.RelativeLayout").child(
                index=1, className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(index=0,resourceId="im.yixin:id/yixin_candidate_item_name")
            if objName.exists:
                name = objName.info["text"].encode("utf-8")
                if name in nameList:
                    i = i + 1
                    continue
                else:
                    nameList.append(name)
                    print name
            if obj.child(text="添加",resourceId="im.yixin:id/yixin_candidate_item_add").exists:
                obj.child( text="添加", resourceId="im.yixin:id/yixin_candidate_item_add" ).click()
                z.sleep(5)
                if d(text="发送验证申请等待对方通过",resourceId="im.yixin:id/add_friend_verify_content").exists:
                    d( text="发送验证申请等待对方通过", resourceId="im.yixin:id/add_friend_verify_content" ).click()
                    cate_id1 = args["repo_material_cate_id"]
                    Material = self.repo.GetMaterial( cate_id1, 0, 1 )
                    if len(Material)==0:
                        z.toast("%s仓库为空"%cate_id1)
                        now = datetime.datetime.now( )
                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                        z.setModuleLastRun( self.mid )
                        z.toast( '模块结束，保存的时间是%s' % nowtime )
                        return
                    message = Material[0]['content']  # 取出验证消息的内容
                    z.input(message)
                    if d(text="发送",resourceId="im.yixin:id/action_bar_right_clickable_textview").exists:
                        d( text="发送", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).click()
                        z.sleep(3)
                        if d( text="发送", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).exists:
                            z.toast("可能操作频繁了")
                            break

                num = num + 1
                z.sleep(1)
                i = i + 1
            elif obj.child(text="通过验证",resourceId="im.yixin:id/yixin_candidate_item_verify").exists:
                obj.child( text="通过验证", resourceId="im.yixin:id/yixin_candidate_item_verify" ).click( )
                i = i + 1
            elif obj.child(text="已添加",resourceId="im.yixin:id/yixin_candidate_item_added").exists:
                i = i + 1
            else:
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                if d(index=0,className="android.widget.ListView",resourceId="im.yixin:id/list").child(index=i,className="android.widget.RelativeLayout").child(
                index=1, className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(index=0,resourceId="im.yixin:id/yixin_candidate_item_name").exists:
                    name = d(index=0,className="android.widget.ListView",resourceId="im.yixin:id/list").child(index=i,className="android.widget.RelativeLayout").child(
                index=1, className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(index=0,resourceId="im.yixin:id/yixin_candidate_item_name").info["text"].encode( "utf-8" )
                    if name in nameList:
                        z.toast("到底了")
                        break
                else:
                    if d(index=0,className="android.widget.ListView",resourceId="im.yixin:id/list").child(index=i-1,className="android.widget.RelativeLayout").child(
                index=1, className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(index=0,resourceId="im.yixin:id/yixin_candidate_item_name").exists:
                        name = d(index=0,className="android.widget.ListView",resourceId="im.yixin:id/list").child(index=i-1,className="android.widget.RelativeLayout").child(
                index=1, className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(index=0,resourceId="im.yixin:id/yixin_candidate_item_name").info["text"].encode( "utf-8" )
                        if name in nameList:
                            z.toast( "到底了" )
                            break
                    else:
                        if d(index=0,className="android.widget.ListView",resourceId="im.yixin:id/list").child(index=i-2,className="android.widget.RelativeLayout").child(
                index=1, className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(index=0,resourceId="im.yixin:id/yixin_candidate_item_name").exists:
                            name = d(index=0,className="android.widget.ListView",resourceId="im.yixin:id/list").child(index=i-2,className="android.widget.RelativeLayout").child(
                index=1, className="android.widget.RelativeLayout").child(index=0,className="android.widget.LinearLayout").child(index=0,resourceId="im.yixin:id/yixin_candidate_item_name").info["text"].encode( "utf-8" )
                            if name in nameList:
                                z.toast( "到底了" )
                                break
                i = 1

        if d(text="清空",resourceId="im.yixin:id/action_bar_right_clickable_textview").exists:
            d( text="清空", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).click()
            z.sleep(1)

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCYixinAddNewFriends

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"repo_cate_id":"113",'number_count':'20',"random_name":"是","clear":"是","time_delay":"3","set_timeStart":"0","set_timeEnd":"0","startTime":"0","endTime":"8",
            "repo_material_cate_id":"255","add_count":"100"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
