# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from zcache import cache
import re
import logging
logging.basicConfig(level=logging.INFO)
class WXPictureMoment:

    def __init__(self):
        self.repo = Repo()

    def timeinterval(self, z, args):
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        logging.info( '现在的时间%s' % nowtime )
        gettime = cache.get( 'WXPictureMoment_time' )
        logging.info( '以前的时间%s' % gettime )
        d1 = datetime.datetime.strptime( nowtime, '%Y-%m-%d %H:%M:%S' )
        if gettime != None:
            d2 = datetime.datetime.strptime( gettime, '%Y-%m-%d %H:%M:%S' )
            delta1 = (d1 - d2)
            # print( delta1 )
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
            set_time = int( args['set_time'] )  # 得到设定的时间
            if allminutes < set_time:  # 由外界设定
                z.toast( '该模块未满足指定时间间隔,程序结束' )
                return 'end'
            else:
                cache.set( 'WXPictureMoment_time', nowtime )

        else:
            cache.set( 'WXPictureMoment_time', nowtime )

    def action(self, d,z, args):
        condition = self.timeinterval(z, args )
        if condition == 'end':
            z.sleep( 2 )
            return
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(8)
        # d(className='android.widget.RelativeLayout', index=3).child(text='我').click()
        obj = d.server.adb.device_serial()     #　获取设备序列号

        # if d(textContains='微信号：').exists:
        #     obj = d(textContains='微信号：').info
        #     obj = obj['text']
        #
        # else:
        #     obj = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=1)\
        #         .child(className='android.widget.LinearLayout',index=1).child(className='android.view.View').info
        #     obj = obj['text']
        cate_id = args['repo_material_id']
        materials = self.repo.GetMaterial(cate_id, 0, 1,obj)
        if len(materials) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"朋友圈素材%s号仓库为空，等待中\"" % cate_id).communicate()
            z.sleep(10)
            return
        t = materials[0]  # 取出验证消息的内容
        z.heartbeat()
        imgs = []
        for i in range(1,10,+1):
            z.heartbeat()
            if t['ext%s'%i] is not None:
                imgs.append(t['ext%s'%i])
        z.heartbeat()
        z.wx_sendsnsline(t["content"], imgs)
        d(text='发送').click()

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXPictureMoment

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A1SK02114")
    z = ZDevice("HT4A1SK02114")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id": "258",'set_time':'3',"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
    # repo = Repo()
    # para = {"PhoneNumber": "http://url.cn/5A2br6W#flyticket", "x_key": "x_01", "x_value": "448856030"}
    # list = repo.GetTIMInfomation("253",para)
    # print(list)



















