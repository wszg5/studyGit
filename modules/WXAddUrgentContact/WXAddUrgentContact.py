# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice


class WXAddUrgentContact:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(9)
        d(text='我').click()
        d(text='设置').click()
        d(textContains='帐号与安全').click()
        d(text='应急联系人').click()
        d(className='android.widget.GridView').child(className='android.widget.ImageView').click()
        d(text='搜索').click()
        add_count = int(args['add_count'])
        cate_id = args["repo_material_id"]  # ------------------
        Material = self.repo.GetMaterial(cate_id, 0, add_count)
        for i in range(0,add_count,+1):
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                time.sleep(10)
                return
            WXName = Material[i]['content']  # 从素材库取出的要发的材料
            z.input(WXName)
            d(className='android.widget.CheckBox').click()
        d(textContains='确定').click()
        d(text='完成').click()


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return WXAddUrgentContact

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
    args = {"repo_material_id": "44","add_count": "3","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
