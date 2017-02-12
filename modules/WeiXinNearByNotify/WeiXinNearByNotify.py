# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WeiXinNearByNotify:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()  # 将微信拉起来
        time.sleep(7)
        if d(text='发现',index=1).exists:
            d(text='发现', index=1).click()
        else:
            d(text='发现', index=0).click()
        d(text='附近的人').click()
        time.sleep(2)
        while d(textContains='正在查找').exists:
            time.sleep(3)
        if d(text='开始查看').exists:
            d(text='开始查看').click()
            if d(text='提示').exists:
                d(text='下次不提示').click()
                time.sleep(0.5)
                d(text='确定').click()
        if d(textContains='查看附近的人').exists:
            d(textContains='查看附近的人').click()
        time.sleep(3)


        set1 = set()
        change = 0
        i = 1
        t = 1
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
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()

            time.sleep(1)
            obj = d(className='android.widget.LinearLayout', index=i).child(index=1).child(className='android.widget.TextView', index=0)     #得到微信名
            if obj.exists:
                change = 1
                obj = obj.info
                name = obj['text']
                if name in set1:    #判断是否已经给该人发过消息
                    i = i+1
                    continue
                else:
                    set1.add(name)
                    print(name)
                d(className='android.widget.ListView',index=0).child(className='android.widget.LinearLayout',index=i).child(className='android.widget.LinearLayout',index=1).click()      #点击第i个人
                GenderFrom = args['gender']     #-------------------------------
                if GenderFrom !='不限':
                    obj = d(className='android.widget.ImageView',index=1,resourceId='com.tencent.mm:id/abr')      #看性别是否有显示
                    if obj.exists:
                        Gender = obj.info
                        Gender = Gender['contentDescription']
                        if Gender ==GenderFrom:
                            print()
                        else:            #如果性别不符号的情况
                            d(description='返回').click()
                            i = i + 1
                            continue
                    else:                 #信息里没有显示出性别的话
                        d(description='返回').click()
                        i = i + 1
                        continue
                time.sleep(1)
                if d(text='打招呼').exists:
                    d(text='打招呼').click()
                else:
                    d(description='返回').click()
                    i = i+1
                    continue

                d(className='android.widget.EditText').click()
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
                    i = i+1
                    continue
                else:
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    time.sleep(2)
                    obj = d(className='android.widget.LinearLayout', index=i-1).child(index=1).child(className='android.widget.TextView', index=0)
                    obj = obj.info
                    name1 = obj['text']      #判断是否已经到底
                    print(name1)
                    if name1 in set1:
                        return
                    for g in range(1,11,+1):
                        time.sleep(1)
                        obj = d(className='android.widget.LinearLayout', index=g).child(className='android.widget.LinearLayout',index=1).child(className='android.widget.LinearLayout',index=0).child(className='android.widget.TextView', index=0) .info
                        time.sleep(1)
                        Tname = obj['text']
                        if Tname==name:
                            break
                    print(g)
                    i = g+1
                    continue


def getPluginClass():
    return WeiXinNearByNotify

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()

    args = {"repo_material_id": "36",'EndIndex':'10','gender':"女","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
