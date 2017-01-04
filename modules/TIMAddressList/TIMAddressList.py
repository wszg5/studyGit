# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class TIMAddressList:
    def __init__(self):
        self.repo = Repo()




    def action(self, d, z,args):
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
            time.sleep(2)
            d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=9).click()
            if d(text='发消息',resourceId='com.tencent.tim:id/txt').exists:                     #通讯录已经展开
                d(text='返回',resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
                time.sleep(1)
                # d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                time.sleep(2)
            else:
                d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=9).click()
                d(resourceId='com.tencent.tim:id/group_item_layout', index=8).click()  # 未展开的情况，先点击展开
                if d(text='验证手机号码', resourceId='com.tencent.tim:id/ivTitleName').exists:  # 判断手机是否启用通讯录
                    return
                else:
                    # d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                    d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                    d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                    time.sleep(2)

        else:                                                                             #没有在联系人界面的话
            d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(className='android.widget.FrameLayout', index=1).click()  # 点击到联系人
            time.sleep(2)
            d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(
                className='android.widget.RelativeLayout', index=9).click()
            if d(text='发消息', resourceId='com.tencent.tim:id/txt').exists:
                d(text='返回', resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
                # d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                time.sleep(2)
            else:
                d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(
                    className='android.widget.RelativeLayout', index=9).click()
                d(resourceId='com.tencent.tim:id/group_item_layout', index=8).click()  # 未展开的情况，先点击展开
                if d(text='验证手机号码', resourceId='com.tencent.tim:id/ivTitleName').exists:  # 判断手机是否启用通讯录
                    return
                else:
                    # d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                    d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                    d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                    time.sleep(2)
        i = 8
        t = 8
        global list
        list = dict()
        EndIndex = int(args['EndIndex'])
        while t < EndIndex:
            time.sleep(2)
            obj = d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(resourceId='com.tencent.tim:id/group_item_layout',index=10)
            if obj.exists and i ==10:      #通讯录好友已经到底的情况
                return
            obj = d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=i)  # 点击第ｉ个人

            if obj.exists:
                obj.click()
                # if d(text='我的电脑').exists:
                #     return

                time.sleep(2)
            else:
                i = i+1
                continue

            obj = d(resourceId='com.tencent.tim:id/name', descriptionContains='昵称:')
            if obj.exists:
                obj = obj.info
                text = obj['text']
                if obj in list:
                    i = i+1
                    continue
            else:
                obj = d(resourceId='com.tencent.tim:id/elv_buddies',className='android.widget.AbsListView',index=1).child(resourceId='com.tencent.tim:id/group_item_layout', index=8,clickable='true',className='android.widget.RelativeLayout')
                if obj.exists:
                    print(obj.info)
                    obj.click()  # 未展开的情况，先点击展开
                    # d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                    d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                    d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
                    i = i+1
                    continue
                else:
                    i = i+1
                    continue


            list.append(text)
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


            #     d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=1).child(className='android.widget.FrameLayout', index=1).click()  # 点击到联系人
            # else:
            #     return
            # elif d(resourceId='com.tencent.tim:id/elv_buddies', className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=i+1).exists:
            #
            #     # d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
            #     d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
            #     d.swipe(width / 2, height * 3 / 5, width / 2, height / 4)
            #     i = 1
            #     time.sleep(3)
            #     continue

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT536SK01667")
    z = ZDevice("HT536SK01667")
    # print(d.dump(compressed=False))
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_material_id":"33","time_delay":"3","EndIndex":"20"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)
