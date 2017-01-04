# coding:utf-8
from uiautomator import Device


from CardSlot import*
from Repo import *
from XunMa import *
import time




class TIMLogin:
    def __init__(self):
        self.repo = Repo()
        self.XunMa = XunMa()
        self.cardslot = CardSlot()



    def action(self, d, args):
        # d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()  # 清除缓存
        # d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        # time.sleep(1)
        # d(resourceId='com.tencent.tim:id/btn_register',index=1,text='新用户').click()
        # token = self.XunMa.GetToken()
        # phoneNumber = self.XunMa.GetPhoneNumber(token)
        # print phoneNumber
        # d(text='请输入你的手机号码',resourceId='com.tencent.tim:id/name').set_text(phoneNumber)
        # d(text='下一步',resourceId='com.tencent.tim:id/name').click()
        # vertifyCode = self.XunMa.GetCode(phoneNumber,token)                                                #获取验证码
        # d(text='请输入短信验证码',resourceId='com.tencent.tim:id/name').set_text(vertifyCode)
        # d(text='下一步',resourceId='com.tencent.tim:id/name').click()
        # time.sleep(1)
        # if d(text='绑定新QQ号码',resourceId='com.tencent.tim:id/action_sheet_button').exists:
        #    d(text='绑定新QQ号码', resourceId='com.tencent.tim:id/action_sheet_button').click()
        # d(resourceId='com.tencent.tim:id/name',className='android.widget.EditText').set_text('qqww')
        # d(text='完成',resourceId='com.tencent.tim:id/name').click()
        # d(text='登录',resourceId='com.tencent.tim:id/name').click()
        # time.sleep(8)
        # d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
        # d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        # # t = 1
        # # self.cardslot.restore(d,t)

        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来

        time.sleep(8)
        if d(text='登陆',resourceId='com.tencent.tim:id/login').exists:
            d(text='新用户注册',resourceId='com.tencent.tim:id/name').click()
            token = self.XunMa.GetToken()
            phoneNumber = self.XunMa.GetPhoneNumber(token)
            print(phoneNumber)
            d(text='请输入你的手机号码', resourceId='com.tencent.tim:id/name').set_text(phoneNumber)
            d(text='下一步', resourceId='com.tencent.tim:id/name').click()
            vertifyCode = self.XunMa.GetCode(phoneNumber, token)  # 获取验证码
            try:
                d(text='请输入短信验证码', resourceId='com.tencent.tim:id/name').set_text(vertifyCode)
            except Exception:
                d(textContains='重新发送', resourceId='com.tencent.tim:id/name').click()

            d(text='下一步', resourceId='com.tencent.tim:id/name').click()
            time.sleep(1)
            if d(text='绑定新QQ号码', resourceId='com.tencent.tim:id/action_sheet_button').exists:
                d(text='绑定新QQ号码', resourceId='com.tencent.tim:id/action_sheet_button').click()
            d(resourceId='com.tencent.tim:id/name', className='android.widget.EditText').set_text('cindy')
            d(text='完成', resourceId='com.tencent.tim:id/name').click()
            d(text='登录', resourceId='com.tencent.tim:id/name').click()
            time.sleep(8)
            d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
            d.server.adb.cmd("shell",
                             "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来


        if d(resourceId='com.tencent.tim:id/btn_register',index=1,text='新用户').exists:
            d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()  # 清除缓存
            d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
            time.sleep(1)
            d(resourceId='com.tencent.tim:id/btn_register',index=1,text='新用户').click()
            token = self.XunMa.GetToken()
            phoneNumber = self.XunMa.GetPhoneNumber(token)
            print (phoneNumber)
            d(text='请输入你的手机号码',resourceId='com.tencent.tim:id/name').set_text(phoneNumber)
            d(text='下一步',resourceId='com.tencent.tim:id/name').click()
            vertifyCode = self.XunMa.GetCode(phoneNumber,token)                                                #获取验证码
            try:
                d(text='请输入短信验证码',resourceId='com.tencent.tim:id/name').set_text(vertifyCode)
            except Exception:
                d(textContains='重新发送',resourceId='com.tencent.tim:id/name').click()

            d(text='下一步',resourceId='com.tencent.tim:id/name').click()
            time.sleep(1)
            if d(text='绑定新QQ号码',resourceId='com.tencent.tim:id/action_sheet_button').exists:
               d(text='绑定新QQ号码', resourceId='com.tencent.tim:id/action_sheet_button').click()
            d(resourceId='com.tencent.tim:id/name',className='android.widget.EditText').set_text('cindy')
            d(text='完成',resourceId='com.tencent.tim:id/name').click()
            d(text='登录',resourceId='com.tencent.tim:id/name').click()
            time.sleep(8)
            d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
            d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        # self.cardslot.backup(d,t)
        else:
            return

        if (args["time_delay"]):
         time.sleep(int(args["time_delay"]))



def getPluginClass():
    return TIMLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT524SK03149")
    d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()  # 清除缓存
    args = {"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
