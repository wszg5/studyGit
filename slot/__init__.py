#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbapi import dbapi
from const import const
import  os

import util

"""Python wrapper for Zunyun Service."""
class slot:
    def __init__(self, type):
        self.dbapi = dbapi()
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

        elif (self.type == "qqlite"):
            self.package = "com.tencent.qqlite"
            self.files = ['files/ConfigStore2.dat']
            self.folders = ['files/user']
            self.maxSlot = const.MAX_SLOTS_QQLITE

        elif (self.type == "eim"):
            self.package = "com.tencent.eim"
            self.files = ['files/ConfigStore2.dat']
            self.folders = ['files/user','databases']
            self.maxSlot = const.MAX_SLOTS_EIM

        else:
            raise SyntaxError("目前还不支持%s卡槽"%self.type)

        self.maxSlot = int(self.maxSlot)

    def backup(self, d, name, info):
        d.server.adb.cmd("shell", "su -c 'chmod -R 777 /data/data/%s/'"%self.package).communicate()
        d.server.adb.cmd("shell", "su -c 'mkdir /data/data/com.zy.bak/'").communicate()
        d.server.adb.cmd("shell", "su -c 'chmod -R 777 /data/data/com.zy.bak/'").communicate()
        d.server.adb.cmd("shell", "su -c 'mkdir /data/data/com.zy.bak/%s'"%self.type).communicate()
        d.server.adb.cmd("shell", "su -c 'rm -r -f /data/data/com.zy.bak/%s/%s/'"%(self.type,name)).communicate()
        d.server.adb.cmd("shell", "su -c 'mkdir /data/data/com.zy.bak/%s/%s'"%(self.type,name)).communicate()
        d.server.adb.cmd("shell", "su -c 'chmod -R 777 /data/data/com.zy.bak/'").communicate()

        for folder in self.folders:
            targetPath = '/data/data/com.zy.bak/%s/%s/%s' % (self.type, name, folder)
            targetPath = os.path.dirname(targetPath)
            d.server.adb.cmd("shell", "su -c 'mkdir -p %s'" % targetPath).communicate()
            cmd = "cp -f -r -p /data/data/%s/%s/  %s" % (self.package, folder, targetPath)
            d.server.adb.cmd("shell", "su -c '%s'"%cmd).communicate()

            #d.server.adb.cmd("shell", "su -c 'cp -r -f -p /data/data/%s/%s/  /data/data/com.zy.bak/%s/%s/%s'" % (self.package, folder, self.type, name, folder)).communicate()
        for file in self.files:
            targetFile = '/data/data/com.zy.bak/%s/%s/%s'%(self.type, name, file)
            targetPath = os.path.dirname(targetFile)
            d.server.adb.cmd("shell", "su -c 'mkdir -p %s'" % targetPath).communicate()
            cmd = "cp -f  /data/data/%s/%s  %s" % (self.package, file, targetFile)
            d.server.adb.cmd("shell", "su -c '%s'" %cmd ).communicate()

        #d.server.adb.cmd("shell", "mkdir /data/data/com.zy.bak/%s/zy_name_%s_name/"%(self.type,name) ).wait()

        self.dbapi.SaveSlotInfo(d.server.adb.device_serial(), self.type, name, "false", "true", info)

    def restore(self, d, name, target=None):
        if target is None:
            target = self.package

        d.server.adb.cmd("shell", "pm clear %s"%target).communicate()
        d.server.adb.cmd("shell", "su -c 'chmod -R 777 /data/data/%s/'" % target).communicate()
        d.server.adb.cmd("shell", "su -c 'chmod -R 777 /data/data/com.zy.bak/'").communicate()
        #d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()
        #d.server.adb.cmd("shell", "rm -r -f  /data/data/com.zy.bak/%s/zy_name_*"%type).wait()
        for folder in self.folders:
            targetPath = '/data/data/%s/%s' % (target, folder)
            targetPath = os.path.dirname(targetPath)
            d.server.adb.cmd("shell", "su -c 'mkdir -p %s'" % targetPath).communicate()
            cmd = "cp -f -r -p /data/data/com.zy.bak/%s/%s/%s/  %s" % (self.type, name, folder, targetPath)
            d.server.adb.cmd("shell", "su -c '%s'" % cmd).communicate()
            d.server.adb.cmd("shell", "su -c 'chmod -R 777 %s'" % targetPath).communicate()
        #for folder in self.folders:
           # d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/%s/%s/%s/ /data/data/%s/"%(self.type, name, folder, self.package)).communicate()

        for file in self.files:
            targetFile = '/data/data/%s/%s'%(target, file)
            targetPath = os.path.dirname(targetFile)
            d.server.adb.cmd("shell", "su -c 'mkdir -p %s'" % targetPath).communicate()
            d.server.adb.cmd("shell", "su -c 'cp -f /data/data/com.zy.bak/%s/%s/%s %s'"%(self.type, name, file, targetFile)).communicate()
            d.server.adb.cmd("shell", "su -c 'chmod -R 777 %s'" % targetFile).communicate()

        #d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/databases/ /data/data/com.tencent.tim/"%name).wait()

        #d.server.adb.cmd("shell", "mkdir /data/data/com.zy.bak/%s/zy_name_%s_name/"%(self.type,name) ).wait()
        self.dbapi.PickSlot(d.server.adb.device_serial(), self.type, name)


    def getEmpty(self, d):
        slots = self.dbapi.ListSlots(d.server.adb.device_serial(), self.type)
        if (len(slots)  == 0):
            return 1
        logger = util.logger
        if (len(slots) < self.maxSlot ):
            maxSlot = slots[-1]
            maxName = maxSlot["name"]
            return int(maxName) + 1
        for slot in slots:
            if (slot["empty"] == "true"):
                return int(slot["name"])
        return 0

    def getSlot(self, d, interval):
        slots = self.dbapi.ListSlotsInterval(d.server.adb.device_serial(), self.type, int(interval) * 60)
        if (len(slots) > 0):
            return int(slots[0]["name"])
        return 0

    def getSlotInfo(self, d, name):
        return self.dbapi.GetSlotInfo(d.server.adb.device_serial(), self.type, name)



def getPluginClass():
    return slot

if __name__ == "__main__":

    clazz = getPluginClass()
    o = clazz("mobileqq")
    from uiautomator import Device

    d = Device("FA48VSR03651")
    #d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").wait()
    #slots = o.getSlot(d, 23)
    #o.backup(d,1,"asdfasfd")
    #o.getEmptySlot(d)

    o.restore(d, 1)
    #d.dump(compressed=False)
    #args = {"repo_cate_id":"131","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    #o.action(d, args)
