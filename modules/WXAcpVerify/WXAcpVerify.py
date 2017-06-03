# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from zcache import cache
import re
import logging
logging.basicConfig(level=logging.INFO)
class WXAcpVerify:
    def __init__(self):
        self.repo = Repo()

    def timeinterval(self, z, args):
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        logging.info( '现在的时间%s' % nowtime )
        gettime = cache.get( 'WXAcpVerify_time' )
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
                cache.set( 'WXAcpVerify_time', nowtime )

        else:
            cache.set( 'WXAcpVerify_time', nowtime )

    def action(self, d,z, args):
        condition = self.timeinterval( z, args )
        if condition == 'end':
            z.sleep( 2 )
            return
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)
        d(text='通讯录').click()
        d(className='android.widget.ListView').child(className='android.widget.RelativeLayout',index=1).click()
        z.sleep(1)
        z.heartbeat()
        set1 = set()
        change = 0
        i = 1
        while True:
            obj = d(className='android.widget.RelativeLayout', index=i).child(index=1).child(className='android.widget.TextView', index=0)  # 得到微信名
            if obj.exists:
                z.heartbeat()
                obj = obj.info
                name = obj['text']
                if name in set1:  # 判断是否已经给该人发过消息
                    i = i + 1
                    continue
                else:
                    set1.add(name)
                    print(name)
                z.heartbeat()
                obj2 = d(className='android.widget.RelativeLayout', index=i).child(index=2).child(text='接受')  # 看是否有加好友验证
                if obj2.exists:
                    z.heartbeat()
                    change = 1      #好友存在且未被添加的情况出现，change值改变

                    d(className='android.widget.ListView',index=0).child(className='android.widget.RelativeLayout',index=i).child(className='android.widget.RelativeLayout',index=1).click()      #点击第i个人
                    GenderFrom = args['gender']     #-------------------------------
                    if GenderFrom !='不限':
                        obj = d(className='android.widget.LinearLayout', index=1).child(
                            className='android.widget.LinearLayout').child(className='android.widget.ImageView',index=1)  # 看性别是否有显示
                        if obj.exists:
                            z.heartbeat()
                            Gender = obj.info
                            Gender = Gender['contentDescription']
                            if Gender !=GenderFrom:
                                           #如果性别不符号的情况
                                d(description='返回').click()
                                i = i+1
                                continue
                        else:                 #信息里没有显示出性别的话
                            d(description='返回').click()
                            i = i + 1
                            continue
                    d(text='通过验证').click()
                    d(text='完成').click()
                    z.heartbeat()
                    z.sleep(1)
                    d(description='返回').click()
                    i = i+1
                    continue
                else:
                    i = i+1
                    continue
            else:
                if change==0:   #一次还没有点击到人
                    if i==1:    #通讯录没有人的情况
                        return
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    i = 1
                    continue
                else:
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    obj = d(className='android.widget.RelativeLayout', index=i-1).child(index=1).child(className='android.widget.TextView', index=0)
                    obj = obj.info
                    name1 = obj['text']      #判断是否已经到底
                    if name1 in set1:
                        break
                    i = 1
                    continue

        if (args["time_delay"]):
                z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXAcpVerify

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {'gender':"男",'set_time':'3',"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)