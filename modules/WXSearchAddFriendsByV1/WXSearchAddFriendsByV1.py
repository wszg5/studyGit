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

        cate_id = args['repo_number_id']
        numberList = self.repo.GetNumber( cate_id, 0, 1 )
        v1 = numberList[0]['number']
        print(v1)

        z.wx_openuser_v1( v1, '13' )

        cate_id = args["repo_material_id"]
        Material = self.repo.GetMaterial( cate_id, 0, 1 )
        if len( Material ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id ).communicate( )
            z.sleep( 10 )
            return
        message = Material[0]['content']  # 取出验证消息的内容


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
    args = {"repo_number_id": "198", "repo_cate_id":'171',"repo_material_id": "39", 'forselect':'混合',"add_count": "3", 'gender':"不限","time_delay": "3"}    #cate_id是仓库号，length是数量
    # o.action(d,z, args)
    repo = Repo( )
    cate_id = args['repo_number_id']
    numberList = repo.GetNumber( cate_id, 0, 1 )
    v1 = numberList[0]['number']
    z.wx_openuser_v1( v1, '13' )
    print( v1 )