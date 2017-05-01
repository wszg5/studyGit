# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class MobilqqPraiseII:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z,args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
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
        d(text='分享新鲜事').click()
        z.sleep(1)
        if d(textContains='需要等级LV3才能发布新鲜事哦').exists:
            z.toast('等级不够')
            return
        d(text='从相册中选取').click()
        while not d(textContains='最近照片').exists:
            z.sleep(2)
        number = int(args['number'])
        if number>9:
            number = 9
        for i in range(0,number):
            forclick = d(className='com.tencent.widget.GridView').child(className='android.widget.RelativeLayout',index=i).\
                child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.CheckBox')
            if forclick.exists:
                forclick.click()
        d(textContains='确定').click()
        z.sleep(2)
        cate_id = args["repo_material_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        if len(Material) == 0:
            d.server.adb.cmd("shell" "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
            z.sleep(10)
            return
        message = Material[0]['content']  # 取出验证消息的内容
        z.input(message)
        d(text='发表').click()
        z.sleep(2)

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqPraiseII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AYSK00084")
    z = ZDevice("HT4AYSK00084")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"number":"20","repo_material_id":"39","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
