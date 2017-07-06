# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from zcache import cache
import re
import logging
logging.basicConfig(level=logging.INFO)

class WXHelloNearPeople:
    def __init__(self):
        self.repo = Repo()

    def timeinterval(self, d, z, args):
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        d1 = datetime.datetime.strptime( nowtime, '%Y-%m-%d %H:%M:%S' )
        logging.info( '现在的时间%s' % nowtime )
        gettime = cache.get( '%s_WXHelloNearPeople_time' % d.server.adb.device_serial( ) )
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
        z.heartbeat( )
        condition = self.timeinterval( d, z, args )
        if condition == 'end':
            z.sleep( 2 )
            return

        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.sleep(7)

        while True:
            if d( text='发现' ).exists and d( text='我' ).exists and d( text='通讯录' ).exists:
                break
            else:
                d( descriptionContains='返回', className='android.widget.ImageView' ).click( )

        z.sleep(2)
        for i in range(0, 2):
            d(text='发现').click()
            z.sleep(2)
        if d(text='附近的人').exists:
            d(text='附近的人').click()
            z.sleep(15)

        if d(textContains='开始查看').exists:
            d(textContains='开始查看').click()
            z.sleep(1.5)
        if d(textContains='下次不提示').exists:
            d(textContains='下次不提示').click()
        if d(text='确定').exists:
            d( text='确定' ).click()

        if d(text='查看附近的人').exists:
            d(text='查看附近的人').click()

        d( descriptionContains='更多' ).click( )
        gender = args['gender']
        if gender == '男':
            d(text='只看男生').click()
            z.sleep(3)
        elif gender == '女':
            d( text='只看女生' ).click()
            z.sleep( 3 )
        else:
            d( text='查看全部' ).click()
            z.sleep( 3 )

        z.sleep(8)
        i = 0
        count = 0
        while True:
            count = count + 1
            if count > int(args['hello_count']):
                logging.info(count)
                logging.info(args['hello_count'])
                logging.info('---------------------打招呼次数和设置次数------------------------')
                z.toast('已完成设置打招呼次数')
                break
            i = i + 1
            nearObj = d(className='android.widget.ListView', index=0).child(className='android.widget.LinearLayout', index=i)
            if nearObj.exists:
                if d(textContains='朋友不够多').exists:
                    continue
                nearObj.click()
                if d(text='打招呼').exists:
                    d(text='打招呼').click()
                    z.sleep(2)
                if d(text='向TA说句话打个招呼').exists:
                    cate_id = args['repo_material_id']
                    Material = self.repo.GetMaterial(cate_id, 0, 1)
                    Msg = Material[0]['content']
                    z.input(Msg)
                    z.sleep(1.5)
                d(text='发送').click()
                z.sleep(3)
                d( descriptionContains='返回', className='android.widget.ImageView' ).click( )
                z.sleep(2)
            else:
                i = 1
                d.swipe( width / 2, height * 7 / 8, width / 2, height / 8 )

        logging.info('---------------------------------------开始保存时间--------------------------------------')
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        cache.set( '%s_WXHelloNearPeople_time' % d.server.adb.device_serial( ), nowtime, None )
        z.toast('模块结束，保存的时间是%s' % nowtime)
        logging.info(nowtime)
        logging.info('---------------------------------------结束保存时间-------------------------------------')


def getPluginClass():
    return WXHelloNearPeople

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

    args = {"repo_material_id": "40", "hello_count": "10", 'gender': '不限', 'run_time': "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
