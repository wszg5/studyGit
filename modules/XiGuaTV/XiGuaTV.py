# coding:utf-8

from uiautomator import Device

from Repo import Repo
from zservice import ZDevice


class XiGuaTV:
    def __init__(self):
        self.repo = Repo()

    def action(self, d, z, args):

        while True:
            z.heartbeat()
            numbers = self.repo.GetAccount(args['repo_account_id'], 120, 1)
            PhoneNumber = numbers[0]['number']  # 即将登陆的QQ号
            Password = numbers[0]['password']

            if d(text='添加帐号').exists:
                d(text='添加帐号').click()
                z.sleep(2)

            d(resourceId='com.tencent.mobileqq:id/account').click()
            z.input(PhoneNumber)
            z.sleep(1)

            d(resourceId='com.tencent.mobileqq:id/password').click()
            z.input(Password)
            z.sleep(1)

            d(text='登录').click()
            z.sleep(int(args['time_delay1']))
            z.heartbeat()

            d.server.adb.cmd( "shell", "pm clear com.ss.android.article.video" ).communicate( )  # 清除缓存

            d.server.adb.cmd( "shell",
                              "am start -n com.ss.android.article.video/com.ixigua.feature.fantasy.FantasyActivity" ).communicate( )  # 拉起

            z.sleep(int(args['time_delay2']))
            z.heartbeat()

def getPluginClass():
    return XiGuaTV

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    clazz = getPluginClass()
    o = clazz()
    d = Device( "7HQWC6U8A679SGAQ" )  # INNZL7YDLFPBNFN7
    z = ZDevice( "7HQWC6U8A679SGAQ" )
    args = {"repo_account_id": "133", "time_delay1": "3", "time_delay2": "3"};
    o.action(d, z, args)

