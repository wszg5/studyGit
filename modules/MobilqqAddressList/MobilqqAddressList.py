# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
from XunMa import *


class TIMAddressList:
    def __init__(self):
        self.repo = Repo()
        self.xuma = XunMa()

    def Bind(self,d):

        newStart = 1
        while newStart == 1:
            token = self.xuma.GetToken()
            try:
                GetBindNumber = self.xuma.GetBindNumber(token)

            except Exception:
                continue

            print(GetBindNumber)
            time.sleep(2)
            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(GetBindNumber)

            time.sleep(1)
            d(text='下一步').click()
            time.sleep(2)
            if d(text='下一步',resourceId='com.tencent.mobileqq:id/name',index=2).exists:
                return 'false'

            if d(text='确定', resourceId='com.tencent.mobileqq:id/name', index='2').exists:
                d(text='确定', resourceId='com.tencent.mobileqq:id/name', index='2').click()

            try:
                code = self.xuma.GetBindCode(GetBindNumber, token)
                newStart = 0
            except Exception:
                d(text='返回',resourceId='com.tencent.mobileqq:id/ivTitleBtnLeftButton').click()
                d(className='android.view.View',descriptionContains='删除').click()
                continue
        d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(code)
        d(text='完成', resourceId='com.tencent.mobileqq:id/name').click()
        return 'true'



    def action(self, d,z, args):
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
        time.sleep(2)
        d(className='android.widget.TabWidget',resourceId='android:id/tabs',index=2).child(className='android.widget.FrameLayout').child(className='android.widget.RelativeLayout').click()     #点击到联系人
        time.sleep(3)
        if d(text='联系人',resourceId='com.tencent.mobileqq:id/ivTitleName').exists:       #如果已经到联系人界面

            wait = 1
            while wait == 1:
                obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.CheckBox',      #刚进联系人界面看是否有展开的列表
                        checked='true')  # 看是否有展开的
                if obj.exists:
                    obj.click()                     #将展开的全部收起来
                    continue
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)
                time.sleep(2)
                wait = 0

            time.sleep(2)
            wait1 = 1
            while wait1 == 1:
                obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.CheckBox',
                        checked='true')  # 防止有多列分组，滑动之后再看有没有展开的列表
                time.sleep(2)
                if obj.exists:
                    obj.click()
                    continue
                wait1 = 0

            for i in range(11, 1, -1):       #收起通讯录之后，再倒序确定通讯录的位置，点击展开并滑动，未绑定通讯录的
                if d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i).exists:
                    d(resourceId='com.tencent.mobileqq:id/elv_buddies', className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).click()
                    if d(resourceId='com.tencent.mobileqq:id/name',className='android.widget.EditText',index=2).exists:

                        text = self.Bind(d)                                 #未开启通讯录的，现绑定通讯录
                        if text=='false':
                            return

                        time.sleep(4)
                        d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).click()
                        time.sleep(1)
                    d.swipe(width / 2, height * 5 / 6, width / 2, height / 5)
                    break
                else:
                    continue


        else:                                                                             #没有在联系人界面的话
            d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=2).child(
                className='android.widget.FrameLayout').child(className='android.widget.RelativeLayout').click()  # 点击到联系人
            wait = 1
            while wait == 1:
                obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.CheckBox',
                        checked='true')  # 看是否有展开的
                if obj.exists:
                    obj.click()
                    continue
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 5)
                wait=0


            wait1 = 1
            while wait1 == 1:
                obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.CheckBox',
                        checked='true')  # 看是否有展开的
                if obj.exists:
                    obj.click()
                    continue
                wait1 = 0

            for i in range(12, 1, -1):
                if d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i).exists:
                    d(resourceId='com.tencent.mobileqq:id/elv_buddies', className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=i - 1).click()
                    d.swipe(width / 2, height * 5 / 6, width / 2, height / 5)
                    break
                else:
                    continue



        i = 1
        t = 1
        EndIndex = int(args['EndIndex'])
        while t < EndIndex:
            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            wait = 1
            while wait == 1:
                try:
                    Material = Material[0]['content']  # 从素材库取出的要发的材料
                    wait = 0
                except Exception:
                    d.server.adb.cmd("shell",
                                     "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到消息\"")
            time.sleep(2)

            obj = d(resourceId='com.tencent.mobileqq:id/elv_buddies',className='android.widget.AbsListView').child(resourceId='com.tencent.mobileqq:id/group_item_layout', index=8)
            if obj.exists and i == 8:  # 通讯录好友已经到底的情况
                return

            if i > 9:
                return

            obj = d(resourceId='com.tencent.mobileqq:id/elv_buddies',
                    className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',
                                                                  index=i).child(
                resourceId='com.tencent.mobileqq:id/text1', index=1)  # 点击第ｉ个人
            if obj.exists:
                obj.click()
                time.sleep(2)
            else:
                i = i + 1
                continue


            d(resourceId='com.tencent.mobileqq:id/txt', text='发消息').click()
            time.sleep(2)
            d(resourceId='com.tencent.mobileqq:id/input', className='android.widget.EditText').click()  # Material
            z.input(Material)
            time.sleep(1)
            d(resourceId='com.tencent.mobileqq:id/fun_btn', text='发送').click()
            i = i + 1
            t = t + 1
            d(resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft', description='返回消息界面').click()
            d(className='android.widget.TabWidget', resourceId='android:id/tabs', index=2).child(
                className='android.widget.FrameLayout', index=1).click()  # 点击到联系人



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    # print(d.dump(compressed=False))

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_material_id":"33",'EndIndex':'5',"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)
