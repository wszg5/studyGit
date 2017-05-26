# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *

class WXAddresslistDepost:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)
        d(description='更多功能按钮').click()
        d(textContains='添加朋友').click()
        d(textContains='手机联系人').click()
        d(text='添加手机联系人').click()
        while d(textContains='正在获取').exists:
            z.sleep(3)
        z.heartbeat()
        set1 = set()
        change = 0
        i = 0
        t = 0
        while True :
            phone = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',
                                                                 index=i).child(
                className='android.widget.LinearLayout').child(className='android.widget.LinearLayout', index=1).child(
                className='android.widget.TextView', index=0)
            if phone.exists:
                z.heartbeat()
                change = 1
                phonenumber = phone.info['text']
                if phonenumber in set1:    #判断是否已经给该人发过消息
                    i = i+1
                    continue
                else:
                    set1.add(phonenumber)
                z.heartbeat()
                d(className='android.widget.ListView',index=0).child(className='android.widget.LinearLayout',index=i).\
                    child(className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).click()      #点击第i个人
                Gender = d(className='android.widget.LinearLayout', index=1).child(className='android.widget.LinearLayout').child(className='android.widget.ImageView',index=1)  # 看性别是否有显示
                if Gender.exists:
                    Gender = Gender.info
                    Gender = Gender['contentDescription']
                else:
                    Gender = '空'
                z.heartbeat()
                nickname = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=1)\
                    .child(className='android.widget.LinearLayout',index=1).child(className='android.widget.TextView')
                if nickname.exists:
                    nickname = nickname.info['text']
                else:
                    nickname = '空'
                z.heartbeat()
                if d(text='地区').exists:
                    for k in range(3,10):
                        if d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=k).child(className='android.widget.LinearLayout',index=0).child(text='地区').exists:
                            break
                    area = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=k).child(className='android.widget.LinearLayout',index=0).\
                        child(className='android.widget.LinearLayout',index=1).child(className='android.widget.TextView').info['text']
                else:
                    area = '空'
                z.heartbeat()
                if d(text='个性签名').exists:
                    for k in range(3,10):
                        if d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=k).child(className='android.widget.LinearLayout',index=0).child(text='个性签名').exists:
                            break
                    sign = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=k).child(className='android.widget.LinearLayout',index=0).\
                        child(className='android.widget.LinearLayout',index=1).child(className='android.widget.TextView').info['text']
                else:
                    sign = '空'
                z.heartbeat()
                para = {"phone":phonenumber,'qq_nickname':nickname,'sex':Gender,"city":area,"x_01":sign}

                # print('--%s--%s--%s--%s--%s'%(phonenumber,nickname,Gender,area,sign))

                inventory = Inventory()
                con = inventory.postData(para)
                # print(con)
                # if con != True:
                #     d.server.adb.cmd("shell",
                #                      "am broadcast -a com.zunyun.zime.toast --es msg \"消息保存失败……\"").communicate()
                #     z.sleep(10)
                #     return
                d(description='返回').click()
                i = i+1
                t = t+1
                continue

            else:
                if change==0:   #一次还没有点击到人
                    if i==1:    #通讯录没有人的情况
                        return
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    i = 1
                    continue
                else:
                    clickCondition = d(className='android.widget.ListView')
                    obj = clickCondition.info
                    obj = obj['visibleBounds']
                    top = int(obj['top'])
                    bottom = int(obj['bottom'])
                    y = bottom - top
                    d.swipe(width / 2, y, width / 2, 0)

                    zz = i + 2
                    for k in range(1, 10):
                        obj2 = d(className = 'android.widget.ListView').child(className='android.widget.LinearLayout', index=zz).child(
                        className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).child(className='android.widget.TextView', index=0) # 结束判断条件
                        if obj2.exists:
                            endphone = obj2.info['text']
                            if endphone in set1:  # 结束条件，如果
                                if (args["time_delay"]):
                                    z.sleep(int(args["time_delay"]))
                                return
                            else:
                                break
                        else:
                            zz = zz - 1
                            continue

                    obj1 = d(className = 'android.widget.ListView').child(className='android.widget.LinearLayout', index=0).child(
                        className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).child(className='android.widget.TextView', index=0)
                    if obj1.exists:  # 实现精准滑动后有的能显示第０列的电话号码，有的显示不出来
                        i = 0
                        continue
                    else:
                        i = 1
                        continue


def getPluginClass():
    return WXAddresslistDepost

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)

































