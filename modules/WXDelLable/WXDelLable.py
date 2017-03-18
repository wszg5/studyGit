# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class WXDelLable:

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
        if d(text='标签').exists:
            d(text='标签').click()
        else:
            d(text='通讯录').click()
            d(text='标签').click()
        if d(textContains='暂无标签').exists:
            return
        z.heartbeat()
        gender = args['gender']
        if gender=='不限':
            lable = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=0). \
                child(className='android.widget.LinearLayout', index=0).child(className='android.widget.TextView',index=0)  # 看标签是否存在
            while lable.exists:
                z.heartbeat()
                lable.long_click()
                time.sleep(1)
                d(text='删除').click()
                d(text='删除').click()
                time.sleep(1)
        else:    #要区分性别的情况
            set1 = set()
            i = 0
            while True:
                obj = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=i).\
                    child(className='android.widget.LinearLayout',index=0).child(className='android.widget.TextView',index=0)     #看第ｉ个标签是否存在
                forClick = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=i).\
                    child(className='android.widget.LinearLayout',index=0)    #用来点击的
                if obj.exists:
                    z.heartbeat()
                    obj = obj.info
                    lable = obj['text']
                    print(lable)
                    if lable in set1:
                        i = i+1
                        continue
                    else:
                        set1.add(lable)     #将标签添加到集合中
                        if gender in lable:     #性别满足要求的情况
                           z.heartbeat()
                           forClick.long_click()
                           d(text='删除').click()
                           d(text='删除').click()
                           time.sleep(1)
                        else:
                            i = i+1
                            continue
                else:
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    obj = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=i). \
                        child(className='android.widget.LinearLayout', index=0).child(
                        className='android.widget.TextView', index=0)  # 看第ｉ个标签是否存在
                    obj1 = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=i - 1). \
                        child(className='android.widget.LinearLayout', index=0).child(
                        className='android.widget.TextView', index=0)  # 看第ｉ个标签是否存在
                    time.sleep(0.5)
                    if obj.exists:       #结束条件
                        obj = obj.info
                        name1 = obj['text']  # 判断是否已经到底
                        if name1 in set1:
                            return
                    elif obj1.exists:
                        obj1 = obj1.info
                        name1 = obj1['text']  # 判断是否已经到底
                        if name1 in set1:
                            return

                    i = 0
                    continue

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXDelLable

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

    args = {'gender':"不限","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
