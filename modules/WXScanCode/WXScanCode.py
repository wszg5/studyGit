# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
import requests
import urllib2
class WXScanCode:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(5)
        cate_id = args['repo_material_id']
        repo = Repo()
        materials = repo.GetMaterial(cate_id, 0, 1)
        if len(materials) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"朋友圈素材%s号仓库为空，等待中\"" % cate_id).communicate()
            z.sleep(10)
            return
        t = materials[0]['ext1']  # 取出验证消息的内容
        z.heartbeat()
        z.wx_scanqr(t)
        z.heartbeat()
        z.sleep(15)
        d.swipe(130, 532, 402, 575, 1)
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXScanCode

if __name__ == "__main__":
    sys.setdefaultencoding('utf8')

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id": "41","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)




















