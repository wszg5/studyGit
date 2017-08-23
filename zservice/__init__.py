#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python wrapper for Zunyun Service."""
import base64
import sys
import os
import subprocess
import time
import itertools
import json
import hashlib
import socket
import re
import collections
import uuid
import requests,datetime

from adb import Adb
from const import const
from zcache import cache

DEVICE_PORT = int(os.environ.get('ZSERVICE_DEVICE_PORT', '19008'))
LOCAL_PORT = int(os.environ.get('ZSERVICE_LOCAL_PORT', '19008'))

if 'localhost' not in os.environ.get('no_proxy', ''):
    os.environ['no_proxy'] = "localhost,%s" % os.environ.get('no_proxy', '')

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2
try:
    from httplib import HTTPException
except:
    from http.client import HTTPException
try:
    if os.name == 'nt':
        import urllib3
except:  # to fix python setup error on Windows.
    pass

__author__ = "ZunYun"
__all__ = ["device", "Device", "rect", "point", "Selector", "JsonRPCError"]


def U(x):
    if sys.version_info.major == 2:
        return x.decode('utf-8') if type(x) is str else x
    elif sys.version_info.major == 3:
        return x


def param_to_property(*props, **kwprops):
    if props and kwprops:
        raise SyntaxError("Can not set both props and kwprops at the same time.")

    class Wrapper(object):

        def __init__(self, func):
            self.func = func
            self.kwargs, self.args = {}, []

        def __getattr__(self, attr):
            if kwprops:
                for prop_name, prop_values in kwprops.items():
                    if attr in prop_values and prop_name not in self.kwargs:
                        self.kwargs[prop_name] = attr
                        return self
            elif attr in props:
                self.args.append(attr)
                return self
            raise AttributeError("%s parameter is duplicated or not allowed!" % attr)

        def __call__(self, *args, **kwargs):
            if kwprops:
                kwargs.update(self.kwargs)
                self.kwargs = {}
                return self.func(*args, **kwargs)
            else:
                new_args, self.args = self.args + list(args), []
                return self.func(*new_args, **kwargs)
    return Wrapper


class JsonRPCError(Exception):

    def __init__(self, code, message):
        self.code = int(code)
        self.message = message

    def __str__(self):
        return "JsonRPC Error code: %d, Message: %s" % (self.code, self.message)


class JsonRPCMethod(object):

    if os.name == 'nt':
        try:
            pool = urllib3.PoolManager()
        except:
            pass

    def __init__(self, url, method, timeout=30):
        self.url, self.method, self.timeout = url, method, timeout

    def __call__(self, *args, **kwargs):
        if args and kwargs:
            raise SyntaxError("Could not accept both *args and **kwargs as JSONRPC parameters.")
        data = {"jsonrpc": "2.0", "method": self.method, "id": self.id()}
        if args:
            data["params"] = args
        elif kwargs:
            data["params"] = kwargs
        jsonresult = {"result": ""}
        if os.name == "nt":
            res = self.pool.urlopen("POST",
                                    self.url,
                                    headers={"Content-Type": "application/json"},
                                    body=json.dumps(data).encode("utf-8"),
                                    timeout=self.timeout)
            jsonresult = json.loads(res.data.decode("utf-8"))
        else:
            result = None
            try:
                req = urllib2.Request(self.url,
                                      json.dumps(data).encode("utf-8"),
                                      {"Content-type": "application/json"})
                result = urllib2.urlopen(req, timeout=self.timeout)
                jsonresult = json.loads(result.read().decode("utf-8"))
            finally:
                if result is not None:
                    result.close()
        if "error" in jsonresult and jsonresult["error"]:
            raise JsonRPCError(
                jsonresult["error"]["code"],
                "%s: %s" % (jsonresult["error"]["data"]["exceptionTypeName"], jsonresult["error"]["message"])
            )
        return jsonresult["result"]

    def id(self):
        m = hashlib.md5()
        m.update(("%s at %f" % (self.method, time.time())).encode("utf-8"))
        return m.hexdigest()


