
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


class Ping:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum



    def action(self, d, z,args):

        z.toast( "准备执行ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while True:
            while i < 200:
                i += 1
                ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
                if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                    z.toast( "网络通畅。模块完成" )
                    return
                z.sleep( 1 )
            if i >= 200:
                z.toast( "网络不通，请检查网络状态,准备开关飞行模式重新ping" )
                d.server.adb.cmd( "shell", "settings put global airplane_mode_on 1" ).communicate( )
                d.server.adb.cmd( "shell",
                                  "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true" ).communicate( )
                z.sleep( 3 )
                d.server.adb.cmd( "shell", "settings put global airplane_mode_on 0" ).communicate( )
                d.server.adb.cmd( "shell",
                                  "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false" ).communicate( )
                if (args["time_delay"]):
                    z.sleep( int( args["time_delay"] ) )



def getPluginClass():
    return Ping

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("HT4AYSK00041")
    z = ZDevice("HT4AYSK00041")

    args = {"time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
