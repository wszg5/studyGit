# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
# import httplib, json
from zservice import ZDevice
import time
import re
from dbapi import *

class TIMLogin:
    def __init__(self):
        self.repo = Repo()
        self.dbapi = dbapi()



    def action(self, d,z, args):



        d.open.quick_settings()
        d(text='飞行模式').click()     #打开飞行开关
        time.sleep(2)
        if d(text='不要再显示此内容。',resourceId='android:id/text1').exists:
            d(text='不要再显示此内容。', resourceId='android:id/text1').click()
            d(text='确定').click()
            d.open.quick_settings()
            time.sleep(1)
            d(text='飞行模式').click()

        device = self.dbapi.GetDevice(d.server.adb.device_serial())
        obj = device["airplaneMode"]
        print(obj)
        on = 1
        while on==1:
            device = self.dbapi.GetDevice(d.server.adb.device_serial())
            obj = device["airplaneMode"]
            print(obj)
            if obj=='true':
                on = 0
            else:
                time.sleep(2)

        print(on)





def getPluginClass():
    return TIMLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT536SK01667")
    z = ZDevice("HT4AVSK01106")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_cate_id":"131","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)
