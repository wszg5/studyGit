# coding:utf-8
import os

from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *
from zcache import cache
import re
import logging
logging.basicConfig(level=logging.INFO)

class WXAssignSearchHello:

    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath(__file__)

    def action(self, d,z, args):

        run_time = float( args['run_time'] ) * 60
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return
        z.heartbeat()


        msg_count = int(args['msg_count'])
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(2)

        while not d(description='搜索',className='android.widget.TextView').exists:
            z.toast("等待进入微信")
            z.sleep(3)

        z.sleep(3)
        d( description='搜索', className='android.widget.TextView' ).click( )
        z.sleep(1)

        cate_id = int( args["repo_number_id"] )  # 得到取号码的仓库号
        number_count = int( args['get_number'] )  # 每次取号码个数
        while True:
            exist_numbers = self.repo.GetNumber( cate_id, 120, number_count, 'exist', 'NO')
            print( exist_numbers )
            remain = number_count - len( exist_numbers )
            normal_numbers = self.repo.GetNumber( cate_id, 120, remain, 'normal','NO')
            numbers = exist_numbers + normal_numbers
            if len( numbers ) > 0:
                break
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，模块结束运行\"" % cate_id ).communicate( )
            z.sleep( 30 )
        if len( numbers ) <= 0:
            return

        for i in range( len( numbers ) ):
            WXnumber = numbers[i]['number']
            z.input( WXnumber )
            z.heartbeat( )
            z.sleep( 3 )
            if d( textContains='联系人' ).exists or d( textContains='最常使用' ).exists:
                if d(textContains='微信号:').exists:
                    d( textContains='微信号:' ).click( )
                else:
                    d(resourceId='com.tencent.mm:id/jp').click()

                z.sleep( 1 )
                for i in range( 0, msg_count ):
                    cate_id = args["repo_material_id"]
                    Material = self.repo.GetMaterial( cate_id, 0, 1 )
                    if len( Material ) == 0:
                        d.server.adb.cmd( "shell",
                                          "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id ).communicate( )
                        z.sleep( 10 )
                        return
                    message = Material[0]['content']  # 取出发送消息的内容
                    d( className='android.widget.EditText' ).click( )
                    z.input( message )
                    z.sleep( 1 )
                    d( text='发送' ).click()
                    z.sleep( 5 )
                d( descriptionContains='返回' ).click( )
                z.sleep(1)
                d( descriptionContains='清除' ).click( )
            else:
                d( descriptionContains='清除' ).click( )
                z.sleep(1.5)

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )


def getPluginClass():
    return WXAssignSearchHello

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AVSK00885")
    z = ZDevice("HT4AVSK00885")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "254", "repo_material_id": "39","msg_count": "1", "get_number": "10", "run_time":"1"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)