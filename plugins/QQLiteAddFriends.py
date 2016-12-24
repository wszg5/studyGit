# coding:utf-8
from uiautomator import Device, AutomatorDeviceUiObject
from Repo import *
import os, time, datetime, random,math
import json
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import traceback

class QQLiteAddFriends:


    def __init__(self):
        self.repo = Repo()

    def action(self, d, args):
        repo_material_cate_id = args["repo_material_cate_id"]
        Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
        repo_material_id = Material[0]['content']         #取出发消息的内容
        repo_number_cate_id = args["repo_number_cate_id"]
        add_count = int(args['add_count'])
        numbers = self.repo.GetNumber(repo_number_cate_id,120,add_count)     #取出add_count条两小时内没有用过的号码
        for i in range(0, add_count, +1):          #循环遍历add_count条号码
            numbers = numbers[i]
            d.server.adb.cmd("shell", "am force-stop com.tencent.qqlite").wait()  # 将qq强制停止
            d.server.adb.cmd("shell",
                             "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").wait()  # 将qq拉起来
            time.sleep(2)
            d(description='更多', resourceId='com.tencent.qqlite:id/0').click()
            time.sleep(2)
            if d(text='添加', resourceId='com.tencent.qqlite:id/action_sheet_button').exists:
                d(text='添加', resourceId='com.tencent.qqlite:id/action_sheet_button').click()
            else:
                d(description='更多', className='android.widget.ImageView').click()
                d(text='添加', resourceId='com.tencent.qqlite:id/action_sheet_button').click()
            d(text='QQ号/手机号/邮箱/群', description='搜索栏、QQ号、手机号、邮箱、群').click()
            time.sleep(1)
            d(text='QQ号/手机号/邮箱/群', resourceId='com.tencent.qqlite:id/et_search_keyword').set_text(numbers)       #添加好友的号码
            d(text='找人:', resourceId='com.tencent.qqlite:id/0', className='android.widget.TextView').click()
            time.sleep(2)
            d(className='android.widget.RelativeLayout', index=1).click()
            if d(descriptionContains='基本信息'):
                obj = d(descriptionContains='基本信息').info
                obj = obj["contentDescription"]           #得到性别等基本信息
                print (obj)
                gender = args['gender']
                if gender == '不限':
                    d(text='加好友', resourceId='com.tencent.qqlite:id/txt', className='android.widget.TextView').click()
                    time.sleep(2)
                    if d(text='必填', className='android.widget.EditText'):
                        continue
                    else:
                        obj1 = d(resourceId='com.tencent.qqlite:id/0', className='android.widget.EditText')
                        if obj1.exists:          # 有的要发送验证消息，有的不需要
                            obj1.set_text(repo_material_id)       #发送验证消息
                            time.sleep(2)
                            d(text='下一步', resourceId='com.tencent.qqlite:id/ivTitleBtnRightText',
                              className='android.widget.TextView').click()
                        time.sleep(2)
                        d(text='发送', resourceId='com.tencent.qqlite:id/ivTitleBtnRightText',
                          className='android.widget.TextView').click()
                        continue  # 放到方法里是结束方法

                elif gender in obj:
                    d(text='加好友', resourceId='com.tencent.qqlite:id/txt', className='android.widget.TextView').click()
                    time.sleep(2)
                    if d(text='必填', className='android.widget.EditText'):
                        continue

                    else:
                        obj = d(resourceId='com.tencent.qqlite:id/0',className='android.widget.EditText')
                        if obj.exists:
                            obj.set_text(repo_material_id)
                            time.sleep(2)
                            d(text='下一步', resourceId='com.tencent.qqlite:id/ivTitleBtnRightText',
                              className='android.widget.TextView').click()  # 有的要发送验证消息，有的不需要
                        time.sleep(2)
                        d(text='发送', resourceId='com.tencent.qqlite:id/ivTitleBtnRightText',
                          className='android.widget.TextView').click()
                        continue  # 放到方法里是结束方法
                else:
                    continue
        if (args["time_delay"]):
            time.sleep(args["time_delay"])

def getPluginClass():
    return QQLiteAddFriends

if __name__ == "__main__":
    c = QQLiteAddFriends()
    d = Device("HT49PSK05055")
    d.dump(compressed=False)
    args = {"cate_id1":"8","cate_id2":"13"}   #cate_id是仓库号，发中文问题
    c.action(d, args)
