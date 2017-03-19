#!/usr/bin/env python
# coding:utf-8
import os, datetime, time, re
import util
import multiprocessing
import traceback
import json
from const import const
import sys, getopt

# s:server_ip
# r:repo_ip
# c:redis_cache_ip
opts, args = getopt.getopt(sys.argv[1:], "s:r:c:t:w:m:q:e",
                           ["server_ip=", "tim_slots=", "wechat_slots=", "mobile_slots=", "qqlite_slots=", "eim_slots=",
                            "repo_ip=", "redis_ip="])
for op, value in opts:
    if op == "-s" or op == "--server_ip":
        const.SERVER_IP = value
    elif op == "-r" or op == "--repo_ip":
        const.REPO_API_IP = value
    elif op == "-c" or op == "--redis_ip":
        const.REDIS_SERVER = value
    elif op == "-t" or op == "--tim_slots":
        const.MAX_SLOTS_TIM = int(value)
    elif op == "-w" or op == "--wechat_slots":
        const.MAX_SLOTS_WECHAT = int(value)
    elif op == "-m" or op == "--mobile_slots":
        const.MAX_SLOTS_MOBILEQQ = int(value)
    elif op == "-q" or op == "--qqlite_slots":
        const.MAX_SLOTS_QQLITE = int(value)
    elif op == "-e" or op == "--eim_slots":
        const.MAX_SLOTS_EIM = int(value)
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from dbapi import dbapi


from zcache import cache
cache.set("ztask_active_time", datetime.datetime.now())

try:
    rst = int(util.exccmd("awk -F. '{print $1}' /proc/uptime"))
    if rst < 500:
        dbapi.log_warn("" , "任务暂缓%s秒后启动" % const.MAX_SLOTS_WECHAT , "系统已经成功启动，任务将在%s秒后启动，请等待..." % const.MAX_SLOTS_WECHAT )
        time.sleep(const.WAIT_START_TIME)
    else:
        print '系统已启动超过500秒，不再等待，直接拉起'
except:
    # noting to do
    ok = 'ok'


optpath = os.getcwd()  # 获取当前操作目录
imgpath = os.path.join(optpath, 'img')  # 截图目录



def cleanEnv():
    # os.system('adb kill-server')
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


def finddevices():
    deviceIds = []
    adb_cmd = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", 'adb devices')
    rst = util.exccmd(adb_cmd)
    devices = re.findall(r'(.*?)\s+device', rst)
    if len(devices) > 1:
        deviceIds = devices[1:]
        logger.info('共找到%s个手机' % str(len(devices) - 1))
        # for i in deviceIds:
        # logger.info('ID为%s' % i)
        return deviceIds
    else:
        logger.error('没有找到手机，请检查')
        return []
        # needcount:需要安装的apk数量，默认为0，既安所有


def startProcess(deviceid):
    from phoneTask import phoneTask

    device_port = portDict[deviceid]
    port = device_port["port"]
    zport = device_port["zport"]
    t = phoneTask(deviceid)
    processDict[deviceid] = multiprocessing.Process(target=t.deviceThread, args=(deviceid, port, zport))
    processDict[deviceid].name = deviceid
    processDict[deviceid].daemon = True
    processDict[deviceid].start()


def installApk(deviceid):
    device_port = portDict[deviceid]
    zport = device_port["zport"]
    from zservice import ZDevice
    z = ZDevice(deviceid, zport)
    z.server.adb.cmd("shell", "su -c 'rm -f /sdcard/NanoHTTPD-*'").communicate()
    z.server.adb.cmd("shell", "su -c 'rm -f /sdcard/share_*'").communicate()
    # 规避解决微信卡死问题
    pkginfo = z.server.adb.package_info("com.tencent.mm")
    if pkginfo is not None:
        z.server.adb.cmd("shell", "su -c 'rm -rf /data/data/com.tencent.mm/tinker/*'").communicate()
        z.server.adb.cmd("shell", "su -c 'mkdir -p /data/data/com.tencent.mm/tinker/'").communicate()
        z.server.adb.cmd("shell", "su -c 'chmod 000 /data/data/com.tencent.mm/tinker/'").communicate()
    z.server.install()


processDict = {}
portDict = {}
installDict = {}



if __name__ == "__main__":
    cleanEnv()
    try:
        file_object = open('ztask.info')
        zinfo = file_object.read()
        zinfo = json.loads(zinfo)
        cache.set("ZTASK_VERSION", zinfo["version"])
    finally:
        cache.set("ZTASK_VERSION", "UNKNOW")
        file_object.close()

    #启动虚拟任务子进程
    import virtualTask
    multiprocessing.Process(target=virtualTask.virtualTask.run)

    logger = util.logger
    port = 30000
    zport = 32000
    while True:
        cache.set("ztask_active_time", datetime.datetime.now())
        try:
            devicelist = finddevices()
            for device in devicelist:
                deviceid = device
                if not portDict.has_key(deviceid):
                    port += 1
                    zport += 1
                    portDict[deviceid] = {"port": port, "zport": zport}

                if deviceid not in installDict:
                    installDict[deviceid] = True
                    import threading
                    t = threading.Thread(target=installApk, args=(deviceid,))
                    t.setDaemon(True)
                    t.start()

                taskid = dbapi.GetDeviceTask(deviceid)
                if taskid:
                    task = dbapi.GetTask(taskid)
                    if task and task.get("status") and task["status"] == "running":
                        if deviceid not in processDict:  #进程从未启动
                            startProcess(deviceid)
                        else:
                            p = processDict[deviceid]
                            if not p.is_alive():      #进程已退出，从新启动进程
                                startProcess(deviceid)
                            else:                     #检查进程心跳是否超过3分钟
                                key = 'timeout_%s' % deviceid
                                activeTime = cache.get(key)
                                if activeTime:
                                   checkTime = (datetime.datetime.now() - datetime.datetime(2017, 1, 1)).seconds
                                   if (checkTime - int(activeTime)) > 180:  #进程心跳时间超过3分种，重启进程
                                       processDict[deviceid].terminate()
                                       startProcess(deviceid)
                    else:
                        if processDict.has_key(deviceid) and processDict.get(deviceid).is_alive():
                            processDict[deviceid].terminate()
                            del processDict[deviceid]
            #检查运行中的进程是否有手机被拔出电脑
            for device in processDict:
                if device not in devicelist:
                    dbapi.log_warn(device , "设备被拔出，运行中任务被强制停止")
                    processDict[device].terminate()
                    del processDict[deviceid]

        except Exception:
            logger.error(traceback.format_exc())
        time.sleep(10)
