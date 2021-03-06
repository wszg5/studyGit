# coding:utf-8
from uiautomator import Device
from zservice import ZDevice
from Repo import *
import time
from slot import Slot


class TIMLogin:
    def __init__(self):
        self.repo = Repo()
        self.type = 'tim'
        # self.slot = Slot('tim')

    def login(self,d,z,args):
        serial = d.server.adb.device_serial( )
        self.slot = Slot( serial, self.type )
        cateId = args['repo_cate_id']
        name = self.repo.GetMaterial(cateId,120,1)
        name = name[0]['content']
        d.server.adb.cmd("shell", "pm clear com.tencent.tim").communicate()  # 清除缓存
        d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
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

        d(resourceId='com.tencent.tim:id/name', className='android.widget.EditText').click()
        z.input(name)
        d(text='完成', resourceId='com.tencent.tim:id/name').click()
        obj = d(resourceId='com.tencent.tim:id/name',className='android.widget.TextView',index=1).info
        info = obj['text']                             #要保存的qq号

        d(text='登录', resourceId='com.tencent.tim:id/name').click()
        time.sleep(6)
        # d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()  # 强制停止
        # d.server.adb.cmd("shell",
        #                  "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        return info



    def action(self, d, z,args):
        serial = d.server.adb.device_serial( )
        self.slot = Slot( serial, self.type )
        time_limit = args['time_limit']
        cate_id = args["repo_cate_id"]
        name = self.slot.getEmpty(d)                    #取空卡槽

        if name ==0:
            name = self.slot.getSlot(d,time_limit)              #没有空卡槽，取２小时没用过的卡槽
            while name==0:                               #2小时没有用过的卡槽也为空的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"卡槽全满，无2小时未用\"").communicate()
                time.sleep(30)
                name = self.slot.getSlot(d,time_limit)

            z.set_mobile_data(False)
            time.sleep(3)
            self.slot.restore(d,name)                      #有２小时没用过的卡槽情况，切换卡槽
            z.set_mobile_data(True)
            time.sleep(8)
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"TIM卡槽切换成功\"").communicate()

            d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            if d(text='帐号无法登录').exists:
                info = self.login(d,z,args)                                             #帐号无法登陆则登陆,重新注册登陆

                # self.repo.BackupInfo(cate_id, d, name, info)  # 将登陆上的仓库cate_id,设备号d，卡槽号name，qq号info，备份到仓库

                self.slot.backup(d,name,info)                                 #登陆之后备份
            else:
                return

        else:                                     #有空卡槽的情况
            z.set_mobile_data(False)
            time.sleep(2)
            z.set_mobile_data(True)
            time.sleep(8)
            info = self.login(d,z,args)

            # self.repo.BackupInfo(cate_id, d, name, info)  # 将登陆上的仓库cate_id,设备号d，卡槽号name，qq号info，备份到仓库

            self.slot.backup(d,name,info)



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return TIMLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")
    # print(d.dump(compressed=False))
    # print(d.info)

    d.server.adb.cmd("shell","ime set com.zunyun.qk/.ZImeService").communicate()
    # d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()  # 清除缓存
    args = {"repo_cate_id":"56","time_delay":"3","time_limit":"120"};    #cate_id是仓库号，length是数量
    # o.slot.restore(d,1)
    o.action(d,z,args)
