# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class TIMAddressList:
    def __init__(self):
        self.repo = Repo()




    def action(self, d, z,args):


        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(5)
        d(className='android.widget.TabWidget',resourceId='android:id/tabs',index=1).child(className='android.widget.FrameLayout',index=1).click()     #点击到联系人
        time.sleep(3)
        if d(text='联系人',resourceId='com.tencent.tim:id/ivTitleName').exists:       #如果已经到联系人界面

            obj =d(className='android.widget.AbsListView', index=1).child(index=8,resourceId='com.tencent.tim:id/group_item_layout').child(checked='false',resourceId='com.tencent.tim:id/name')
            if obj.exists:
                time.sleep(2)
                d(resourceId='com.tencent.tim:id/group_item_layout', index=8).click()  # 未展开的情况，先点击展开
                time.sleep(1)
                d.swipe(width / 2, height * 5/ 6, width / 2, height / 4)

            else:
                d.swipe(width / 2, height * 5/ 6, width / 2, height / 4)

        else:                                                                             #没有在联系人界面的话
            d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(className='android.widget.FrameLayout', index=1).click()  # 点击到联系人

            obj = d(className='android.widget.AbsListView', index=1).child(index=8,resourceId='com.tencent.tim:id/group_item_layout').child(checked='false', resourceId='com.tencent.tim:id/name')
            if obj.exists:
                d(resourceId='com.tencent.tim:id/group_item_layout', index=8).click()  # 未展开的情况，先点击展开
                d.swipe(width / 2, height * 5/ 6, width / 2, height / 4)
            else:
                d.swipe(width / 2, height * 5/ 6, width / 2, height / 4)

        i = 1
        t = 1
        EndIndex = int(args['EndIndex'])
        while t < EndIndex+1:
            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            wait = 1
            while wait == 1:
                try:
                    Material = Material[0]['content']  # 从素材库取出的要发的材料
                    wait = 0
                except Exception:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到消息\"").communicate()
                    time.sleep(30)

            time.sleep(2)
            obj = d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(resourceId='com.tencent.tim:id/group_item_layout',index=10)
            if obj.exists and i ==10:      #通讯录好友已经到底的情况
                return

            if i > 11:
                return

            obj = d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=i).child(resourceId='com.tencent.tim:id/text1',index=1)  # 点击第ｉ个人
            if obj.exists:
                obj.click()
                time.sleep(2)
            else:
                i = i+1
                continue



            d(resourceId='com.tencent.tim:id/txt', text='发消息').click()
            time.sleep(2)
            d(resourceId='com.tencent.tim:id/input', className='android.widget.EditText').click()  # Material
            z.input(Material)
            time.sleep(1)
            d(resourceId='com.tencent.tim:id/fun_btn', text='发送').click()
            i = i+1
            t = t+1
            d(resourceId='com.tencent.tim:id/ivTitleBtnLeft', description='返回消息界面').click()
            d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(className='android.widget.FrameLayout', index=1).click()  # 点击到联系人
            continue




        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")
    # print(d.dump(compressed=False))
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id":"39","time_delay":"3","EndIndex":"8"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)
