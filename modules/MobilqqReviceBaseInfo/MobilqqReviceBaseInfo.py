# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class MobilqqRouseAdd:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell",  "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)
        d(description='帐户及设置').click()
        d(descriptionContains='等级：').click()
        d(text='编辑').click()
        d(text='详细资料').click()
        z.sleep(2)
        d(text='编辑').click()
        d(descriptionContains='昵称').child(className='android.widget.EditText', index=1).long_click()
        message = d(descriptionContains='昵称').child(className='android.widget.EditText', index=1).info['text']
        i = 0
        z.heartbeat()
        length = len(message)
        while i < length:
            d.press.delete()
            i = i + 1
        cate_id = args["repo_material_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        if len(Material) == 0:
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
            z.sleep(10)
            return
        name = Material[0]['content']  # 取出验证消息的内容
        z.input(name)    #改名字
        z.heartbeat()
        getGender = d(descriptionContains='性别').child(className='android.widget.TextView',index=1).info['text']
        gender = args['gender']
        if gender!=getGender:
            d(descriptionContains='性别').child(className='android.widget.TextView', index=1).click()
            if getGender=='男':
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)
                d(text='完成').click()
            else:
                d.swipe(width / 2, height * 5 / 7, width / 2, height * 6 / 7)
                d(text='完成').click()
        d(text='完成').click()

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqRouseAdd

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id":"39","gender":"女","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

