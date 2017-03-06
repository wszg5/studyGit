# coding:utf-8
from uiautomator import Device
from zservice import ZDevice
from Repo import *
from XunMa import *
import time
from slot import slot
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class TIMRegisterWithSlot:

    def __init__(self):
        self.repo = Repo()
        self.xm = None
        self.slot = slot('tim')

    def registerWithSlot(self,d,z,args):
        cateId = args['repo_cate_id']
        self.xm = XunMa(d.server.adb.device_serial())

        d.server.adb.cmd("shell", "pm clear com.tencent.tim").communicate()  # 清除缓存
        d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来

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
        for i in range(0,3):
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
        obj = d(resourceId='com.tencent.tim:id/name',className='android.widget.TextView',index=1).info
        info = obj['text']                             #要保存的qq号
        d(text='登录', resourceId='com.tencent.tim:id/name').click()
        time.sleep(2)

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
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽全满，无2小时未用\"").communicate()
                time.sleep(30)
                name = self.slot.getSlot(d,time_limit)

            z.set_mobile_data(False)
            time.sleep(3)
            self.slot.restore(d,name)                      #有２小时没用过的卡槽情况，切换卡槽
            z.set_mobile_data(True)
            time.sleep(8)

            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"TIM卡槽成功切换成"+str(name)+"\"").communicate()
            time.sleep(1)

            d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来

            self.swipe(d)

            if d(text='消息',resourceId='com.tencent.tim:id/ivTitleName').exists:
                obj = self.slot.getSlotInfo(d,name)  #得到切换后的QQ号
                info = obj['info']  #info为QQ号
                self.repo.BackupInfo(cate_id,'using',info,'%s_%s'%(d.server.adb.device_serial(),name))  # 将登陆上的仓库cate_id,设备号d，卡槽号name，qq号info，备份到仓库
            else:
                info = self.registerWithSlot(d,z,args)
                if info != False:
                    #帐号无法登陆则重新注册登陆
                    self.slot.backup(d, name, info)  # 登陆之后备份,将备份后的信息传到后台　仓库号，状态，QQ号，备注设备id_卡槽id
                    self.repo.BackupInfo(cate_id, 'using', info, '%s_%s'%(d.server.adb.device_serial(),name))  # 将登陆上的仓库cate_id,设备号d，卡槽号name，qq号info，备份到仓库
                else:
                    d.server.adb.cmd("shell","am broadcast -a com.zunyun.zime.toast --es msg \"TIM卡槽备份失败\"").communicate()


        else:                           #有空卡槽的情况

            z.set_mobile_data(False)
            time.sleep(3)
            z.set_mobile_data(True)
            time.sleep(8)
            info = self.registerWithSlot(d,z,args)
            if info!=False:
                self.slot.backup(d,name,info)          #设备信息，卡槽号，QQ号
                self.repo.BackupInfo(cate_id, 'using', info,'%s_%s'%(d.server.adb.device_serial(),name))     #仓库号,使用中,QQ号,设备号_卡槽号
            else:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"TIM卡槽备份失败\"").communicate()

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
    return TIMRegisterWithSlot

if __name__ == "__main__":

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52DSK00474")
    z = ZDevice("HT52DSK00474")


    d.server.adb.cmd("shell","ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_cate_id":"102","time_delay":"3","time_limit":"120"};               #cate_id是仓库号，length是数量

    o.action(d,z,args)

    # slot = slot('tim')
    # slot.restore(d, 8)  # 有２小时没用过的卡槽情况，切换卡槽
    #
    # time.sleep(8)
    #
    # d.server.adb.cmd("shell",
    #                  "am broadcast -a com.zunyun.zime.toast --es msg \"TIM卡槽成功切换成" + str(8) + "\"").communicate()
    # time.sleep(1)
    #
    # d.server.adb.cmd("shell",
    #                  "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
    #
    # o.swipe(d)
