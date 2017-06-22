# coding:utf-8
from uiautomator import Device
from Repo import *
from smsCode import smsCode
import time, string, random
from zservice import ZDevice
from slot import Slot


class WeiXinRegister:
    def __init__(self):
        self.type = 'wechat'
        self.repo = Repo()
        # self.slot = Slot(self.type)
        self.xm = None
        self.cache_phone_key = 'cache_phone_key'

    def GenPassword(self, numOfNum=4, numOfLetter=4):
        # 选中numOfNum个数字
        slcNum = [random.choice(string.digits) for i in range(numOfNum)]
        # 选中numOfLetter个字母
        slcLetter = [random.choice(string.lowercase) for i in range(numOfLetter)]
        slcChar = slcLetter + slcNum
        genPwd = ''.join([i for i in slcChar])
        return genPwd

    def qiehuan(self):
        z.heartbeat()
        time_limit = args['time_limit']
        slotnum = self.slot.getEmpty(d)  # 取空卡槽
        if slotnum == 0:  # 没有空卡槽的话
            slotnum = self.slot.getSlot( d, time_limit )  # 没有空卡槽，取２小时没用过的卡槽
            print( slotnum )
            while slotnum == 0:  # 2小时没用过的卡槽也为没有的情况
                d.server.adb.cmd("shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"").communicate()
                z.heartbeat()
                z.sleep(30)
                slotnum = self.slot.getSlot(d, time_limit)
            z.heartbeat()
            d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存

            d.server.adb.cmd("shell", "settings put global airplane_mode_on 1").communicate()
            d.server.adb.cmd("shell",
                              "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true").communicate()
            z.sleep(6)

    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        self.scode = smsCode(d.server.adb.device_serial())
        while True:
            d.press.home()
            d.server.adb.cmd("shell", "pm clear com.tencent.mm").communicate()  # 清除缓存，返回home页面

            while True:
                if d(text='微信').exists:
                    d(text='微信').click()
                    break
                d.swipe( width - 20, height / 2, 0, height / 2, 5 )

            z.sleep(8)
            if d(text='注册').exists:
                d(text='注册').click()
            cate_id = args['repo_name_id']  # 得到昵称库的id
            Material = self.repo.GetMaterial(cate_id, 0, 1)  # 修改昵称
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                z.sleep(10)
                return
            z.heartbeat()
            name = Material[0]['content']  # 从素材库取出的要发的材料
            z.input(name)       #name

            if not d(text='中国').exists:
                d(text='国家/地区').click()
                d(className='android.support.v7.widget.LinearLayoutCompat',index=1).click()
                z.input('中')
                d(text='中国').click()

            d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout', index=2).child(
                className='android.widget.EditText', index=1).click()
            d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout', index=2).child(
                className='android.widget.EditText', index=1).click.bottomright()
            z.heartbeat()

            PhoneNumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER,'13064522307')#获取接码平台手机号码
            z.heartbeat()
            print(PhoneNumber)
            z.input(PhoneNumber)
            d(className='android.widget.LinearLayout',index=3).child(className='android.widget.EditText').click()
            d(textContains='密码').click()
            z.heartbeat()
            password = self.GenPassword()
            z.input(password)
            print(password)
            print('↑ ↑ ↑ ↑ ↑ ↑ ↑　↑  上面是手机＋密码 ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ')
            z.heartbeat()
            d(text='注册').click()
            d(text='确定').click()
            if d(textContains='正在验证').exists:
                z.sleep(35)
            z.heartbeat()
            code = self.scode.GetVertifyCode(PhoneNumber, self.scode.WECHAT_REGISTER)#获取接码验证码
            self.scode.defriendPhoneNumber(PhoneNumber,self.scode.WECHAT_REGISTER)
            if code == '':
                z.toast( PhoneNumber + '手机号,获取不到验证码' )
                continue
            z.heartbeat()
            print('验证码：'+code)
            d(text='请输入验证码').click()
            z.input(code)
            d(text='下一步', className='android.widget.Button').click()

            while d(text='验证码不正确，请重新输入').exists:
                d(text='确定').click()
                d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout',index=0).child(className='android.widget.LinearLayout',index=2).child(
                    className='android.widget.LinearLayout',index=0).child(className='android.widget.EditText', index=1).click.bottomright()
                # code = '596028'
                code = self.scode.GetVertifyCode(PhoneNumber, self.scode.WECHAT_REGISTER)
                self.scode.defriendPhoneNumber(PhoneNumber,self.scode.WECHAT_REGISTER)
                if code == '':
                    z.toast(PhoneNumber+'手机号,获取不到验证码')
                    break
                z.sleep(8)
                z.heartbeat()
                print(code)
                d(text='请输入验证码').click()
                z.input(code)
                d(text='下一步', className='android.widget.Button').click()

                if d(text='你操作频率过快，请重新输入').exists:
                    d(text='确定').click
                    break

            time.sleep(1.5)

            while True:
                if d(text='是我的，立刻登录').exists:
                    d(text='是我的，立刻登录').click()
                    z.sleep(3)
                    if d(textContains='看看手机通讯录里谁在使用微信？').exists:
                        d(text='是').click()

                    if d(textContains='有人正通过短信验证码').exists:
                        d(text='确定').click()
                        break

                if d(textContains='非法软件注册').exists:
                    d(text='取消').click()
                    break

                if d(text='该帐号长期未登录，为保护帐号安全，系统将其自动置为保护状态。点击确定按钮可立即激活帐号解除保护状态。').exists:
                    d(text='取消')
                    break

                if d(textContains='帐号有异常').exists:
                    d(text='取消').click()
                    break

                if d(textContains='限制登录').exists:
                    d(text='取消').click()
                    break

                if d(textContains='长期没有登陆，帐号已被收回').exists:
                    d(text='取消').click()
                    break

                if d(textContains='相同手机号不可频繁重复注册微信帐号').exists:
                    d(text='确定').click()
                    break

                if d(textContains='是否立即验证').exists:
                    d(text='确定').click()
                    z.sleep(15)

                if d(text='确认登录').exists:
                    break

                if d( description='通过扫码验证身份', className='android.view.View', index=1 ).exists:
                    break

                if d(text='验证身份').exists:
                    a = ''
                    for i in range(1, 5):
                        if d(description='请选择你最近一次登录设备的名称').exists:
                            number = random.randint(1, 5)
                            if number == 1:
                                d(resourceId='x0', className='android.widget.RadioButton').click()
                                d(resourceId='submitBtn', className='android.view.View',
                                   descriptionContains='下一步').click()  # 下一步
                            if number == 2:
                                d(resourceId='x1', className='android.widget.RadioButton').click()
                                d(resourceId='submitBtn', className='android.view.View',
                                   descriptionContains='下一步').click()  # 下一步
                            if number == 3:
                                d(resourceId='x2', className='android.widget.RadioButton').click()
                                d(resourceId='submitBtn', className='android.view.View',
                                   descriptionContains='下一步').click()  # 下一步
                            if number == 4:
                                d(resourceId='x3', className='android.widget.RadioButton').click()
                                d(resourceId='submitBtn', className='android.view.View',
                                   descriptionContains='下一步').click()  # 下一步
                            if number == 5:
                                d(resourceId='x4', className='android.widget.RadioButton',).click()
                                d(resourceId='submitBtn', className='android.view.View',
                                   descriptionContains='下一步').click()  # 下一步
                        elif d(description='请从下面头像中选出两位你的好友').exists:
                            d.swipe(230, 450, 240, 450)
                            d.swipe(400, 450, 410, 450)
                            d(resourceId='submitBtn', className='android.view.View',
                               descriptionContains='下一步').click()  # 下一步
                        else:
                            d(resourceId='x5', className='android.widget.RadioButton',
                               descriptionContains='以上都不是').click()  # 以上都不是
                            d(resourceId='submitBtn', className='android.view.View',
                               descriptionContains='下一步').click()  # 下一步

                if d(descriptionContains='验证失败', className='android.view.View', index=1).exists:
                    d(descriptionContains='关闭页面', className='android.view.View', index=3).click()

                if d(descriptionContains='验证通过', className='android.view.View', index=1).exists:
                    d(descriptionContains='关闭页面', className='android.view.View', index=3).click()

            continue





def getPluginClass():
    return WeiXinRegister

if __name__ == "__main__":
    import sys
    reload( sys )
    sys.setdefaultencoding( 'utf8' )

    clazz = getPluginClass()
    o = clazz()
    d = Device("916c6fd5")#INNZL7YDLFPBNFN7
    z = ZDevice("916c6fd5")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    'dingdingdingdingdindigdingdingdingdingdingdingdingdingdingdingdingdignin'
    # repo = Repo()
    # repo.RegisterAccount('', 'gemb1225', '13045537833', '109')
    args = {"repo_name_id": "167","repo_number_id": "109","add_count": "9","time_delay": "3"}  # cate_id是仓库号，发中文问题
    o.action(d,z, args)









