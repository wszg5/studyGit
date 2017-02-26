# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class EIMMass:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.eim").communicate()  # 强制停止   3001369923  Bn2kJq5l
        d.server.adb.cmd("shell", "am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(5)
        d(description='联系人栏').click()
        d(text='外部联系人').click()
        set1 = set()
        time.sleep(2)
        for out1 in range(3,13,+1):   #用来控制分组
           if d(index=out1,descriptionContains='分组已折叠').exists:
               obj = d(index=out1,className='android.widget.RelativeLayout').child(className='android.widget.TextView',index=1).info
               number = obj['text']
               number = number.split('/')
               number = int(number[1])
               if number == 0:    #分组里没有好友的情况
                   continue
               else:
                   d(index=out1, className='android.widget.RelativeLayout').click()
                   i = 0   #用来统计分组的人数
                   t = out1+1
                   while i<number:   #用来对当前分组挨个发消息
                       cate_id = args["repo_material_id"]  # ------------------
                       Material = self.repo.GetMaterial(cate_id, 0, 1)
                       if len(Material) == 0:
                           d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                           time.sleep(10)
                           return
                       Material = Material[0]['content']  # 从素材库取出的要发的材料



                       obj = d(index=t,className='android.widget.RelativeLayout').child(className='android.widget.TextView',index=1)
                       if obj.exists:   #判断是否滑屏
                           infor = obj.info
                           name = infor['text']
                           if name in set1:
                               t = t+1
                               continue
                           else:
                               set1.add(name)
                               print(name)
                               obj.click()
                               d(text='发消息').click()
                               if d(text='发消息').exists:
                                   d(text='发消息').click()
                               d(className='android.widget.EditText').click()
                               z.input(Material)
                               d(text='发送').click()
                               d(text='返回').click()
                               d(text='返回').click()
                               i = i+1
                               t = t+1
                               if i == number:
                                   if d(descriptionContains='分组已展开').exists:
                                        d(descriptionContains='分组已展开').click()
                                   else:
                                       d(text='联系人').click()
                                       d(text='外部联系人').click()
                               continue
                       else:
                           d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                           for record in range(1,15,+1):
                               obj1 = d(index=record, className='android.widget.RelativeLayout').child(className='android.widget.TextView', index=1).info
                               Tname = obj1['text']
                               print(Tname)
                               if Tname in set1:
                                   continue
                               else:
                                   break
                           t = record
                           continue

           else:
               break





        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return EIMMass

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()


    args = {"repo_material_id":"122","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

