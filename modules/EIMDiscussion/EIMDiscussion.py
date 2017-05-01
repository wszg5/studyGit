# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class EIMDiscussion:
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

        count = int(args['count'])
        t = 0
        i = 1
        endCondition = 0
        set1 = set()
        while True:
            if t<count:
                forclick = d(className='android.view.View').child(className='android.widget.RelativeLayout',index=i).child(className='android.widget.TextView')
                if forclick.exists:
                    name = forclick.info['text']
                    if name in set1:
                        i = i+1
                        continue
                    set1.add(name)
                    endCondition = 1
                    print(name)
                    forclick.click()
                    d(className='android.widget.EditText').click()
                    cate_id = args["repo_material_id"]
                    Material = self.repo.GetMaterial(cate_id, 0, 1)
                    if len(Material) == 0:
                        d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                        z.sleep(10)
                        return
                    message = Material[0]['content']  # 取出验证消息的内容
                    z.input(message)
                    d(text='发送').click()
                    d(textContains='返回').click()
                    i = i+1
                    t = t+1
                else:
                    if endCondition ==0:
                        break
                    str = d.info  # 获取屏幕大小等信息
                    width = str["displayWidth"]
                    clickCondition = d(className='android.view.View')
                    obj = clickCondition.info
                    obj = obj['visibleBounds']
                    top = int(obj['top'])
                    bottom = int(obj['bottom'])
                    y = bottom - top
                    d.swipe(width / 2, y, width / 2, 0)
                    endCondition = 0
                    z.sleep(3)
                    i = 1
            else:
                break


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return EIMDiscussion

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AYSK00084")
    z = ZDevice("HT4AYSK00084")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id":"140","count":"100","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

