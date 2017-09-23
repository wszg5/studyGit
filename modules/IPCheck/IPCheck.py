# coding:utf-8
from uiautomator import Device
from Repo import *
from zcache import cache
from zservice import ZDevice


class IPCheck:
    def __init__(self):
        self.repo = Repo()


    def action(self,d,z,args):
        z.toast("开始执行：检测手机IP模块")
        while True:
            # 开关飞行模式
            d.server.adb.cmd( "shell", "settings put global airplane_mode_on 1" ).communicate( )
            d.server.adb.cmd( "shell",
                              "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true" ).communicate( )
            z.sleep( 6 )
            d.server.adb.cmd( "shell", "settings put global airplane_mode_on 0" ).communicate( )
            d.server.adb.cmd( "shell",
                              "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false" ).communicate( )
            while True:
                ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
                print(ping)
                if 'icmp_seq'and 'bytes from'and'time' in ping[0]:
                    break
                z.sleep(2)

            # 获取手机IP
            IPList = d.server.adb.cmd( "shell", "curl http://ipecho.net/plain" ).communicate( )
            IP = IPList[0]
            print( IP )

            # IP添加到缓存
            ip = cache.get( IP )
            print(ip)
            if ip is None:
                timeoutStr = args['time_out']
                timeout = int( timeoutStr ) * 60
                cache.set( IP, IP, timeout )
                break
            else:
                continue





def getPluginClass():
    return IPCheck

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4B7SK00086")
    z = ZDevice("HT4B7SK00086")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"time_out": "1"};
    o.action(d, z, args)
    # ip = cache.get( "117.61.158.146" )
    # print(ip)