# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random


class ImpContact:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum


    def action(self, d, args):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        filename = os.path.join(base_dir, "%s.txt"%(self.GetUnique()) )


        cate_id = args["repo_cate_id"]
        numbers = self.repo.GetNumber(cate_id, 0, 50)
        if numbers:
            file_object = open(filename, 'w')
            lines = ""
            for number in numbers:
                lines = "%s%s %s\r" %(lines, number, number)

            file_object.writelines(lines)
            lines=""
            file_object.close()
            d.server.adb.cmd("shell", "am", "start", "-a", "tb.clear.connacts").wait()
            d.server.adb.cmd("push", filename, "/data/local/tmp/contacts.txt").wait()
            d.server.adb.cmd("shell", "am", "start", "-n", "com.zunyun.qk/.ImportActivity", "-t", "text/plain",  "-d", "file:///data/local/tmp/contacts.txt").wait()
            os.remove(filename)
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return ImpContact

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A3SK00853")
    d.dump(compressed=False)
    args = {"repo_cate_id":"21","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
