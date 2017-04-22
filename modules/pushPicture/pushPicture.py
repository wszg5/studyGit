# coding:utf-8
import uuid

import requests

from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXPictureMoment:

    def sendpicture(self, images):    #微信发图片
        imgs = ""
        for k, v in enumerate(images):

            '''
                try:
                    pic = requests.get(each, timeout=10)
                except requests.exceptions.ConnectionError:
                    print '【错误】当前图片无法下载'
                    continue
                string = 'pictures\\' + str(i) + '.jpg'
                fp = open(string, 'wb')
                fp.write(pic.content)
                fp.close()
            '''
            try:
                pic = requests.get(v, timeout=10)
            except requests.exceptions.ConnectionError:
                print '【错误】当前图片无法下载'
                continue
            string = '/tmp/%s.jpg' %  uuid.uuid1()
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            #print '%s -- %s' %(k,v)
            imgTarget = "/sdcard/tmp/%s"%k
            self.server.adb.cmd("push", string,  imgTarget).wait()
            d.server.adb.cmd("shell", "am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/DCIM/%s.jpg\"" % uuid.uuid1()).communicate()
            imgs = "%s,%s"%(imgs,imgTarget)


    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        obj = d.server.adb.device_serial()     #　获取设备序列号

        cate_id = args['repo_material_id']
        materials = self.repo.GetMaterial(cate_id, 0, 1,obj)
        if len(materials) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"朋友圈素材%s号仓库为空，等待中\"" % cate_id).communicate()
            z.sleep(10)
            return
        t = materials[0]
        print(t)
        z.heartbeat()
        imgs = []
        for i in range(1,10,+1):
            z.heartbeat()
            if t['ext%s'%i] is not None:
                imgs.append(t['ext%s'%i])
        z.heartbeat()
        print(imgs)
        self.sendpicture(imgs)

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXPictureMoment

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id": "146","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)




















