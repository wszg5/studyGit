# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random


class TimSlotLogin:
    def __init__(self):
        self.repo = Repo()

    def backup(self, d, name):
        d.server.adb.cmd("shell", "su -c 'chmod -R 777 /data/data/com.tencent.tim/'").wait()
        d.server.adb.cmd("shell", "su -c 'mkdir /data/data/com.zy.bak/'").wait()
        d.server.adb.cmd("shell", "su -c 'chmod -R 777 /data/data/com.zy.bak/'").wait()
        d.server.adb.cmd("shell", "mkdir /data/data/com.zy.bak/tim").wait()
        d.server.adb.cmd("shell", "rm -r -f /data/data/com.zy.bak/tim/%s/"%name).wait()
        d.server.adb.cmd("shell", "rm -r -f  /data/data/com.zy.bak/tim/zy_name_*").wait()

        d.server.adb.cmd("shell", "mkdir /data/data/com.zy.bak/tim/%s"%name).wait()
        d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/databases/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/shared_prefs/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/txlib/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        #d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/jpeglib/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        #d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/mailsdklib/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/files/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        #d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/app_webview/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        #d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/app_systemface/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        #d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/app_profilecard/  /data/data/com.zy.bak/tim/%s/"%name).wait()

        d.server.adb.cmd("shell", "mkdir /data/data/com.zy.bak/tim/zy_name_%s_name/"%name ).wait()


    def restore(self, d, name):
        #d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()
        d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()
        d.server.adb.cmd("shell", "rm -r -f  /data/data/com.zy.bak/tim/zy_name_*").wait()

        d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/databases/ /data/data/com.tencent.tim/"%name).wait()
        d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/shared_prefs/ /data/data/com.tencent.tim/"%name).wait()
        d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/txlib/ /data/data/com.tencent.tim/"%name).wait()
        #d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/jpeglib/ /data/data/com.tencent.tim/"%name).wait()
        #d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/mailsdklib/ /data/data/com.tencent.tim/"%name).wait()
        d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/files/ /data/data/com.tencent.tim/"%name).wait()
        #d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/app_webview/ /data/data/com.tencent.tim/"%name).wait()
        #d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/app_systemface/ /data/data/com.tencent.tim/"%name).wait()
        #d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/app_profilecard/ /data/data/com.tencent.tim/"%name).wait()

        d.server.adb.cmd("shell", "mkdir /data/data/com.zy.bak/tim/zy_name_%s_name/"%name ).wait()



    def action(self, d, args):
        #self.backup(d, "61768504")
        self.restore(d, "30527485")

def getPluginClass():
    return TimSlotLogin

if __name__ == "__main__":
    print os.getcwd()
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT36VS902645")
    #d.dump(compressed=False)
    args = {"repo_cate_id":"131","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
