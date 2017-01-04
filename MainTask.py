# coding:utf-8

import os, sys, time, re, csv
import util

import traceback
import threading
import json

<<<<<<< HEAD
pool = RethinkPool(max_conns=120, initial_conns=10, host='192.168.1.33',
                     port=28015,
                     db='stf')
=======
from dbapi import dbapi
<<<<<<< HEAD
from const import const
>>>>>>> 8f9b11ca2ef866b4e9aad3b3b58faea961148ab2
=======
import sys

reload(sys)
>>>>>>> 6bd88d048104b7d8df072cc8c10e176fe304b9da

sys.setdefaultencoding('utf8')

optpath = os.getcwd()  # 获取当前操作目录
imgpath = os.path.join(optpath, 'img')  # 截图目录
dbapi = dbapi()

def cleanEnv():
    #os.system('adb kill-server')
    needClean = ['log.log', 'img', 'tmp']
    pwd = os.getcwd()
    for i in needClean:
        delpath = os.path.join(pwd, i)
        if os.path.isfile(delpath):
            cmd = 'rm -rf "%s"' % delpath
            os.system(cmd)
        elif os.path.isdir(delpath):
            cmd = 'rm -rf "%s"' % delpath
            os.system(cmd)
    if not os.path.isdir('tmp'):
        os.mkdir('tmp')


def runwatch(d, data):
    times = 120
    while True:
        if data == 1:
            return True
        # d.watchers.reset()
        d.watchers.run()
        times -= 1
        if times == 0:
            break
        else:
            time.sleep(0.5)




def finddevices():
    deviceIds = []
    adb_cmd = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", 'adb devices')
    rst = util.exccmd(adb_cmd)
    devices = re.findall(r'(.*?)\s+device', rst)
    if len(devices) > 1:
        deviceIds = devices[1:]
        logger.info('共找到%s个手机' % str(len(devices) - 1))
        for i in deviceIds:
            logger.info('ID为%s' % i)
        return deviceIds
    else:
        logger.error('没有找到手机，请检查')
        return []

        # needcount:需要安装的apk数量，默认为0，既安所有



def runStep(d, z, step):
    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"%s\""%step["name"])
    pluginName = step["mid"]
    plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
    clazz = plugin.getPluginClass()
    o = clazz()
    if step.has_key("arg"):
        o.action(d, z, json.loads(step["arg"]))

def deviceTask(deviceid, port, zport):
    device = dbapi.GetDevice(deviceid)
    taskid = device.get("task_id")

    from uiautomator import Device
    from zservice import ZDevice

    if  taskid :
        task = dbapi.GetTask(taskid)

        if (task and task.get("status") and task["status"] == "running"):
            d = Device(deviceid, port)
            util.doInThread(runwatch, d, 0, t_setDaemon=True)
            d.server.adb.cmd("uninstall", "jp.co.cyberagent.stf")
            d.server.adb.cmd("uninstall", "jp.co.cyberagent.stf")

            z = ZDevice(deviceid, zport)
            while True:
                steps = dbapi.GetTaskSteps(taskid)

                #设置zime输入法
                d.server.adb.cmd("shell",
                             "ime set com.zunyun.qk/.ZImeService").wait()
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.qk.unlock").wait()

                for step in steps:
                    try:

                        runStep(d, z, step)
                    except Exception, e:
                        logger.error(step)
                        logger.error(traceback.format_exc())
                        time.sleep(3)

                    #检查设备对应的任务状态
                    device = dbapi.GetDevice(deviceid)
                    new_taskid = device.get("task_id")
                    if new_taskid is None or new_taskid == "": #任务中删除了该设备
                        return
                    if (new_taskid != taskid): #设备对应的taskid发生了变化
                        return

                    task = dbapi.GetTask(new_taskid)
                    if task.get("status") != "running": #任务状态已停止
                        return
    else :
        time.sleep(5)



def deviceThread(deviceid, port, zport):
    while True:
        try:

            deviceTask(deviceid, port, zport)
        except Exception, e:
            logger.error(traceback.format_exc())
        time.sleep(5)
    print("%s thread finished"%deviceid)


# 需要配置好adb 环境变量
# 1.先确定有几台手机
# 2.再确定有多少个应用
# 3.先安装mkiller,启动mkiller
# 4.再安装测试的样本
# 5.检查是否有取消安装的按钮出现，出现说明测试通过，没出现说明测试失败
if __name__ == "__main__":
    cleanEnv()
    logger = util.logger
    port = 30000
    zport = 33000
    threadDict = {}
    while True:
        devicelist = dbapi.finddevices()
        for device in devicelist:
            deviceid = device["serial"]
            if (threadDict.has_key(deviceid)): continue
            port = port + 1
            zport = zport + 1
            threadDict[deviceid] = threading.Thread(target=deviceThread, args=(deviceid, port, zport))
            threadDict[deviceid].setName(deviceid)
            threadDict[deviceid].setDaemon(True)
            threadDict[deviceid].start()

        #for k,v in threadDict: ##循环线程dictionary，对于已经被移除的手机删除线程
          #  t.
         #   x =5
        time.sleep(60)