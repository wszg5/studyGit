# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class TIMSendMail:
    def __init__(self):

        self.repo = Repo()


    def action(self, d, z, args):

        sendText='sendText'
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMSendMail

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52DSK00474")
    # material=u'有空聊聊吗'
    z = ZDevice("HT52DSK00474")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_cate_id": "43", "repo_material_cate_id": "36", "add_count": "9", "time_delay": "3"};  # cate_id是仓库号，length是数量
    # o.action(d, z, args)
    d(text='用户名/手机/邮箱', className='android.widget.EditText').set_text('x879212013')
    d(index=1, className='android.widget.EditText').set_text('x173835196')
    d(text='登录', className='android.widget.Button').click()