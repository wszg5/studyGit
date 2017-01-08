# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random


class SearchAddFriends:
    def __init__(self):
        self.repo = Repo()



    def action(self, d, args):

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
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()
        # 将微信拉起来
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()
        time.sleep(5)
        # RunApp "com.tencent.mm", ".plugin.sns.ui.SnsTimeLineUI" '朋友圈

        d(description='更多功能按钮', className='android.widget.RelativeLayout').click()
        time.sleep(1)
        if d(text='添加朋友', resourceId='com.tencent.mm:id/f6').exists:
            d(text='添加朋友', resourceId='com.tencent.mm:id/f6').click()
        else:
            d(resourceId='com.tencent.mm:id/f5', className='android.widget.ImageView').click()
            time.sleep(1)
            d(text='添加朋友', resourceId='com.tencent.mm:id/f6').click()
        d(resourceId='com.tencent.mm:id/gl', index='1', className='android.widget.TextView').click()

        d(text='搜索', resourceId='com.tencent.mm:id/gl').set_text('c85965263')  # repo_number_cate_id
        d(resourceId='com.tencent.mm:id/hi', textContains='搜索:').click()

        time.sleep(2)
        if (d(description='男', resourceId='com.tencent.mm:id/abd').exists):
            d(text='添加到通讯录',resourceId='com.tencent.mm:id/ab3').click()
            d(resourceId='com.tencent.mm:id/c4i', className='android.widget.EditText').set_text('c85965263')
            d(resourceId='com.tencent.mm:id/g9', text='发送').click()
        else:
            print (d(description='男', resourceId='com.tencent.mm:id/abd').exists)



def getPluginClass():
    return SearchAddFriends

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49XSK01883")
    d.dump(compressed=False)
    args = {"repo_number_cate_id": "13", "repo_material_cate_id": "8", "gender": "女", "add_count": "9","time_delay": "3"}  # cate_id是仓库号，发中文问题
    o.action(d, args)