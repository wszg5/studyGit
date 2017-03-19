# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
class WeiXinAddressList:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(7)
        d(text='通讯录').click()
        if not d(text='新的朋友').exists:
            d(text='通讯录').click()
        z.heartbeat()
        set1 = set()
        change = 0
        i = 1
        t = 1
        ending = 0     #用来判断是否到底
        EndIndex = int(args['EndIndex'])         #------------------
        while t < EndIndex + 1:
            cate_id = args["repo_material_id"]   #------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                time.sleep(10)
                return
            message = Material[0]['content']  # 从素材库取出的要发的材料

            time.sleep(1)
            wxName = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=i).child(className='android.widget.LinearLayout').child(className='android.view.View')     #得到微信名
            if wxName.exists:
                z.heartbeat()
                change = 1      #好友存在且未被添加的情况出现，change值改变
                Name = wxName.info
                name = Name['text']
                if name=='微信团队':
                    i = i+1
                    continue
                if name in set1:    #判断是否已经给该人发过消息
                    i = i+1
                    continue
                else:
                    set1.add(name)
                    print(name)
                wxName.click()
                GenderFrom = args['gender']     #-------------------------------
                if GenderFrom !='不限':
                    Gender = d(className='android.widget.LinearLayout', index=1).child(
                        className='android.widget.LinearLayout').child(className='android.widget.ImageView',index=1)  # 看性别是否有显示
                    if Gender.exists:
                        z.heartbeat()
                        Gender = Gender.info
                        Gender = Gender['contentDescription']
                        if Gender !=GenderFrom:
                                       #如果性别不符号的情况
                            d(description='返回').click()
                            i = i+1
                            continue
                    else:                 #信息里没有显示出性别的话
                        z.heartbeat()
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
                z.heartbeat()
                d(className='android.widget.EditText').click()
                z.input(message)       #----------------------------------------
                # d(text = '发送').click()
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


                    i = 1
                    continue

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WeiXinAddressList

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id": "39",'EndIndex':'10','gender':"女","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
