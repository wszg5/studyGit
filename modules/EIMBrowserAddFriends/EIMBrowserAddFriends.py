# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class EIMBrowserAddFriends:
    def __init__(self):
        self.repo = Repo()




    def action(self, d,z, args):
        repo_material_cate_id = args["repo_material_cate_id"]
        Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
        wait = 1  # 判断素材仓库里是否由素材
        while wait == 1:
            try:
                material = Material[0]['content']  # 取出验证消息的内容
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到验证消息\"")

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


        d.server.adb.cmd("shell", "am force-stop com.android.chrome").wait()  # 强制停止
        for i in range (1,add_count,+1):
            numbers = list[i]
            d.server.adb.cmd("shell","am start -a android.intent.action.VIEW -d http://www.jianli58.com/qq.html").wait()  # 拉起来
            time.sleep(3)
            d(className='android.widget.Button',index=2,description='清空号码').click()
            d(className='android.widget.EditText',index=1,clickable='false').click()
            d.press.back()
            d(className='android.widget.EditText',index=1,clickable='false').set_text(numbers)
            d(className='android.widget.Button',index=3,description='开始聊天').click()
            # d(resourceId='com.tencent.eim:id/ivTitleBtnRightImage',className='android.widget.ImageView').click()
            # d(text='加为好友',resourceId='com.tencent.eim:id/name').click()
            d(text='加为好友',className='android.widget.TextView',index=1).click()
            d(resourceId='com.tencent.eim:id/name',className='android.widget.EditText').click()
            z.input(material)
            d(text='下一步',resourceId='com.tencent.eim:id/ivTitleBtnRightText').click()
            d(text='发送',resourceId='com.tencent.eim:id/ivTitleBtnRightText').click()


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))




def getPluginClass():
    return EIMBrowserAddFriends

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT536SK01667")
    z = ZDevice("HT536SK01667")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id":"49","repo_material_cate_id":"34","add_count":"9","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)
