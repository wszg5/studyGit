# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class TIMTempoSendMessage:

    def __init__(self):
        self.repo = Repo()


    def action(self, d, z, args):
        add_count = int(args['add_count'])  # 要添加多少人
        repo_number_cate_id = int(args["repo_number_id"])  # 得到取号码的仓库号
        numbers = self.repo.GetNumber(repo_number_cate_id, 0, add_count)  # 取出totalNumber条两小时内没有用过的号码

        if len(numbers) == 0:
            d.server.adb.cmd("shell","am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码%s号仓库为空，等待中\"" % repo_number_cate_id).communicate()
            return

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)

        for i in range(0, add_count, +1):  # 总人数
            repo_material_cate_id = args["repo_material_cate_id"]
            Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell","am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_material_cate_id).communicate()
                return
            material = Material[0]['content']

            numbers = list[i]

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
    return TIMTempoSendMessage


if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT57FSK00089")
    # material=u'有空聊聊吗'
    z = ZDevice("HT57FSK00089")
    # d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id":"43","repo_material_cate_id":"36","add_count":"9","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)





