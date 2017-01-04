# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import os,re,subprocess
from Repo import *
from RClient import *
import time, datetime, random
class EIMLogin:
    def __init__(self):
        self.repo = Repo()




    def action(self, d, args):
        d.server.adb.cmd("shell", "pm clear com.tencent.eim").wait()  # 清除缓存
        # d.server.adb.cmd("shell", "am force-stop com.tencent.eim").wait()  # 强制停止   3001369923  Bn2kJq5l
        d.server.adb.cmd("shell",
                         "am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        d()




        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))
def getPluginClass():
    return EIMLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT4A3SK00853")
    # d.dump(compressed=False)
    args = {"repo_cate_id":"6","time_limit":"120","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)