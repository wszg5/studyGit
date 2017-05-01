# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class MobilqqMassDiscussion:
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
        d(description='快捷入口').click()
        d(text='创建群聊').click()
        d(text='从群聊中选择').click()
        if not d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=1).exists:
            z.toast('没有群存在')
            z.sleep(2)
            return
        d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=1).click()
        while d(textContains='加载').exists:
            z.sleep(2)
        z.sleep(2)

        count = int(args['count'])
        i = 1
        t = 0
        kk = 0     #用来判断群里是否有人
        gg = 0     #用来·判断是否滑到底
        while True:
            if t<count:
                forclick = d(className='android.widget.AbsListView').child(className='android.widget.FrameLayout',index=i)
                if forclick.exists:
                    kk = 1
                    if forclick.child(className='android.widget.RelativeLayout',index=0).child(className='android.widget.CheckBox', checked='false').exists:
                        forclick.child(className='android.widget.RelativeLayout',index=0).child(className='android.widget.CheckBox',checked='false').click()
                        gg = 1
                        i = i+1
                        t = t+1
                    else:
                        i = i + 1
                        continue

                else:
                    if kk==0:
                        z.toast('无好友')
                        break
                    if gg==0:
                        z.toast('已选全部好友')
                        break
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    gg = 0
                    z.sleep(3)
                    i = 1
            else:
                break
        d(textContains='发起').click()
        d(text='创建多人聊天').click()
        if d(textContains='发起').exists:
            z.toast('发起多人聊天失败')
            return
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

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqMassDiscussion

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AYSK00084")
    z = ZDevice("HT4AYSK00084")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id":"39","count":"115","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
