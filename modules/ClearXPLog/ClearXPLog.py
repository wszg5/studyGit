# coding:utf-8
from __future__ import division

import os
import random

from smsCode import smsCode
import string
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice
from adb import Adb

class ClearXPLog:
    def __init__(self):

        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )

    def action(self, d, z, args):
        time_delay = int( args["time_delay"] )
        run_time = float( time_delay )
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return

        serial = d.server.adb.device_serial( )
        a = Adb( serial=serial )
        path = "/data/data/de.robv.android.xposed.installer/log/error.log"
        a.run_cmd( "shell", "su -c 'rm -r -f %s'" % path )
        path = "/data/data/de.robv.android.xposed.installer/log/error.log.old"
        a.run_cmd( "shell", "su -c 'rm -r -f %s'" % path )

        z.toast( "模块完成" )
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        # z.toast( '模块结束,保存的时间是%s' % nowtime )
        return





def getPluginClass():
    return ClearXPLog

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT536SK01664")
    z = ZDevice("3c454f7f")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"time_delay": "1440"}


    # o.action(d, z, args)
    serial = d.server.adb.device_serial( )
    a = Adb( serial=serial )
    result = a.run_cmd( "shell", "ps|grep wifi")
    # result = a.run_cmd( "shell", "reboot")
    print result
'''
CmdReturn(output='gps       680   1     14908  1224  ffffffff b6ec7a84 S /system/bin/xtwifi-inet-agent
gps       683   1     12768  1980  ffffffff b6e7da84 S /system/bin/xtwifi-client\r\n', exit_code=0)

CmdReturn(output='gps       680   1     14908  1224  ffffffff b6ec7a84 S /system/bin/xtwifi-inet-agent\r\n
gps       683   1     12768  1980  ffffffff b6e7da84 S /system/bin/xtwifi-client\r\n
wifi      6976  1     7352   2624  ffffffff b6de8854 S /system/bin/wpa_supplicant\r\n', exit_code=0)

CmdReturn(output='wifi      1273  1     3804   1828  ffffffff 00000000 S /system/bin/wpa_supplicant\r\n', exit_code=0)

CmdReturn(output='gps       695   1     14908  1200  ffffffff b6f53a84 S /system/bin/xtwifi-inet-agent\r\n
gps       697   1     12768  1956  ffffffff b6e8ea84 S /system/bin/xtwifi-client\r\n
wifi      1570  1     7352   2264  ffffffff b6e3d854 S /system/bin/wpa_supplicant\r\n', exit_code=0)


'''