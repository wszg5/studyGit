# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class WXPublicNum:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(7)
        endIndex = int(args['EndIndex'])
        d(description='搜索').click()
        endCondition = 0
        while endCondition<endIndex:
            cate_id = args["repo_material_id"]  # ------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                time.sleep(10)
                return
            link = Material[0]['content']  # 从素材库取出的要发的材料
            z.input(link)
            d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=0).child(className='android.widget.RelativeLayout',index=0).click()    #点击搜索
            if d(textContains='没有更多的').exists:
                endCondition = endCondition+1
                d(description='清除').click()
                continue
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXPublicNum

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id": "128", 'EndIndex': '64', "time_delay": "3"}   #cate_id是仓库号，length是数量
    o.action(d,z, args)
