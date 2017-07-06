# coding:utf-8
import datetime
from uiautomator import Device
from Repo import *
from zcache import cache
from zservice import ZDevice
from random import choice
import re
import logging
logging.basicConfig(level=logging.INFO)


class WXSearchAddDepost:

    def __init__(self):
        self.repo = Repo()

    def timeinterval(self, d, z, args):
        now = datetime.datetime.now()
        nowtime = now.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转化为字符串 datetime => string
        d1 = datetime.datetime.strptime(nowtime, '%Y-%m-%d %H:%M:%S')
        logging.info('现在的时间%s' % nowtime)
        gettime = cache.get('%s_WXSearchAddDepost_time' % d.server.adb.device_serial())
        logging.info('以前的时间%s' % gettime)

        if gettime != None:
            d2 = datetime.datetime.strptime(gettime, '%Y-%m-%d %H:%M:%S')
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
        condition = self.timeinterval( d, z, args )
        if condition == 'end':
            z.sleep( 2 )
            return

        z.heartbeat()

        count = 1
        while True:
            wayList = ['3','6','13','15','17','18','30','39']

            if count > int(args['add_count']):
                z.toast(args['add_count']+'个好友已加完')
                break

            cateId = args['repo_material_id']
            Material = self.repo.GetMaterial( cateId, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']  # 从素材库取出的要发的材料
            z.sleep( 1 )

            cate_id = args['repo_number_id']
            numberList = self.repo.GetNumber( cate_id, 0, 1 )
            v1 = numberList[0]['number']

            if args['add_friend_way'] == '随机':
                indexStr = choice(wayList)
            else:
                indexStr = args['add_friend_way']

            z.wx_openuser_v1(v1, indexStr)
            z.sleep(3)

            z.heartbeat()
            if d( text='添加到通讯录' ).exists:
                d( text='添加到通讯录' ).click( )
                z.sleep( 5 )

            if d(text='发消息').exists:
                count = count + 1

            if d(text='验证申请').exists:
                count = count + 1
                deltext = d( className='android.widget.EditText', index=1 ).info  # 将之前消息框的内容删除
                deltext = deltext['text']
                lenth = len( deltext )
                m = 0
                while m < lenth:
                    d.press.delete()
                    m = m + 1
                z.heartbeat()
                d( className='android.widget.EditText', index=1 ).click( )
                z.input( message )
                z.sleep( 2 )

                d( text='发送' ).click( )
                z.sleep( 1 )
                d( description='返回' ).click( )

            if d(text='确定').exists:
                d(text='确定').click()

            if d( descriptionContains='返回' ).exists:
                d( descriptionContains='返回' ).click( )

            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        cache.set( '%s_WXSearchAddDepost_time' % d.server.adb.device_serial( ), nowtime, None )
        z.toast( '模块结束，保存的时间是%s' % nowtime )


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
    args = {"repo_number_id": "198", "repo_material_id": "39", "add_count": "3", 'run_time':'0', "add_friend_way":"随机", "time_delay": "5"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
