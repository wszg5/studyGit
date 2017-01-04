# coding:utf-8
from uiautomator import Device
from Repo import *


class FilterQQNumber:
    def __init__(self):
        self.repo = Repo()


    def action(self, QQNumber, args):
        QQNumber = '1633132378'
        print (len(QQNumber))









def getPluginClass():
    return FilterQQNumber

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49PSK05055")
    args = {"repo_cate_id":"131","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
