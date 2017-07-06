# coding:utf-8
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

    def timeinterval(self, d, z, args):
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        d1 = datetime.datetime.strptime( nowtime, '%Y-%m-%d %H:%M:%S' )
        logging.info( '现在的时间%s' % nowtime )
        gettime = cache.get( '%s_WXAssignSearchHello_time' % d.server.adb.device_serial( ) )
        logging.info( '以前的时间%s' % gettime )

        if gettime != None:
            d2 = datetime.datetime.strptime( gettime, '%Y-%m-%d %H:%M:%S' )
            delta1 = (d1 - d2)
            print( delta1 )
            delta = re.findall( r"\d+\.?\d*", str( delta1 ) )  # 将天小时等数字拆开
            day1 = int( delta[0] )
            hours1 = int( delta[1] )
            minutes1 = 0
            if 'days' in str( delta1 ):
                minutes1 = int( delta[2] )
                allminutes = day1 * 24 * 60 + hours1 * 60 + minutes1
            else:
                allminutes = day1 * 60 + hours1  # 当时间不超过天时此时天数变量成为小时变量
            logging.info( "day=%s,hours=%s,minutes=%s" % (day1, hours1, minutes1) )

            logging.info( '两个时间的时间差%s' % allminutes )
            run_time = int( args['run_time'] ) * 60  # 得到设定的时间
            if allminutes < run_time:  # 由外界设定
                z.toast( '该模块未满足指定时间间隔,程序结束' )
                return 'end'
        else:
            z.toast( '尚未保存时间' )

    def action(self, d,z, args):
        z.heartbeat()
        condition = self.timeinterval( d, z, args )
        if condition == 'end':
            z.sleep( 2 )
            return

        msg_count = int(args['msg_count'])
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(5)

        d(description='搜索',className='android.widget.TextView').click()
        z.sleep(1)

        cate_id = int( args["repo_number_id"] )  # 得到取号码的仓库号
        number_count = int( args['get_number'] )  # 每次取号码个数
        while True:
            exist_numbers = self.repo.GetNumber( cate_id, 8888, number_count, 'exist' )
            print( exist_numbers )
            remain = number_count - len( exist_numbers )
            normal_numbers = self.repo.GetNumber( cate_id, 8888, remain, 'normal' )
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
                d( textContains='微信号:' ).click( )
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
                    d( text='发送' ).click( )
                    z.sleep( 5 )
                d( descriptionContains='返回' ).click( )
                z.sleep( 1 )
                d( descriptionContains='清除' ).click( )
            else:
                d( descriptionContains='清除' ).click( )
                z.sleep( 1.5 )

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        cache.set( '%s_WXAssignSearchHello_time' % d.server.adb.device_serial( ), nowtime, None )
        z.toast( '模块结束，保存的时间是%s' % nowtime )


def getPluginClass():
    return WXAssignSearchHello

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
    args = {"repo_number_id": "44", "repo_material_id": "39","msg_count": "1", "get_number": "10", "run_time":"1"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
