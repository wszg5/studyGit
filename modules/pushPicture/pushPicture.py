# coding:utf-8
import os
import uuid

import requests

from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXPictureMoment:



    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        num = int(args['num'])
        cate_id = args['repo_material_id']
        time = int(args['time'])
        materials = self.repo.GetMaterial(cate_id,time, num)
        count = len(materials)
        if len(materials) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"朋友圈素材%s号仓库为空，等待中\"" % cate_id).communicate()
            z.sleep(10)
            return

        imgs = []
        for i in range(0, count, +1):

            t = materials[i]['content']
            if t is not None:
                imgs.append(t)
            z.heartbeat()
        z.sendpicture(imgs)
        if (args["time_delay"]):

            z.sleep(int(args["time_delay"]))

    # def sendPIC(self,imag):
    #         self.server.adb.cmd( "shell", "rm -r /sdcard/DCIM/" ).communicate( )
    #         imgs = ""
    #         for k, v in enumerate( images ):
    #             form = v[-3:]
    #             print(form)
    #             '''
    #                 try:
    #                     pic = requests.get(each, timeout=10)
    #                 except requests.exceptions.ConnectionError:
    #                     print '【错误】当前图片无法下载'
    #                     continue
    #                 string = 'pictures\\' + str(i) + '.jpg'
    #                 fp = open(string, 'wb')
    #                 fp.write(pic.content)
    #                 fp.close()
    #             '''
    #             try:
    #                 pic = requests.get( v, timeout=10 )
    #             except requests.exceptions.ConnectionError:
    #                 print ('【错误】当前图片无法下载')
    #                 continue
    #             string = '/tmp/%s.%s' % (uuid.uuid1( ), form)
    #             fp = open( string, 'wb' )
    #             fp.write( pic.content )
    #             fp.close( )
    #             # print '%s -- %s' %(k,v)
    #             imgTarget = "/sdcard/DCIM/%s.%s" % (k, form)
    #             self.server.adb.cmd( "push", string, imgTarget ).wait( )
    #             self.server.adb.cmd( "shell",
    #                                  "am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://%s" % imgTarget ).communicate( )

def getPluginClass():
    return WXPictureMoment

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("37f7b82f")
    z = ZDevice("37f7b82f")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id": "392",'num':'3','time':'0',"time_delay": "3"}    #cate_id是仓库号，length是数量
    # o.action(d,z, args)
    import string
    salt = ''.join( random.sample( string.ascii_letters + string.digits, random.randint(1,11) ) )
    print salt
    with open('/home/zunyun/text/z.png','rb') as f:
        form = 'png'
        string = '/tmp/%s.%s' % (uuid.uuid1( ), form)
        fp = open( string, 'wb' )
        fp.write( f.read() )
        fp.close( )
    # print '%s -- %s' %(k,v)
    name = 'abcdefghijklmnopqrestuvwxyz0123456789'
    imgTarget = "/sdcard/Android/%s.%s" % (salt, form)
    d.server.adb.cmd( "push", string, imgTarget ).wait( )
    d.server.adb.cmd( "shell","am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://%s" % imgTarget ).communicate( )



















