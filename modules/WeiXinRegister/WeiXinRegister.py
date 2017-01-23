# coding:utf-8
from uiautomator import Device
from Repo import *
from XunMa import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')




class RegisterAccount:
    def __init__(self):

        self.repo = Repo()
        self.XunMa = XunMa()

    def action(self, d,z, args):
        for i in range(0, 72, +1):
            # d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()
            d.server.adb.cmd("shell", "pm clear com.tencent.mm").wait()  # 清除缓存
            # 将微信拉起来
            d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()
            time.sleep(6)
            if d(text='注册', className='android.widget.Button').exists:
                d(text='注册', className='android.widget.Button').click()


            d(resourceId='com.tencent.mm:id/c3h',index=0).child(resourceId='com.tencent.mm:id/gn',index=1).set_text("wedid")
            phoneNumber = self.XunMa.GetPhoneNumber('2356')
            d(resourceId='com.tencent.mm:id/bop',index=2).child(className='android.widget.EditText',index=1).set_text(phoneNumber)
            d(resourceId='com.tencent.mm:id/c3m',index=3).child(className='android.widget.EditText',index=1).set_text('13141314abc')
            # d(index=1, resourceId='com.tencent.mm:id/gn').set_text('magic')     #name从昵称库获取
            # d(index=0, resourceId='com.tencent.mm:id/ou').set_text('86')
            # d(index=1, resourceId='com.tencent.mm:id/bmd').set_text(phoneNumber)
            # d(resourceId='com.tencent.mm:id/fe', index=0).child(index=3, resourceId='com.tencent.mm:id/c2d').child(index=1,resourceId='com.tencent.mm:id/gl').click()
            # d(resourceId='com.tencent.mm:id/fe', index=0).child(index=3, resourceId='com.tencent.mm:id/c2d').child(index=1,resourceId='com.tencent.mm:id/gl').set_text('13141314abc')
            d()
            d(text='注册', className='android.widget.Button').click()
            d(text='确定', className='android.widget.Button').click()
            time.sleep(2)
            while d(textContains='正在验证').exists:
                time.sleep(2)

            code = self.XunMa.GetVertifyCode(phoneNumber,'2356',6)
            if '失败'==code:
                continue
            print(code)
            d(text='请输入验证码', className='android.widget.EditText').set_text(code)
            d(text='下一步', className='android.widget.Button').click()

            time.sleep(1.5)
            if d(text='不是我的，继续注册').exists:
                d(text='不是我的，继续注册').click()
                continue
            if d(textContains='不可频繁重复注册').exists:
                continue
            else:
                d(text='确定', className='android.widget.Button').click()
                print '成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功成功'
                time.sleep(20)
                break


def getPluginClass():
    return RegisterAccount

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()


    # d.dump(compressed=False)
    args = {"repo_number_cate_id": "13", "repo_material_cate_id": "8", "gender": "女", "add_count": "9","time_delay": "3"}  # cate_id是仓库号，发中文问题
    o.action(d,z, args)