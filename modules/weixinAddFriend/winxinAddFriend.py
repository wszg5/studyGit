# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random


class ImpContact:
    def __init__(self):
        self.repo = Repo()




    def action(self, d, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()  # 将微信拉起来
        time.sleep(5)
        d(description='更多功能按钮',className='android.widget.RelativeLayout').click()
        time.sleep(1)
        if d(text='添加朋友',resourceId='com.tencent.mm:id/f6').exists:
            d(text='添加朋友', resourceId='com.tencent.mm:id/f6').click()
        else:
            d(resourceId='com.tencent.mm:id/f5',className='android.widget.ImageView').click()
            time.sleep(1)
            d(text='添加朋友', resourceId='com.tencent.mm:id/f6').click()
        d(resourceId='com.tencent.mm:id/gl',index='1',className='android.widget.TextView').click()
        d(text='搜索',resourceId='com.tencent.mm:id/gl').set_text('wxid_im6j00eq41y122')       #ccnn527xj
        d(resourceId='com.tencent.mm:id/hi',textContains='搜索:').click()

        # d(text='添加到通讯录',resourceId='com.tencent.mm:id/ab3').click()




def getPluginClass():
    return ImpContact

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AVSK01106")
    args = {"repo_cate_id":"131","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
