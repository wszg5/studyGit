# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random


class AccountStateJudge:
    def __init__(self):

        self.repo = Repo()

    def action(self, d, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()
        # 将微信拉起来
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()

        for i in range(50, 110):
            time.sleep(1)
            print 'out'
            if d(description='搜索', className='android.widget.TextView').exists:
                print 'in'
                time.sleep(3)
                d(description='搜索', className='android.widget.TextView').click()
                time.sleep(2)
                d(text='搜索', className='android.widget.EditText').set_text('17099094579')
                time.sleep(2)
                d(textContains='查找', className='android.widget.TextView').click()
                time.sleep(2)
                obj = d.info
                print obj

                break


def getPluginClass():
    return AccountStateJudge

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49XSK01883")
    d.dump(compressed=False)
    args = {"repo_number_cate_id": "13", "repo_material_cate_id": "8", "gender": "女", "add_count": "9","time_delay": "3"}  # cate_id是仓库号，发中文问题
    o.action(d, args)