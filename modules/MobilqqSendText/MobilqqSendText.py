# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
import traceback
from PIL import Image
import colorsys

class MobilqqSendText:
    def __init__(self):
        self.repo = Repo()
        self.xuma = None

    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(6)
        if not d(text='消息', resourceId='com.tencent.mobileqq:id/name').exists:  # 到了通讯录这步后看号有没有被冻结
            return 2
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
            d(text='关闭').click()
            z.sleep(1)

        d(className='android.widget.TabWidget', resourceId='android:id/tabs').child(
            className='android.widget.FrameLayout').child(className='android.widget.RelativeLayout').click()  # 点击到联系人
        z.sleep(4)
        z.heartbeat()
        if d(text='主题装扮').exists:
            d(text='关闭').click()
        if d(text='马上绑定').exists:
            d(text='关闭').click()
        if d(text='通讯录').exists:
            d(text='关闭').click()

        if not d(text='联系人', resourceId='com.tencent.mobileqq:id/ivTitleName').exists:  # 如果没到联系人界面
            d(className='android.widget.TabWidget', resourceId='android:id/tabs').child(className='android.widget.FrameLayout').child(
                className='android.widget.RelativeLayout').click()  # 点击到联系人
            time.sleep(0.5)
        z.heartbeat()
        if not d(className='android.widget.LinearLayout',index=7).child(resourceId='com.tencent.mobileqq:id/text1',className='android.view.View',index=0).exists:   #好友已经展开的情况
            wait = 1
            while wait == 1:
                obj = d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.CheckBox',
                        checked='true')  # 看是否有展开的
                if obj.exists:
                    obj.click()  # 将展开的全部收起来
                    continue
                z.sleep(2)
                wait = 0
            d(resourceId='com.tencent.mobileqq:id/elv_buddies', className='android.widget.AbsListView').child(
                resourceId='com.tencent.mobileqq:id/group_item_layout', index=6).click()  # 将好友展开

        z.heartbeat()
        set1 = set()
        change = 0
        i = 7
        t = 1
        gg = 0
        EndIndex = int(args['EndIndex'])
        while t < EndIndex + 1:
            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                z.sleep(10)
                return
            message = Material[0]['content']  # 从素材库取出的要发的材料
            z.sleep(1)
            z.heartbeat()
            obj = d(resourceId='com.tencent.mobileqq:id/elv_buddies', className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=i).child(
                resourceId='com.tencent.mobileqq:id/name',index=0)  # 点击第ｉ个人
            z.sleep(1)
            if obj.exists:
                z.heartbeat()
                change = 1
                obj.click()
                if obj.exists:     #当第一次没点击上的话再次点击
                    obj.click()
                z.sleep(2)
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 3)     #滑动是为了将QQ号显示出来
                z.heartbeat()
                QQNumber = d(resourceId='com.tencent.mobileqq:id/info',className='android.widget.TextView',index=0)
                if QQNumber.exists:
                    QQNumber = QQNumber.info
                else:       #
                    z.sleep(2)
                    d.swipe(width / 2, height * 4 / 5, width / 2, height / 3)  # 上次滑动仍没显示QQ号的情况
                    QQNumber = d(resourceId='com.tencent.mobileqq:id/info', className='android.widget.TextView',index=0)
                    if QQNumber.exists:
                        QQNumber = QQNumber.info
                    elif d(text='帐号').exists:
                        QQNumber = d(text='帐号').right(className='android.widget.TextView').info
                    print('走里面了')
                z.heartbeat()
                QQNumber = QQNumber['text']  # 得到电话号码，并保存到set集合中成为唯一标识
                time.sleep(0.5)
                if QQNumber in set1:
                    d(textContains='返回').click()
                    i = i + 1
                    continue
                else:
                    set1.add(QQNumber)
                    print(QQNumber)
            else:
                if change == 0:  # 第一次滑动，开始ｉｎｄｅｘ不是通讯录里的人的时候，当点击开始发消息时将该值变为１
                    if gg==0:
                        i = i + 1
                        gg = 1
                        continue
                    else:
                        return
                else:

                    endCondition = d(className='android.widget.AbsListView').child(className='android.widget.FrameLayout',index=i)   #结束条件
                    if endCondition.exists:
                        return
                    d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)        #没到最后一个人，继续滑动发消息
                    z.sleep(5)
                    i = 2
                    continue
            z.heartbeat()
            time.sleep(0.5)
            d(text='发消息').click()
            z.sleep(1)

            d(className='android.widget.EditText').click()  # message
            z.input(message)
            z.sleep(1)
            d(resourceId='com.tencent.mobileqq:id/fun_btn', text='发送').click()
            i = i + 1
            t = t + 1
            z.heartbeat()
            if d(text='返回').exists:
                d(text='返回').click()
                d(text='返回').click()
                continue
            else:
                d(textContains='消息').click()


            d(className='android.widget.TabWidget', resourceId='android:id/tabs').child(
                className='android.widget.FrameLayout').child(
                className='android.widget.RelativeLayout').click()  # 发完消息后点击到联系人
            z.heartbeat()
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqSendText

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id":"39",'EndIndex':'30',"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)












