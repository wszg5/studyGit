# coding:utf-8
from requests import delete
from uiautomator import Device
from Repo import *
import os, time, datetime, random
import util

class TIMAddressList:
    def __init__(self):
        self.repo = Repo()



    def action(self, d, args):

        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        time.sleep(1)
        d(resourceId='com.tencent.tim:id/name',description='快捷入口').click()
        time.sleep(1)
        if d(text='加好友',resourceId='com.tencent.tim:id/name').exists:
            d(text='加好友',resourceId='com.tencent.tim:id/name').click()
        else:
            d(resourceId='com.tencent.tim:id/name', description='快捷入口').click()
            d(text='加好友',resourceId='com.tencent.tim:id/name').click()
        time.sleep(2)
        d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/name').click()
        d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword').click()
        d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword').set_text(23457)  # 要改为从库里取
        d(text='找人:', resourceId='com.tencent.tim:id/name').click()

        time.sleep(2)
        for i in range(0,3,+1):
            if d(text='没有找到相关结果',className='android.widget.TextView').exists:
                d(resourceId='com.tencent.tim:id/ib_clear_text',description='清空').click()
                obj = d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(3053760992+i)  # 要改为从库里取
                obj = d(text='网络查找人', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(3053760992 + i)  # 要改为从库里取

                d(text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search').click()
                continue

            time.sleep(2)
            if d(className='android.widget.AbsListView').child(index=1,resourceId='com.tencent.tim:id/name').exists:      #在同一查条件有多个人

                d(className='android.widget.AbsListView').child(index=1, resourceId='com.tencent.tim:id/name').click()

            d(text='加好友',resourceId='com.tencent.tim:id/name').click()
            time.sleep(1)
            if d(text='加好友',resourceId='com.tencent.tim:id/name').exists:
                time.sleep(1)
                d(text='返回',resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
                d(resourceId='com.tencent.tim:id/ib_clear_text', description='清空').click()
                obj = d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(152267 + i)  # 要改为从库里取
                obj = d(text='网络查找人', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(23456 + i)
                time.sleep(1)
                d(text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search').click()
                continue

            time.sleep(2)
            if d(text='必填',resourceId='com.tencent.tim:id/name').exists:
                d(text='返回',resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
                time.sleep(1)
                d(text='返回',resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
                d(resourceId='com.tencent.tim:id/ib_clear_text', description='清空').click()
                obj = d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(152267+i)  # 要改为从库里取
                obj = d(text='网络查找人',resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(23456+i)
                time.sleep(1)
                d(text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search').click()
                continue

            time.sleep(1)
            obj = d(text='发送',resourceId='com.tencent.tim:id/ivTitleBtnRightText')
            if obj.exists:
                obj.click()
                if d(text='添加失败，请勿频繁操作',resourceId='com.tencent.tim:id/name').exists:
                    return
                d(text='返回', resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
                d(resourceId='com.tencent.tim:id/ib_clear_text', description='清空').click()
                obj = d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(305376099 + i)  # 要改为从库里取
                obj = d(text='网络查找人', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(305376099 + i)
                d(text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search').click()
                continue

            time.sleep(2)

            obj = d(className='android.widget.EditText', resourceId='com.tencent.tim:id/name').info
            obj = obj['text']
            lenth = len(obj)
            t = 0
            while t < lenth:
                d.press.delete()
                t = t + 1
            d(className='android.widget.EditText',resourceId='com.tencent.tim:id/name').set_text('do you uuu')
            d(text='下一步',resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
            d(text='发送',resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
            if d(text='添加失败，请勿频繁操作', resourceId='com.tencent.tim:id/name').exists:
                return
            d(text='返回',resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
            d(resourceId='com.tencent.tim:id/ib_clear_text',description='清空').click()
            obj = d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword')
            if obj.exists:
                obj.set_text(305376099+i)  # 要改为从库里取
            obj = d(text='网络查找人', resourceId='com.tencent.tim:id/et_search_keyword')
            if obj.exists:
                obj.set_text(305376099+i)
            d(text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search').click()
            # d(text='搜索',resourceId='com.tencent.tim:id/btn_cancel_search').click()








def runwatch(d, data):
    times = 120
    while True:
        if data == 1:
            return True
        # d.watchers.reset()
        d.watchers.run()
        times -= 1
        if times == 0:
            break
        else:
            time.sleep(0.5)

def getPluginClass():
    return TIMAddressList

if __name__ == "__main__":

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A3SK00853")
    args = {"repo_cate_id":"131","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    util.doInThread(runwatch, d, 0, t_setDaemon=True)
    o.action(d, args)