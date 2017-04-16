# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class MobilqqNewsPrise:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z,args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)
        z.heartbeat()
        d(description='快捷入口').click()
        d(textContains='加好友').click()
        d(textContains='附近的人').click()
        while not d(textContains='等级').exists:
            z.sleep(2)
        d(text='新鲜事').click()
        count = int(args['count'])
        i = 0
        t = 0
        while t<count:
            forexist = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i)
            if forexist.exists:
                    forclick = forexist.child(className='android.widget.RelativeLayout',index=3).child(className='android.widget.LinearLayout',index=1)
                    time.sleep(0.5)

                    if forclick.exists:
                        if forclick.child(description='点赞').exists:
                            forclick.child(description='点赞').click()
                        else:
                            i = i + 1
                        forclick.child(description='评论').click()
                        cate_id = args["repo_material_id"]
                        Material = self.repo.GetMaterial(cate_id, 0, 1)
                        if len(Material) == 0:
                            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                            z.sleep(10)
                            return
                        message = Material[0]['content']  # 取出验证消息的内容
                        z.input(message)
                        d(text='发送').click()
                        i = i+1
                        t = t+1
                    else:
                        i = i+1

            else:
                str = d.info  # 获取屏幕大小等信息
                width = str["displayWidth"]
                clickCondition = d(className='android.widget.AbsListView')
                obj = clickCondition.info
                obj = obj['visibleBounds']
                top = int(obj['top'])
                bottom = int(obj['bottom'])
                y = bottom - top
                d.swipe(width / 2, y, width / 2, 0)
                z.sleep(6)
                i = 0

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqNewsPrise

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AYSK00084")
    z = ZDevice("HT4AYSK00084")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id":"145","count":"115","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
