# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from zcache import cache
import re
import logging
logging.basicConfig(level=logging.INFO)

class WXAutoReplyMsg:
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
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.sleep(7)

        msg_count = int(args['msg_count'])

        while True:
            if d( text='发现' ).exists and d( text='我' ).exists and d( text='通讯录' ).exists:
                d(text='微信').click()
                break
            else:
                d( descriptionContains='返回', className='android.widget.ImageView' ).click( )
        z.sleep(2)
        i = 0
        while True:
            i = i + 1
            nearObj = d(className='android.widget.ListView', index=0).child(className='android.widget.LinearLayout', index=i).child(
                className='android.widget.RelativeLayout',index=0).child(className='android.widget.TextView', index=1)
            if nearObj.exists:
                nearObj.click()
                z.sleep(1.5)
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
                d( descriptionContains='返回' ).click()
                z.sleep( 1 )
            else:
                if i > 18:
                    d.swipe( width / 2, height / 7, width / 2, height * 6 / 7 )
                    z.sleep(3)
                    i = 0
                continue


def getPluginClass():
    return WXAutoReplyMsg

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

    args = {"repo_material_id": "200", "msg_count": "1"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
