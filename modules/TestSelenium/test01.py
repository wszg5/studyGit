# coding:utf-8

from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice
from selenium import webdriver


class Test01:
    def __init__(self):

        self.repo = Repo()


    def action(self, d, z, args):

        drive = webdriver.Firefox()
        print drive

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return Test01

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"time_delay":"3","set_timeStart":"100","set_timeEnd":"120","startTime":"0","endTime":"8",
            "repo_number_cate_id":"119","repo_material_cate_id":"39",'gender':"男","add_count":"5"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )