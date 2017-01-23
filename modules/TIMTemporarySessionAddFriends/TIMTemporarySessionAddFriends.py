# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class TIMTemporarySessionAddFriends:
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
                if d(text='仅此一次', resourceId='android:id/button_once').exists:
                    d(text='仅此一次', resourceId='android:id/button_once').click()

            d(text='加为好友', className='android.widget.TextView', index=2).click()
            time.sleep(2)
            if d(text='加为好友', className='android.widget.TextView', index=2).exists:  # 拒绝被添加好友的情况
                continue
            if d(text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText').exists:  # 可直接添加为好友的情况
                d(text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
                if d(resourceId='com.tencent.tim:id/name', text='添加失败，请勿频繁操作').exists:  # 操作过于频繁的情况
                    return
                continue
            if d(text='必填', resourceId='com.tencent.tim:id/name').exists:  # 需要验证时
                continue
            obj = d(resourceId='com.tencent.tim:id/name', index='3').info
            print(obj)
            obj = obj['text']
            length = len(obj)
            k = 0
            while k < length:
                length = length - 1
                d.press.delete()
            time.sleep(2)
            d(resourceId='com.tencent.tim:id/name', className='android.widget.EditText').click()  # 要发的消息
            z.input(material)
            d(text='下一步', resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
            d(text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
            time.sleep(1)
            if d(resourceId='com.tencent.tim:id/name', text='添加失败，请勿频繁操作').exists:  # 操作过于频繁的情况
                return


            if (args["time_delay"]):
                time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMTemporarySessionAddFriends

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT57FSK00089")
    # material=u'有空聊聊吗'
    z = ZDevice("HT57FSK00089")
    # d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id": "43", "repo_material_cate_id": "36", "add_count": "9",
            "time_delay": "3"};  # cate_id是仓库号，length是数量
    o.action(d, z, args)
