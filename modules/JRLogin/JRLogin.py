# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class JRLogin:
    def __init__(self):
        self.repo = Repo()

    def action(self, d, z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.ss.android.article.news").communicate()  # 将今日头条强制停止
        # d.server.adb.cmd("shell", "pm clear com.ss.android.article.news").communicate()  # 清除缓存
        d.server.adb.cmd("shell", "am start -n com.ss.android.article.news/com.ss.android.article.news.activity.SplashActivity").communicate()  # 将今日头条拉起来
        time.sleep(7)
        cate_id = args["repo_cate_id"]
        numbers = self.repo.GetAccount(cate_id,120, 1)
        if len(numbers) == 0:
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.zime.toast --es msg \"QQ帐号库%s号仓库为空，等待中\"" % cate_id).communicate()
            time.sleep(10)
            return
        QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        QQPassword = numbers[0]['password']
        time.sleep(1)
        d(className='android.widget.TabWidget').child(className='android.widget.RelativeLayout',index=3).click()
        d(resourceId='com.ss.android.article.news:id/aey').click()       #点击QQ头像
        z.heartbeat()
        while not d(text='QQ登录').exists:
            time.sleep(2)
        z.heartbeat()
        if d(text='登录').exists:
            d(text='登录').click()
        else:
            d(textContains='QQ号/手机号').click()
            z.input(QQNumber)
            d(resourceId='com.tencent.mobileqq:id/password').click()
            z.input(QQPassword)
            d(text='登录').click()
            z.heartbeat()


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return JRLogin


if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_cate_id":"37",'time_delay': "3"}  # cate_id是仓库号，length是数量
    o.action(d, z, args)
