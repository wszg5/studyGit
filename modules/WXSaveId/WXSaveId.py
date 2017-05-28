# coding:utf-8
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class WXSaveId:
    def __init__(self):
        self.repo = Repo()

    def action(self, d, z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)
        cate_id = args['repo_wxcade_id']
        d(text='发现').click()
        d(text='附近的人').click()
        z.sleep(1)
        if d(text='开始查看').exists:
            d(text='开始查看').click()
            d(text='下次不提示').click()
            d(text='确定').click()
        z.sleep(2)

        if d(text='查看附近的人').exists:
            d( text='查看附近的人' ).click()
        while True:
            if d(description='更多').exists:
                break
            else:
                z.sleep(2)
        d(description='更多' ).click()
        gender = args['gender']
        if gender=='男':
            d(text='只看男生').click()
            z.sleep(5)
        elif gender=="女":
            d(text='只看女生').click()
            z.sleep(5)
        else:
            d(text='查看全部').click()
            z.sleep(5)

        serial = z.wx_action("opennearui")  # 得到微信ｉｄ，字符串样式
        print(serial)
        ids = json.loads(serial)  # 将字符串改为list样式
        print(ids)
        lenth = len(ids)
        z.heartbeat()

        for i in range(lenth):
            z.heartbeat()
            wxid = ids[i]
            print(wxid)
            if 'v1_' not in wxid:
                continue
            self.repo.uploadPhoneNumber(wxid, cate_id)
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return WXSaveId


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

    args = {"repo_wxcade_id": "172", 'gender':"不限",'time_delay': "3"}  # cate_id是仓库号，length是数量
    o.action(d, z, args)


