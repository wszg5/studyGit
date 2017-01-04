# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random


class TIMAddressList:
    def __init__(self):
        self.repo = Repo()




    def action(self, d, args):
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        time.sleep(5)
        d(className='android.widget.TabWidget',resourceId='android:id/tabs',index=1).child(className='android.widget.FrameLayout',index=1).click()     #点击到联系人
        time.sleep(3)
        if d(text='联系人',resourceId='com.tencent.tim:id/ivTitleName').exists:       #如果已经到联系人界面

            if d(resourceId='com.tencent.tim:id/elv_buddies',className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=10).exists:  #看通讯录是否已经展开，已经展开的话直接滑动
                d.swipe(width / 2, height * 7 / 9, width / 2, height / 5)
            else:
                d(resourceId='com.tencent.tim:id/group_item_layout', index=8).click()    #未展开的情况
                if d(text='验证手机号码',resourceId='com.tencent.tim:id/ivTitleName').exists:      #判断手机是否启用通讯录
                    return
                d.swipe(width / 2, height * 7 / 9, width / 2, height / 5)

        else:                                                                             #没有在联系人界面的话
            d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(
                className='android.widget.FrameLayout', index=1).click()  # 点击到联系人
            if d(resourceId='com.tencent.tim:id/elv_buddies',className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=10) .exists:    #看通讯录是否已经展开，已经展开的话直接滑动
                d.swipe(width / 2, height * 7 / 9, width / 2, height / 5)
            else:
                d(resourceId='com.tencent.tim:id/group_item_layout', index=8).click()
                if d(text='验证手机号码', resourceId='com.tencent.tim:id/ivTitleName').exists:
                    return
                d.swipe(width / 2, height * 7 / 9, width / 2, height / 5)

        for i in range(1,6,+1):
            time.sleep(2)
            d(resourceId='com.tencent.tim:id/elv_buddies',className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i).click()   #点击第ｉ个人
            d(resourceId='com.tencent.tim:id/txt',text='发消息').click()
            d(resourceId='com.tencent.tim:id/input',className='android.widget.EditText').set_text("1234")
            time.sleep(1)
            d(resourceId='com.tencent.tim:id/fun_btn',text='发送').click()
            d(resourceId='com.tencent.tim:id/ivTitleBtnLeft',description='返回消息界面').click()
            d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(
                className='android.widget.FrameLayout', index=1).click()  # 点击到联系人












def getPluginClass():
    return TIMAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A3SK00853")
    args = {"repo_cate_id":"131","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
