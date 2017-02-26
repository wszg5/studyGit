# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WeiXinAddFriendByAddressList:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(7)
        d(description='更多功能按钮').click()
        d(textContains='添加朋友').click()
        d(text='手机联系人').click()
        d(text='添加手机联系人').click()
        while d(textContains='正在获取').exists:
            time.sleep(3)


        set1 = set()
        change = 0
        i = 0
        t = 0
        EndIndex = int(args['EndIndex'])         #------------------
        while t < EndIndex :
            cate_id = args["repo_material_id"]   #------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                time.sleep(10)
                return
            Material = Material[0]['content']  # 从素材库取出的要发的材料

            time.sleep(1)
            obj = d(className='android.widget.LinearLayout', index=i).child(className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).child(textContains='微信:')     #得到微信名
            if obj.exists:
                obj2 = d(className='android.widget.LinearLayout', index=i).child(className='android.widget.LinearLayout').child(className='android.widget.FrameLayout').child(text='已添加')     #该编号好友已经被添加的情况
                if obj2.exists:
                    i = i+1
                    continue

                change = 1      #好友存在且未被添加的情况出现，change值改变
                obj = obj.info
                name = obj['text']
                if name in set1:    #判断是否已经给该人发过消息
                    i = i+1
                    continue
                else:
                    set1.add(name)
                print(i)
                d(className='android.widget.ListView',index=0).child(className='android.widget.LinearLayout',index=i).\
                    child(className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).click()      #点击第i个人
                GenderFrom = args['gender']     #-------------------------------
                if GenderFrom !='不限':
                    obj = d(className='android.widget.LinearLayout',index=1).child(className='android.widget.LinearLayout').child(className='android.widget.ImageView',index=1)      #看性别是否有显示
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
                if d(text='添加到通讯录').exists:
                    d(text='添加到通讯录').click()
                    time.sleep(0.5)
                    if d(text='发消息').exists:
                        d(description='返回').click()
                        i = i+1
                        continue

                elif d(text='通过验证').exists:
                    d(text='通过验证').click()
                    d(description='返回').click()
                    i = i + 1
                    continue


                else:
                    d(description='返回').click()
                    i = i+1
                    continue
                time.sleep(1)
                obj = d(className='android.widget.EditText', index=1).info  # 将之前消息框的内容删除
                obj = obj['text']
                lenth = len(obj)
                m = 0
                while m < lenth:
                    d.press.delete()
                    m = m + 1
                d(className='android.widget.EditText', index=1).click()
                z.input(Material)       #----------------------------------------
                d(text = '发送').click()
                time.sleep(1)
                # d(description='返回').click()
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
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    obj = d(className='android.widget.LinearLayout', index=i-1).child(className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).child(textContains='微信:')
                    time.sleep(0.5)
                    if obj.exists:
                        obj = obj.info
                        name1 = obj['text']      #判断是否已经到底
                        if name1 in set1:
                            return
                    else:
                        print()
                    for g in range(1,10,+1):
                        obj = d(className='android.widget.LinearLayout', index=g).child(className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).child(textContains='微信:').info
                        Tname = obj['text']
                        if Tname==name:
                            break
                    i = g+1
                    continue
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WeiXinAddFriendByAddressList

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()


    args = {"repo_material_id": "39",'EndIndex':'100','gender':"女","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
