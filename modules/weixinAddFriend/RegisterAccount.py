# coding:utf-8
from uiautomator import Device
from Repo import *
from XunMa import *
import os, time, datetime, random




class RegisterAccount:
    def __init__(self):

        self.repo = Repo()
        self.XunMa = XunMa()

    def action(self, d, args):
        for i in range(0, 72, +1):
            d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()
            d.server.adb.cmd("shell", "pm clear com.tencent.mm").wait()  # 清除缓存
            # 将微信拉起来
            d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()
            for i in range(50, 110):
                time.sleep(1)
                print 'out'
                if d(text='注册', className='android.widget.Button').exists:
                    print 'in'
                    time.sleep(3)
                    d(text='注册', className='android.widget.Button').click()

                    break
            time.sleep(2)
            token = self.XunMa.GetToken()
            phoneNumber = self.XunMa.GetPhoneNumber(token, '2356')
            print token
            print phoneNumber
            d(index=1, resourceId='com.tencent.mm:id/gl').set_text('magic')
            d(index=0, resourceId='com.tencent.mm:id/ou').set_text('86')
            d(index=1, resourceId='com.tencent.mm:id/blj').set_text(phoneNumber)
            d(resourceId='com.tencent.mm:id/fe', index=0).child(index=3, resourceId='com.tencent.mm:id/c2d').child(index=1,resourceId='com.tencent.mm:id/gl').click()
            d(resourceId='com.tencent.mm:id/fe', index=0).child(index=3, resourceId='com.tencent.mm:id/c2d').child(index=1,resourceId='com.tencent.mm:id/gl').set_text('13141314abc')
            d(text='注册', className='android.widget.Button').click()
            d(text='确定', className='android.widget.Button').click()
            vertifyCode = self.XunMa.GetTIMLittleCode(phoneNumber, token)
            time.sleep(35-vertifyCode[1]*2)
            print vertifyCode
            d(text='请输入验证码', className='android.widget.EditText').set_text(vertifyCode[0])
            d(text='下一步', className='android.widget.Button').click()

            time.sleep(1.5)
            if d(text='不是我的，继续注册', resourceId='com.tencent.mm:id/bo3').exists:
                d(text='不是我的，继续注册', className='android.widget.Button').click()
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
    d = Device("HT4BDSK00858")
    d.dump(compressed=False)
    args = {"repo_number_cate_id": "13", "repo_material_cate_id": "8", "gender": "女", "add_count": "9","time_delay": "3"}  # cate_id是仓库号，发中文问题
    o.action(d, args)