#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5

from dbapi import dbapi
from zcache import cache


class client_ruokuai(object):

    def __init__(self, username, password):

        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = '72358'
        self.soft_key = 'a6b010fff6d247669c4b4bde98673709'
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }
        self.im_type_list = {
            '4_number_char': 3040
        }

    def getCode(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': self.im_type_list[im_type],
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im.read())}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)

        #{"Result":"答题结果","Id":"题目Id(报错使用)"}
        result =  r.json()
        if "Error_Code" in  result:
            if result["Error_Code"] == "10202":
                if not cache.get("RK_ERROR_PASS"):
                    cache.set("RK_ERROR_PASS", True)
                    dbapi.log_error("","若快用户密码错误","若快打码用户密码错误，请修改")
                return None
        return {"Result": result["Result"], "Id": result["Id"]}

    def reportError(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


if __name__ == "__main__":
    lz = client_ruokuai("power0021", "13141314")
    im = open("/home/zunyun/yzm.jpg", 'rb')
    print lz.getCode(im, "4_number_char")
    print lz.reportError("f91bfe4d-eb8e-4bd7-b6d5-1ca002b69d95")
