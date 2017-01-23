# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class TIMBrowserAddFriends:

    def __init__(self):
        self.repo = Repo()


    def action(self, d, z, args):
        add_count = int(args['add_count'])  # 要添加多少人
        repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            numbers = self.repo.GetNumber(repo_number_cate_id, 120, add_count)  # 取出add_count条两小时内没有用过的号码
            if "Error" in numbers:  # 没有取到号码的时候
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到号码\"")
                continue
            wait = 0
        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)

        for i in range(0, add_count, +1):  # 总人数
            repo_material_cate_id = args["repo_material_cate_id"]
            Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
            wait = 1  # 判断素材仓库里是否由素材
            while wait == 1:
                try:
                    material = Material[0]['content']  # 取出验证消息的内容
                    wait = 0
                except Exception:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到验证消息\"")

            numbers = list[i]
            print(numbers)
            time.sleep(1)
            z.openQQChat(numbers)  # 唤起浏览器临时会话
            time.sleep(1)
            while d(text='TIM', resourceId='android:id/text1').exists:
                d(text='TIM', resourceId='android:id/text1').click()
                time.sleep(1)
                if d(text='仅此一次', resourceId='android:id/button_once').exists:
                    d(text='仅此一次', resourceId='android:id/button_once').click()

            d(className='android.widget.EditText', index=0).click()
            z.input(material)
            time.sleep(1)
            d(text= '发送',className='android.widget.Button', index=1).click()



            if (args["time_delay"]):
                time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMBrowserAddFriends


if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT57FSK00089")
    # material=u'有空聊聊吗'
    z = ZDevice("HT57FSK00089")
    # d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id":"43","repo_material_cate_id":"36","add_count":"9","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)





