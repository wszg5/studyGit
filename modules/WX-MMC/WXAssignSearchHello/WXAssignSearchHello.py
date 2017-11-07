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
        z.toast( "正在ping网络是否通畅" )
        while True:
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                break
            z.sleep( 2 )

        z.toast( "开始执行：微信指定好友互聊" )
        run_time_min = int( args['run_time_min'] )
        run_time_max = int( args['run_time_max'] )
        run_time = float( random.randint( run_time_min, run_time_max ) ) * 60
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'模块在锁定时间内，无法运行' )
            z.sleep( 2 )
            return

        start_time = args['start_time']
        stop_time = args['stop_time']
        try:
            if self.repo.timeCompare(start_time, stop_time):
                z.toast('处于' + start_time + '～' + stop_time + '时间段内，模块不运行')
                z.sleep(2)
                return
        except:
            logging.exception( "exception" )
            z.toast( "输入时间格式有误" )
            return

        z.heartbeat()
        msg_count = int(args['msg_count'])
        hello_count_array = args['hello_count'].split('~')
        hello_count = random.randint( int(hello_count_array[0]), int(hello_count_array[1]) ) # 每次取号码个数
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(6)

        while not d(description='搜索',className='android.widget.TextView').exists:
            z.toast("等待进入微信")
            z.sleep(3)

        z.sleep(3)
        d( description='搜索', className='android.widget.TextView' ).click( )
        z.sleep(1)

        cate_id = int( args["repo_number_id"] )  # 得到取号码的仓库号
        while True:
            exist_numbers = self.repo.GetNumber( cate_id, 0, hello_count, 'exist', 'NO')
            print( exist_numbers )
            remain = hello_count - len( exist_numbers )
            normal_numbers = self.repo.GetNumber( cate_id, 0, remain, 'normal', 'NO')
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
                d(className='android.widget.ListView').child(className='android.widget.RelativeLayout', index=1).click( )

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
                    z.sleep( int(args['time_delay']) )
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
    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "269", "repo_material_id": "39", "hello_count": "1~3", "msg_count": "1", "time_delay": "3", 'run_time_min': '1', 'run_time_max': '3', 'start_time': '', 'stop_time': ''}    #cate_id是仓库号，length是数量
    o.action(d, z, args)