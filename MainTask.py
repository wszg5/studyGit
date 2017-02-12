#!/usr/bin/env python
# coding:utf-8
import os, sys, time, re, csv
import util
import multiprocessing
import traceback
import json
from const import const
import sys, getopt

#s:server_ip
#r:repo_ip
#c:redis_cache_ip
opts, args = getopt.getopt(sys.argv[1:], "s:r:c:", ["server_ip=", "repo_ip=", "redis_ip="])
for op, value in opts:
    if op == "-s" or  op == "--server_ip" :
        const.SERVER_IP = value
    elif op == "-r" or  op == "--repo_ip" :
        const.REPO_API_IP = value
    elif op == "-c" or  op == "--redis_ip" :
        const.REDIS_SERVER = value


try:
    rst = int(util.exccmd("awk -F. '{print $1}' /proc/uptime"))
    if rst < 500:
        time.sleep(const.WAIT_START_TIME)
    else:
        print '系统已启动超过500秒，不再等待，直接拉起'
except:
    #noting to do
    ok = 'ok'


from dbapi import dbapi
import sys
reload(sys)
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
        #for i in deviceIds:
            #logger.info('ID为%s' % i)
        return deviceIds
    else:
        logger.error('没有找到手机，请检查')
        return []
        # needcount:需要安装的apk数量，默认为0，既安所有
def runStep(d, z, step):
    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"%s\""%step["name"])
    pluginName = step["mid"]
    plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
    clazz = plugin.getPluginClass()
    o = clazz()
    if step.has_key("arg"):
        o.action(d, z, json.loads(step["arg"]))
def deviceTask(deviceid, port, zport):
    taskid = dbapi.GetDeviceTask(deviceid)
    from uiautomator import Device
    from zservice import ZDevice
    if  taskid :
        task = dbapi.GetTask(taskid)
        if (task and task.get("status") and task["status"] == "running"):
            d = Device(deviceid, port)
            #d.server.adb.cmd("uninstall", "jp.co.cyberagent.stf")
            z = ZDevice(deviceid, zport)
            while True:
                steps = dbapi.GetTaskSteps(taskid)
                #设置zime输入法
                d.server.adb.cmd("shell","ime set com.zunyun.zime/.ZImeService").wait()
                d.server.adb.cmd("shell","am broadcast -a com.zunyun.zime.unlock").wait()
                for step in steps:
                    try:
                        runStep(d, z, step)
                    except Exception:
                        logger.error(step)
                        logger.error(traceback.format_exc())
                        time.sleep(3)
                    #检查设备对应的任务状态
                    new_taskid = dbapi.GetDeviceTask(deviceid)
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
        except Exception:
            logger.error(traceback.format_exc())
        time.sleep(5)
    print("%s thread finished"%deviceid)



def StartProcess(deviceid):
    device_port = portDict[deviceid]
    port = device_port["port"]
    zport = device_port["zport"]
    processDict[deviceid] = multiprocessing.Process(target=deviceThread, args=(deviceid, port, zport))
    processDict[deviceid].name = deviceid
    processDict[deviceid].daemon = True
    processDict[deviceid].start()



def installApk(deviceid):
    device_port = portDict[deviceid]
    zport = device_port["zport"]
    from zservice import ZDevice
    z = ZDevice(deviceid, zport)
    z.server.install()


processDict = {}
portDict = {}
installDict = {}




if __name__ == "__main__":
    cleanEnv()
    logger = util.logger
    port = 30000
    zport = 33000
    while True:
        try:
            devicelist = finddevices()
            for device in devicelist:
                deviceid = device

                if (not portDict.has_key(deviceid)):
                    port = port + 1
                    zport = zport + 1
                    portDict[deviceid] = {"port": port, "zport": zport}

                if (not installDict.has_key(deviceid)):
                    installDict[deviceid] = True
                    import threading
                    t = threading.Thread(target=installApk, args=(deviceid,))
                    t.setDaemon(True)
                    t.start()

                taskid = dbapi.GetDeviceTask(deviceid)
                if taskid:
                    task = dbapi.GetTask(taskid)
                    if (task and task.get("status") and task["status"] == "running"):
                        if (not processDict.has_key(deviceid)):
                            StartProcess(deviceid)
                        else:
                            p = processDict[deviceid]
                            if (not p.is_alive()):
                                StartProcess(deviceid)
                    else:
                        if (processDict.has_key(deviceid) and processDict.get(deviceid).is_alive()):
                            processDict[deviceid].terminate()
        except Exception:
            logger.error(traceback.format_exc())
        time.sleep(30)
