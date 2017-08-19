# coding:utf-8
import colorsys
import os

# from reportlab.graphics.shapes import Image
from PIL import Image

from smsCode import smsCode
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class QLAddFriendsByCard:
    def __init__(self):
        self.repo = Repo()



    def action(self, d,z,args):
        z.toast( "准备执行轻聊版唤醒名片加好友模块" )
        z.sleep(1)
        z.heartbeat( )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：轻聊版唤醒名片加好友" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.qqlite" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text='消息' ).exists:  # 到了通讯录这步后看号有没有被冻结
            z.toast( "卡槽状态正常，继续执行" )
        else:
            z.toast( "卡槽状态异常，跳过此模块" )
            return
        z.heartbeat()

        gender1 = args['gender']
        cate_id1 = args["repo_material_cate_id"]
        add_count = int(args['add_count'])  # 要添加多少人
        count = 0
        while count<add_count:            #总人数
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
            # print(QQnumber)
            z.sleep(2)

            z.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"'%QQnumber)  # qq名片页面
            # z.sleep(5)
            if d(text='QQ轻聊版').exists:
                z.heartbeat( )
                d(text='QQ轻聊版').click()
                z.sleep(2)
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()
                    z.heartbeat( )
            z.sleep(1)
            if d(text="消息").exists:
                continue
            z.heartbeat()
            if d(text="申请加群").exists:
                continue

            obj = d(index=1,resourceId="com.tencent.qqlite:id/0",className="android.widget.RelativeLayout").child(index=2,resourceId="com.tencent.qqlite:id/0",className="android.widget.TextView")
            if obj.exists:
                obj = obj.info
                gender2 = obj["text"][0:1]
            else:
                gender2 = "不限"

            if gender1 != '不限':
                z.heartbeat( )
                if gender1 == gender2:  # gender1是外界设定的，gender2是读取到的
                    z.sleep( 1 )
                else:
                    continue
            z.sleep(1)
            d.dump( compressed=False )
            d(text='加好友',className="android.widget.TextView").click()
            z.sleep(1)
            z.heartbeat()
            if d(text='加好友',className="android.widget.TextView").exists:    #拒绝被添加的轻况
                print("拒绝添加或请求失败")
                continue
            if d(text='必填').exists:                     #要回答问题的情况
                print("需要回答问题")
                z.heartbeat( )
                continue
            d.dump( compressed=False )
            if d(text="风险提示").exists:   #风险提示
                print( "该账号有风险" )
                z.heartbeat()
                continue
            obj = d( text='发送', resourceId='com.tencent.qqlite:id/ivTitleBtnRightText' )  # 不需要验证可直接添加为好友的情况
            if obj.exists:
                z.sleep( 2 )
                obj.click( )
                if d( text='添加失败，请勿频繁操作').exists:
                    z.heartbeat( )
                    z.toast( "频繁操作,跳出模块" )
                    print( "频繁操作,跳出模块" )
                    return
                else:
                    print( QQnumber + "请求发送成功" )
                continue
            d.dump( compressed=False )
            # obj = d(index=3, className='android.widget.EditText', resourceId='com.tencent.qqlite:id/name' ).info  # 将之前消息框的内容删除        需要发送验证信息
            obj = d(index=3,className="android.widget.EditText",resourceId="com.tencent.qqlite:id/0").info
            obj = obj['text']
            lenth = len( obj )
            t = 0
            while t < lenth:
                d.press.delete( )
                t = t + 1
            time.sleep( 1 )
            z.input(message)
            d(text='下一步',resourceId='com.tencent.qqlite:id/ivTitleBtnRightText').click()
            z.sleep( 1 )
            d(text='发送').click()
            if d(  text='添加失败，请勿频繁操作' ).exists:  # 操作过于频繁的情况
                z.toast("频繁操作,跳出模块")
                print("频繁操作,跳出模块")
                return
            print(QQnumber+"请求发送成功")
            z.heartbeat()
            count = count + 1
            if count == add_count:
                z.toast("加好友请求次数达到设定值，模块完成")
                break
        # z.toast("模块完成！")
        z.sleep(1)

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return QLAddFriendsByCard

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_cate_id":"119","repo_material_cate_id":"39",'gender':"男","add_count":"5","time_delay":"3"}

    o.action(d, z, args)