# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class TIMZoneAddFriends:
    def __init__(self):

        self.repo = Repo()


    def action(self, d, z, args):

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMZoneAddFriends

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT57FSK00089")
    # material=u'有空聊聊吗'
    z = ZDevice("HT57FSK00089")
    # d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id": "43", "repo_material_cate_id": "36", "add_count": "9",
            "time_delay": "3"};  # cate_id是仓库号，length是数量
    o.action(d, z, args)