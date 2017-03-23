# coding:utf-8
from uiautomator import Device

from zservice import ZDevice

class FlightSwitch:


    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "settings put global airplane_mode_on 1").communicate()
        d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true").communicate()
        z.sleep(5)
        z.heartbeat()
        d.server.adb.cmd("shell", "settings put global airplane_mode_on 0").communicate()
        d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false").communicate()
        z.sleep(8)
        z.heartbeat()

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return FlightSwitch

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()


    args = {"repo_material_id":"39","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

