# coding:utf-8
import os
import uuid

import requests

from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXPictureMoment:



    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        num = int(args['num'])
        cate_id = args['repo_material_id']
        time = int(args['time'])
        materials = self.repo.GetMaterial(cate_id,time, num)
        count = len(materials)
        if len(materials) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"朋友圈素材%s号仓库为空，等待中\"" % cate_id).communicate()
            z.sleep(10)
            return

        imgs = []
        for i in range(0, count, +1):

            t = materials[i]['content']
            if t is not None:
                imgs.append(t)
            z.heartbeat()
        z.sendpicture(imgs)
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXPictureMoment

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id": "153",'num':'10','time':'0',"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)




















