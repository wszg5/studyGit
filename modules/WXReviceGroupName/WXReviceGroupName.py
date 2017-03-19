# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXReviceGroupName:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(7)
        endIndex = int(args['EndIndex'])
        d(description='搜索').click()
        z.heartbeat()
        endCondition = 0
        while endCondition<endIndex:
            cate_id = args["repo_material_id"]  # ------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                time.sleep(10)
                return
            z.heartbeat()
            groupName = Material[0]['content']  # 从素材库取出的要发的材料
            z.input(groupName)
            if not d(text='群聊').exists:
                d(description='清除').click()
                continue
            for i in range(0, 13, +1):
                # if not d(text='群聊').exists:
                #     d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                obj = d(className='android.widget.ListView').child(className='android.widget.RelativeLayout',
                                                                   index=i).child(text='群聊')
                if obj.exists:
                    g = i + 1
                    break
            z.heartbeat()
            d(className='android.widget.ListView').child(className='android.widget.RelativeLayout',index=g).child(className='android.widget.LinearLayout',index=0).click()
            d(description='聊天信息').click()
            d(text='群聊名称').click()
            obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
            obj = obj['text']
            lenth = len(obj)
            t = 0
            while t < lenth:
                d.press.delete()
                t = t + 1
            z.heartbeat()
            cate_id1 = args["repo_material_id1"]  # ------------------
            Material1 = self.repo.GetMaterial(cate_id1, 0, 1)
            if len(Material1) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id1).communicate()
                time.sleep(10)
                return
            newName = Material1[0]['content']  # 从素材库取出的要发的材料
            z.input(newName)
            d(text='保存').click()
            d(description='返回').click()
            d(description='返回').click()
            d(description='清除').click()
            z.heartbeat()
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXReviceGroupName

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
    args = {"repo_material_id": "129","repo_material_id1": "39", 'EndIndex': '64', "time_delay": "3"}   #cate_id是仓库号，length是数量
    o.action(d,z, args)
