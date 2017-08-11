# coding=utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *


class TIMUpdateName:
    def __init__(self):
        self.repo = Repo( )

    def action(self, d, z, args):
        repo_cate_id = args["repo_cate_id"]
        numbers = self.repo.GetAccount( repo_cate_id, 30, 1 )
        if len( numbers ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"号码%s号仓库为空，等待中\"" % repo_cate_id ).communicate( )
            return
        numbers = numbers[0]["number"]
        repo_name_id = args["repo_name_id"]
        MaterialName = self.repo.GetMaterial( repo_name_id, 0, 1 )
        if len( MaterialName ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_name_id ).communicate( )
            return
        name = MaterialName[0]['content']
        repo_key_word = args["repo_key_word"]
        MaterialKeyWord = self.repo.GetMaterial( repo_key_word, 0, 1 )
        keyWord = MaterialKeyWord[0]["content"]

        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        z.sleep( 1 )
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )
        z.heartbeat( )
        z.sleep( 3 )

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
            if d( text='邮件').exists:
                z.heartbeat( )
                d(index=0, resourceId='com.tencent.tim:id/head',className="android.widget.ImageView" ).click( )
                break

        # d(index=0,resourceId="com.tencent.tim:id/name",className="android.widget.TextView").click()
        d(index=0,text="昵称").click()
        obj=d(index=0,resourceId="com.tencent.tim:id/name",className="android.widget.EditText")
        obj = obj.info["text"]
        if keyWord in obj:
            d(text="完成").click()
        else:                               # 发送验证消息
            d(descriptionContains="删除 按钮").click()
            z.sleep( 2 )
            z.heartbeat( )
            z.input(name+" +"+keyWord+":"+numbers)
            # z.input( name )
            z.sleep(1)
            d(text="完成").click()
        z.sleep(2)
        d(text="返回",resourceId="com.tencent.tim:id/ivTitleBtnLeft").click()




def getPluginClass():
    return TIMUpdateName


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
    args = {"repo_name_id": "211","repo_key_word":"212","repo_cate_id": "132"}  # repo_name_id:QQ修改昵称仓库号，birthday_ xxx :年龄范围
    o.action( d, z, args )

