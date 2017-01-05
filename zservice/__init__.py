#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python wrapper for Zunyun Service."""

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
import xml.dom.minidom

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


class Adb(object):

    def __init__(self, serial=None, adb_server_host=None, adb_server_port=None):
        self.__adb_cmd = None
        self.default_serial = serial if serial else os.environ.get("ANDROID_SERIAL", None)
        self.adb_server_host = str(adb_server_host if adb_server_host else 'localhost')
        self.adb_server_port = str(adb_server_port if adb_server_port else '5037')
        self.adbHostPortOptions = []
        if self.adb_server_host not in ['localhost', '127.0.0.1']:
            self.adbHostPortOptions += ["-H", self.adb_server_host]
        if self.adb_server_port != '5037':
            self.adbHostPortOptions += ["-P", self.adb_server_port]

    def adb(self):
        if self.__adb_cmd is None:
            if "ANDROID_HOME" in os.environ:
                filename = "adb.exe" if os.name == 'nt' else "adb"
                adb_cmd = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", filename)
                if not os.path.exists(adb_cmd):
                    raise EnvironmentError(
                        "Adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])
            else:
                import distutils
                if "spawn" not in dir(distutils):
                    import distutils.spawn
                adb_cmd = distutils.spawn.find_executable("adb")
                if adb_cmd:
                    adb_cmd = os.path.realpath(adb_cmd)
                else:
                    raise EnvironmentError("$ANDROID_HOME environment not set.")
            self.__adb_cmd = adb_cmd
        return self.__adb_cmd

    def cmd(self, *args, **kwargs):
        '''adb command, add -s serial by default. return the subprocess.Popen object.'''
        serial = self.device_serial()
        if serial:
            if " " in serial:  # TODO how to include special chars on command line
                serial = "'%s'" % serial
            return self.raw_cmd(*["-s", serial] + list(args))
        else:
            return self.raw_cmd(*args)

    def raw_cmd(self, *args):
        '''adb command. return the subprocess.Popen object.'''
        cmd_line = [self.adb()] + self.adbHostPortOptions + list(args)
        if os.name != "nt":
            cmd_line = [" ".join(cmd_line)]
        return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def device_serial(self):
        if not self.default_serial:
            devices = self.devices()
            if devices:
                if len(devices) is 1:
                    self.default_serial = list(devices.keys())[0]
                else:
                    raise EnvironmentError("Multiple devices attached but default android serial not set.")
            else:
                raise EnvironmentError("Device not attached.")
        return self.default_serial

    def devices(self):
        '''get a dict of attached devices. key is the device serial, value is device name.'''
        out = self.raw_cmd("devices").communicate()[0].decode("utf-8")
        match = "List of devices attached"
        index = out.find(match)
        if index < 0:
            raise EnvironmentError("adb is not working.")
        return dict([s.split("\t") for s in out[index + len(match):].strip().splitlines() if s.strip()])

    def forward(self, local_port, device_port):
        '''adb port forward. return 0 if success, else non-zero.'''
        return self.cmd("forward", "tcp:%d" % local_port, "tcp:%d" % device_port).wait()

    def forward_list(self):
        '''adb forward --list'''
        version = self.version()
        if int(version[1]) <= 1 and int(version[2]) <= 0 and int(version[3]) < 31:
            raise EnvironmentError("Low adb version.")
        lines = self.raw_cmd("forward", "--list").communicate()[0].decode("utf-8").strip().splitlines()
        return [line.strip().split() for line in lines]

    def version(self):
        '''adb version'''
        match = re.search(r"(\d+)\.(\d+)\.(\d+)", self.raw_cmd("version").communicate()[0].decode("utf-8"))
        return [match.group(i) for i in range(4)]


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

        cmd = list(itertools.chain(
            ["shell", "am", "startservice"],
            ["-a", "com.zunyun.qk.ACTION_START"]
        ))

        self.zservice_process = self.adb.cmd(*cmd)
        self.adb.forward(self.local_port, self.device_port)

        while not self.alive and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        if not self.alive:
            raise IOError("RPC server not started!")

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

    def set_mobile_data(self, status):
        '''Get the device info.'''
        return self.server.jsonrpc.setMobileData(status)

    def input(self, text):
        '''click at arbitrary coordinates.'''
        return self.server.jsonrpc.Input(text)

    def long_click(self, x, y):
        '''long click at arbitrary coordinates.'''
        return self.swipe(x, y, x + 1, y + 1)

    def swipe(self, sx, sy, ex, ey, steps=100):
        return self.server.jsonrpc.swipe(sx, sy, ex, ey, steps)

    def swipePoints(self, points, steps=100):
        ppoints = []
        for p in points:
            ppoints.append(p[0])
            ppoints.append(p[1])
        return self.server.jsonrpc.swipePoints(ppoints, steps)

    def drag(self, sx, sy, ex, ey, steps=100):
        '''Swipe from one point to another point.'''
        return self.server.jsonrpc.drag(sx, sy, ex, ey, steps)

    def dump(self, filename=None, compressed=True, pretty=True):
        '''dump device window and pull to local file.'''
        content = self.server.jsonrpc.dumpWindowHierarchy(compressed, None)
        if filename:
            with open(filename, "wb") as f:
                f.write(content.encode("utf-8"))
        if pretty and "\n " not in content:
            xml_text = xml.dom.minidom.parseString(content.encode("utf-8"))
            content = U(xml_text.toprettyxml(indent='  '))
        return content

    def screenshot(self, filename, scale=1.0, quality=100):
        '''take screenshot.'''
        result = self.server.screenshot(filename, scale, quality)
        if result:
            return result

        device_file = self.server.jsonrpc.takeScreenshot("screenshot.png",
                                                         scale, quality)
        if not device_file:
            return None
        p = self.server.adb.cmd("pull", device_file, filename)
        p.wait()
        self.server.adb.cmd("shell", "rm", device_file).wait()
        return filename if p.returncode is 0 else None

    def freeze_rotation(self, freeze=True):
        '''freeze or unfreeze the device rotation in current status.'''
        self.server.jsonrpc.freezeRotation(freeze)

    @property
    def orientation(self):
        '''
        orienting the devie to left/right or natural.
        left/l:       rotation=90 , displayRotation=1
        right/r:      rotation=270, displayRotation=3
        natural/n:    rotation=0  , displayRotation=0
        upsidedown/u: rotation=180, displayRotation=2
        '''
        return self.__orientation[self.info["displayRotation"]][1]

    @orientation.setter
    def orientation(self, value):
        '''setter of orientation property.'''
        for values in self.__orientation:
            if value in values:
                # can not set upside-down until api level 18.
                self.server.jsonrpc.setOrientation(values[1])
                break
        else:
            raise ValueError("Invalid orientation.")

    @property
    def last_traversed_text(self):
        '''get last traversed text. used in webview for highlighted text.'''
        return self.server.jsonrpc.getLastTraversedText()

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

    def wakeup(self):
        '''turn on screen in case of screen off.'''
        self.server.jsonrpc.wakeUp()

    def sleep(self):
        '''turn off screen in case of screen on.'''
        self.server.jsonrpc.sleep()

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

