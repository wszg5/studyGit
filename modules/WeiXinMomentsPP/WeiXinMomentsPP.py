# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from zcache import cache
import re
import logging
logging.basicConfig(level=logging.INFO)

class WeiXinMomentsPP:

    def __init__(self):
        self.repo = Repo()

    def timeinterval(self, z, args):
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        logging.info( '现在的时间%s' % nowtime )
        gettime = cache.get( 'WeiXinMoments_time' )
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
                cache.set( 'WeiXinMoments_time', nowtime )

        else:
            cache.set( 'WeiXinMoments_time', nowtime )

    def action(self, d,z, args):
        condition = self.timeinterval( z, args )
        if condition == 'end':
            z.sleep( 2 )
            return
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.heartbeat()
        d.press.home( )
        if d( text='微信' ).exists:
            d( text='微信' ).click( )
        else:
            # d.swipe( width - 20, height / 2, 0, height / 2, 5 )
            z.toast( '该页面没有微信' )
            z.sleep( 2 )
            return
        z.sleep( 5 )
        while True:
            if d( text='发现' ) and d( text='我' ) and d( text='通讯录' ).exists:
                break
            else:
                d( descriptionContains='返回', className='android.widget.ImageView' ).click( )
        d(className='android.widget.RelativeLayout', index=3).child(text='我').click()
        wxname = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=1)\
            .child(className='android.widget.LinearLayout',index=1).child(className='android.view.View').info   #得到微信名，为了判断朋友圈哪些已被我点赞评论
        myname = wxname['text']
        z.heartbeat()
        z.wx_action('opensnsui')
        z.sleep(3)
        # myname = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=0).child(
        #     className='android.widget.TextView').info
        # myname = myname['text']
        d.swipe(width / 2, height * 4 / 5, width / 2, height / 4)
        z.sleep(1)
        z.heartbeat()
        i = 0
        t = 0
        EndIndex = int(args['EndIndex'])         #------------------
        while t < EndIndex :
            cate_id = args["repo_material_id"]   #------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                z.sleep(10)
                return
            message = Material[0]['content']  # 从素材库取出的要发的材料

            judexist = d(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=i).child(className='android.widget.FrameLayout').child(description='评论')   #首先看第i个人是否存在，
            if judexist.exists:
                z.heartbeat()
                obj1 = d(className='android.widget.ListView').child(className='android.widget.FrameLayout', index=i).child(className='android.widget.LinearLayout',index=4)    #判断该好友是否有点赞评论
                if obj1.exists:  #给该好友评论的情况
                    z.heartbeat()
                    getName = d(className='android.widget.FrameLayout', index=i).child(className='android.widget.LinearLayout',index=4).child(index=0,className='android.widget.TextView')
                    if getName.exists:
                        getName = getName.info
                        getName = getName['text']
                        if myname in getName:
                            i = i + 1
                            continue

                obj2 = d(className='android.widget.ListView').child(className='android.widget.FrameLayout', index=i).child(className='android.widget.LinearLayout',index=3)    #判断该好友是否有点赞评论,没有图片index会少一个
                if obj2.exists:  #给该好友评论的情况
                    z.heartbeat()
                    getName1 = d(className='android.widget.FrameLayout', index=i).child(className='android.widget.LinearLayout',index=3).child(index=0,className='android.widget.TextView')
                    if getName1.exists:
                        getName1 = getName1.info
                        getName1 = getName1['text']
                        if myname in getName1:
                            i = i + 1
                            continue
                z.heartbeat()
                judexist.click()
                if d(text='赞').exists:
                    d(text='赞').click()
                    time.sleep(0.5)
                else:                         #赞被屏幕遮住的情况
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    z.heartbeat()
                    z.sleep(2)
                    if d(className='android.widget.FrameLayout', index=0).child(className='android.widget.FrameLayout', index='3').child(description='评论').exists:
                        i = 0
                    else:
                        i = 1
                    continue
                z.heartbeat()
                time.sleep(0.5)
                judexist.click()
                d(text='评论').click()
                d(className='android.widget.EditText').click()
                z.input(message)
                d(text='发送').click()
                i = i+1
                t = t+1
                continue
            else:

                obja = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=2).child(className='android.widget.LinearLayout')\
                    .child(className='android.widget.LinearLayout').child(className='android.widget.ImageView')
                if obja.exists:
                    return
                d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                z.sleep(2)
                z.heartbeat()
                obj = d(className='android.widget.ListView').child(className='android.widget.FrameLayout',
                                                                   index=0).child(
                    className='android.widget.FrameLayout').child(description='评论')
                if obj.exists:
                    i = 0
                    continue
                else:
                    i = 1
                    continue
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return WeiXinMomentsPP

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

    args = {"repo_material_id": "39",'set_time':'3','EndIndex':'100',"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)






