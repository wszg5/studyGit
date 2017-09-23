# coding:utf-8
import os
import time, datetime
from uiautomator import Device
from zservice import ZDevice


class SSTPONorOFF:
    def __init__(self):
        self.mid = os.path.realpath( __file__ )

    def action(self, d, z,args):
        z.toast( "SSTP开关切换ip模块：开始执行" )
        z.server.adb.run_cmd( "shell",
                              "am start -n it.colucciweb.sstpvpnclient/it.colucciweb.sstpvpnclient.MainActivity" )  # 唤醒一号通SSTP客户端
        z.sleep( 3 )
        if d( textContains='已断开连接' ).exists:
            d( resourceId='it.colucciweb.sstpvpnclient:id/start_stop' ).click( )
        else:
            d( resourceId='it.colucciweb.sstpvpnclient:id/start_stop' ).click( )
            z.sleep(int(args["time_delay"]))
            d( resourceId='it.colucciweb.sstpvpnclient:id/start_stop' ).click( )
        z.sleep( 5 )
        d.press.home( )



def getPluginClass():
    return SSTPONorOFF

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT53ASK01833")
    z = ZDevice("HT53ASK01833")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"time_delay": "3"};
    o.action(d, z, args)

