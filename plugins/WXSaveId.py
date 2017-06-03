# coding:utf-8
from uiautomator import Device
from Repo import *
from zservice import ZDevice
import datetime
import re
from zcache import cache
import logging
logging.basicConfig(level=logging.INFO)

class WXSaveId:
    def __init__(self):
        self.repo = Repo()

    def timeinterval(self,d,z,args):
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' ) # 将日期转化为字符串 datetime => string
        logging.info('现在的时间%s'%nowtime)
        gettime = cache.get( '%s_time'%d.server.adb.device_serial() )
        logging.info('以前的时间%s'%gettime)
        d1 = datetime.datetime.strptime( nowtime, '%Y-%m-%d %H:%M:%S' )
        if gettime != None:
            d2 = datetime.datetime.strptime( gettime, '%Y-%m-%d %H:%M:%S' )
            delta1 = (d1 - d2)
            #print( delta1 )
            delta = re.findall( r"\d+\.?\d*", str( delta1 ) )   #将天小时等数字拆开
            day1 = int( delta[0] )
            hours1 = int( delta[1] )
            minutes1 = 0
            if 'days' in str(delta1):
                minutes1 = int( delta[2] )
                allminutes = day1 * 24 * 60 + hours1 * 60 + minutes1
            else:
                allminutes = day1*60 + hours1      #当时间不超过天时此时天数变量成为小时变量
            logging.info( "day=%s,hours=%s,minutes=%s" % (day1, hours1, minutes1) )


            logging.info('两个时间的时间差%s'%allminutes)
            set_time = int(args['set_time'])     #得到设定的时间
            if allminutes < set_time:  # 由外界设定
                z.toast( '该模块未满足指定时间间隔,程序结束' )
                return 'end'
            else:
                cache.set( '%s_time'%d.server.adb.device_serial(), nowtime )

        else:
            cache.set( '%s_time'%d.server.adb.device_serial(), nowtime )

    def action(self, d, z, args):
        condition = self.timeinterval(d,z,args)
        if condition=='end':
            z.toast('时间间隔不满足')
            z.sleep(2)
            return
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)
        cate_id = args['repo_wxcade_id']
        d(text='发现').click()
        d(text='附近的人').click()
        z.sleep(1)
        if d(text='开始查看').exists:
            d(text='开始查看').click()
            d(text='下次不提示').click()
            d(text='确定').click()
        z.sleep(2)

        if d(text='查看附近的人').exists:
            d( text='查看附近的人' ).click()
        while True:
            if d(description='更多').exists:
                break
            else:
                z.sleep(2)
        d(description='更多' ).click()
        gender = args['gender']
        if gender=='男':
            d(text='只看男生').click()
            z.sleep(5)
        elif gender=="女":
            d(text='只看女生').click()
            z.sleep(5)
        else:
            d(text='查看全部').click()
            z.sleep(5)

        serial = z.wx_action("opennearui")  # 得到微信ｉｄ，字符串样式
        print(serial)
        ids = json.loads(serial)  # 将字符串改为list样式
        print(ids)
        lenth = len(ids)
        z.heartbeat()

        for i in range(lenth):
            z.heartbeat()
            wxid = ids[i]
            print(wxid)
            if 'v1_' not in wxid:
                continue
            self.repo.uploadPhoneNumber(wxid, cate_id)
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return WXSaveId


if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_wxcade_id": "131",'set_time':'0', 'gender':"不限",'time_delay': "3"}  # cate_id是仓库号，length是数量
    o.action(d, z, args)


