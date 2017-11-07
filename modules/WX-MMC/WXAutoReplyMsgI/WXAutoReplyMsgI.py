# coding:utf-8
import os

from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from zcache import cache
import re
import logging
logging.basicConfig(level=logging.INFO)

class WXAutoReplyMsgI:
    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )

    def action(self, d,z, args):
        z.toast( "正在ping网络是否通畅" )
        while True:
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                break
            z.sleep( 2 )

        z.toast( "开始执行：微信监测自动回复 循环监测" )
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
            if self.repo.timeCompare( start_time, stop_time ):
                z.toast( '处于' + start_time + '～' + stop_time + '时间段内，模块不运行' )
                z.sleep( 2 )
                return
        except:
            logging.exception( "exception" )
            z.toast( "输入时间格式有误" )
            return

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(20)
        z.heartbeat()

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        msg_count = int(args['msg_count'])

        while True:
            if d( text='发现' ).exists and d( text='我' ).exists and d( text='通讯录' ).exists:
                d(text='微信').click()
                break
            else:
                d( descriptionContains='返回', className='android.widget.ImageView' ).click( )
        z.sleep(2)
        if d(text='腾讯新闻').exists:
            d(text='腾讯新闻').long_click()
            z.sleep(2)
            if d(text='删除该聊天').exists:
                d(text='删除该聊天').click()

        if d(text='微信团队').exists:
            d(text='微信团队').long_click()
            z.sleep(2)
            if d(text='删除该聊天').exists:
                d(text='删除该聊天').click()

        i = 1
        j = 0
        while True:
            nearObj = d(className='android.widget.RelativeLayout', index=0).child(className='android.widget.TextView', resourceId='com.tencent.mm:id/il', index=1)
            if nearObj.exists:
                if j > int(args['reply_count']):
                    break
                if nearObj.exists:
                    nearObj.click()
                z.sleep(1.5)
                for k in range( 0, msg_count ):
                    if d( textContains='(', resourceId='com.tencent.mm:id/gh' ).exists:
                        break
                    cate_id = args["repo_material_id"]
                    Material = self.repo.GetMaterial( cate_id, 0, 1 )
                    if len(Material) == 0:
                        d.server.adb.cmd("shell",
                                          "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id).communicate()
                        z.sleep(10)
                        return
                    message = Material[0]['content']  # 取出发送消息的内容
                    if d(className='android.widget.EditText').exists:
                        d(className='android.widget.EditText').click()
                    else:
                        break
                    z.input(message)
                    z.sleep(1)
                    d(text='发送').click()
                d(descriptionContains='返回').click()
                z.sleep(1)
                if d(className='android.widget.ListView', index=0).child(className='android.widget.LinearLayout',
                                                                         index=i).exists:
                    d(className='android.widget.ListView', index=0).child(className='android.widget.LinearLayout',
                                                                             index=i).long_click()
                if d(text='删除该聊天').exists:
                    d(text='删除该聊天').click()
                z.sleep( 1 )
                j += 1
            else:
                continue

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )


def getPluginClass():
    return WXAutoReplyMsgI

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

    args = {"repo_material_id": "207", "msg_count": "1","reply_count": "3", 'run_time_min': '1', 'run_time_max': '3', 'start_time': '', 'stop_time': ''}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
