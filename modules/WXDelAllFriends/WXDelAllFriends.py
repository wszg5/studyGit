# coding:utf-8
from uiautomator import Device
from Repo import *
from zservice import ZDevice

class WXDelAllFriends:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)
        d(text='通讯录').click()
        d(className='android.widget.LinearLayout').child(text='通讯录').click()
        i = 1
        judexist = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=1)
        while True:
            if judexist.exists:
                judexist.click()
                if d(description='更多').exists:
                    d(description='更多').click()
                else:
                    d(description='返回').click()   #当点击的人是自己的情况
                    judexist = d( className='android.widget.ListView' ).child( className='android.widget.LinearLayout',index=2 )
                    continue

                if d(text='删除').exists:
                    d(text='删除').click()
                    d(text='删除').click()
                else:
                    d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
                    d(text='删除').click()
                    d(text='删除').click()

            else:
                break

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXDelAllFriends

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {'time_delay':"3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