class JsonRPCClient(object):

    def __init__(self, url, timeout=30, method_class=JsonRPCMethod):
        self.url = url
        self.timeout = timeout
        self.method_class = method_class

    def __getattr__(self, method):
        return self.method_class(self.url, method, timeout=self.timeout)


_init_local_port = LOCAL_PORT - 1


def next_local_port(adbHost=None):
    def is_port_listening(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((str(adbHost) if adbHost else '127.0.0.1', port))
        s.close()
        return result == 0
    global _init_local_port
    _init_local_port = _init_local_port + 1 if _init_local_port < 32764 else LOCAL_PORT
    while is_port_listening(_init_local_port):
        _init_local_port += 1
    return _init_local_port


class NotFoundHandler(object):

    '''
    Handler for UI Object Not Found exception.
    It's a replacement of UiAutomator watcher on device side.
    '''

    def __init__(self):
        self.__handlers = collections.defaultdict(lambda: {'on': True, 'handlers': []})

    def __get__(self, instance, type):
        return self.__handlers[instance.adb.device_serial()]


class AutomatorServer(object):

    """start and quit rpc server on device.
    """

    __sh_files = {
        "install.sh": "libs/install.sh"
    }

    __apk_files = ["libs/zime.apk"]
    # Used for check if installed
    __apk_vercode = '1.9.6'
    __zserial_vercode = '3.2.2'
    __apk_pkgname = 'com.zunyun.zime'

    __sdk = 0

    handlers = NotFoundHandler()  # handler UI Not Found exception

    def __init__(self, serial=None, local_port=None, device_port=None, adb_server_host=None, adb_server_port=None):
        self.zservice_process = None
        self.adb = Adb(serial=serial, adb_server_host=adb_server_host, adb_server_port=adb_server_port)
        self.device_port = int(device_port) if device_port else DEVICE_PORT
        if local_port:
            self.local_port = local_port
        else:
            try:  # first we will try to use the local port already adb forwarded
                for s, lp, rp in self.adb.forward_list():
                    if s == self.adb.device_serial() and rp == 'tcp:%d' % self.device_port:
                        self.local_port = int(lp[4:])
                        break
                else:
                    self.local_port = next_local_port(adb_server_host)
            except:
                self.local_port = next_local_port(adb_server_host)

    def getPackageVersion(self):
        pkginfo = self.adb.package_info(self.__apk_pkgname)
        if pkginfo is None:
            return None
        return pkginfo['version_name']


    def need_install(self):
        pkginfo = self.adb.package_info(self.__apk_pkgname)
        if pkginfo is None:
            return True
        if pkginfo['version_name'] != self.__apk_vercode:
            return True

        pkginfo = self.adb.package_info('com.sollyu.xposed.hook.model')
        if pkginfo is None:
            return True
        if pkginfo['version_name'] != self.__zserial_vercode:
            return True


        pkginfo = self.adb.package_info('de.robv.android.xposed.installer')
        out = self.adb.cmd("shell","\"su -c 'cat /data/data/de.robv.android.xposed.installer/shared_prefs/enabled_modules.xml'\"").communicate()[0].decode('utf-8')
        if pkginfo is not None and out.find("<int name=\"com.zunyun.zime\" value=\"1\" />") == -1:
            return True
        if pkginfo is not None and out.find("<int name=\"com.sollyu.xposed.hook.model\" value=\"1\" />") == -1:
            return True
        return False

    def install(self):
        base_dir = os.path.dirname(__file__)
        if self.need_install():
            self.adb.cmd("shell", "am force-stop com.zunyun.zime").communicate()  # 强制停止
            self.adb.cmd("shell", "su -c 'rm /data/local/tmp/install.sh'").communicate()
            self.adb.cmd("shell", "su -c 'chmod - R 777 /data/data/de.robv.android.xposed.installer/'").communicate()

            self.adb.cmd("shell", "su -c 'rm /data/local/tmp/zime.apk'").communicate()
            #self.adb.cmd("shell", " ").communicate()
            self.adb.cmd("shell", "pm uninstall com.zunyun.zime").communicate()
            filename = os.path.join(base_dir, 'libs/install.sh')
            self.adb.cmd("push", filename, "/data/local/tmp/").communicate()
            filename = os.path.join(base_dir, 'libs/zime.apk')
            self.adb.cmd("push", filename, "/data/local/tmp/").communicate()
            #if self.getPackageVersion() != self.__apk_vercode:
            filename = os.path.join(base_dir, 'libs/zserial.apk')
            self.adb.run_cmd("install -r %s" % filename)

            self.adb.cmd("shell", "su -c 'chmod 777 /data/local/tmp/install.sh'").communicate()
            self.adb.cmd("shell", "su -c 'sh /data/local/tmp/install.sh'").communicate()
            self.adb.cmd("shell", "su -c 'chmod - R 777 /data/data/de.robv.android.xposed.installer/'").communicate()

            self.adb.cmd("shell", "reboot").communicate()





    @property
    def jsonrpc(self):
        return self.jsonrpc_wrap(timeout=int(os.environ.get("jsonrpc_timeout", 90)))

    def jsonrpc_wrap(self, timeout):
        server = self
        ERROR_CODE_BASE = -32000

        def _JsonRPCMethod(url, method, timeout, restart=True):
            _method_obj = JsonRPCMethod(url, method, timeout)

            def wrapper(*args, **kwargs):
                URLError = urllib3.exceptions.HTTPError if os.name == "nt" else urllib2.URLError
                try:
                    return _method_obj(*args, **kwargs)
                except (URLError, socket.error, HTTPException) as e:
                    if restart:
                        server.stop()
                        server.start(timeout=30)
                        return _JsonRPCMethod(url, method, timeout, False)(*args, **kwargs)
                    else:
                        raise
                except JsonRPCError as e:
                    if e.code >= ERROR_CODE_BASE - 1:
                        server.stop()
                        server.start()
                        return _method_obj(*args, **kwargs)
                    elif e.code == ERROR_CODE_BASE - 2 and self.handlers['on']:  # Not Found
                        try:
                            self.handlers['on'] = False
                            # any handler returns True will break the left handlers
                            any(handler(self.handlers.get('device', None)) for handler in self.handlers['handlers'])
                        finally:
                            self.handlers['on'] = True
                        return _method_obj(*args, **kwargs)
                    raise
            return wrapper

        return JsonRPCClient(self.rpc_uri,
                             timeout=timeout,
                             method_class=_JsonRPCMethod)

    def __jsonrpc(self):
        return JsonRPCClient(self.rpc_uri, timeout=int(os.environ.get("JSONRPC_TIMEOUT", 90)))

    def start(self, timeout=5):
        self.install()
        cmd = list(itertools.chain(
            ["shell", "am", "startservice"],
            ["-a", "com.zunyun.zime.ACTION_START"]
        ))

        self.zservice_process = self.adb.cmd(*cmd)
        self.adb.forward(self.local_port, self.device_port)

        while not self.alive and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        if not self.alive:
            #尝试port+4000
            if self.local_port < 60000 :
                self.local_port = self.local_port + 4000
            else :
                self.local_port = self.local_port - 4000
            raise IOError("RPC server not started! zport : %s" % self.local_port)

    def ping(self):
        try:
            return self.__jsonrpc().ping()
        except:
            return None

    @property
    def alive(self):
        '''Check if the rpc server is alive.'''
        return self.ping() == "pong"

    def stop(self):
        '''Stop the rpc server.'''
        '''
        if self.zservice_process and self.zservice_process.poll() is None:
            res = None
            try:
                res = urllib2.urlopen(self.stop_uri)
                self.zservice_process.wait()
            except:
                self.zservice_process.kill()
            finally:
                if res is not None:
                    res.close()
                self.zservice_process = None
        try:
            out = self.adb.cmd("shell", "ps", "-C", "uiautomator").communicate()[0].decode("utf-8").strip().splitlines()
            if out:
                index = out[0].split().index("PID")
                for line in out[1:]:
                    if len(line.split()) > index:
                        self.adb.cmd("shell", "kill", "-9", line.split()[index]).wait()
        except:
            pass
        '''
    @property
    def stop_uri(self):
        return "http://%s:%d/stop" % (self.adb.adb_server_host, self.local_port)

    @property
    def rpc_uri(self):
        return "http://%s:%d/jsonrpc/0" % (self.adb.adb_server_host, self.local_port)




class ZRemoteDevice(object):

    '''zservice wrapper of android device'''


    def __init__(self, serial=None, local_port=None, adb_server_host=None, adb_server_port=None):
        self.server = AutomatorServer(
            serial=serial,
            local_port=local_port,
            adb_server_host=adb_server_host,
            adb_server_port=adb_server_port
        )


    def __getattr__(self, attr):
        '''alias of fields in info property.'''
        info = self.info
        if attr in info:
            return info[attr]
        elif attr in self.__alias:
            return info[self.__alias[attr]]
        else:
            raise AttributeError("%s attribute not found!" % attr)

    def mb_substr(self, s, start, length=None, encoding="UTF-8"):
        u_s = s.decode(encoding)
        return (u_s[start:(start + length)] if length else u_s[start:]).encode(encoding)

    def cmd(self, *args, **kwargs):
        return self.server.adb.cmd(*args, **kwargs).communicate()

    def toast(self, message):
        message = '%s %s' %( datetime.datetime.now().strftime('%H:%M:%S') , message)
        self.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \\\"%s\\\"" % message)

    def log_warn(self, message, level="warn"):
        from dbapi import dbapi
        dbapi.log_warn(self.server.adb.device_serial(), message, level)

    def log_error(self, message):
        self.log_warn(message, "error")

    def heartbeat(self):
        key = 'timeout_%s' % self.server.adb.device_serial()
        cache.set(key, (datetime.datetime.now()  - datetime.datetime(2017, 1 ,1)).seconds)

    ##设置模块运行时间戳
    def setModuleLastRun(self, mid):
        key = '%s_%s' % (self.server.adb.device_serial(), mid);
        cache.set(key, int(time.time()), None)


    ##返回本设备运行模块与当前时间的间隔（单位：分钟）
    def getModuleRunInterval(self, mid):
        key = '%s_%s' % (self.server.adb.device_serial(), mid);
        lasttime = cache.get(key)
        if lasttime is None:
            return None
        return (int(time.time()) - int(lasttime))/60;

    def nameToPhone(self, name):
        phone = ''
        for char in name.decode('utf8'):
            phone += str(const.CHINESE_ARRAY.index(char))

        return phone[0:11]

    def phoneToName(self, phone):
        num = int(phone[0:3])
        name = const.CHINESE_ARRAY[num]

        num = int(phone[3:6])
        name += const.CHINESE_ARRAY[num]

        num = int(phone[6:9])
        name += const.CHINESE_ARRAY[num]

        num = int(phone[9:11]) * 10
        name += const.CHINESE_ARRAY[num]
        return name

    def checkTopActivity(self, activityName):
        out = self.cmd("shell", "dumpsys activity top  | grep ACTIVITY")[0].decode('utf-8')
        if out.find(activityName) > -1:
            return  True
        return False

    def getTopActivity(self):
        out = self.cmd("shell", "dumpsys activity top  | grep ACTIVITY")[0].decode('utf-8')
        #out = self.server.adb.cmd("shell",
                     #          "dumpsys activity top  | grep ACTIVITY").communicate()
        return out


    def sleep(self, second):
        while(second > 0):
            time.sleep(1)
            second = second -1

    def set_mobile_data(self,status):
        '''Get the device info.'''
        return self.server.jsonrpc.setMobileData(status)

    def get_mobile_data_state(self):
        '''Get the device info.'''
        return self.server.jsonrpc.getMobileDataState()

    def input(self, text):
        t = base64.b64encode(text)
        self.cmd("shell", "am broadcast -a ZY_INPUT_TEXT --es text \\\"%s\\\"" % t)
        return True

    def isNetConnected(self):
        ping = self.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
        if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
            return  True
        return False

    def qq_openUser(self, num):
        self.server.adb.run_cmd("shell",
                         'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"' % num)  # qq名片页面

    def qq_getLoginStatus(self, d, maxSleep = 40):
        if maxSleep < 0:
           return {'success': False, 'remark': 'Timeout'}

        if not self.isNetConnected():
            self.toast('网络未连接，超时等待 %d' % maxSleep)
            self.sleep(2)
            return self.qq_getLoginStatus(d, maxSleep - 2)


        activity = self.getTopActivity()
        if 'com.tencent.mobileqq' not in activity:
            return {'success': False, 'remark': u'当前界面非QQ界面' + activity}

        if 'com.tencent.mobileqq/.activity.InstallActivity' in activity:
            self.toast('QQ正在更新数据，请稍等, %d' % maxSleep)
            self.sleep(2)
            return self.qq_getLoginStatus(d, maxSleep - 2)


        if 'com.tencent.mobileqq/.activity.RegisterGuideActivity' in activity:
            return {'success': False, 'remark': 'RegisterGuideActivity'}

        if 'com.tencent.mobileqq/.activity.LoginActivity' in activity:
            return {'success': False, 'remark': 'LoginActivity'}

        if 'com.tencent.mobileqq/.activity.NotificationActivity' in activity:
            if d(textContains='身份过期').exists:
                return {'success': False, 'remark': u'身份过期'}

            if d(resourceId='com.tencent.mobileqq:id/dialogLeftBtn').exists:
                self.toast('发现弹窗，点击左侧按钮后再行判断')
                d(resourceId='com.tencent.mobileqq:id/dialogLeftBtn').click()
                self.sleep(2)
                return self.qq_getLoginStatus(d)

            if d(resourceId='com.tencent.mobileqq:id/dialogRightBtn').exists:
                self.toast('发现弹窗，点击右侧按钮后再行判断')
                d(resourceId='com.tencent.mobileqq:id/dialogRightBtn').click()
                self.sleep(2)
                return self.qq_getLoginStatus(d)


        if 'com.tencent.mobileqq/.activity.UpgradeActivity' in activity:  #QQ更新提醒
            self.toast('发现升级弹窗，点击暂不升级后再行判断')
            d(text='暂不升级').click()
            self.sleep(2)
            return self.qq_getLoginStatus(d)

        if 'com.tencent.mobileqq/.activity.PhoneUnityIntroductionActivity' in activity:  # QQ主界面
            return {'success': True, 'remark': 'PhoneUnityIntroductionActivity'}

        if 'com.tencent.mobileqq/.activity.phone.PhoneMatchActivity' in activity:  # QQ主界面
            return {'success': True, 'remark': 'PhoneMatchActivity'}


        if 'com.tencent.mobileqq/.activity.SplashActivity' in activity:
            #主界面尝试唤起10000号名片
            self.qq_openUser('10000')
            if d( text='QQ' ).exists:
                d( text='QQ' ).click( )

            while maxSleep > 0:
                self.toast('尝试拉取10000号资料, %d' % maxSleep)
                self.sleep(2)
                maxSleep = maxSleep -2
                activity = self.getTopActivity()
                if 'com.tencent.mobileqq/.activity.FriendProfileCardActivity' not in activity:
                    return self.qq_getLoginStatus(d, maxSleep)

                if d(textContains='系统消息').exists:
                    d.press.back()
                    return {'success': True, 'remark': 'ok'}
            return {'success': False, 'remark': 'check 10000 info Timeout'}

        self.toast('存在未判断的QQ界面状态，请提取日志')
        import util
        logger = util.logger
        logger.info('UNKNOW ACTIVITY: %s' % activity)

    def wx_restart(self):
        self.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止

        self.server.adb.cmd("shell", "su -c 'rm -rf /data/data/com.tencent.mm/tinker/*'").communicate()
        self.server.adb.cmd("shell", "su -c 'mkdir -p /data/data/com.tencent.mm/tinker/'").communicate()
        self.server.adb.cmd("shell", "su -c 'chmod 000 /data/data/com.tencent.mm/tinker/'").communicate()

        self.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来


    '''
    openyaoyiyao   打开摇一摇界面
    openyaoyiyaosayhi 打开摇一摇打招呼的人
    searchui 打开搜索页面
    opennearsayhi 打开附近打招呼的人界面
    opennearui 打开附近的人界面
    opensnsui 朋友圈界面
    openinfoui     打开我的个人信息页面
    openaddui    打开添加界面
    openscanui    打开二维码扫描界面

    ###任意界面打开方式：
    adb shell dumpsys activity top
    如：com.tencent.mm/.plugin.scanner.ui.BaseScanUI   name1:scanner  name2:.ui.BaseScanUI
    如：com.tencent.mm/.plugin.subapp.ui.pluginapp.AddMoreFriendsUI   name1:subapp  name2:.ui.pluginapp.AddMoreFriendsUI
    '''
    def wx_action(self, action):
        if action == "openaddui":
            self.server.adb.cmd("shell", "am broadcast -a MyAction --es act \"openwx\" --es name1 \"subapp\" --es name2 \".ui.pluginapp.AddMoreFriendsUI\"").communicate()

        if action == "openscanui":
            self.server.adb.cmd("shell", "am broadcast -a MyAction --es act \"openwx\" --es name1 \"scanner\" --es name2 \".ui.BaseScanUI\"").communicate()

        if action == "opennearui":
            self.server.adb.cmd("shell", "am broadcast -a MyAction --es act \"%s\"" % action).communicate()
            time.sleep(15)
            return self.server.jsonrpc.wx_result()

        else:
            self.server.adb.cmd("shell", "am broadcast -a MyAction --es act \"%s\""%action).communicate()
        return True

    '''
    sendlinksns 发送朋友圈链接信息
    '''
    def wx_sendlinksns(self, points, steps=100):
        ppoints = []
        for p in points:
            ppoints.append(p[0])
            ppoints.append(p[1])
        return self.server.jsonrpc.swipePoints(ppoints, steps)

    def wx_userList(self):
        return self.server.jsonrpc.wx_result()


    '''
    执行微信SQL
    '''
    def wx_execute_sql(self, sql):
        self.server.adb.cmd("shell",   "am broadcast -a MyAction --es act \"sqlhelper\" --es sql \"%s\"" % sql).communicate()
        return self.server.jsonrpc.wx_sql(sql)

    '''
    sendlinksns 发送图文朋友圈
    images以,分隔
    '''
    def wx_sendsnsline(self, description, images):    #微信发图片
        imgs = ""
        for k, v in enumerate(images):

            '''
                try:
                    pic = requests.get(each, timeout=10)
                except requests.exceptions.ConnectionError:
                    print '【错误】当前图片无法下载'
                    continue
                string = 'pictures\\' + str(i) + '.jpg'
                fp = open(string, 'wb')
                fp.write(pic.content)
                fp.close()
            '''
            try:
                pic = requests.get(v, timeout=10)
            except requests.exceptions.ConnectionError:
                print '【错误】当前图片无法下载'
                continue
            string = '/tmp/%s.jpg' %  uuid.uuid1()
            print(string)
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            #print '%s -- %s' %(k,v)
            imgTarget = "/data/local/tmp/%s"%k
            self.server.adb.cmd("push", string,  imgTarget).wait()
            imgs = "%s,%s"%(imgs,imgTarget)
        self.server.adb.cmd("shell", "am broadcast -a MyAction --es act \"sendsnsline\" --es description \"%s\" --es images \"%s\""%(description,imgs)).communicate()
        return True

    def sendpicture(self, images):    #微信发图片
        self.server.adb.cmd("shell", "rm -r /sdcard/DCIM/picture/").communicate()
        imgs = ""
        for k, v in enumerate(images):
            form = v[-3:]
            print(form)
            '''
                try:
                    pic = requests.get(each, timeout=10)
                except requests.exceptions.ConnectionError:
                    print '【错误】当前图片无法下载'
                    continue
                string = 'pictures\\' + str(i) + '.jpg'
                fp = open(string, 'wb')
                fp.write(pic.content)
                fp.close()
            '''
            try:
                pic = requests.get(v, timeout=10)
            except requests.exceptions.ConnectionError:
                print '【错误】当前图片无法下载'
                continue
            string = '/tmp/%s.%s' %  (uuid.uuid1(),form)
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            #print '%s -- %s' %(k,v)
            imgTarget = "/sdcard/DCIM/picture/%s.%s"%(k,form)
            self.server.adb.cmd("push", string,  imgTarget).wait()
            self.server.adb.cmd("shell", "am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://%s"%imgTarget ).communicate()

           # adb push / home / zunyun / 11.jpg / sdcard / DCIM　将本地图片推到手机的一个目录
            #adb shell am broadcast - a android.intent.action.MEDIA_SCANNER_SCAN_FILE - d file: // / sdcard / DCIM / 11.jpg　　　＃让这张图片显示在相册里

    def wx_openurl(self, url):
        self.server.adb.cmd("shell", "am broadcast -a MyAction --es act \"openurl\" --es url \"%s\""%url).communicate()
        return True

    def wx_openuser(self, userid):
        self.server.adb.cmd("shell", "am broadcast -a MyAction --es act \"openuser\" --es userid \"%s\""%userid).communicate()

        return True

    def wx_openuserchat(self, userid):
        self.server.adb.cmd("shell", "am broadcast -a MyAction --es act \"openchatui\" --es userid \"%s\""%userid).communicate()

        return True

    def wx_openuser_v1(self, v1, contactScene):
        self.server.adb.cmd("shell", "su -c 'am start -n com.tencent.mm/.plugin.profile.ui.ContactInfoUI --es Contact_User %s --ei Contact_Scene %s'" % (v1, contactScene)).communicate()

        return True

    def wx_yaoyiyao(self):
        base_dir = os.path.dirname(__file__)
        filename = os.path.join(base_dir, 'libs/isyaoyiyao')
        self.server.adb.cmd("push", filename, "/sdcard/").wait()
        return True

    def wx_scanqr(self, img):
        try:
            pic = requests.get(img, timeout=10)
        except requests.exceptions.ConnectionError:
            print '【错误】当前图片无法下载'
            return None
        string = '/tmp/%s.jpg' % uuid.uuid1()
        fp = open(string, 'wb')
        fp.write(pic.content)
        fp.close()
        self.server.adb.cmd("push", string, "/sdcard/qr.jpg").communicate()
        self.wx_action("openscanui")
        return True

    def wx_sendtextsns(self, text):
        self.server.adb.cmd("shell", "am broadcast -a MyAction --es act \"sendtextsns\" --es text \"%s\""%text).communicate()

        return True

    def img_crop(self, sourcePng, point):
        from PIL import Image
        img = Image.open(sourcePng)
        print img.size
        left = int(point["x1"] * img.size[0])
        top = int(point["y1"] * img.size[1])
        right = int(point["x2"] * img.size[0])
        bottom = int(point["y2"] * img.size[1])
        box = (left, top, right, bottom)  # left top right bottom
        region = img.crop( box )  # 截取验证码的图片

        img = Image.new( 'RGBA', (right - left, bottom - top) )
        img.paste( region, (0, 0) )
        cropedPng = '/tmp/%s.png' % uuid.uuid1()
        img.save( cropedPng )
        return cropedPng

    '''
    一键生成串号，pkg:目标应用的packageName
    return：串号信息
    '''
    def generate_serial(self, pkg):
        self.server.adb.run_cmd("shell",
                         'am broadcast -a com.zunyun.serial.action --include-stopped-packages   -n com.sollyu.xposed.hook.model/com.sollyu.android.appenv.ActionReceiver --es ac generate --es pkg %s' % pkg)
        return None

    def get_serial(self, pkg):
        path = '/sdcard/serial.json'
        out = self.server.adb.run_cmd("shell", "\"su -c 'rm %s'\"" % path).output
        self.server.adb.run_cmd("shell",
                         'am broadcast -a com.zunyun.serial.action --include-stopped-packages   -n com.sollyu.xposed.hook.model/com.sollyu.android.appenv.ActionReceiver --es ac get --es pkg %s --es fileName %s' % (pkg, path))
        out = self.server.adb.run_cmd("shell", "\"su -c 'cat %s'\"" % path).output
        return out

    def set_serial(self, pkg, serial):
        t = base64.b64encode(serial)

        self.server.adb.run_cmd("shell",
                         'am broadcast -a com.zunyun.serial.action --include-stopped-packages   -n com.sollyu.xposed.hook.model/com.sollyu.android.appenv.ActionReceiver --es ac set --es pkg %s --es serial %s' % (pkg, t))
        return None

    def clear_traversed_text(self):
        '''clear the last traversed text.'''
        self.server.jsonrpc.clearLastTraversedText()

    @property
    def open(self):
        '''
        Open notification or quick settings.
        Usage:
        d.open.notification()
        d.open.quick_settings()
        '''
        @param_to_property(action=["notification", "quick_settings"])
        def _open(action):
            if action == "notification":
                return self.server.jsonrpc.openNotification()
            else:
                return self.server.jsonrpc.openQuickSettings()
        return _open

    @property
    def handlers(self):
        obj = self

        class Handlers(object):

            def on(self, fn):
                if fn not in obj.server.handlers['handlers']:
                    obj.server.handlers['handlers'].append(fn)
                obj.server.handlers['device'] = obj
                return fn

            def off(self, fn):
                if fn in obj.server.handlers['handlers']:
                    obj.server.handlers['handlers'].remove(fn)

        return Handlers()


    @property
    def press(self):
        '''
        press key via name or key code. Supported key name includes:
        home, back, left, right, up, down, center, menu, search, enter,
        delete(or del), recent(recent apps), volume_up, volume_down,
        volume_mute, camera, power.
        Usage:
        d.press.back()  # press back key
        d.press.menu()  # press home key
        d.press(89)     # press keycode
        '''
        @param_to_property(
            key=["home", "back", "left", "right", "up", "down", "center",
                 "menu", "search", "enter", "delete", "del", "recent",
                 "volume_up", "volume_down", "volume_mute", "camera", "power"]
        )
        def _press(key, meta=None):
            if isinstance(key, int):
                return self.server.jsonrpc.pressKeyCode(key, meta) if meta else self.server.jsonrpc.pressKeyCode(key)
            else:
                return self.server.jsonrpc.pressKey(str(key))
        return _press


    @property
    def screen(self):
        '''
        Turn on/off screen.
        Usage:
        d.screen.on()
        d.screen.off()

        d.screen == 'on'  # Check if the screen is on, same as 'd.screenOn'
        d.screen == 'off'  # Check if the screen is off, same as 'not d.screenOn'
        '''
        devive_self = self

        class _Screen(object):
            def on(self):
                return devive_self.wakeup()

            def off(self):
                return devive_self.sleep()

            def __call__(self, action):
                if action == "on":
                    return self.on()
                elif action == "off":
                    return self.off()
                else:
                    raise AttributeError("Invalid parameter: %s" % action)

            def __eq__(self, value):
                info = devive_self.info
                if "screenOn" not in info:
                    raise EnvironmentError("Not supported on Android 4.3 and belows.")
                if value in ["on", "On", "ON"]:
                    return info["screenOn"]
                elif value in ["off", "Off", "OFF"]:
                    return not info["screenOn"]
                raise ValueError("Invalid parameter. It can only be compared with on/off.")

            def __ne__(self, value):
                return not self.__eq__(value)

        return _Screen()

    @property
    def wait(self):
        '''
        Waits for the current application to idle or window update event occurs.
        Usage:
        d.wait.idle(timeout=1000)
        d.wait.update(timeout=1000, package_name="com.android.settings")
        '''
        @param_to_property(action=["idle", "update"])
        def _wait(action, timeout=1000, package_name=None):
            if timeout / 1000 + 5 > int(os.environ.get("JSONRPC_TIMEOUT", 90)):
                http_timeout = timeout / 1000 + 5
            else:
                http_timeout = int(os.environ.get("JSONRPC_TIMEOUT", 90))
            if action == "idle":
                return self.server.jsonrpc_wrap(timeout=http_timeout).waitForIdle(timeout)
            elif action == "update":
                return self.server.jsonrpc_wrap(timeout=http_timeout).waitForWindowUpdate(package_name, timeout)
        return _wait

    def exists(self, **kwargs):
        '''Check if the specified ui object by kwargs exists.'''
        return self(**kwargs).exists

ZDevice = ZRemoteDevice

