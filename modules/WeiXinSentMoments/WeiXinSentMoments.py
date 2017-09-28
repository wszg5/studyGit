# coding:utf-8
import os

from uiautomator import Device
from Repo import *
import datetime
from zservice import ZDevice

class WeiXinSentMoments:

    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )


    def action(self, d, z, args):
        run_time = float( args['run_time'] ) * 60
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return

        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(5)
        cate_id = args["repo_material_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        if len(Material) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id).communicate()
            z.sleep(10)
            return
        message = Material[0]['content']  # 取出验证消息的内容

        z.heartbeat()
        z.wx_sendtextsns(message)
        z.sleep(3)
        # z.input('.')
        # d.press.delete()
        d(text='发送').click()


        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )

        z.heartbeat()
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return WeiXinSentMoments

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

    args = {"repo_material_id": "257","run_time": "1","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)



















