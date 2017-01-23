# coding:utf-8
from RClient import *
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
from XunMa import *
import traceback
from PIL import Image
import colorsys
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MobilqqSendText:
    def __init__(self):
        self.repo = Repo()
        self.xuma = XunMa()

    def action(self, d,z, args):

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(6)
        if d(text='消息', resourceId='com.tencent.mobileqq:id/name').exists:  # 到了通讯录这步后看号有没有被冻结
            print
        else:
            return 2
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
            d(text='关闭').click()
            time.sleep(1)

        d(className='android.widget.TabWidget', resourceId='android:id/tabs').child(
            className='android.widget.FrameLayout').child(className='android.widget.RelativeLayout').click()  # 点击到联系人
        time.sleep(4)

        if d(text='主题装扮').exists:
            d(text='关闭').click()
        if d(text='马上绑定').exists:
            d(text='关闭').click()
        if d(text='通讯录').exists:
            d(text='关闭').click()

        if d(text='联系人', resourceId='com.tencent.mobileqq:id/ivTitleName').exists:  # 如果已经到联系人界面
            print
        else:
            d(className='android.widget.TabWidget', resourceId='android:id/tabs').child(className='android.widget.FrameLayout').child(
                className='android.widget.RelativeLayout').click()  # 点击到联系人
            time.sleep(0.5)

        if d(className='android.widget.LinearLayout',index=7).child(resourceId='com.tencent.mobileqq:id/text1',className='android.view.View',index=0).exists:   #好友已经展开的情况
            d.swipe(width / 2, height * 4 / 5, width / 2, height / 3)      #第一次滑动，将第一个人滑到靠上的位置
        else:
            wait = 1
            while wait == 1:
                obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.CheckBox',
                        checked='true')  # 看是否有展开的
                if obj.exists:
                    obj.click()  # 将展开的全部收起来
                    continue
                time.sleep(2)
                wait = 0
            d(resourceId='com.tencent.mobileqq:id/elv_buddies', className='android.widget.AbsListView').child(
                resourceId='com.tencent.mobileqq:id/group_item_layout', index=6).click()  # 将好友展开
            d.swipe(width / 2, height * 4 / 5, width / 2, height / 3)      #第一次滑动，将第一个人滑到靠上的位置


        set1 = set()
        change = 0
        i = 6
        t = 6
        EndIndex = int(args['EndIndex'])
        while t < EndIndex + 1:
            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            wait = 1
            while wait == 1:
                try:
                    Material = Material[0]['content']  # 从素材库取出的要发的材料
                    wait = 0
                except Exception:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
            time.sleep(1)
            obj1 = d(resourceId='com.tencent.mobileqq:id/elv_buddies', className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=i).child(
                resourceId='com.tencent.mobileqq:id/name',index=0)  # 点击第ｉ个人
            time.sleep(0.5)
            if obj1.exists:
                change = 1
                obj1.click()
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 3)     #滑动是为了将QQ号显示出来
                time.sleep(1)
                QQNumber = d(resourceId='com.tencent.mobileqq:id/info',className='android.widget.TextView',index=0).info
                QQNumber = QQNumber['text']  # 得到电话号码，并保存到set集合中成为唯一标识
                time.sleep(1)
                if QQNumber in set1:
                    d(textContains='返回').click()
                    i = i + 1
                    continue
                else:
                    set1.add(QQNumber)
                    print(QQNumber)
            else:
                if change == 0:  # 第一次滑动，开始ｉｎｄｅｘ不是通讯录里的人的时候，当点击开始发消息时将该值变为１
                    i = i + 1
                    continue
                else:
                    obj = d(resourceId='com.tencent.mobileqq:id/elv_buddies',
                            className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i).child(
                        className='android.widget.CheckBox')         #看是否滑到了最后一个人
                    if obj.exists:
                        return
                    d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)        #没到最后一个人，继续滑动发消息
                    time.sleep(2)
                    i = 2
                    continue

            d(resourceId='com.tencent.mobileqq:id/txt', text='发消息').click()
            time.sleep(1)

            d(resourceId='com.tencent.mobileqq:id/input', className='android.widget.EditText').click()  # Material
            # z.input(Material)
            time.sleep(1)
            d(resourceId='com.tencent.mobileqq:id/fun_btn', text='发送').click()
            i = i + 1
            t = t + 1
            d(resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft', textContains='消息').click()

            d(className='android.widget.TabWidget', resourceId='android:id/tabs').child(
                className='android.widget.FrameLayout').child(
                className='android.widget.RelativeLayout').click()  # 发完消息后点击到联系人

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqSendText

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")

    # obj = d(resourceId='com.tencent.mobileqq:id/elv_buddies', className='android.widget.AbsListView').child(
    #     className='android.widget.LinearLayout', index=2).child(
    #     resourceId='com.tencent.mobileqq:id/name', index=0)  # 点击第ｉ个人
    # obj.click()

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id":"37",'EndIndex':'30',"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)












