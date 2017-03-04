# coding:utf-8
from uiautomator import Device
from zservice import ZDevice
from Repo import *
from XunMa import *
import time


class TIMSimpleRegister:

    def __init__(self):
        self.repo = Repo()
        self.xm = None

    def action(self, d, z,args):
        cateId = args['repo_cate_id']
        self.xm = XunMa(d.server.adb.device_serial())

        d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来

        time.sleep(6)
        if d(text='消息', resourceId='com.tencent.tim:id/ivTitleName').exists:
            return

        d.server.adb.cmd("shell", "pm clear com.tencent.tim").communicate()  # 清除缓存
        d.server.adb.cmd("shell",
                         "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来

        self.swipe(d)

        if d(className='android.widget.Button', text='新用户').exists:
            d(className='android.widget.Button', text='新用户').click()
        time.sleep(2)

        phoneNumber = self.xm.GetPhoneNumber('2111')
        print '手机号'
        print phoneNumber
        print '============'
        time.sleep(2)

        d(text='请输入你的手机号码', className='android.widget.EditText').set_text(phoneNumber)

        time.sleep(1)
        d(text='下一步', className='android.widget.Button').click()
        time.sleep(2)

        for j in range(0, 15):
            time.sleep(1)
            if d(text='请输入短信验证码', className='android.widget.EditText').exists:
                break
            if d(text='分享', className='android.widget.TextView').exists:
                d(text='填写手机号码', className='android.widget.TextView').click()
                d(text='下一步', className='android.widget.Button').click()
                continue

        if j == 14:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"TIM验证码跳转失败\"").communicate()
            return False

        time.sleep(1)
        while 1:
            if d(text='请输入短信验证码', className='android.widget.EditText').exists:
                break
            else:
                time.sleep(1)

        vertifyCode = self.xm.GetVertifyCode(phoneNumber, '2111')  # 获取验证码

        if vertifyCode == "":
            if d(text='重新发送', className='android.widget.TextView').exists:
                d(text='重新发送', className='android.widget.TextView').click()
                time.sleep(2)
                print '重新发送'
                vertifyCode = self.xm.GetVertifyCode(phoneNumber, '2111')

                if vertifyCode == '':
                    self.xm.ReleasePhone(phoneNumber, '2111')
                    print '验证码获取失败'
                    return False

        print vertifyCode
        self.xm.defriendPhoneNumber(phoneNumber, '2111')
        d(text='请输入短信验证码', className='android.widget.EditText').set_text(vertifyCode)

        time.sleep(1)
        for i in range(0, 3):
            if d(text='下一步', className='android.widget.Button').exists:
                d(text='下一步', className='android.widget.Button').click()
            else:
                time.sleep(1)

        while 1:
            if d(text='绑定新QQ号码', className='android.widget.TextView').exists:
                d(text='绑定新QQ号码', className='android.widget.TextView').click()
                break
            elif d(text='设置昵称', className='android.widget.TextView').exists:
                break
            else:
                time.sleep(1)

        nickNameList = self.repo.GetMaterial(cateId, 0, 1)
        nickName = nickNameList[0]["content"]
        nickName = nickName.encode("utf-8")

        d(resourceId='com.tencent.tim:id/name', className='android.widget.EditText').click()
        z.input(nickName)
        d(text='完成', resourceId='com.tencent.tim:id/name').click()
        obj = d(resourceId='com.tencent.tim:id/name', className='android.widget.TextView', index=1).info
        info = obj['text']  # 要保存的qq号
        d(text='登录', resourceId='com.tencent.tim:id/name').click()
        time.sleep(2)

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

    def swipe(self, d):
        time.sleep(3)
        for k in range(1, 35):
            time.sleep(1)
            if d(className='android.widget.TextView', text='熟悉的QQ习惯').exists:
                str = d.info  # 获取屏幕大小等信息
                height = str["displayHeight"]
                width = str["displayWidth"]
                for i in range(0, 2):
                    d.swipe(width * 0.75, height * 0.5, width * 0.05, height * 0.5, 10)
                    time.sleep(1)
                d(className='android.widget.Button', text='立即体验').click()
                break

        if k == 34:
            return False
        time.sleep(2)



def getPluginClass():
    return TIMSimpleRegister

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52DSK00474")
    z = ZDevice("HT52DSK00474")


    d.server.adb.cmd("shell","ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_cate_id":"102","time_delay":"3","time_limit":"120"};               #cate_id是仓库号，length是数量

    o.action(d,z,args)