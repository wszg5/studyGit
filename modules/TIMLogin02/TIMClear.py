# coding:utf-8
import logging
from PIL import Image
from imageCode import imageCode
from smsCode import smsCode
from uiautomator import Device
import os
import util
from Repo import *
import time, datetime, random
from slot import Slot
from zservice import ZDevice
import colorsys
# from imageCode import imageCode
import base64


class TIMClear:

    def __init__(self):
        self.repo = Repo()

    def action(self,d,z,args):
        # z.toast("清空tim")
        # d.server.adb.cmd( "shell", "pm clear com.tencent.tim" ).communicate( )  # 清除缓存


        z.heartbeat( )
        z.toast('模块完成')


def getPluginClass():
    return TIMClear


if __name__ == "__main__":
    import sys
    reload( sys )
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT537SK00838")
    z = ZDevice("HT537SK00838")

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_cate_id": "264", "time_limit1": "120","time_delay1":"10","time_delay": "3","failCount":"3","random_code":"乱码"}  # cate_id是仓库号，length是数量
    o.action(d, z, args)
    # d.server.adb.cmd( "shell", "pm clear com.tencent.tim" ).communicate( )  # 清除缓存
    # d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
    # z.server.adb.run_cmd( "shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" )
    # serial = d.server.adb.device_serial( )
    # type = 'tim'
    # slot = Slot( serial, type )
    # d.server.adb.cmd( "shell", "pm clear com.tencent.mobileqq" ).communicate( )  # 清除缓存
    # slot.clear( "1" )
    # for i in range(2,20):
    #     slot.clear(i)
    #     print('已经清除')
    # print('全部清除')
