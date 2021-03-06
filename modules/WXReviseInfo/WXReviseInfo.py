# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
class WXReviseInfo:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)
        z.wx_action('openinfoui')
        z.heartbeat()
        d(text='昵称').click()
        obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
        obj = obj['text']
        lenth = len(obj)
        m = 0
        while m < lenth:
            d.press.delete()
            m = m + 1
        z.heartbeat()
        cate_id = args['repo_name_id']     #得到昵称库的id
        Material = self.repo.GetMaterial(cate_id, 0, 1)     #修改昵称
        if len(Material) == 0:
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
            z.sleep(10)
            return
        name = Material[0]['content']  # 从素材库取出的要发的材料
        z.input(name)
        d(text='保存').click()
        z.heartbeat()
        gender = args['gender']
        d(text='性别').click()
        d(text=gender).click()

        d(text='地区').click()
        z.sleep(2)
        d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=1).click()

        d(text='个性签名').click()
        obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
        obj = obj['text']
        lenth = len(obj)
        m = 0
        while m < lenth:
            d.press.delete()
            m = m + 1
        z.heartbeat()
        cate_id = args['repo_persigned_id']
        Material = self.repo.GetMaterial(cate_id, 0, 1)  # 修改个性签名
        if len(Material) == 0:
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
            z.sleep(10)
            return
        z.heartbeat()
        persigned = Material[0]['content']  # 从素材库取出的要发的材料

        z.input(persigned)
        d(text='保存').click()


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return WXReviseInfo

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
    # z.wx_action('searchui')
    args = {"repo_name_id": "102",'repo_persigned_id':'48','gender':"男","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
