# coding:utf-8
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class WXNormalDetection:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z,args):
        while d(text='提示').exists:
            d(text='确定').click()

        d.press.home()

        if d(text='微信').exists:
            d(text='微信').click()
            z.sleep(10)

        if d(text='登录') and d(text='忘记密码') and d(text='更多').exists:
            saveCate = args['repo_information_id']
            para = {'x_19': 'WXRegister','x_20':d.server.adb.device_serial(),'x_26':'登陆状态NO'}
            self.repo.PostInformation( saveCate, para )
        else:
            z.toast('该设备微信号正常')


def getPluginClass():
    return WXNormalDetection

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("916c6fd5")
    z = ZDevice("916c6fd5")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # d.server.adb.cmd("shell", "am start -a android.intent.action.MAIN -n com.android.settings/.Settings").communicate()    #打开android设置页面

    args = {"repo_information_id":"137", "time_delay": "1"};
    o.action(d, z, args)
