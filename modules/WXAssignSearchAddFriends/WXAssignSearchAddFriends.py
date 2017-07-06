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

class WXAssignSearchAddFriends:

    def __init__(self):
        self.repo = Repo()

    def timeinterval(self, d, z, args):
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        d1 = datetime.datetime.strptime( nowtime, '%Y-%m-%d %H:%M:%S' )
        logging.info( '现在的时间%s' % nowtime )
        gettime = cache.get( '%s_WXSearchAddFriends_time' % d.server.adb.device_serial( ) )
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
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(5)

        d(description='更多功能按钮',className='android.widget.RelativeLayout').click()
        z.sleep(1)
        if d(text='添加朋友').exists:
            d(text='添加朋友').click()
        else:
            d(description='更多功能按钮', className='android.widget.RelativeLayout').click()
            z.sleep(1)
            d(text='添加朋友').click()
        z.heartbeat()
        d(index='1',className='android.widget.TextView').click()   #点击搜索好友的输入框

        cate_id = int( args["repo_number_id"] )  # 得到取号码的仓库号
        number_count = int( args['get_number'] )  # 每次取一个号码
        while True:
            exist_numbers = self.repo.GetNumber( cate_id, 8888, number_count, 'exist' )
            remain = number_count - len( exist_numbers )
            normal_numbers = self.repo.GetNumber( cate_id, 8888, remain, 'normal' )
            numbers = exist_numbers + normal_numbers
            if len( numbers ) > 0:
                break
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，结束运行\"" % cate_id ).communicate( )
            z.sleep( 30 )
        if len( numbers ) <= 0:
            return

        for i in range(len(numbers)):

            WXnumber = numbers[i]['number']
            z.input( WXnumber )
            z.heartbeat( )
            z.sleep( 3 )
            d( textContains='搜索:' ).click( )
            while d(textContains='正在查找联系人').exists:
                z.sleep(2)

            if d( textContains='操作过于频繁' ).exists:
                continue
                # return
            z.sleep( 2 )
            if d( textContains='用户不存在' ).exists:
                d( descriptionContains='清除', index=2 ).click( )
                z.sleep( 1 )
                continue
            if d( textContains='状态异常' ).exists:
                d( descriptionContains='清除', index=2 ).click( )
                continue
            z.heartbeat( )

            if d( text='设置备注和标签' ).exists:
                d( text='设置备注和标签' ).click( )
                z.sleep( 3 )
                beizhuObj = d( className='android.widget.EditText', index=1 )
                if beizhuObj.exists:
                    deltext = beizhuObj.info  # 将之前消息框的内容删除
                    deltext = deltext['text']
                    lenth = len( deltext )
                    m = 0
                    while m < lenth:
                        d.press.delete( )
                        m = m + 1
                    z.input( WXnumber )
                    d( text='保存' ).click( )
                    z.sleep( 3 )

            z.heartbeat( )
            if d( text='添加到通讯录' ).exists:  # 存在联系人的情况
                d( text='添加到通讯录' ).click( )

                if d( text='发消息' ).exists:
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='清除' ).click( )
                    continue
                elif d( text='验证申请' ).exists:
                    d( text='发送' ).click( )
                    z.sleep( 2 )
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 2 )
                    d( descriptionContains='清除' ).click( )
                    continue
                else:
                    if d( text='取消' ).exists:
                        d( text='取消' ).click( )
                        d( descriptionContains='返回' ).click( )
                        z.sleep( 3 )
                        d( descriptionContains='清除' ).click( )
                        continue

                    if d( text='确定' ).exists:
                        d( text='确定' ).click( )
                        d( descriptionContains='返回' ).click( )
                        z.sleep( 3 )
                        d( descriptionContains='清除' ).click( )
                        continue

                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='清除' ).click( )
                    continue
            elif d( text='发消息' ).exists:
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='清除' ).click( )
                    continue

def getPluginClass():
    return WXAssignSearchAddFriends

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
    args = {"repo_number_id": "131","get_number": "10"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
