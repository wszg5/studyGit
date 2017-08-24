# coding=utf-8
import colorsys
import os

from PIL import Image

from smsCode import smsCode
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *


class MobilqqUpdateName:
    def __init__(self):
        self.repo = Repo( )

    def action(self, d, z, args):
        z.toast( "准备执行QQ修改昵称(关键词)" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ修改昵称(关键词)" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text='消息' ).exists:  # 到了通讯录这步后看号有没有被冻结
            z.toast( "卡槽状态正常，继续执行" )
        else:
            z.toast( "卡槽状态异常，跳过此模块" )
            return
        z.heartbeat( )
        while True:                          #由于网速慢或手机卡可能误点
            z.heartbeat( )
            if d(index=1,className="android.widget.RelativeLayout").child( index=0, className='android.widget.Button',description="帐户及设置" ).exists:  # 点击ＱＱ头像.exists:
                z.sleep(1)
                z.heartbeat()
                d(index=1,className="android.widget.RelativeLayout").child( index=0, className='android.widget.Button',description="帐户及设置" ).click()
                z.heartbeat( )
                # d( resourceId="com.tencent.mobileqq:id/name", index=0,className='android.widget.RelativeLayout' ).child(
                #     index=0, className='android.widget.FrameLayout').child(resourceId="com.tencent.mobileqq:id/head", index=1,className='android.widget.ImageView').click( )  # 点击ＱＱ头像
                z.heartbeat( )
            if d( index=1, resourceId='com.tencent.mobileqq:id/head', className='android.widget.ImageView' ).exists:
                d( index=1, resourceId='com.tencent.mobileqq:id/head', className='android.widget.ImageView' ).click( )
                break
            if d(text="加好友").exists:    #由于网速慢或手机卡可能误点
                d(text="加好友").click()
                d(text="返回",className="android.widget.TextView").click()
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,className="android.widget.RelativeLayout" ).click( )
            z.sleep( 3 )

        # z.heartbeat( )
        # d( index=1, resourceId='com.tencent.mobileqq:id/head', className='android.widget.ImageView' ).click( )  # 再点击ＱＱ头像
        z.heartbeat( )
        d( text='编辑资料', resourceId='com.tencent.mobileqq:id/txt' ).click( )
        z.heartbeat( )
        d( index=1, resourceId='com.tencent.mobileqq:id/name',
           className='android.widget.EditText' ).click( )  # 点击昵称

        z.sleep( 1 )
        keyWordList = []
        while True:
            repo_key_word = args["repo_key_word"]
            MaterialKeyWord = self.repo.GetMaterial( repo_key_word, 0, 100 )
            for i in range( 0, 100 ):
                if i < len( MaterialKeyWord ):
                    keyWord = MaterialKeyWord[i]["content"]
                    keyWordList.append( keyWord )
                else:
                    break
            break
        num = random.randint( 0, len( keyWordList ) - 1 )
        obj = d( index=1, resourceId='com.tencent.mobileqq:id/name',className='android.widget.EditText' ).info["text"]
        repo_name_id = args["repo_name_id"]
        name = self.repo.GetMaterial( repo_name_id, 0, 1 )
        name_content = name[0]['content']
        oneclick = True
        z.heartbeat( )

        for item2 in keyWordList:
            if item2 in obj:
                z.toast( "昵称符合要求，无需更改" )
                print("昵称符合要求，无需更改,停止模块" )
                return
            else:  # 发送验证消息
                if item2==keyWordList[len(keyWordList)-1]:
                    break
                continue

        d( index=1, resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText' ).click( )
        obj = d( index=1, resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText' ).info
        obj = obj['text']
        lenth = len( obj )
        # d( index=1, resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText' ).clear_text( )
        oneclick = True
        t = 0
        while t < lenth:
            # z.heartbeat( )
            if t < lenth / 2:
                d.press.delete( )
                t = t + 1
            else:
                le = len(
                    d( index=1, resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText' ).info[
                        "text"] )
                d.press.delete( )  # 将昵称中的消息框的内容删除
                if len( d( index=1, resourceId='com.tencent.mobileqq:id/name',
                           className='android.widget.EditText' ).info[
                            "text"] ) < le:
                    t = t + 1
                else:
                    d( index=1, resourceId='com.tencent.mobileqq:id/name',className='android.widget.EditText' ).click( )
                    t = 0
                    lenth = len( d( index=1, resourceId='com.tencent.mobileqq:id/name',
                                    className='android.widget.EditText' ).info["text"] )
                    if obj == d( index=1, resourceId='com.tencent.mobileqq:id/name',
                                 className='android.widget.EditText' ).info["text"]:
                        break
        z.input(name_content)
        z.sleep( 1 )

        time.sleep( 1 )
        z.heartbeat( )
        d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click( )
        z.heartbeat( )
        # d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click( )
        # time.sleep( 2 )


def getPluginClass():
    return MobilqqUpdateName


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT54VSK01061" )
    z = ZDevice( "HT54VSK01061" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).wait( )
    args = {"repo_name_id": "211","repo_key_word": "212"}  # repo_name_id:QQ修改昵称仓库号，birthday_ xxx :年龄范围
    o.action( d, z, args )
    # a = o.WebViewBlankPages(d)
    # print(a)


