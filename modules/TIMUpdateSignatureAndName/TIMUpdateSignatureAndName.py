# coding=utf-8
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *


class TIMUpdateSignatureAndName:
    def __init__(self):
        self.repo = Repo( )

    def action(self, d, z, args):
        z.toast( "准备执行TIM修改个性签名和昵称模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM修改个性签名和昵称" )
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

        if d( text='消息' ).exists:  # 到了通讯录这步后看号有没有被冻结
            z.toast( "卡槽TIM状态正常，继续执行" )
        else:
            z.toast( "卡槽TIM状态异常，跳过此模块" )
            return
        z.heartbeat( )


        repo_key_word = args["repo_key_word"]
        MaterialKeyWord = self.repo.GetMaterial( repo_key_word, 0, 1 )
        keyWord = MaterialKeyWord[0]["content"]

        repo_cate_qq_id = args["repo_cate_qq_id"]
        # repo_cate_wx_id = args["repo_cate_wx_id"]
        #
        # if keyWord == "微信":
        #     numbers = self.repo.GetAccount( repo_cate_wx_id, 60, 1 )
        # else:
        #     numbers = self.repo.GetAccount( repo_cate_qq_id, 30, 1 )
        numbers = self.repo.GetAccount( repo_cate_qq_id, 30, 1 )
        if len( numbers ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"号码%s号仓库为空，等待中\"" % repo_cate_qq_id ).communicate( )
            return
        numbers = numbers[0]["number"]
        repo_name_id = args["repo_name_id"]
        MaterialName = self.repo.GetMaterial( repo_name_id, 0, 1 )
        if len( MaterialName ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_name_id ).communicate( )
            return
        name = MaterialName[0]['content']

        while True:
            if d( index=1, className='android.widget.ImageView' ).exists:
                z.heartbeat( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            if d( text="加好友" ).exists:  # 由于网速慢或手机卡可能误点
                d( text="加好友" ).click( )
                d( text="返回", className="android.widget.TextView" ).click( )
                d( index=2, className="android.widget.FrameLayout" ).child( index=0,
                                                                            className="android.widget.RelativeLayout" ).click( )
            z.sleep( 3 )
            if d( text='我的名片夹', resourceId='com.tencent.tim:id/name', className="android.widget.TextView" ).exists:
                z.heartbeat( )
                d( index=0, resourceId='com.tencent.tim:id/head', className="android.widget.ImageView" ).click( )
                break

        #修改个人签名
        d( text="个人签名" ).click( )
        obj = d( index=0, resourceId="com.tencent.tim:id/name", className="android.widget.EditText" )
        obj = obj.info["text"]
        if "+wx" in obj or "+口口" in obj:
            z.toast("个性签名符合要求，无需更改")
            d( text="完成" ).click( )
        else:  # 发送验证消息
            lenth = len( obj )
            t = 0
            while t < lenth:
                z.heartbeat( )
                d.press.delete( )
                t = t + 1
            time.sleep( 1 )
            z.sleep( 2 )
            z.heartbeat( )
            z.input( "你好!请加" + " +" + keyWord + ":" + numbers+"!　福利多多！！" )
            z.sleep( 1 )
            d( text="完成" ).click( )
        z.sleep(2)

        d( index=0, text="昵称" ).click( )
        obj = d( index=0, resourceId="com.tencent.tim:id/name", className="android.widget.EditText" )
        obj = obj.info["text"]
        if "+wx" in obj or "+口口" in obj:
            z.toast( "昵称符合要求，无需更改" )
            d( text="完成" ).click( )
        else:  # 发送验证消息
            d( descriptionContains="删除 按钮" ).click( )
            z.sleep( 2 )
            z.heartbeat( )
            z.input( name + " +" + keyWord + ":" + numbers )
            # z.input( name )
            z.sleep( 1 )
            d( text="完成" ).click( )
        z.sleep( 2 )
        d( text="返回", resourceId="com.tencent.tim:id/ivTitleBtnLeft" ).click( )


def getPluginClass():
    return TIMUpdateSignatureAndName


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
    # args = {"repo_name_id": "211", "repo_key_word": "212", "repo_cate_wx_id": "118","repo_cate_qq_id":"132"}
    args = {"repo_name_id": "211", "repo_key_word": "212", "repo_cate_qq_id": "132"}
    o.action( d, z, args )
