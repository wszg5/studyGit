# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WXSearchDepost:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        add_count = int(args['add_count'])

        cate_id = int(args["repo_number_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            numbers = self.repo.GetNumber(cate_id, 120, add_count)  # 取出add_count条两小时内没有用过的号码
            if "Error" in numbers:  #
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"第%s号号码仓库为空，等待中……\"" % cate_id).communicate()
                time.sleep(20)
                continue
            wait = 0

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()  # 将微信拉起来
        time.sleep(3)

        d(description='更多功能按钮',className='android.widget.RelativeLayout').click()
        time.sleep(1)
        if d(text='添加朋友').exists:
            d(text='添加朋友').click()
        else:
            d(description='更多功能按钮', className='android.widget.RelativeLayout').click()
            time.sleep(1)
            d(text='添加朋友').click()
        d(className='android.widget.TextView',index=1).click()   #点击搜索好友的输入框
        for i in range(0,add_count,+1):
            print(i)
            d(text='搜索').set_text(list[i])       #ccnn527xj  list[i]
            d(textContains='搜索:').click()
            if d(textContains='操作过于频繁').exists:
                return
            time.sleep(2)
            if d(textContains='用户不存在').exists:
                d(descriptionContains='清除',index=2).click()
                time.sleep(1)
                continue

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXSearchDepost

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # d(text='搜索').set_text('18297775923')
    args = {"repo_number_id": "40", "add_count": "5","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
