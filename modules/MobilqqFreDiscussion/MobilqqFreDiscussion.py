# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class MobilqqFreDiscussion:
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
        if not d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=2).exists:  #判断最近联系人是否展开，再收起
            d(text='最近联系人').click()

        for m in range(1,10):
            if d(className='android.widget.RelativeLayout',index=m).child(text='我的好友').exists:
                break

        count = int(args['count'])
        i = m+1
        retract = d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=i) #判断是否有多个分组
        if retract.exists:
            d(text='我的好友').click()
            for g in range(16,0,-1):
                forre = d(className='android.widget.AbsListView').child(className='android.widget.FrameLayout', index=g)
                if forre.exists:
                    forre.click()
        d(text='我的好友').click()
        t = 0
        kk = 0
        while True:
            if t<count:
                forclick = d(className='android.widget.AbsListView').child(className='android.widget.FrameLayout',index=i)
                if forclick.exists:
                    kk = 1
                    if forclick.child(className='android.widget.CheckBox',checked='true').exists:
                        i = i+1
                        continue
                    forclick.click()
                    i = i+1
                    t = t+1

                else:
                    if kk==0:
                        z.toast('无好友')
                        break
                    if d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i).exists:
                        z.toast('已选全部好友')
                        break
                    d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
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
    return MobilqqFreDiscussion

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id":"39","count":"115","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
