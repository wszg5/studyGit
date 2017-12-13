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
<<<<<<< HEAD
=======

        Str = d.info  # 获取屏幕大小等信息
        height = float( Str["displayHeight"] )
        width = float( Str["displayWidth"] )
>>>>>>> facaf2f92b3245033c2f6322d18dbd855f0e4f29

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
<<<<<<< HEAD
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
=======
        cate_id = int( args["repo_material_people_id"] )  # 得到取呢称的仓库号
        while True:
            Material_People = self.repo.GetMaterial( cate_id, 0, hello_count)
            if len( Material_People ) > 0:
>>>>>>> facaf2f92b3245033c2f6322d18dbd855f0e4f29
                break

            d.server.adb.cmd( "shell", "am broadcast -a com.zunyun.zime.toast --es msg \"呢称素材%s号仓库为空，等待中……\"" % cate_id ).communicate( )
            z.sleep( 10 )

        for i in range( len( Material_People ) ):
            if d( text='通讯录' ).exists:
                d( text='通讯录' ).click( )

            p = 0
            WXnema = Material_People[i]['content']
            while True:
                p += 1
                if d(text=WXnema).exists:
                    d(text=WXnema).click()
                    break
                else:
                    d.swipe( width / 2, height * 6 / 7, width / 2, height / 7 )
                    if p > 30:
                        z.toast("当前微信号没有此好友： "+ WXnema)
                        break
            if p > 30:
                continue

            z.heartbeat( )
            z.sleep( 3 )
<<<<<<< HEAD
            if d( textContains='联系人' ).exists or d( textContains='最常使用' ).exists:
                d(className='android.widget.ListView').child(className='android.widget.RelativeLayout', index=1).click( )
=======
            if d( text='发消息' ).exists and d( text='视频聊天' ).exists:
                d(text='发消息').click()
>>>>>>> facaf2f92b3245033c2f6322d18dbd855f0e4f29

                z.sleep( 1 )
                for i in range( 0, msg_count ):
                    cateid = args["repo_material_msg_id"]
                    Material = self.repo.GetMaterial( cateid, 0, 1 )
                    if len( Material ) == 0:
                        d.server.adb.cmd( "shell",
                                          "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cateid ).communicate( )
                        z.sleep( 10 )
                        return
                    message = Material[0]['content']  # 取出发送消息的内容
                    d( className='android.widget.EditText' ).click( )
                    z.input( message )
                    z.sleep( 1 )
                    d( text='发送' ).click()
                    z.sleep( int(args['time_delay']) )
                d( descriptionContains='返回' ).click( )

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
<<<<<<< HEAD
    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "269", "repo_material_id": "39", "hello_count": "1~3", "msg_count": "1", "time_delay": "3", 'run_time_min': '1', 'run_time_max': '3', 'start_time': '', 'stop_time': ''}    #cate_id是仓库号，length是数量
=======
    d = Device("HT4A1SK02114")
    z = ZDevice("HT4A1SK02114")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_people_id": "167", "repo_material_msg_id": "39", "hello_count": "1~3", "msg_count": "1", "time_delay": "3", 'run_time_min': '1', 'run_time_max': '3', 'start_time': '', 'stop_time': ''}    #cate_id是仓库号，length是数量
>>>>>>> facaf2f92b3245033c2f6322d18dbd855f0e4f29
    o.action(d, z, args)