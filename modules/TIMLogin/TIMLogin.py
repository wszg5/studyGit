# coding:utf-8
from uiautomator import Device
from Repo import *
from XunMa import *
import time




class TIMLogin:
    def __init__(self):
        self.repo = Repo()
        self.XunMa = XunMa()



    def action(self, d, args):
        d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()  # 清除缓存
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        time.sleep(1)
        d(resourceId='com.tencent.tim:id/btn_register',index=1,text='新用户').click()
        token = self.XunMa.GetToken()
        phoneNumber = self.XunMa.GetPhoneNumber(token)
        print phoneNumber
        d(text='请输入你的手机号码',resourceId='com.tencent.tim:id/name').set_text(phoneNumber)
        d(text='下一步',resourceId='com.tencent.tim:id/name').click()
        vertifyCode = self.XunMa.GetCode(phoneNumber,token)                                                #获取验证码
        d(text='请输入短信验证码',resourceId='com.tencent.tim:id/name').set_text(vertifyCode)
        d(text='下一步',resourceId='com.tencent.tim:id/name').click()
        time.sleep(1)
        if d(text='绑定新QQ号码',resourceId='com.tencent.tim:id/action_sheet_button').exists:
           d(text='绑定新QQ号码', resourceId='com.tencent.tim:id/action_sheet_button').click()
        d(resourceId='com.tencent.tim:id/name',className='android.widget.EditText').set_text('qqww')
        d(text='完成',resourceId='com.tencent.tim:id/name').click()
        d(text='登录',resourceId='com.tencent.tim:id/name').click()
        time.sleep(8)
        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来



def getPluginClass():
    return TIMLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49XSK01883")
    args = {"repo_cate_id":"131","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
