#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, time, re, json

from const import const
import signal
from zcache import cache
import util
import traceback
import datetime
import multiprocessing

logger = util.logger
from dbapi import dbapi

class virtualTask:
    def __init__(self, serial):
        self.serial = serial
        self.processDict = None
        self.taskid = None
        self.task = None

    def finddevices(self):
        return dbapi.GetBusyVirtualDevices()

    @staticmethod
    def run(self):
        while True:
            cache.set("ztask_virtual_active_time", datetime.datetime.now())
            try:
                devicelist = self.finddevices()
                for device in devicelist:
                    deviceid = device["serial"]
                    taskid = device["task_id"]
                    if taskid:
                        task = dbapi.GetTask(taskid)
                        if task and task.get("status") and task["status"] == "running":
                            if deviceid not in self.processDict:  # 进程从未启动
                                self.startProcess(deviceid)
                            else:
                                p = self.processDict[deviceid]
                                if not p.is_alive():  # 进程已退出，从新启动进程
                                    self.startProcess(deviceid)
                                else:  # 检查进程心跳是否超过3分钟
                                    key = 'timeout_%s' % deviceid
                                    activeTime = cache.get(key)
                                    if activeTime:
                                        checkTime = (datetime.datetime.now() - datetime.datetime(2017, 1, 1)).seconds
                                        if (checkTime - int(activeTime)) > 180:  # 进程心跳时间超过3分种，重启进程
                                            self.processDict[deviceid].terminate()
                                            self.startProcess(deviceid)
                        else:
                            if self.processDict.has_key(deviceid) and self.processDict.get(deviceid).is_alive():
                                self.processDict[deviceid].terminate()
                                del self.processDict[deviceid]
                    elif deviceid in self.processDict:
                        self.processDict[device].terminate()
                        del self.processDict[deviceid]
            except Exception:
                logger.error(traceback.format_exc())
            time.sleep(10)


    def runStep(self, d, step):
        pluginName = step["mid"]
        plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
        clazz = plugin.getPluginClass()
        o = clazz()
        if step.has_key("arg"):
            o.action(None, None, json.loads(step["arg"]))

    def handler(self, signum, frame):
        key = 'timeout_%s' % self.serial
        activeTime = cache.get(key)
        if (activeTime is None):
            self.z.heartbeat()
            return
        checkTime = (datetime.datetime.now() - datetime.datetime(2017, 1 ,1)).seconds
        #print checkTime - int(activeTime)
        if (checkTime - int(activeTime)) > 120 :
            raise AssertionError

        signal.signal(signal.SIGALRM, self.handler)
        signal.alarm(60)

    def deviceTask(self, deviceid):
        self.taskid = dbapi.GetDeviceTask(deviceid)
        if self.taskid:
            self.task = dbapi.GetTask(self.taskid)
            if (self.task and self.task.get("status") and self.task["status"] == "running"):
                while True:
                    steps = dbapi.GetTaskSteps(self.taskid)
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

    def virtualDeviceMainProcess(self, deviceid):
        while True:
            try:
                self.deviceTask(deviceid)
            except Exception:
                logger.error(traceback.format_exc())
            time.sleep(5)
        print("%s thread finished" % deviceid)


    def startProcess(self, deviceid):
        self.processDict[deviceid] = multiprocessing.Process(target=self.virtualDeviceMainProcess, args=(deviceid))
        self.processDict[deviceid].name = deviceid
        self.processDict[deviceid].daemon = True
        self.processDict[deviceid].start()
