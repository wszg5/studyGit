# coding:utf-8

from multiprocessing import Process, Queue

from uiautomator import Device
import  time,threading,os
from zservice import ZDevice
import random
import re
from Repo import *

class MobilqqPicWall:
    def __init__(self):
        self.repo = Repo()

    def reviceyear(self):
        setyear = random.randint(1990, 2000)
        nowyear = d(textContains='年', index='3').info['text']
        nowyear = int(re.findall(r"\d+\.?\d*", nowyear)[0])
        if setyear < nowyear:
            num = nowyear - setyear
            for i in range(0, num):
                d(textContains='年', index=2).click()
        else:
            num = setyear - nowyear
            for i in range(0, num):
                d(textContains='年', index=4).click()

    def revicemonth(self):
        setmonth = random.randint(1, 12)  # 设置月份
        nowmonth = d(textContains='月', index='3').info['text']
        nowmonth = int(re.findall(r"\d+\.?\d*", nowmonth)[0])
        if setmonth < nowmonth:
            num = nowmonth - setmonth
            for i in range(0, num):
                d(textContains='月', index=2).click()
        else:
            num = setmonth - nowmonth
            for i in range(0, num):
                if d(textContains='月', index=4).exists:
                    d(textContains='月', index=4).click()
                else:
                    d(textContains='月', index=3).click()

    def reviceday(self):
        setday = random.randint(1, 30)  # 设置月份
        nowday = d(textContains='日', index='3').info['text']
        nowday = int(re.findall(r"\d+\.?\d*", nowday)[0])
        if setday < nowday:
            num = nowday - setday
            for i in range(0, num):
                d(textContains='日', index=2).click()
        else:
            num = setday - nowday
            for i in range(0, num):
                if d(textContains='日', index=4).exists:
                    d(textContains='日', index=4).click()
                else:
                    d(textContains='月', index=3).click()


    def action(self, d,z, args):


        # 父进程创建Queue，并传给各个子进程：
        q = Queue()
        t = Process(target=self.reviceyear)
        t1 = Process(target=self.revicemonth)
        t2 = Process(target=self.reviceday)
        t.start()
        t1.start()
        t2.start()
        t.join()
        t1.join()
        t2.join()
        print()





        d(text='完成').click()




        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqPicWall

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_name_id":"139","repo_declaration_id":"140","repo_company_id":"141","repo_school_id":"142","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)

