# coding:utf-8
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice

class MobilqqSentTheory:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z,args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)
        z.heartbeat()
        d(className='android.widget.TabWidget').child(className='android.widget.FrameLayout',index=2).click()
        d(text='好友动态').click()
        while not d(textContains='说说').exists:
            z.sleep(2)
        d(description='写说说等按钮').click()
        z.sleep(2)
        d(className='android.widget.RelativeLayout',index=1).child(className='android.widget.LinearLayout',index=1)\
            .child(className='android.widget.LinearLayout',index=0).child(className='android.widget.ImageView').click()   #点击到说说页面
        z.sleep(2)
        while not d(textContains='说点什么').exists:
            z.sleep(1)
        z.heartbeat()
        cate_id = args["repo_material_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        if len(Material) == 0:
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
            z.sleep(10)
            return
        message = Material[0]['content']  # 取出验证消息的内容
        z.input(message)
        d(text='照片/视频').click()
        number = int(args['number'])
        d(text='从手机选择').click()
        z.heartbeat()
        z.sleep(5)
        for i in range(0,number):
            forclick = d(className='com.tencent.widget.GridView').child(className='android.widget.RelativeLayout',index=i).\
                child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.CheckBox')
            if forclick.exists:
                forclick.click()
        z.heartbeat()
        d(textContains='确定').click()
        while d(textContains='上传中').exists:
            z.sleep(2)
        z.sleep(4)
        d(text='发表').click()
        z.sleep(3)

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqSentTheory

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id":"145","number":"15","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
