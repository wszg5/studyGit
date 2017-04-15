#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, time, re, json

from const import const
import signal
from zcache import cache
import util
import traceback
import datetime


logger = util.logger
from dbapi import dbapi

class phoneTask:
    def __init__(self, serial):
        self.serial = serial
        self.d = None
        self.z = None
        self.taskid = None
        self.task = None

    def runStep(self, d, step):
        self.z.toast("步骤:%s , 任务:%s" % (step["name"],self.task["name"]))
        pluginName = step["mid"]
        plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
        clazz = plugin.getPluginClass()
        o = clazz()
        if step.has_key("arg"):
            o.action(d, self.z, json.loads(step["arg"]))

    def handler(self, signum, frame):
  #      if self.task["show_task_info"]:
        self.z.cmd("shell", "am broadcast -a com.zunyun.zime.action --es ac \"Task\" --es sac \"running\" --es task_name \"%s\"" % self.task["name"]);


        self.z.cmd("shell",
           "am broadcast -a com.zunyun.zime.action --es ac \"Task\" --es sac \"show_window\" --es task_name \"%s\"" %
           self.task["name"]);

#        else:
 #           self.z.cmd("shell", "am broadcast -a com.zunyun.zime.action --es ac \"Task\" --es sac \"stop\"");

        key = 'timeout_%s' % self.serial
        activeTime = cache.get(key)
        if (activeTime is None):
            self.z.heartbeat()
            return

        checkTime = (datetime.datetime.now() - datetime.datetime(2017, 1 ,1)).seconds
        #print checkTime - int(activeTime)
        if (checkTime - int(activeTime)) > 120 :
            raise AssertionError
        elif (checkTime - int(activeTime)) > 60 :
            self.z.toast("模块暂停时间过长，即将强制跳过。。。")

        signal.signal(signal.SIGALRM, self.handler)
        signal.alarm(60)

    def deviceTask(self, deviceid, port, zport):
        self.taskid = dbapi.GetDeviceTask(deviceid)
        from uiautomator import Device
        from zservice import ZDevice
        if self.taskid:
            self.task = dbapi.GetTask(self.taskid)
            if (self.task and self.task.get("status") and self.task["status"] == "running"):
                self.z = ZDevice(deviceid, zport)
                self.z.cmd("shell",
                           "am broadcast -a com.zunyun.zime.action --es ac \"Task\" --es sac \"running\" --es task_name \"%s\"" %
                           self.task["name"]);

                self.z.cmd("shell",
                           "am broadcast -a com.zunyun.zime.action --es ac \"Task\" --es sac \"show_window\" --es task_name \"%s\"" %
                           self.task["name"]);
                self.d = Device(deviceid, port)

                while True:
                    steps = dbapi.GetTaskSteps(self.taskid)
                    # 设置zime输入法
                    self.d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").communicate()
                    self.d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.unlock").communicate()
                    for step in steps:
                        try:
                            self.z.heartbeat()
                            signal.signal(signal.SIGALRM, self.handler)
                            signal.alarm(60)
                            self.runStep(self.d, step)
                            signal.alarm(0)
                        except AssertionError:
                            print "ERROR::::%s Moudle execute timeout for 120 seconds" % step["name"]
                        except Exception:
                            logger.error(step)
                            logger.error(traceback.format_exc())
                            time.sleep(3)
                        # 检查设备对应的任务状态
                        new_taskid = dbapi.GetDeviceTask(deviceid)
                        if new_taskid is None or new_taskid == "":  # 任务中删除了该设备
                            return
                        if (new_taskid != self.taskid):  # 设备对应的taskid发生了变化
                            return
                        task = dbapi.GetTask(new_taskid)
                        if task.get("status") != "running":  # 任务状态已停止
                            return
        else:
            time.sleep(5)

    def deviceThread(self, deviceid, port, zport):
        while True:
            try:
                self.deviceTask(deviceid, port, zport)
            except Exception:
                logger.error(traceback.format_exc())
            time.sleep(5)
        print("%s thread finished" % deviceid)


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
