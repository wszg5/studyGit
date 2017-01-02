# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
# import httplib, json
# import urllib
import time
import re

class TIMLogin:
    def __init__(self):
        self.repo = Repo()



    def action(self, d, args):
        #
        # d.open.quick_settings()
        # d(text='飞行模式', resourceId='com.android.systemui:id/quick_setting_text').click()
        # if d(text='不要再显示此内容。',resourceId='android:id/text1').exists:
        #     d(text='不要再显示此内容。', resourceId='android:id/text1').click()
        #     d(text='确定').click()
        #     d.open.quick_settings()
        # time.sleep(1)
        # d(text='飞行模式',resourceId='com.android.systemui:id/quick_setting_text').click()

        d.server.adb.cmd("shell", "settings put global airplane_mode_on 1 ").wait()  # 打开飞行模式
        d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE –ez state true ").wait()  # 打开飞行模式

        d.server.adb.cmd("shell", "settings put global airplane_mode_on 0am broadcast -a android.intent.action.AIRPLANE_MODE –ez state false").wait()   #关闭飞行模式







def getPluginClass():
    return TIMLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A3SK00853")
    args = {"repo_cate_id":"131","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
