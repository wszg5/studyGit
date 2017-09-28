# coding:utf-8
import colorsys
import os

# from reportlab.graphics.shapes import Image
from PIL import Image

from smsCode import smsCode
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class TIMAddFriendByShareCard:
    def __init__(self):
        self.repo = Repo()

    def action(self):
        if 100<0:
            return
        return
        print("能不能到这")
        print( "能不能到这" )

def getPluginClass():
    return TIMAddFriendByShareCard

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    # d = Device("HT54VSK01061")
    # z = ZDevice("HT54VSK01061")
    # d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # args = {"repo_number_cate_id":"119","repo_material_cate_id":"39",'gender':"男","add_count":"3","time_delay":"3","switch_card":"否"}    #cate_id是仓库号，length是数量

    o.action()