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
        count = int(args["count"])

        d( text="短信" ).click( )
        Str = d.info  # 获取屏幕大小等信息
        height = Str["displayHeight"]
        width = Str["displayWidth"]
        for i in range(1,count):
            # if d(text="短信").exists:
            z.input("1")
            # if d(resourceId="com.android.mms:id/send_button",className="android.widget.Button",description="发送短信").exists:
            # d( resourceId="com.android.mms:id/send_button", className="android.widget.Button",description="发送短信" ).click()
            d.click(673/720*width,1236/1280*height)

def getPluginClass():
    return SendText


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "cda0ae8d" )
    z = ZDevice( "cda0ae8d" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).communicate( )
    args = {"count":"10"};  # cate_id是仓库号，length是数量
    o.action( d, z, args )
