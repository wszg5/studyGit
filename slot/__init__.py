#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import json
import shutil

import time

from adb import Adb

from const import const
import os


"""Python wrapper for Zunyun Service."""
class Slot:
    def __init__(self, serial,  type):

        self.serial = serial
        self.adb = Adb(serial=serial)
        self.type = type
        if (self.type == "tim"):
            self.package = "com.tencent.tim"
            self.files = ['files/ConfigStore2.dat']
            self.folders = ['files/user']
            self.maxSlot = const.MAX_SLOTS_TIM

        elif (self.type == "wechat"):
            self.package = "com.tencent.mm"
            self.files = []
            self.folders = ['MicroMsg']
            self.maxSlot = const.MAX_SLOTS_WECHAT

        elif (self.type == "mobileqq"):
            self.package = "com.tencent.mobileqq"
            self.files = ['files/ConfigStore2.dat']
            self.folders = ['files/user']
            self.maxSlot = const.MAX_SLOTS_MOBILEQQ

        elif (self.type == "mobileqqi"):
            self.package = "com.tencent.mobileqqi"
            self.files = ['files/ConfigStore2.dat']
            self.folders = ['files/user']
            self.maxSlot = const.MAX_SLOTS_QQINTERNATION

        elif (self.type == "qqlite"):
            self.package = "com.tencent.qqlite"
            self.files = ['files/ConfigStore2.dat']
            self.folders = ['files/user']
            self.maxSlot = const.MAX_SLOTS_QQLITE

        elif (self.type == "eim"):
            self.package = "com.tencent.eim"
            self.files = ['files/ConfigStore2.dat']
            self.folders = ['files/user', 'databases']
            self.maxSlot = const.MAX_SLOTS_EIM

        elif (self.type == "token"):
            self.package = "com.tencent.token"
            self.files = []
            self.folders = ['app_webview/Cookies']
            self.maxSlot = const.MAX_SLOTS_TOKEN

        elif (self.type == "qqmail"):
            self.package = "com.tencent.androidqqmail"
            self.files = []
            self.folders = ['databases']
            self.maxSlot = const.MAX_SLOTS_QQMAIL

        elif (self.type == "163mail"):
            self.package = "com.tencent.androidqqmail"
            self.files = []
            self.folders = ['databases']
            self.maxSlot = const.MAX_SLOTS_163MAIL

        elif (self.type == "now"):
            self.package = "com.tencent.now"
            self.files = []
            self.folders = ['files', 'databases', 'shared_prefs']
            self.maxSlot = const.MAX_SLOTS_NOW

        elif (self.type == "yixin"):
            self.package = "im.yixin"
            self.files = ['databases/conf.dat']
            self.folders = []
            self.maxSlot = const.MAX_SLOTS_YIXIN

        else:
            raise SyntaxError("目前还不支持%s卡槽"%self.type)

        self.maxSlot = int(self.maxSlot)

    def backup(self, id, info):
        self.adb.run_cmd("shell", "su -c 'chmod -R 777 /data/data/%s/'"%self.package)
        self.adb.run_cmd("shell", "su -c 'mkdir /data/data/com.zy.bak/'")
        self.adb.run_cmd("shell", "su -c 'chmod -R 777 /data/data/com.zy.bak/'")
        self.adb.run_cmd("shell", "su -c 'mkdir /data/data/com.zy.bak/%s'"%self.type)
        self.adb.run_cmd("shell", "su -c 'rm -r -f /data/data/com.zy.bak/%s/%s/'" % (self.type, id))
        self.adb.run_cmd("shell", "su -c 'mkdir /data/data/com.zy.bak/%s/%s'" % (self.type, id))
        self.adb.run_cmd("shell", "su -c 'chmod -R 777 /data/data/com.zy.bak/'")

        for folder in self.folders:
            targetPath = '/data/data/com.zy.bak/%s/%s/%s' % (self.type, id, folder)
            targetPath = os.path.dirname(targetPath)
            self.adb.run_cmd("shell", "su -c 'mkdir -p %s'" % targetPath)
            cmd = "cp -f -r -p /data/data/%s/%s/  %s" % (self.package, folder, targetPath)
            self.adb.run_cmd("shell", "su -c '%s'" % cmd)

            #self.adb.run_cmd("shell", "su -c 'cp -r -f -p /data/data/%s/%s/  /data/data/com.zy.bak/%s/%s/%s'" % (self.package, folder, self.type, name, folder))
        for file in self.files:
            targetFile = '/data/data/com.zy.bak/%s/%s/%s'%(self.type, id, file)
            targetPath = os.path.dirname(targetFile)
            self.adb.run_cmd("shell", "su -c 'mkdir -p %s'" % targetPath)
            cmd = "cp -f  /data/data/%s/%s  %s" % (self.package, file, targetFile)
            self.adb.run_cmd("shell", "su -c '%s'" %cmd )

        self.adb.run_cmd("shell", "ime set com.zunyun.zime/.ZImeService")
        #self.adb.run_cmd("shell", "mkdir /data/data/com.zy.bak/%s/zy_name_%s_name/"%(self.type,name) ).wait()
        t = base64.b64encode(info)

        self.adb.run_cmd("shell",
                         'am broadcast -a com.zunyun.zime.action --es ac save_slot --es id %s --es type %s --es remark "%s"' % (id, self.type, t))

        #dbapi.SaveSlotInfo(d.server.adb.device_serial(), self.type, name, "false", "true", info)

    def restore(self, id, target=None):
        if target is None:
            target = self.package

        self.adb.run_cmd("shell", "pm clear %s" % target)
        self.adb.run_cmd("shell", "su -c 'chmod -R 777 /data/data/%s/'" % target)
        self.adb.run_cmd("shell", "su -c 'chmod -R 777 /data/data/com.zy.bak/'")
        #self.adb.run_cmd("shell", "pm clear com.tencent.tim").wait()
        #self.adb.run_cmd("shell", "rm -r -f  /data/data/com.zy.bak/%s/zy_name_*"%type).wait()
        for folder in self.folders:
            targetPath = '/data/data/%s/%s' % (target, folder)
            targetPath = os.path.dirname(targetPath)
            self.adb.run_cmd("shell", "su -c 'mkdir -p %s'" % targetPath)
            cmd = "cp -f -r -p /data/data/com.zy.bak/%s/%s/%s/  %s" % (self.type, id, folder, targetPath)
            self.adb.run_cmd("shell", "su -c '%s'" % cmd)
            self.adb.run_cmd("shell", "su -c 'chmod -R 777 %s'" % targetPath)
        #for folder in self.folders:
           # self.adb.run_cmd("shell", "cp -r -f -p /data/data/com.zy.bak/%s/%s/%s/ /data/data/%s/"%(self.type, name, folder, self.package))

        for file in self.files:
            targetFile = '/data/data/%s/%s'%(target, file)
            targetPath = os.path.dirname(targetFile)
            self.adb.run_cmd("shell", "su -c 'mkdir -p %s'" % targetPath)
            self.adb.run_cmd("shell", "su -c 'cp -f /data/data/com.zy.bak/%s/%s/%s %s'" % (self.type, id, file, targetFile))
            self.adb.run_cmd("shell", "su -c 'chmod -R 777 %s'" % targetPath)

        #self.adb.run_cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/databases/ /data/data/com.tencent.tim/"%name).wait()

        #self.adb.run_cmd("shell", "mkdir /data/data/com.zy.bak/%s/zy_name_%s_name/"%(self.type,name) ).wait()
        #dbapi.PickSlot(d.server.adb.device_serial(), self.type, name)
        self.adb.run_cmd("shell", "su -c 'chmod -R 777 /data/data/%s/'" % target)


        self.adb.run_cmd("shell", "ime set com.zunyun.zime/.ZImeService")
        self.adb.run_cmd("shell",
                         "am broadcast -a com.zunyun.zime.action --es ac restore_slot --es id %s --es type %s " % (id, self.type))


    def backupToDisk(self, id):
        # self.adb.run_cmd("shell", "su -c 'chmod -R 777 /data/data/%s/'"%self.package)
        self.adb.run_cmd( "shell", "su -c 'chmod 777 /data/data/com.tencent.token/app_webview/'")
        os.system( "chmod 777 /data/data/com.tencent.token/app_webview/" )
        os.system("chmod 777 /home/zunyun/data/data/com.zy.bak/")

        for folder in self.folders:
            targetPath = '/home/zunyun/data/data/com.zy.bak/%s/%s/%s' % (self.type, id, folder)
            targetPath = os.path.dirname(targetPath)
            # if not os.path.exists(targetPath):
            #     os.mkdir(targetPath)

            url = "/data/data/%s/%s/" % (self.package, folder)
            # file = os.read(url)

            # cmd = "cp -rf /data/data/%s/%s/  %s" % (self.package, folder, "/home/zunyun/data/data/com.zy.bak")
            # cmd = "adb pull /data/data/%s/%s %s" % (self.package, folder, "/home/zunyun/data/data/com.zy.bak")
            cmd = "adb pull /data/data/com.tencent.token/app_webview/Cookies /home/zunyun/data/data/com.zy.bak/"
            # self.adb.run_cmd(cmd)
            os.system("adb pull /data/data/com.tencent.token/app_webview/Cookies /home/zunyun/data/data/com.zy.bak/")


    def clear(self, id):
        self.adb.run_cmd("shell", "su -c 'rm -r -f /data/data/com.zy.bak/%s/%s/'" % (self.type, id))


        self.adb.run_cmd("shell", "ime set com.zunyun.zime/.ZImeService")
        self.adb.run_cmd("shell",
                         "am broadcast -a com.zunyun.zime.action --es ac clear_slot --es id %s --es type %s " % (id, self.type))


    def getEmpty(self):
        slots = self.getSlots()
        if not slots:
            return 1;
        for index in range(1, self.maxSlot + 1):
            if not slots.has_key(str(index)) :
                return index
        return 0

    ##获得符合间隔时间的，并且最长时间未用的卡槽，单位分钟
    def getAvailableSlot(self, interval):
        result = []
        slots = self.getSlots()
        #换行成JSONArray
        for key in slots.keys():
            if key.isdigit():
                slot = slots[key]
                slot['id'] = key
                result.append(slot)

        result.sort(key=lambda x: x["UpdatedAt"], reverse=False)
        slot = result[0]
        if (int(time.time()) - slot["UpdatedAt"]/1000)/60 > interval:
            return slot

    def getSlotInfo(self, id):
        slots = self.getSlots()
        return slots[id]

    def getSlots(self):
        path = "/sdcard/.zime/slot_%s" % self.type
        adb = Adb(serial=self.serial)
        out = adb.run_cmd("shell", "\"su -c 'cat %s'\"" % path).output
        if self.check_json_format(out):
            return json.loads(out)


    def check_json_format(self, raw_msg):
        """
        用于判断一个字符串是否符合Json格式
        :param self:
        :return:check_json_format
        """
        if isinstance(raw_msg, str):       # 首先判断变量是否为字符串
            try:
                json.loads(raw_msg, encoding='utf-8')
            except ValueError:
                return False
            return True
        else:
            return False

if __name__ == "__main__":
    slot = Slot("FA53CSR02947", "mobileqq")

    print slot.getAvailableSlot(25)
    #id = slot.getEmpty()
    #slot.backup(id, "XXXX%s" % str(id))
    #print(slot.getSlots())
    #print(slot.getSlotInfo("2"))