# coding:utf-8
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice

class MobilqqTheory:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z,args):
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)
        z.heartbeat()
        d(className='android.widget.TabWidget').child(className='android.widget.FrameLayout',index=2).click()
        d(text='好友动态').click()
        while not d(textContains='说说').exists:
            z.sleep(2)
        fordel = d(className='android.widget.FrameLayout', index=2).child(className='android.widget.FrameLayout', index=1)
        if not fordel.exists:
            fordel = d(className='android.widget.FrameLayout', index=1).child(className='android.widget.FrameLayout', index=1)
        fordel = fordel.info['visibleBounds']
        deltop = int(fordel['top'])
        delbottom = int(fordel['bottom'])
        y1 = delbottom - deltop
        d.swipe(width / 2, height * 2 / 3, width / 2, height / 5)
        count = int(args['count'])
        i = 1
        t = 0
        while True:
            if t<count:
                z.sleep(1)
                forclick = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i).child(className='android.widget.RelativeLayout',index=5)
                forclick1 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i).child(className='android.widget.RelativeLayout', index=8) #遇到公共频道的情况
                if forclick.exists:
                    z.sleep(1)
                    forclick.child(className='android.widget.ImageView',index=1).click()
                    time.sleep(0.5)
                    forclick.child(className='android.widget.ImageView',index=2).click()
                    cate_id = args["repo_material_id"]
                    Material = self.repo.GetMaterial(cate_id, 0, 1)
                    if len(Material) == 0:
                        d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                        z.sleep(10)
                        return
                    message = Material[0]['content']  # 取出验证消息的内容
                    z.input(message)
                    if d(text='发送').exists:
                        d(text='发送').click()
                    if i ==0:
                        i = i+2
                    else:
                        i = i+1
                    t = t+1

                elif forclick1.exists:
                    forclick1.child(className='android.widget.ImageView', index=1).click()
                    forclick1.child(className='android.widget.ImageView', index=2).click()
                    cate_id = args["repo_material_id"]
                    Material = self.repo.GetMaterial(cate_id, 0, 1)
                    if len(Material) == 0:
                        d.server.adb.cmd("shell",
                                         "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                        z.sleep(10)
                        return
                    message = Material[0]['content']  # 取出验证消息的内容
                    z.input(message)
                    if d(text='发送').exists:
                        d(text='发送').click()
                    i = i + 1
                    t = t + 1

                elif i==1 and d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=0)\
                        .child(className='android.widget.RelativeLayout',index=5).child(className='android.widget.ImageView',index=1,clickable='true').exists:
                    i = 0
                    continue
                else:
                    str = d.info  # 获取屏幕大小等信息
                    width = str["displayWidth"]
                    clickCondition = d(className='android.widget.AbsListView')
                    obj = clickCondition.info
                    obj = obj['visibleBounds']
                    top = int(obj['top'])
                    bottom = int(obj['bottom'])
                    y = bottom - top
                    y = y - y1
                    d.swipe(width / 2, y, width / 2, 0)
                    z.sleep(3)
                    i = 1
            else:
                break


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqTheory

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id":"145","count":"15","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
