# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WeiXinNearByNotify:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(9)
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
        d(description='更多').click()
        GenderFrom = args['gender']  # -------------------------------
        if GenderFrom != '不限':
            d(textContains=GenderFrom).click()
            while d(textContains='正在查找').exists:
                time.sleep(2)
        else:
            d(textContains='全部').click()
            while d(textContains='正在查找').exists:
                time.sleep(2)

        set1 = set()
        change = 0
        i = 1
        t = 1
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
            obj = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=i).child(
                index=1).child(className='android.widget.LinearLayout', index=0).child(
                className='android.widget.TextView',
                index=0)       #得到微信名
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

                time.sleep(1)
                if d(text='打招呼').exists:
                    d(text='打招呼').click()
                else:
                    d(description='返回').click()
                    i = i+1
                    continue

                d(className='android.widget.EditText').click()
                z.input(message)       #----------------------------------------
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
                    if name1 in set1:
                        return

                    i = 1
                    continue
        d(description='更多').click()
        d(text='清除位置并退出').click()
        d(text='确定').click()
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return WeiXinNearByNotify

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

    args = {"repo_material_id": "39",'EndIndex':'64','gender':"女","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)


































