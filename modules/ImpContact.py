# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
import json
from zservice import ZDevice


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


    def action(self, d,z, args):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        filename = os.path.join(base_dir, "%s.txt"%(self.GetUnique()) )

        number_count = args['number_count']
        cate_id = args["repo_cate_id"]
        print(cate_id)
        numbers = self.repo.GetNumber(cate_id, 0, number_count)
        wait = 1  # 判断素材仓库里是否由素材
        while wait == 1:
            try:
                t = numbers[0]  # 取出验证消息的内容
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，等待中\""%cate_id).communicate()

                time.sleep(30)

        if numbers:
            file_object = open(filename, 'w')
            lines = ""
            for number in numbers:
                lines = "%s%s %s\r" %(lines, number, number)

            file_object.writelines(lines)
            lines=""
            file_object.close()
            d.server.adb.cmd("shell", "am", "start", "-a", "tb.clear.connacts").communicate()
            d.server.adb.cmd("push", filename, "/data/local/tmp/contacts.txt").communicate()
            d.server.adb.cmd("shell", "am", "start", "-n", "com.zunyun.qk/.ImportActivity", "-t", "text/plain",  "-d", "file:///data/local/tmp/contacts.txt").communicate()
            os.remove(filename)
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return ImpContact

if __name__ == "__main__":

    # global args
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").communicate()
    d.server.adb.cmd("shell",
                     "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，等待中\"" % 55).communicate()


    # d.dump(compressed=False)
    args = {"repo_cate_id":"44","length":"30",'number_count':'80',"time_delay":"3"}    #cate_id是仓库号，length是数量

    o.action(d,z, args)
