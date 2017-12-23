# coding:utf-8
import os

from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXAUTOAgreedVerify:

    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum


    def impContact(self, d,z, args):
        z.heartbeat()
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)

        filename = os.path.join(base_dir, "%s.txt"%(self.GetUnique()) )
        file_object = open( filename, 'w' )
        lines = ""
        pname = "系统号码"
        lines = "%s%s----%s\r" % (lines, pname, '13376085678')

        file_object.writelines( lines )
        file_object.close( )
        isclear = '是'
        if isclear == '是':
            d.server.adb.cmd( "shell", "pm clear com.android.providers.contacts" ).communicate( )

        d.server.adb.cmd( "push", filename, "/data/local/tmp/contacts.txt" ).communicate( )
        d.server.adb.cmd( "shell", "am", "start", "-n", "com.zunyun.zime/.ImportActivity", "-t", "text/plain", "-d",
                       "file:////data/local/tmp/contacts.txt" ).communicate( )
        os.remove( filename )
        out = d.server.adb.cmd( "shell",
                                "dumpsys activity top  | grep ACTIVITY" ).communicate( )[0].decode( 'utf-8' )
        while out.find( "com.zunyun.zime/.ImportActivity" ) > -1:
            z.heartbeat( )
            out = d.server.adb.cmd( "shell",
                                    "dumpsys activity top  | grep ACTIVITY" ).communicate( )[0].decode( 'utf-8' )
            z.sleep( 5 )




    def action(self, d, z, args):
        z.toast( "正在ping网络是否通畅" )
        while True:
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                break
            z.sleep( 2 )

        z.toast( "开始执行：微信自动同意验证请求" )
        run_time_min = int( args['run_time_min'] )
        run_time_max = int( args['run_time_max'] )
        run_time = float( random.randint( run_time_min, run_time_max ) ) * 60
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'模块在锁定时间内，无法运行' )
            z.sleep(2)
            return

        start_time = args['start_time']
        stop_time = args['stop_time']
        try:
            if self.repo.timeCompare( start_time, stop_time ):
                z.toast('处于' + start_time + '～' + stop_time + '时间段内，模块不运行' )
                z.sleep(2)
                return
        except:
            logging.exception("exception")
            z.toast("输入时间格式有误")
            return

        z.toast("清空通讯录,添加系统号")
        self.impContact(d, z, args)
        if (args["time_delay1"]):
            z.sleep(int(args["time_delay1"]))
            z.heartbeat()

        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来

        z.sleep(20)
        z.heartbeat()
        if d(text='通讯录').exists:
            d( text='通讯录').click()
            z.sleep(2)

        if d(text='新的朋友').exists:
            d(text='新的朋友').click()

        GGObj = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=0).child(
            className='android.widget.RelativeLayout', index=1).child(className='android.widget.LinearLayout', index=0).child(
            className='android.widget.LinearLayout', index=1)

        if GGObj.exists:
            GGObj.click()

        set1 = set()
        length = 0
        i = 1
        while True:
            z.sleep(2)
            wxname = d(className='android.widget.ListView').child(className='android.widget.RelativeLayout', index=i).child(className='android.widget.RelativeLayout')
            if wxname.exists:
                z.heartbeat()
                nameObj = wxname.child(className='android.widget.RelativeLayout', index=1).child(className='android.widget.TextView', index=0)
                if nameObj.exists:
                    name = nameObj.info['text']  # 得到微信名
                    if name in set1:  # 判断是否已经给该人发过消息
                        i = i + 1
                        continue
                    else:
                        set1.add(name)
                    print(name)

                weiAdd = wxname.child(className='android.widget.RelativeLayout', index=2).child(text='接受')  # 该编号好友添加的情况
                yiAdd = wxname.child(className='android.widget.RelativeLayout', index=2).child(text='已添加')  # 该编号好友添加的情况
                if weiAdd.exists:
                    weiAdd.click()
                    z.sleep(1)
                    if d(text='完成').exists:
                        d(text='完成').click()
                        z.sleep(3)
                    if d(text='发消息').exists:
                        d(description='返回').click()
                        z.sleep(2)
                        wxname.child( className='android.widget.RelativeLayout', index=2).long_click()
                        if d(text='删除').exists:
                            d(text='删除').click()
                    continue
                elif yiAdd.exists:
                    wxname.child( className='android.widget.RelativeLayout', index=2 ).long_click( )
                    if d( text='删除' ).exists:
                        d( text='删除' ).click( )
                else:
<<<<<<< HEAD
                    i = i + 1
=======
                    wxname.child( className='android.widget.RelativeLayout', index=2 ).long_click( )
                    if d( text='删除' ).exists:
                        d( text='删除' ).click( )
                    # i = i + 1
>>>>>>> facaf2f92b3245033c2f6322d18dbd855f0e4f29
                    continue

            else:
                if len(set1) == length:
                    break
                else:
                    length = len(set1)
                    d.swipe( width / 2, height * 6 / 7, width / 2, height / 7 )
                    i = 1
                    continue

        now = datetime.datetime.now()
        nowtime = now.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun(self.mid)
        z.toast('模块结束，保存的时间是%s' % nowtime)

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXAUTOAgreedVerify

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

    args = {'run_time_min': '1', 'run_time_max': '3', 'start_time': '', 'stop_time': '', "time_delay1": "30", "time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d, z, args)

































