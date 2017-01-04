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
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        d(className='android.widget.TabWidget',resourceId='android:id/tabs',index=2).child(className='android.widget.FrameLayout',index=1).click()     #点击到联系人
        time.sleep(3)
        if d(text='联系人',resourceId='com.tencent.mobileqq:id/ivTitleName').exists:       #如果已经到联系人界面

            if d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=10).exists:  #看通讯录是否已经展开，已经展开的话直接滑动
                d.swipe(width / 2, height * 5/ 6, width / 2, height / 4)
            else:
                d(resourceId='com.tencent.mobileqq:id/group_item_layout', index=8).click()    #未展开的情况，先点击展开
                if d(text='验证手机号码',resourceId='com.tencent.mobileqq:id/ivTitleName').exists:      #判断手机是否启用通讯录
                    return
                # d.swipe(width / 2, height * 7 / 9, width / 2, height / 7)
                d.swipe(width / 2, height * 5/ 6, width / 2, height / 4)

        else:                                                                             #没有在联系人界面的话
            d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(
                className='android.widget.FrameLayout', index=1).click()  # 点击到联系人
            if d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=10) .exists:    #看通讯录是否已经展开，已经展开的话直接滑动
                d.swipe(width / 2, height * 5/ 6, width / 2, height / 4)
            else:
                d(resourceId='com.tencent.mobileqq:id/group_item_layout', index=8).click()
                if d(text='验证手机号码', resourceId='com.tencent.mobileqq:id/ivTitleName').exists:
                    return
                d.swipe(width / 2, height * 5/ 6, width / 2, height / 4)

        t = 8
        i = 8
        global list
        list = list()
        EndIndex = 20
        while t<EndIndex:
            if i<EndIndex:
                time.sleep(2)
                obj = d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i)
                if obj.exists:
                    obj.click()   #点击第ｉ个人
                    if d(text='加好友').exists:                    #到达通讯录的最后一个人
                        obj = d(resourceId='com.tencent.mobileqq:id/name',descriptionContains='昵称')
                        obj = obj.info
                        print(obj)
                        obj1 = obj["text"]  # 要保存到集合唯一标志
                        if obj1 in list:
                            i = i + 1
                            d(resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft', text='返回').click()
                            continue
                        else:
                            list.append(obj1)
                        d(resourceId='com.tencent.mobileqq:id/txt',text='发消息').click()
                        d(resourceId='com.tencent.mobileqq:id/input',className='android.widget.EditText').set_text('')#Material
                        time.sleep(1)
                        d(resourceId='com.tencent.mobileqq:id/fun_btn',text='发送').click()
                        t = t+1
                        i = i+1
                        d(resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft',description='返回消息界面').click()
                        d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=2).child(className='android.widget.FrameLayout', index=1).click()  # 点击到联系人
                    else:
                        return
                else:
                        d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                        i = 8
                        continue
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A3SK00853")
    args = {"repo_material_id":"8","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
