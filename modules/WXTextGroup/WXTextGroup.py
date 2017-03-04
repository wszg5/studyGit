# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice


class WXTextGroup:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(7)
        endIndex = int(args['EndIndex'])
        d(description='搜索').click()
        endCondition = 0
        while endCondition<endIndex:
            cate_id = args["repo_material_id"]  # ------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                time.sleep(10)
                return
            groupName = Material[0]['content']  # 从素材库取出的要发的材料
            z.input(groupName)

            if  d(text='群聊').exists:
                for i in range(0, 13, +1):
                    obj = d(className='android.widget.ListView').child(className='android.widget.RelativeLayout',
                                                                       index=i).child(text='群聊')
                    if obj.exists:
                        g = i + 1
                        break
            elif d(text='最常使用').exists:
                for i in range(0, 13, +1):
                    obj = d(className='android.widget.ListView').child(className='android.widget.RelativeLayout',
                                                                       index=i).child(text='最常使用')
                    if obj.exists:
                        g = i + 1
                        break
            else:
                d(description='清除').click()
                continue

            d(className='android.widget.ListView').child(className='android.widget.RelativeLayout',index=g).child(className='android.widget.LinearLayout',index=0).click()
            d(className='android.widget.EditText').click()


            cate_id1 = args["repo_material_id1"]  # ------------------
            Material1 = self.repo.GetMaterial(cate_id1, 0, 1)
            if len(Material1) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id1).communicate()
                time.sleep(10)
                return
            message = Material1[0]['content']  # 从素材库取出的要发的材料
            z.input(message)
            d(text='发送').click()
            d(description='返回').click()
            d(description='清除').click()

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXTextGroup

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
