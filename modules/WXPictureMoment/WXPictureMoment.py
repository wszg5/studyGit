# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXPictureMoment:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(8)
        # d(className='android.widget.RelativeLayout', index=3).child(text='我').click()
        obj = d.server.adb.device_serial()     #　获取设备序列号

        # if d(textContains='微信号：').exists:
        #     obj = d(textContains='微信号：').info
        #     obj = obj['text']
        #
        # else:
        #     obj = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=1)\
        #         .child(className='android.widget.LinearLayout',index=1).child(className='android.view.View').info
        #     obj = obj['text']
        cate_id = args['repo_material_id']
        materials = self.repo.GetMaterial(cate_id, 0, 1,obj)
        if len(materials) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"朋友圈素材%s号仓库为空，等待中\"" % cate_id).communicate()
            time.sleep(10)
            return
        t = materials[0]  # 取出验证消息的内容
        z.heartbeat()
        imgs = []
        for i in range(1,10,+1):
            z.heartbeat()
            if t['ext%s'%i] is not None:
                imgs.append(t['ext%s'%i])
        z.heartbeat()
        z.wx_sendsnsline(t["content"], imgs)
        d(text='发送').click()

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXPictureMoment

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
    args = {"repo_material_id": "43","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)




















