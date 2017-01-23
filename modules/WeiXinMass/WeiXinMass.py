# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WeiXinMass:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()  # 将微信拉起来
        time.sleep(7)
        cate_id = args["repo_material_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        wait = 1  # 判断素材仓库里是否由素材
        while wait == 1:
            try:
                material = Material[0]['content']  # 取出验证消息的内容
                wait = 0
            except Exception:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.qk.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id).communicate()
                time.sleep(20)
        time.sleep(2)
        d(text='我').click()
        d(text='设置').click()
        d(text='通用').click()
        d(text='功能').click()
        d(text='群发助手').click()
        d(text='开始群发').click()
        if d(text='新建群发').exists:
            d(text='新建群发').click()
        elif d(text='新建群发').exists:
            d(text='新建群发').click()
        d(text='全选').click()
        d(textContains='下一步').click()
        d(className='android.widget.EditText').click()
        z.input(material)
        d(text='发送').click()


def getPluginClass():
    return WeiXinMass

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_material_id": "36","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)





