# coding:utf-8
import json
import mimetypes
import os, stat
import urllib
import urllib2

import requests
import time

from dbapi import dbapi
from zcache import cache

class client_lianzong(object):
    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.soft_id = '6303'
        self.soft_name = 'xxxx'
        self.soft_secret = 'ofn9oLOIyNDRQjzI3mSbeYc1O3iviTZycrqY7ctb'
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
            'Content-Type': 'application/json',
        }
        self.im_type_list = {
            '4_number_char': 1001,
            '5_char':1013
        }

    def getCode(self, im, im_type, timeout=60):
        import base64
        #f = open(r'c:\jb51.gif', 'rb')  # 二进制方式打开图文件
        if isinstance(im, str):
            ls_f = base64.b64encode(im)
        else:
            ls_f = base64.b64encode(im.read())  # 读取文件内容，转换为base64编码
            im.close()
        #f.close()
        params = {
                    "ts":int(time.time()),
                    "softwareId": self.soft_id,
                    "software": self.soft_name,
                    "sdk":"PYTHON/1.0",
                    "username": self.username,
                    "userPassword": self.password,
                    "captchaData":ls_f,
                    "captchaType":1,
                    "captchaMinLength":4,
                    "captchaMaxLength":8
                  }
        params = json.dumps(params)
        sign =  params + "|" + self.soft_secret
        import hashlib
        m2 = hashlib.md5()
        m2.update(sign)
        sign = m2.hexdigest()


        headers = {'L-Request-Signature': sign}
        headers.update(self.headers)
        requests.adapters.DEFAULT_RETRIES = 5
        request = urllib2.Request(url='https://api.jsdama.com/upload', headers=headers, data=params)
        response = urllib2.urlopen(request)

        r = response.read()
        #r = requests.post('https://api.jsdama.com/upload', data=params, headers=self.headers)
        result = json.loads(r)
        if result["errorCode"] == 0:
            params = {
                "ts": int(time.time()),
                "softwareId": self.soft_id,
                "software": self.soft_name,
                "sdk": "PYTHON/1.0",
                "username": self.username,
                "userPassword": self.password,
                "captchaId": result["data"]["captchaId"]
            }
            params = json.dumps(params)
            sign = params + "|" + self.soft_secret
            import hashlib
            m2 = hashlib.md5()
            m2.update(sign)
            sign = m2.hexdigest()

            headers = {'L-Request-Signature': sign}
            headers.update(self.headers)
            requests.adapters.DEFAULT_RETRIES = 5
            request = urllib2.Request(url='https://api.jsdama.com/recognition', headers=headers, data=params)
            response = urllib2.urlopen(request)

            r = response.read()
            result = json.loads(r)
            if result["errorCode"] == 0:
                return {"Result": result["data"]["recognition"], "Id": result["data"]["captchaId"]}
        else:
            if not cache.get("LIANZONG_CODE_ERROR"):
                cache.set("LIANZONG_CODE_ERROR", True)
                dbapi.log_error("", "联众打码异常", result["errorMessage"])
                return

    def reportError(self, im_id):
        params = {
                    "ts":int(time.time()),
                    "softwareId": self.soft_id,
                    "software": self.soft_name,
                    "sdk":"PYTHON/1.0",
                    "username": self.username,
                    "userPassword": self.password,
                    "captchaId":im_id
                  }

        params = json.dumps(params)
        sign =  params + "|" + self.soft_secret
        import hashlib
        m2 = hashlib.md5()
        m2.update(sign)
        sign = m2.hexdigest()

        headers = {'L-Request-Signature': sign}
        headers.update(self.headers)
        requests.adapters.DEFAULT_RETRIES = 5
        request = urllib2.Request(url='https://api.jsdama.com/report-error', headers=headers, data=params)
        response = urllib2.urlopen(request)

        return response.read()


if __name__ == "__main__":
    lz = client_lianzong("power001", "13141314Abcd")
    im = open("/home/zunyun/2222.png", 'rb')
    print lz.getCode(im, "5_char")
    print lz.reportError("20170416:000000000005912504973")
