# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class MobilqqAddByAddressListII:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(6)
        cate_id = args["repo_material_id"]  # ------------------
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        try:
            Material = Material[0]['content']  # 从素材库取出的要发的材料
            wait = 0
        except Exception:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()

        if d(text='消息', resourceId='com.tencent.mobileqq:id/name').exists:  # 到了通讯录这步后看号有没有被冻结
            print
        else:
            return 2
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
            d(text='关闭').click()
            time.sleep(1)
        if d(text='主题装扮').exists:
            d(text='关闭').click()
        if d(text='马上绑定').exists:
            d(text='关闭').click()
        if d(text='通讯录').exists:
            d(text='关闭').click()
        d(description='快捷入口').click()
        d(textContains='加好友').click()
        d(text='添加手机联系人').click()
        d(text='多选').click()

        while True:
            if d(text='#').exists:
                for m in range(0,12,+1):
                    obj = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',
                                                                          index=m).child(className='android.widget.TextView').info
                    if obj['text']=='#':
                        break
                    else:
                        m = m+1
                        continue

                break
            else:
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)
        set1 = set()
        i = m+1
        t = 0
        EndIndex = int(args['EndIndex'])         #------------------
        while t < EndIndex :
            obj = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i)  #滑动的条件
            if obj.exists:
                obj1 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=i)\
                    .child(className='android.widget.LinearLayout',index=2).child(className='android.widget.TextView')     #第i个内容存在并且是人的情况
                if obj1.exists:
                    obj1 = obj1.info
                    phone = obj1['text']
                    if phone in set1:
                        i = i+1
                        continue
                    else:
                        set1.add(phone)
                        print(phone)
                        obj5 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i)\
                            .child(className='android.widget.FrameLayout').child(text='等待验证')
                        if obj5.exists:
                            d(textContains='加好友').click()
                            obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
                            obj = obj['text']
                            lenth = len(obj)
                            mn = 0
                            while mn < lenth:
                                d.press.delete()
                                mn = mn + 1
                            z.input(Material)
                            d(text='发送').click()
                            return
                        obj4 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i).child(className='android.widget.CheckBox')  #勾选框没被遮住的情况
                        if obj4.exists:
                            obj4.click()
                        else:
                            d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i).click()
                        i = i+1
                        t = t+1
                        continue    #--------------------------------------------
                else:

                    i = i+1
                    continue
            else:
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)
                obj2 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=i-1) \
                    .child(className='android.widget.LinearLayout', index=2).child(
                    className='android.widget.TextView')  # 结束条件
                if obj2.exists:
                    obj2 = obj2.info
                else:
                    obj2 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i - 2) \
                        .child(className='android.widget.LinearLayout', index=2).child(
                        className='android.widget.TextView').info  # 结束条件
                EndPhone = obj2['text']
                if EndPhone in set1:
                    d(textContains='加好友').click()
                    obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
                    obj = obj['text']
                    lenth = len(obj)
                    mn = 0
                    while mn < lenth:
                        d.press.delete()
                        mn = mn + 1
                    z.input(Material)
                    d(text='发送').click()
                    return

                for g in range(0,12,+1):
                    obj3 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=g)\
                    .child(className='android.widget.LinearLayout',index=2).child(className='android.widget.TextView')     #第i个内容存在并且是人的情况
                    if obj3.exists:
                        obj3 = obj3.info
                    else:
                        g = g+1
                        continue
                    Tphone = obj3['text']
                    if Tphone==phone:
                        break
                i = g+1
                print(i)
                continue



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqAddByAddressListII

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id": "36",'EndIndex':'100',"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)





















