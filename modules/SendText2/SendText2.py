# coding:utf-8
from __future__ import division
import colorsys
import os
from PIL import Image
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice


class SendText:
    def __init__(self):
        self.repo = Repo( )
        self.xuma = None

    def action(self, d, z, args):
        count = args["count"]
        timeSleep = int(args["timeSleep"])
        # text = args["text"]
        # number = args["number"]
        # if d(index=1,className="android.widget.LinearLayout").child(index=1,resourceId="com.liyi.apps.sendgogo:id/editText1",className="android.widget.EditText").exists:
        # d( index=1, className="android.widget.LinearLayout" ).child( index=1, resourceId="com.liyi.apps.sendgogo:id/editText1", className="android.widget.EditText" ).click()
        # z.input(number)
        # # if d(index=1,className="android.widget.LinearLayout").child( index=3, resourceId="com.liyi.apps.sendgogo:id/editText2",className="android.widget.EditText" ).exists:
        # d( index=1, className="android.widget.LinearLayout" ).child( index=3, resourceId="com.liyi.apps.sendgogo:id/editText2",className="android.widget.EditText" ).click( )
        # z.input( text )
        # # if d(index=1,className="android.widget.LinearLayout").child( index=5, resourceId="com.liyi.apps.sendgogo:id/editText3",className="android.widget.EditText" ).exists:
        # d( index=1, className="android.widget.LinearLayout" ).child( index=5, resourceId="com.liyi.apps.sendgogo:id/editText3",className="android.widget.EditText" ).click( )
        # z.input( count )
        # d.dump( compressed=False )
        for i in range(0,int(count)):
            # if d(index=6,text="确定发送",resourceId="com.liyi.apps.sendgogo:id/button1",className="android.widget.Button").exists:
            d( index=6,text="确定发送", resourceId="com.liyi.apps.sendgogo:id/button1", className="android.widget.Button" ).click()
            z.heartbeat( )
            if timeSleep>3:
                time.sleep(timeSleep-3)
                z.heartbeat( )
            else:
                time.sleep(1)
                z.heartbeat( )



def getPluginClass():
    return SendText


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT524SK00685" )
    z = ZDevice( "HT524SK00685" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).communicate( )
    args = {"count":"10","timeSleep":"3"}  # cate_id是仓库号，length是数量
    o.action( d, z, args )
