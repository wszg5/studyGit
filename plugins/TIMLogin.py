# coding:utf-8
from uiautomator import Device
from zservice import ZDevice
from CardSlot import*
from Repo import *
from XunMa import *
import time
from slot import slot


class TIMLogin:
    def __init__(self):
        self.repo = Repo()
        self.XunMa = XunMa()
        self.cardslot = CardSlot()
        self.slot = slot('tim')


    def login(self):
        d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()  # 清除缓存
        d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        time.sleep(8)
        d(text='新用户', resourceId='com.tencent.tim:id/btn_register').click()
        token = self.XunMa.GetToken()
        phoneNumber = self.XunMa.GetPhoneNumber(token)
        print(phoneNumber)
        d(text='请输入你的手机号码', resourceId='com.tencent.tim:id/name').set_text(phoneNumber)
        d(text='下一步', resourceId='com.tencent.tim:id/name').click()
        try:
            vertifyCode = self.XunMa.GetCode(phoneNumber, token)  # 获取验证码
        except Exception:
            d(textContains='重新发送', resourceId='com.tencent.tim:id/name').click()
            vertifyCode = self.XunMa.GetCode(phoneNumber, token)  # 获取验证码

        d(text='请输入短信验证码', resourceId='com.tencent.tim:id/name').set_text(vertifyCode)
        d(textContains='重新发送', resourceId='com.tencent.tim:id/name').click()

        d(text='下一步', resourceId='com.tencent.tim:id/name').click()
        time.sleep(1)
        if d(text='绑定新QQ号码', resourceId='com.tencent.tim:id/action_sheet_button').exists:
            d(text='绑定新QQ号码', resourceId='com.tencent.tim:id/action_sheet_button').click()
        d(resourceId='com.tencent.tim:id/name', className='android.widget.EditText').set_text('cindy')
        d(text='完成', resourceId='com.tencent.tim:id/name').click()
        obj = d(resourceId='com.tencent.tim:id/name',className='android.widget.TextView',index=1).info
        info = obj['text']                             #要保存的qq号

        d(text='登录', resourceId='com.tencent.tim:id/name').click()
        time.sleep(8)
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
        d.server.adb.cmd("shell",
                         "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        return info



    def action(self, d, z,args):
        name = self.slot.getEmpty(d)                    #取空卡槽
        if name ==0:
            name = self.slot.getSlot(d,120)              #没有空卡槽，取２小时没用过的卡槽
            while name==0:                               #2小时没有用过的卡槽也为空的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"卡槽全满，无2小时未用\"")
                time.sleep(30)
                name = self.slot.getSlot(d,120)

            self.slot.restore(d,name)                      #有２小时没用过的卡槽情况，切换卡槽
            d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
            if d(text='帐号无法登录').exists:
                info = self.login()                                             #帐号无法登陆则登陆,重新注册登陆
                self.slot.backup(d,name,info)                                 #登陆之后备份
            else:
                return

        else:                                     #有空卡槽的情况
            info = self.login()
            self.slot.backup(d,name,info)











        # d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
        # d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        # time.sleep(8)
        # if d(text='登陆',resourceId='com.tencent.tim:id/login').exists:
        #     d(text='新用户注册',resourceId='com.tencent.tim:id/name').click()
        #     token = self.XunMa.GetToken()
        #     phoneNumber = self.XunMa.GetPhoneNumber(token)
        #     print(phoneNumber)
        #     d(text='请输入你的手机号码', resourceId='com.tencent.tim:id/name').set_text(phoneNumber)
        #     d(text='下一步', resourceId='com.tencent.tim:id/name').click()
        #     vertifyCode = self.XunMa.GetCode(phoneNumber, token)  # 获取验证码
        #     try:
        #         d(text='请输入短信验证码', resourceId='com.tencent.tim:id/name').set_text(vertifyCode)
        #     except Exception:
        #         d(textContains='重新发送', resourceId='com.tencent.tim:id/name').click()
        #
        #     d(text='下一步', resourceId='com.tencent.tim:id/name').click()
        #     time.sleep(1)
        #     if d(text='绑定新QQ号码', resourceId='com.tencent.tim:id/action_sheet_button').exists:
        #         d(text='绑定新QQ号码', resourceId='com.tencent.tim:id/action_sheet_button').click()
        #     d(resourceId='com.tencent.tim:id/name', className='android.widget.EditText').set_text('cindy')
        #     d(text='完成', resourceId='com.tencent.tim:id/name').click()
        #     d(text='登录', resourceId='com.tencent.tim:id/name').click()
        #     time.sleep(8)
        #     d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
        #     d.server.adb.cmd("shell",
        #                      "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        #
        #
        # if d(resourceId='com.tencent.tim:id/btn_register',index=1,text='新用户').exists:
        #     d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()  # 清除缓存
        #     d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        #     time.sleep(1)
        #     d(resourceId='com.tencent.tim:id/btn_register',index=1,text='新用户').click()
        #     token = self.XunMa.GetToken()
        #     phoneNumber = self.XunMa.GetPhoneNumber(token)
        #     print (phoneNumber)
        #     d(text='请输入你的手机号码',resourceId='com.tencent.tim:id/name').set_text(phoneNumber)
        #     d(text='下一步',resourceId='com.tencent.tim:id/name').click()
        #     vertifyCode = self.XunMa.GetCode(phoneNumber,token)                                                #获取验证码
        #     try:
        #         d(text='请输入短信验证码',resourceId='com.tencent.tim:id/name').set_text(vertifyCode)
        #     except Exception:
        #         d(textContains='重新发送',resourceId='com.tencent.tim:id/name').click()
        #
        #     d(text='下一步',resourceId='com.tencent.tim:id/name').click()
        #     time.sleep(1)
        #     if d(text='绑定新QQ号码',resourceId='com.tencent.tim:id/action_sheet_button').exists:
        #        d(text='绑定新QQ号码', resourceId='com.tencent.tim:id/action_sheet_button').click()
        #     d(resourceId='com.tencent.tim:id/name',className='android.widget.EditText').set_text('cindy')
        #     d(text='完成',resourceId='com.tencent.tim:id/name').click()
        #     d(text='登录',resourceId='com.tencent.tim:id/name').click()
        #     time.sleep(8)
        #     d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
        #     d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        # # self.cardslot.backup(d,t)
        # else:
        #     return

        if (args["time_delay"]):
         time.sleep(int(args["time_delay"]))



def getPluginClass():
    return TIMLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AVSK01106")
    z = ZDevice("HT4AVSK01106")
    d.server.adb.cmd("shell","ime set com.zunyun.qk/.ZImeService").wait()
    d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()  # 清除缓存
    args = {"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z,args)
