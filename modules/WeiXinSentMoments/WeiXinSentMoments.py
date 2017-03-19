# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WeiXinSentMoments:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(5)
        cate_id = args["repo_material_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        if len(Material) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id).communicate()
            time.sleep(10)
            return
        message = Material[0]['content']  # 取出验证消息的内容

        z.heartbeat()
        z.wx_sendtextsns(message)
        z.input('.')
        d.press.delete()
        d(text='发送').click()
        z.heartbeat()
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return WeiXinSentMoments

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id": "48","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)




















