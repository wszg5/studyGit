# coding=utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *


class QQUpdateNameGenderBirthday:
    def __init__(self):
        self.repo = Repo( )

    def action(self, d, z, args):
        # for i in range(0,10):
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).wait( )  # 强制停止
        z.heartbeat( )
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).wait( )  # 将qq拉起来
        z.sleep(6)
        z.heartbeat( )
        while True:                          #由于网速慢或手机卡可能误点
            z.heartbeat( )
            if d(resourceId="com.tencent.mobileqq:id/conversation_head",index=0,className='android.widget.ImageView').exists:  # 点击ＱＱ头像.exists:
                # d(index=0,className="android.widget.RelativeLayout").child( index=1,resourceId="com.tencent.tim:id/name", className='android.widget.ImageView' ).click()
                z.heartbeat( )
                d( resourceId="com.tencent.mobileqq:id/conversation_head", index=0,className='android.widget.ImageView' ).click( )  # 点击ＱＱ头像
                z.heartbeat( )
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

        obj = d( index=1, resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText' ).info
        obj = obj['text']
        lenth = len( obj )
        t = 0
        while t < lenth:
            z.heartbeat( )
            d.press.delete( )  # 将昵称中的消息框的内容删除
            t = t + 1

        repo_name_id = args["repo_name_id"]
        name = self.repo.GetMaterial( repo_name_id, 0, 1 )
        name_content = name[0]['content']
        # d( className='android.widget.EditText', descriptionContains='昵称,编辑框,,' ).click()
        # d( text='昵称' ).click( )
        z.heartbeat( )
        z.input( name_content )

        # if random.randint( 0, 2 ) == 1:
        #     gender = "男"
        # else:
        #     gender = "女"
        z.heartbeat( )
        z.sleep(2)
        gender = args["gender"]

        # d(index=4,resourceId="com.tencent.mobileqq:id/name",className="android.widget.LinearLayout").child( text=gender,index=1,className="android.widget.TextView",resourceId="com.tencent.mobileqq:id/name" ).click( )
        d(text="性别").click()
        z.heartbeat( )
        d( text=gender).click( )

        d( index=2, text="完成", resourceId="com.tencent.mobileqq:id/name" ).click( )
        z.heartbeat( )
        d( index=5, resourceId='com.tencent.mobileqq:id/name', className='android.widget.LinearLayout' ).click( )

        birthday_start = int( args["birthday_start"] )
        birthday_end = int( args["birthday_end"] )
        randomYear = random.randint( birthday_start, birthday_end )
        while True:
            year = str( randomYear ) + "年"
            obj = d( className='android.widget.FrameLayout', index=1 ).child( className='android.widget.LinearLayout', index=1 ).child(
                className='android.view.View', resourceId='com.tencent.mobileqq:id/name', index=0 ).child(
                className='android.widget.TextView', text=year )
            if obj.exists:
                z.heartbeat( )
                obj.click( )
                yearNum = int( obj.info['text'][0:4] )
                break
            else:
                while True:
                    obj = d( className='android.widget.LinearLayout', index=1 ).child(
                        className='android.view.View', resourceId='com.tencent.mobileqq:id/name', index=0 ).child(
                        className='android.widget.TextView', index=3 )
                    yearNum = int( obj.info['text'][0:4] )
                    z.heartbeat( )
                    obj.click( )
                    if yearNum < randomYear:
                        while True:
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=0 ).child(
                                className='android.widget.TextView', index=6 )
                            z.heartbeat( )
                            obj.click( )
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=0 ).child(
                                className='android.widget.TextView', text=year )
                            if obj.exists:
                                z.heartbeat( )
                                obj.click( )
                                break
                    else:
                        while True:
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=0 ).child(
                                className='android.widget.TextView', index=0 )
                            z.heartbeat( )
                            obj.click( )
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=0 ).child(
                                className='android.widget.TextView', text=year )
                            if obj.exists:
                                z.heartbeat( )
                                obj.click( )
                                break

                    break

        randomMonth = random.randint( 1, 12 )
        while True:
            month = str( randomMonth ) + "月"
            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                className='android.view.View', resourceId='com.tencent.mobileqq:id/name', index=1 ).child(
                className='android.widget.TextView', text=month )
            if obj.exists:
                z.heartbeat( )
                obj.click( )
                monthNum = int( obj.info['text'][:-1] )
                break
            else:
                while True:
                    obj = d( className='android.widget.LinearLayout', index=1 ).child(
                        className='android.view.View', resourceId='com.tencent.mobileqq:id/name', index=1 ).child(
                        className='android.widget.TextView', index=3 )
                    z.heartbeat( )
                    obj.click( )
                    monthNum = int( obj.info['text'][:-1] )
                    obj.click( )
                    if monthNum < randomMonth:
                        while True:
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=1 ).child( className='android.widget.TextView', index=6 )
                            z.heartbeat( )
                            obj.click( )
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=1 ).child( className='android.widget.TextView', text=month )
                            if obj.exists:
                                z.heartbeat( )
                                obj.click( )
                                break
                    else:
                        while True:
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=1 ).child( className='android.widget.TextView', index=0 )
                            z.heartbeat( )
                            obj.click( )
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=1 ).child( className='android.widget.TextView', text=month )
                            if obj.exists:
                                z.heartbeat( )
                                obj.click( )

                                break

                    break
        randomDay = random.randint(0,28)
        if monthNum in [1, 3, 5, 7, 8, 10, 12]:
            randomDay = random.randint( 1, 31 )
        elif monthNum in [4, 6, 9, 11]:
            randomDay = random.randint( 1, 30 )
        if yearNum % 400 == 0 or yearNum % 4 == 0 and yearNum % 100 != 0:
            if monthNum == 2:
                randomDay = random.randint( 1, 29 )
        else:
            if monthNum == 2:
                randomDay = random.randint( 1, 28 )
        z.heartbeat( )
        while True:
            day = str( randomDay ) + "日"
            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                className='android.view.View', resourceId='com.tencent.mobileqq:id/name', index=2 ).child(
                className='android.widget.TextView', text=day )
            if obj.exists:
                z.heartbeat( )
                obj.click( )
                break
            else:
                while True:
                    obj = d( className='android.widget.LinearLayout', index=1 ).child(
                        className='android.view.View', resourceId='com.tencent.mobileqq:id/name', index=2 ).child(
                        className='android.widget.TextView', index=3 )
                    if obj.exists:
                        z.heartbeat( )
                        obj.click( )
                    dayNum = int( obj.info['text'][:-1] )
                    if dayNum < randomDay:
                        while True:
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=2 ).child(
                                className='android.widget.TextView', index=6 )
                            z.heartbeat( )
                            obj.click( )
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=2 ).child(
                                className='android.widget.TextView', text=day )
                            if obj.exists:
                                z.heartbeat( )
                                obj.click( )
                                break
                    else:
                        while True:
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=2 ).child(
                                className='android.widget.TextView', index=0 )
                            z.heartbeat( )
                            obj.click( )
                            obj = d( className='android.widget.LinearLayout', index=1 ).child(
                                className='android.view.View', resourceId='com.tencent.mobileqq:id/name',
                                index=2 ).child(
                                className='android.widget.TextView', text=day )
                            if obj.exists:
                                z.heartbeat( )
                                obj.click( )
                                break

                    break
        time.sleep( 1 )
        z.heartbeat( )
        d( index=2, text="完成", resourceId="com.tencent.mobileqq:id/name" ).click( )
        d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click( )
        z.heartbeat( )
        d( text="返回", resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click( )
        time.sleep( 2 )


def getPluginClass():
    return QQUpdateNameGenderBirthday


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT53XSK00427" )
    z = ZDevice( "HT53XSK00427" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).wait( )
    args = {"repo_name_id": "211", "birthday_start": "1980","birthday_end": "2000","gender":"男"}  # repo_name_id:QQ修改昵称仓库号，birthday_ xxx :年龄范围
    o.action( d, z, args )
