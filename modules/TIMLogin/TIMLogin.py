# coding:utf-8
from uiautomator import Device
from zservice import ZDevice
from Repo import *
from XunMa import *
import time
from slot import slot

class TIMLogin:

    def __init__(self):
        self.repo = Repo()
        self.XunMa = XunMa()
        self.slot = slot('tim')

    def login(self,d,z,args):
        cateId = args['repo_cate_id']
        name = self.repo.GetMaterial(cateId,120,1)
        name = name[0]['content']
        d.server.adb.cmd("shell", "pm clear com.tencent.tim").communicate()  # 清除缓存
        d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(8)

        for k in range(1, 35):
            time.sleep(1)
            if d(resourceId='com.tencent.tim:id/title', index=1, text='熟悉的QQ习惯').exists:
                str = d.info  # 获取屏幕大小等信息
                height = str["displayHeight"]
                width = str["displayWidth"]
                for i in range(0, 2):
                    d.swipe(width * 0.75, height * 0.5, width * 0.05, height * 0.5, 10)
                    time.sleep(1)
                d(resourceId='com.tencent.tim:id/name', index=1, text='立即体验').click()
                break

        if k == 35:
            return ''
        time.sleep(2)
        d(text='新用户', resourceId='com.tencent.tim:id/btn_register').click()

        phoneNumber = self.XunMa.GetPhoneNumber('144')
        print(phoneNumber)
        d(text='请输入你的手机号码', resourceId='com.tencent.tim:id/name').set_text(phoneNumber)
        d(text='下一步', resourceId='com.tencent.tim:id/name').click()
        time.sleep(4)
        try:
            vertifyCode = self.XunMa.GetVertifyCode(phoneNumber)  # 获取验证码
        except Exception:
            d(textContains='重新发送', resourceId='com.tencent.tim:id/name').click()
            vertifyCode = self.XunMa.GetVertifyCode(phoneNumber)  # 获取验证码
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
        # d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        return info


    def action(self, d, z,args):
        time_limit = args['time_limit']
        cate_id = args["repo_cate_id"]

        name = self.slot.getEmpty(d)                    #取空卡槽
        print name
        if name ==0:
            name = self.slot.getSlot(d,time_limit)              #没有空卡槽，取２小时没用过的卡槽
            print '切换为'+str(name)
            while name == 0:                               #2小时没有用过的卡槽也为空的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"卡槽全满，无2小时未用\"").communicate()
                time.sleep(30)
                name = self.slot.getSlot(d,time_limit)

            z.set_mobile_data(False)
            time.sleep(3)
            self.slot.restore(d,name)                      #有２小时没用过的卡槽情况，切换卡槽
            z.set_mobile_data(True)
            time.sleep(8)

            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"TIM卡槽成功切换成"+str(name)+"\"").communicate()
            time.sleep(1)

            d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            time.sleep(6)

            if d(text='消息',resourceId='com.tencent.tim:id/ivTitleName').exists:
                obj = self.slot.getSlotInfo(d,name)  #得到切换后的QQ号
                info = obj['info']  #info为QQ号
                self.repo.BackupInfo(cate_id,'using',info,'%s_%s'%(d.server.adb.device_serial(),name))  # 将登陆上的仓库cate_id,设备号d，卡槽号name，qq号info，备份到仓库
            else:
                info = self.login(d,z,args)                                             #帐号无法登陆则登陆,重新注册登陆
                self.slot.backup(d, name, info)  # 登陆之后备份,将备份后的信息传到后台　仓库号，状态，QQ号，备注设备id_卡槽id
                self.repo.BackupInfo(cate_id, 'using', info, '%s_%s'%(d.server.adb.device_serial(),name))  # 将登陆上的仓库cate_id,设备号d，卡槽号name，qq号info，备份到仓库


        else:                           #有空卡槽的情况
            z.set_mobile_data(False)
            time.sleep(3)
            z.set_mobile_data(True)
            time.sleep(8)
            info = self.login(d,z,args)
            self.slot.backup(d,name,info)          #设备信息，卡槽号，QQ号
            self.repo.BackupInfo(cate_id, 'using', info,'%s_%s'%(d.server.adb.device_serial(),name))     #仓库号,使用中,QQ号,设备号_卡槽号


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return TIMLogin

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT57FSK00089")
    z = ZDevice("HT57FSK00089")
    slot = slot('tim')

    # print(d.dump(compressed=False))
    # print(d.info)
    slot.restore(d, 1)  # 有２小时没用过的卡槽情况，切换卡槽

    d.server.adb.cmd("shell","ime set com.zunyun.qk/.ZImeService").communicate()
    # d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()  # 清除缓存
    args = {"repo_cate_id":"38","time_delay":"3","time_limit":"120"};    #cate_id是仓库号，length是数量

    # args = {"step_id":"17010410261870600","repo_cate_id":"33","time_limit":"3","time_delay":"3"}
    # o.slot.restore(d,1)
    o.action(d,z,args)