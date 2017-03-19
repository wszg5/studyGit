# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXAcpVerify:
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
        d(className='android.widget.ListView').child(className='android.widget.RelativeLayout',index=1).click()
        time.sleep(1)
        z.heartbeat()
        set1 = set()
        change = 0
        i = 1
        while True:
            obj = d(className='android.widget.RelativeLayout', index=i).child(index=1).child(className='android.widget.TextView', index=0)  # 得到微信名
            if obj.exists:
                z.heartbeat()
                obj = obj.info
                name = obj['text']
                if name in set1:  # 判断是否已经给该人发过消息
                    i = i + 1
                    continue
                else:
                    set1.add(name)
                    print(name)
                z.heartbeat()
                obj2 = d(className='android.widget.RelativeLayout', index=i).child(index=2).child(text='接受')  # 看是否有加好友验证
                if obj2.exists:
                    z.heartbeat()
                    change = 1      #好友存在且未被添加的情况出现，change值改变

                    d(className='android.widget.ListView',index=0).child(className='android.widget.RelativeLayout',index=i).child(className='android.widget.RelativeLayout',index=1).click()      #点击第i个人
                    GenderFrom = args['gender']     #-------------------------------
                    if GenderFrom !='不限':
                        obj = d(className='android.widget.LinearLayout', index=1).child(
                            className='android.widget.LinearLayout').child(className='android.widget.ImageView',index=1)  # 看性别是否有显示
                        if obj.exists:
                            z.heartbeat()
                            Gender = obj.info
                            Gender = Gender['contentDescription']
                            if Gender !=GenderFrom:
                                           #如果性别不符号的情况
                                d(description='返回').click()
                                i = i+1
                                continue
                        else:                 #信息里没有显示出性别的话
                            d(description='返回').click()
                            i = i + 1
                            continue
                    d(text='通过验证').click()
                    d(text='完成').click()
                    z.heartbeat()
                    time.sleep(1)
                    d(description='返回').click()
                    i = i+1
                    continue
                else:
                    i = i+1
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
                    obj = d(className='android.widget.RelativeLayout', index=i-1).child(index=1).child(className='android.widget.TextView', index=0)
                    obj = obj.info
                    name1 = obj['text']      #判断是否已经到底
                    if name1 in set1:
                        break
                    i = 1
                    continue

        if (args["time_delay"]):
                time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXAcpVerify

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
    args = {'gender':"男","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)