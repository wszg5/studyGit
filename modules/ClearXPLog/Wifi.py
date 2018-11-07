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

import time


class Wifi:
    def __init__(self):

        self.repo = Repo()

    def adb_shell(self,adb):
        result = adb.run_cmd("shell", "ifconfig wlan0")
        # result = a.run_cmd( "shell", "reboot")
        # print result
        return str(result)

    def action(self, d, z, args):
        z.toast('执行检测是否连接wifi')
        serial = d.server.adb.device_serial( )
        adb = Adb( serial=serial )
        try:
            result = self.adb_shell(adb)
            if "output='wlan0" in result and 'ip' in result:
                z.toast(u'wifi 正常连接')
            else:
                z.toast( u'wifi 连接异常,3秒后重启' )
                time.sleep(3)
                adb.run_cmd( "shell", "reboot" )
                return

        except Exception as e:
            e = str(e)

            if 'timeout' in e:
                z.toast(u'执行adb命令超时，当成wifi异常，3秒后重启')
                time.sleep(3)
                adb.run_cmd( "shell", "reboot" )
                return
            else:
                z.toast(u'未知错误：%s' % e)

        z.toast( "模块完成" )
        return





def getPluginClass():
    return Wifi

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("37f7b82f")
    z = ZDevice("37f7b82f")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {}
    o.action(d, z, args)

    '''
    CmdReturn(output='gps       679   1     14908  1320  ffffffff b6f08a84 S /system/bin/xtwifi-inet-agent\r\n
    gps       681   1     12768  2156  ffffffff b6f21a84 S /system/bin/xtwifi-client\r\n', exit_code=0)



    CmdReturn(output='gps       679   1     14908  1320  ffffffff b6f08a84 S /system/bin/xtwifi-inet-agent\r\ngps       681   1     12768  2156  ffffffff b6f21a84 S /system/bin/xtwifi-client\r\nwifi      4359  1     7348   2616  ffffffff b6e89854 S /system/bin/wpa_supplicant\r\n', exit_code=0)

    CmdReturn(output='gps       679   1     14908  1320  ffffffff b6f08a84 S /system/bin/xtwifi-inet-agent\r\ngps       681   1     12768  2156  ffffffff b6f21a84 S /system/bin/xtwifi-client\r\nwifi      6364  1     7356   2596  ffffffff b6e21854 S /system/bin/wpa_supplicant\r\n', exit_code=0)
    '''