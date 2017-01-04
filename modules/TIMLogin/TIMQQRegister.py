# coding:utf-8
from uiautomator import Device
from XunMa640 import *
from Repo import *
import time


class TIMQQRegister:
    def __init__(self):
        self.XunMa640 = XunMa640()
        self.repo = Repo()
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}

        self.domain = "192.168.1.51"
        self.port = 8888

    def action(self, d):
        d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()  # 清除缓存
        d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        time.sleep(1)
        d(resourceId='com.tencent.tim:id/btn_register',index=1,text='新用户').click()
        token = self.XunMa640.GetToken()
        phoneNumber = self.XunMa640.GetPhoneNumber(token, '640')

        data = self.XunMa640.UploadPhoneNumber(phoneNumber, token)
        if data == 0:
            print "************++++++++++++++++++++++**************"


        print phoneNumber
        d(text='请输入你的手机号码',resourceId='com.tencent.tim:id/name').set_text(phoneNumber)
        d(text='下一步',resourceId='com.tencent.tim:id/name').click()
        vertifyCode = self.XunMa640.GetCode(phoneNumber, token)                                                #获取验证码
        d(text='请输入短信验证码',resourceId='com.tencent.tim:id/name').set_text(vertifyCode)

        nickNameList = self.repo.GetMaterial(56, 0, 1)
        nickName = nickNameList[0]["name"]

        time.sleep(1)
        # 关闭设备锁
        if d(description='开启设备锁，保障QQ帐号安全。', className='android.widget.CheckBox').exists:
            d(description='开启设备锁，保障QQ帐号安全。', className='android.widget.CheckBox').click()
            d(text='下一步', resourceId='com.tencent.tim:id/name').click()



            time.sleep(1)

            print nickName
            d(index=1, className='android.widget.EditText').set_text(nickName)
            d(text='完成', className='android.widget.Button').click()
            obj = d(index=1, className='android.widget.TextView', resourceId='com.tencent.tim:id/name').info
            qqNumber = obj["text"]
            d(text='登录', className='android.widget.Button').click()


            password = ''
            print qqNumber


        else:
            d(text='下一步', resourceId='com.tencent.tim:id/name').click()
            time.sleep(1)
            d(className='android.widget.RelativeLayout', index=2).click()

            print nickName
            d(text='昵称', className='android.widget.EditText').set_text(nickName)
            d(text='密码', className='android.widget.EditText').set_text('13141314abc')
            d(text='注册', resourceId='com.tencent.tim:id/btn_register').click()
            obj = d(index=1, className='android.widget.TextView', resourceId='com.tencent.tim:id/name').info
            qqNumber = obj["text"]

            password = '13141314abc'
            print qqNumber


        self.repo.TIMUploadAccount(phoneNumber, password, phoneNumber)

        # d.open.quick_settings()
        # d(text='飞行模式').click()
        #
        # if d(text='不要再显示此内容。', resourceId='android:id/text1').exists:
        #     d(text='不要再显示此内容。', resourceId='android:id/text1').click()
        #     d(text='确定').click()
        #     d.open.quick_settings()
        #     time.sleep(1)
        #     d(text='飞行模式').click()









def getPluginClass():
    return TIMQQRegister

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT524SK03149")
    # repo = Repo()
    # nickNameList = repo.GetMaterial(56, 0, 1)
    # nickName = nickNameList[0]["name"]
    # # nickName = str(nickName)
    # print nickName

    o.action(d)