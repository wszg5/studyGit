# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random


class AddressAddFriends:
    def __init__(self):

        self.repo = Repo()
        # repo_material_cate_id = args["repo_material_cate_id"]
        # Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
        # wait = 1  # 判断素材仓库里是否由素材
        # while wait == 1:
        #     try:
        #         repo_material_id = Material[0]['content']  # 取出验证消息的内容
        #         wait = 0
        #     except Exception:
        #         d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到验证消息\"")
        #
        # repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        # add_count = int(args['add_count'])  # 要添加多少人
        #
        # wait = 1
        # while wait == 1:
        #     numbers = self.repo.GetNumber(repo_number_cate_id, 120, add_count)  # 取出add_count条两小时内没有用过的号码
        #     if "Error" in numbers:  #
        #         d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到号码\"")
        #         continue
        #     wait = 0
        #
        # list = numbers  # 将取出的号码保存到一个新的集合
        # 将微信强制停止

    def action(self, d, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()
        # 将微信拉起来
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()
        # time.sleep(10)
        # RunApp "com.tencent.mm", ".plugin.sns.ui.SnsTimeLineUI" '朋友圈

        for i in range(50, 110):
            time.sleep(1)
            print 'not connect'
            if d(description='更多功能按钮', index =1, className='android.widget.RelativeLayout').exists:
                print 'connect'
                time.sleep(3)
                d(description='更多功能按钮', index =1, className='android.widget.RelativeLayout').click()
                break

        time.sleep(3)
        # if d(text='添加朋友', className='android.widget.TextView').exists:
        if d(text='添加朋友', resourceId='com.tencent.mm:id/f6').exists:
            d(text='添加朋友', resourceId='com.tencent.mm:id/f6').click()
        else:
            d(resourceId='com.tencent.mm:id/f5', className='android.widget.ImageView').click()
            time.sleep(1)
            d(text='添加朋友', resourceId='com.tencent.mm:id/f6').click()
        time.sleep(1)
        d(text='手机联系人', resourceId='android:id/title').click()
        time.sleep(1)
        d(text='添加手机联系人', className='android.widget.TextView').click()
        str = d.info
        height = str["displayHeight"]
        width = str["displayWidth"]
        t=0
        for i in range(1, 15):
            print i

            time.sleep(2)
            if d(resourceId='com.tencent.mm:id/apx', index=0).child(className='android.widget.LinearLayout', clickable='true', index=i-1-t).exists():
                d(resourceId='com.tencent.mm:id/apx', index=0).child(className='android.widget.LinearLayout',clickable='true', index=i - 1 - t).click()
                time.sleep(1)
                if (d(description='男', resourceId='com.tencent.mm:id/abd').exists):
                    d(text='添加到通讯录', resourceId='com.tencent.mm:id/ab3').click()
                    d(resourceId='com.tencent.mm:id/c4i', className='android.widget.EditText').set_text('c85965263')
                    d(resourceId='com.tencent.mm:id/g9', text='发送').click()
                    time.sleep(1)
                    d(description='返回', resourceId='com.tencent.mm:id/gq').click()
                else:
                    print '返回'
                    d(description='返回', resourceId='com.tencent.mm:id/gq').click()
                    continue

            else:
                t+=i
                d.swipe(width / 2, height * 3 / 5, width / 2, height / 5)
                d.swipe(width / 2, height * 3 / 5, width / 2, height / 5)
                 # EndIndex = EndIndex-i
                i = 0
                continue





def getPluginClass():
    return AddressAddFriends

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49XSK01883")
    d.dump(compressed=False)
    args = {"repo_number_cate_id": "13", "repo_material_cate_id": "8", "gender": "女", "add_count": "9","time_delay": "3"}  # cate_id是仓库号，发中文问题
    o.action(d, args)