# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *

class WXSearchAddDepost:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()

        count = 0
        while True:
            count = count + 1
            if count > int(args['add_count']):
                break

            cate_id = args['repo_number_id']
            numberList = self.repo.GetNumber( cate_id, 0, 1 )
            v1 = numberList[0]['number']
            z.wx_openuser_v1( v1, '13' )
            z.sleep( 3 )

            z.heartbeat( )
            if d( text='添加到通讯录' ).exists:
                d( text='添加到通讯录' ).click( )
                z.sleep( 5 )

            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial( cate_id, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']  # 取出验证消息的内容

            if d( text='你已添加了想好，现在可以开始聊天了。' ).exists:
                d.click( 180, 850 )
            z.input( message )

            if d(text='发送').exists:
                d(text='发送').click()
                z.input(3)
                d( descriptionContains='返回' ).click( )

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXSearchAddDepost

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "198", "repo_material_id": "40", "add_count": "3", "time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)