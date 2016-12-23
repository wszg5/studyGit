#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5
import rethinkdb as r
from rethinkpool import RethinkPool

class RClient(object):

    def __init__(self):
        pool = RethinkPool(max_conns=120, initial_conns=10, host='192.168.1.33',
                           port=28015,
                           db='stf')
        with pool.get_resource() as res:
            rk_user = r.table('setting').get('rk_user').run(res.conn)
            rk_pwd = r.table('setting').get('rk_password').run(res.conn)

        if rk_user["value"] and rk_pwd["value"]:
            self.username = rk_user["value"]
            self.password = md5(rk_pwd["value"]).hexdigest()
        else:
            return

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

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    rc = RClient()
    im = open('/home/zunyun/PycharmProjects/untitled3/home.jpg', 'rb').read()
    print rc.rk_create(im, 3040)