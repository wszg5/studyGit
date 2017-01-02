# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random


class TIMAddressList:
    def __init__(self):
        self.repo = Repo()




    def action(self, d, args):
        cate_id = args["repo_material_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        wait = 1
        while wait == 1:
            try:
                Material = Material[0]['content']  # 从素材库取出的要发的材料
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到消息\"")

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        time.sleep(5)
        d(className='android.widget.TabWidget',resourceId='android:id/tabs',index=1).child(className='android.widget.FrameLayout',index=1).click()     #点击到联系人
        time.sleep(3)
        if d(text='联系人',resourceId='com.tencent.tim:id/ivTitleName').exists:       #如果已经到联系人界面
            time.sleep(1)
            if d(resourceId='com.tencent.tim:id/elv_buddies',className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=10).exists:  #看通讯录是否已经展开，已经展开的话直接滑动
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                # d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                # d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
            else:
                time.sleep(1)
                d(resourceId='com.tencent.tim:id/group_item_layout', index=8).click()    #未展开的情况，先点击展开
                if d(text='验证手机号码',resourceId='com.tencent.tim:id/ivTitleName').exists:      #判断手机是否启用通讯录
                    return
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                # d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                # d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)


        else:                                                                             #没有在联系人界面的话
            time.sleep(2)
            d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(
                className='android.widget.FrameLayout', index=1).click()  # 点击到联系人
            if d(resourceId='com.tencent.tim:id/elv_buddies',className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=10) .exists:    #看通讯录是否已经展开，已经展开的话直接滑动
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                # d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                # d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)

            else:
                time.sleep(1)
                d(resourceId='com.tencent.tim:id/group_item_layout', index=8).click()
                if d(text='验证手机号码', resourceId='com.tencent.tim:id/ivTitleName').exists:
                    return
                # d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                # d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)


        i = 1
        t = 1
        global list
        list = list()
        EndIndex = 5
        while t < EndIndex:
            time.sleep(2)
            obj = d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=i)  # 点击第ｉ个人
            if obj.exists:
                obj.click()
                time.sleep(2)
                obj = d(resourceId='com.tencent.tim:id/name', descriptionContains='昵称:')
                if obj.exists:
                    obj = obj.info
                    text = obj['text']
                    if obj in list:
                        continue
                    list.append(text)
                    d(resourceId='com.tencent.tim:id/txt', text='发消息').click()
                    time.sleep(2)
                    d(resourceId='com.tencent.tim:id/input', className='android.widget.EditText').set_text(Material.encode("utf-7"))  # Material
                    time.sleep(1)
                    d(resourceId='com.tencent.tim:id/fun_btn', text='发送').click()
                    i = i+1
                    t = t+1
                    d(resourceId='com.tencent.tim:id/ivTitleBtnLeft', description='返回消息界面').click()
                    d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(className='android.widget.FrameLayout', index=1).click()  # 点击到联系人
                else:
                    return
            else:
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                i = 1
                continue

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54WSK00081")
    args = {"repo_material_id":"33","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
