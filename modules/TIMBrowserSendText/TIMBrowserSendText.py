# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random


class TIMBrowserSendText:
    def __init__(self):
        self.repo = Repo()




    def action(self, d, args):
        totalNumber = 5
        d.server.adb.cmd("shell", "am force-stop com.android.chrome").wait()  # 强制停止
        for i in range (1,totalNumber,+1):
            d.server.adb.cmd("shell","am start -n com.android.chrome/com.google.android.apps.chrome.Main").wait()  # 拉起来
            time.sleep(3)
            d(className='android.widget.Button',index=2,description='清空号码').click()
            d(className='android.widget.EditText',index=1,clickable='false').click()
            d.press.back()
            d(className='android.widget.EditText',index=1,clickable='false').set_text("12357341")
            d(className='android.widget.Button',index=3,description='开始聊天').click()
            d(resourceId='com.tencent.tim:id/input',className='android.widget.EditText').set_text("1")
            d(text='发送',resourceId='com.tencent.tim:id/fun_btn').click()





def getPluginClass():
    return TIMBrowserSendText

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49YSK01576")
    args = {"repo_cate_id":"131","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
