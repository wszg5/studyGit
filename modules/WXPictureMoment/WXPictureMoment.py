# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
import requests
import urllib2
import os
sys.setdefaultencoding('utf8')
class WeiXinSentMoments:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()  # 将微信拉起来
        time.sleep(5)
        # cate_id = args["repo_material_id"]
        # Material = self.repo.GetMaterial(cate_id, 0, 1)
        # wait = 1  # 判断素材仓库里是否由素材
        # while wait == 1:
        #     try:
        #         material = Material[0]['content']  # 取出验证消息的内容
        #         picture = Material[0]['ext1']
        #         wait = 0
        #     except Exception:
        #         d.server.adb.cmd("shell",
        #                          "am broadcast -a com.zunyun.qk.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id).communicate()
        #         time.sleep(20)


        #urlretrieve()
        req = urllib2.Request('http://pic6.huitu.com/res/20130116/84481_20130116142820494200_1.jpg')
        res = urllib2.urlopen(req)
        print (res.code)
        picture = res.read()
        print (res.read())
        res.close()
        material = '看对方结果看及附加发'
        # urllib2.urlretrieve('http://pic6.huitu.com/res/20130116/84481_20130116142820494200_1.jpg', 'mtp://[usb:001,060]/')
        # urllib.urlretrieve('http://paas.eztcn.com.cn/paas/api/v2/captcha/small.do?phone=13683270570', 'f:/xxx.jpg')
        z.wx_sendsnsline(material,picture)
        z.input('.')
        d(text='发送').click()



def getPluginClass():
    return WeiXinSentMoments

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # z.wx_action('opensnsui')
    # z.wx_sendtextsns('你好')
    # d(text='你的手机号码').set_text(17601543818)
    # d(resourceId='com.tencent.mm:id/gr').set_text('13141314abc')
    # d(text='登录').click()
    # z.input('13141314abc')
    args = {"repo_material_id": "36","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)



















