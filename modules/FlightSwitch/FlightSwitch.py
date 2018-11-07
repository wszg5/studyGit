# coding:utf-8
import httplib
import os
import re

from const import const
from uiautomator import Device

from zservice import ZDevice

class FlightSwitch:
    def __init__(self):
        pass

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "settings put global airplane_mode_on 1").communicate()
        d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true").communicate()
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))
        z.heartbeat()
        d.server.adb.cmd("shell", "settings put global airplane_mode_on 0").communicate()
        d.server.adb.cmd("shell", "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false").communicate()
        z.sleep(8)
        z.heartbeat()
        ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
        info = ping[0]
        ip = re.findall(r'\d+\.\d+\.\d+\.\d+', info)[0]
        print ip
        result = self.ooo(z,ip,'10000','ABCD')
        if not result:
            self.action(d,z,args)


    def checkIp(self, number, id, type):
        path = "/repo_api/number/writeBackInfo?number=%s&id=%s&type=%s" % (number, id, type)
        domain = const.REPO_API_IP
        port = 8888
        # domain = 'data.161998.com'
        # port = 80
        conn = httplib.HTTPConnection( domain, port, timeout=30 )
        conn.request( "GET", path )
        response = conn.getresponse( )
        if response.status == 200:
            data = response.read( )
            return data
        else:
            return []
            # get my ipaddress anf disconnect broadband connection.

    '/repo_api/number/writeBackInfo?number=123.138.12.14&id=10001&type=AB'

    def ooo(self, z, ip, id, idType):
        # if exist running broadband connection, disconnected it.
            # self.ShowIpAddress(pid)
        # if len( idType ) > 4:
        #     return
        # try:
        #     ipArr = ip.split( "." )
        # except:
        #     return
        z.toast("ip: %s" % ip)
        # ip2 = ""
        # if len( idType ) == 2:
        #     ip2 = ipArr[0] + "." + ipArr[1]
        # elif len( idType ) == 3:
        #     ip2 = ipArr[0] + "." + ipArr[1] + "." + ipArr[2]
        # elif len( idType ) == 4:
        #     ip2 = ip
        result2 = self.checkIp( ip, id, "ABCD" )
        if result2 == "guolv":
            print u"[ ip 重复 ]"
            z.toast( u"[ ip 重复 ]" )
            return False
        else:
            print u"[ ip 没重复 ]"
            z.toast( u"[ ip 没重复 ]" )
        # result = self.checkIp( ip2, id, "AB" )
        # if result == "guolv":
        #     print u"[ ip 黑了 ]"
        #     z.toast( u"[ ip 黑了 ]" )
        #     return False
        # else:
        #     if len( idType ) == 4:
        #         ip2 = ipArr[0] + "." + ipArr[1] + "." + ipArr[2]
        #         result = self.checkIp( ip2, id, "AB" )
        #         if result == "guolv":
        #             print u"[ ip 黑了 ]"
        #             z.toast( u"[ ip 黑了 ]" )
        #             return False
        #         else:
        #             print u"[ip 没黑]"
        #             result2 = self.checkIp( ip, id, "ABCD" )
        #             if result2 == "guolv":
        #                 print u"[ ip 重复 ]"
        #                 z.toast( u"[ ip 重复 ]" )
        #                 return False
        #             else:
        #                 z.toast( u"[ ip 没重复 ]" )
        #     else:
        #         print u"[ip 没黑]"
        #         result2 = self.checkIp( ip, id, "ABCD" )
        #         if result2 == "guolv":
        #             print u"[ ip 重复 ]"
        #             z.toast( u"[ ip 没重复 ]" )
        #             return False
        return True


def getPluginClass():
    return FlightSwitch

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cc0e9474")
    z = ZDevice("cc0e9474")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()


    args = {"time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

    '123.125.115.110'
