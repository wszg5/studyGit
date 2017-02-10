# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WeiXinAddressList:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        # d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()  # 将微信拉起来
        time.sleep(7)
        d(text='通讯录').click()
        if d(text='新的朋友').exists:
            print()
        else:
            d(text='通讯录').click()

        set1 = set()
        change = 0
        i = 1
        t = 1
        ending = 0     #用来判断是否到底
        EndIndex = int(args['EndIndex'])         #------------------
        while t < EndIndex + 1:
            cate_id = args["repo_material_id"]   #------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            wait = 1
            while wait == 1:
                try:
                    Material = Material[0]['content']  # 从素材库取出的要发的材料
                    wait = 0
                except Exception:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()

            time.sleep(1)
            obj = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=i).child(className='android.widget.LinearLayout').child(className='android.view.View')     #得到微信名
            if obj.exists:
                change = 1      #好友存在且未被添加的情况出现，change值改变
                obj1 = obj.info
                name = obj1['text']
                if name=='微信团队':
                    i = i+1
                    continue
                if name in set1:    #判断是否已经给该人发过消息
                    i = i+1
                    continue
                else:
                    set1.add(name)
                    print(name)
                obj.click()
                GenderFrom = args['gender']     #-------------------------------
                if GenderFrom !='不限':
                    obj = d(className='android.widget.LinearLayout', index=1).child(
                        className='android.widget.LinearLayout').child(className='android.widget.ImageView',index=1)  # 看性别是否有显示
                    if obj.exists:
                        Gender = obj.info
                        Gender = Gender['contentDescription']
                        if Gender ==GenderFrom:
                            print()
                        else:            #如果性别不符号的情况
                            d(description='返回').click()
                            i = i+1
                            continue
                    else:                 #信息里没有显示出性别的话
                        d(description='返回').click()
                        i = i + 1
                        continue

                d(text='发消息').click()


                time.sleep(1)
                obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
                obj = obj['text']
                lenth = len(obj)
                m = 0
                while m < lenth:
                    d.press.delete()
                    m = m + 1
                d(className='android.widget.EditText').click()
                z.input(Material)       #----------------------------------------
                d(text = '发送').click()
                time.sleep(1)
                d(description='返回').click()
                d(text='通讯录').click()
                i = i+1
                t = t+1
                continue

            else:
                if change==0:   #一次还没有点击到人
                    i = i+1
                    continue
                else:
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    time.sleep(2)

                    if ending == 1:     #结束条件
                        return
                    if d(textContains='位联系人').exists:
                        ending = 1

                        # return
                    for g in range(0,12,+1):
                        time.sleep(0.5)
                        obj = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=g).child(className='android.widget.LinearLayout').child(className='android.view.View')  # 得到微信名
                        obj = obj.info
                        Tname = obj['text']
                        if Tname==name:
                            break
                    i = g+1
                    continue

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WeiXinAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()


    args = {"repo_material_id": "36",'EndIndex':'100','gender':"女","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
