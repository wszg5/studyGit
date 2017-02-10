# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WXYaoYiYao:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(3)
        EndIndex = int(args['EndIndex'])         #------------------
        z.server.install()
        z.wx_action("openyaoyiyao")
        for i in range(1,EndIndex,+1):
            cate_id = args["repo_material_id"]  # ------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            wait = 1
            while wait == 1:
                try:
                    Material = Material[0]['content']  # 从素材库取出的要发的材料
                    wait = 0
                except Exception:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()

            z.wx_yaoyiyao()
            time.sleep(5)
            while d(textContains='正在搜').exists:
                time.sleep(2)
            d(textContains='相距').click()
            d(text='打招呼').click()
            d(className='android.widget.EditText').click()
            z.input(Material)
            d(text='发送').click()
            d(description='返回').click()

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return WXYaoYiYao

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id": "36",'EndIndex':'10',"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
