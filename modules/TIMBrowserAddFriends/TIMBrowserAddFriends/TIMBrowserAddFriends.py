# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice


class TIMBrowserAddFriends:
    def __init__(self):
        self.repo = Repo()




    def action(self, d,z,args):
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
            if "Error" in numbers:  #没有取到号码的时候
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到号码\"")
                continue
            wait = 0

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)




        d.server.adb.cmd("shell", "am force-stop com.android.chrome").wait()  # 强制停止
        for i in range (0,add_count,+1):            #总人数
            numbers = list[i]
            print(numbers)
            time.sleep(1)
            d.server.adb.cmd("shell","am start -a android.intent.action.VIEW -d http://www.jianli58.com/qq.html").wait()  # 拉起来
            time.sleep(3)
            d(className='android.widget.Button',index=2,description='清空号码').click()
            d(className='android.widget.EditText',index=1,clickable='false').click()
            if d(className='android.widget.EditText',index=1,clickable='false').exists:
                d.press.back()
            d(className='android.widget.EditText',index=1,clickable='false').set_text(numbers)#   要添加的好友
            d(className='android.widget.Button',index=3,description='开始聊天').click()
            time.sleep(1)
            d(text='加为好友',className='android.widget.TextView',index=2).click()
            time.sleep(2)
            if d(text='加为好友',className='android.widget.TextView',index=2).exists:     #拒绝被添加好友的情况
                continue

            if d(text='发送',resourceId='com.tencent.tim:id/ivTitleBtnRightText').exists:   #可直接添加为好友的情况
                d(text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
                if d(resourceId='com.tencent.tim:id/name',text='添加失败，请勿频繁操作').exists:    #操作过于频繁的情况
                    return
                continue


            if d(text='必填',resourceId='com.tencent.tim:id/name').exists:                #需要验证时
                continue

            obj = d(resourceId='com.tencent.tim:id/name',index='3').info
            print(obj)
            obj = obj['text']
            length = len(obj)
            k = 0
            while k<length:
                length = length-1
                d.press.delete()
            print(material.encode("utf-7"))
            print(material)
            time.sleep(2)
            d(resourceId='com.tencent.tim:id/name',className='android.widget.EditText').click()        #要发的消息
            z.input(material)
            d(text='下一步',resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
            d(text='发送',resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
            if d(resourceId='com.tencent.tim:id/name', text='添加失败，请勿频繁操作').exists:  # 操作过于频繁的情况
                return


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMBrowserAddFriends

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT524SK03149")
    # material=u'有空聊聊吗'

    z = ZDevice("HT4A3SK00853")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id":"37","repo_material_cate_id":"33","add_count":"9","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
