# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice


class MobilqqOfficialAccont:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z,args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(6)
        d(textContains='搜索').click()
        d(descriptionContains='公众号').click()
        add_count = int(args['add_count'])  # 要添加多少人

        for i in range (0,add_count,+1):            #总人数
            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                time.sleep(10)
                return
            message = Material[0]['content']  # 取出验证消息的内容
            z.input(message)
            d(textContains='搜索').click()
            time.sleep(2)
            if d(textContains='没有找到').exists:
                d(descriptionContains='搜索聊天或者联系人').child(description='清空').click()
                continue
            d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout', index=1).child(
                className='android.widget.RelativeLayout', index=1).click()      #点击众多公众号排在第一行的那个
            if d(text='进入公众号').exists:
                d(textContains='返回').click()
                d(descriptionContains='搜索聊天或者联系人').child(description='清空').click()
                continue
            else:
                d(text='加关注').click()
                time.sleep(2)
                d(text='返回').click()
                d(text='返回').click()
                d(descriptionContains='搜索聊天或者联系人').child(description='清空').click()

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqOfficialAccont

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()


    args = {"repo_material_id":"39","add_count":"1","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
