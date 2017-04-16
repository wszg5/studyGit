# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class EIMMass:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.eim").communicate()  # 强制停止   3001369923  Bn2kJq5l
        d.server.adb.cmd("shell", "am start -n com.tencent.eim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(5)
        z.heartbeat()
        d(description='联系人栏').click()
        d(text='讨论组').click()
        d(description='更多').click()
        d(text='外部联系人').click()
        d(text='我的好友').click()
        count = int(args['count'])
        if count>50:
            count=50
        t = 0
        i = 1
        while True:
            if t<count:
                forexist = d(className='android.view.View').child(className='android.widget.FrameLayout',index=i)
                if forexist.exists:
                    forclick = forexist.child(className='android.widget.RelativeLayout').child(className='android.widget.CheckBox',checked='false')
                    if forclick.exists:
                        g = 1
                        forclick.click()
                        i = i+1
                        t = t+1
                    else:
                        i = i+1
                else:
                    if g ==0:
                        z.toast('没有好友可选')
                        break
                    d.swipe(width / 2,height * 5 / 6, width / 2, height / 4)
                    g= 0
                    i = 1
            else:
                break
        d(textContains='完成').click()
        cate_id = args["repo_material_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        if len(Material) == 0:
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
            z.sleep(10)
            return
        message = Material[0]['content']  # 取出验证消息的内容
        d(className='android.widget.EditText').click()
        z.input(message)
        d(text='发送').click()

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return EIMMass

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AYSK00084")
    z = ZDevice("HT4AYSK00084")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # z.input('读书群')
    # z.input('一起读书学习')
    args = {"repo_material_id":"39","count":"100","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

