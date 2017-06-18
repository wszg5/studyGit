# coding:utf-8
from uiautomator import Device
from Repo import *
from smsCode import smsCode
import time, string, random
from zservice import ZDevice

class WeiXinRegister:
    def __init__(self):

        self.repo = Repo()
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

    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        self.scode = smsCode(d.server.adb.device_serial())
        while True:
            d.press.home()
            d.server.adb.cmd("shell", "pm clear com.tencent.mm").communicate()  # 清除缓存，返回home页面
            if d(text='微信').exists:
                d(text='微信').click()
            else:
                d.swipe(width - 20, height / 2, 0, height / 2,5)
                if d(text='微信').exists:
                    d(text='微信').click()
            z.sleep(5)
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
                d(textContains='国家').click()
                d(className='android.support.v7.widget.LinearLayoutCompat',index=1).click()
                z.input('中')
                d(text='中国').click()

            d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout', index=2).child(
                className='android.widget.EditText', index=1).click()
            d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout', index=2).child(
                className='android.widget.EditText', index=1).click.bottomright()
            z.heartbeat()

            # PhoneNumber = '18458194478'
            PhoneNumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER,'13941940790')
            z.heartbeat()
            print(PhoneNumber)
            z.input(PhoneNumber)
            d(className='android.widget.LinearLayout',index=3).child(className='android.widget.EditText').click()
            d(textContains='密码').click()
            z.heartbeat()
            password = self.GenPassword()
            z.input(password)
            print(password)
            print('-------------------------------------上面是密码')
            z.heartbeat()
            d(text='注册').click()
            d(text='确定').click()
            z.sleep(2)
            if d(textContains='正在验证').exists:
                z.sleep(40)
            z.heartbeat()
            # code = '769679'
            code = self.scode.GetVertifyCode(PhoneNumber, self.scode.WECHAT_REGISTER)
            self.scode.defriendPhoneNumber(PhoneNumber,self.scode.WECHAT_REGISTER)
            z.heartbeat()
            if '失败'==code:
                code = self.scode.GetVertifyCode( PhoneNumber, self.scode.WECHAT_REGISTER)
                self.scode.defriendPhoneNumber( PhoneNumber, self.scode.WECHAT_REGISTER)
            print(code)
            d(text='请输入验证码').click()
            z.input(code)
            d(text='下一步', className='android.widget.Button').click()

            while d(text='验证码不正确，请重新输入').exists:
                d(text='确定').click()
                if d(text='收不到验证码？').exists:
                    continue
                d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout',index=0).child(className='android.widget.LinearLayout',index=2).child(
                    className='android.widget.LinearLayout',index=0).child(className='android.widget.EditText', index=1).click.bottomright()
                # code = '596028'
                code = self.scode.GetVertifyCode(PhoneNumber, self.scode.WECHAT_REGISTER)
                self.scode.defriendPhoneNumber(PhoneNumber,self.scode.WECHAT_REGISTER)
                z.sleep(8)
                z.heartbeat()
                if '失败' == code:
                    continue
                print(code)
                d(text='请输入验证码').click()
                z.input(code)
                d(text='下一步', className='android.widget.Button').click()
                if d(text='你操作频率过快，请重新输入').exists:
                    d(text='确定').click
                    continue

            if d( text='收不到验证码？' ).exists:
                break

            time.sleep(1.5)
            if d(text='不是我的，继续注册').exists:
                d(text='不是我的，继续注册').click()
                continue
            if d(textContains='不可频繁重复注册').exists:
                continue
            else:
                z.heartbeat()
                d(textContains='是我的').click()
                d(text='确定', className='android.widget.Button').click()
                cate_id = args['repo_number_id']
                self.repo.RegisterAccount('',password,PhoneNumber,cate_id)
                print('成功')
                z.sleep(20)


def getPluginClass():
    return WeiXinRegister

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    'dingdingdingdingdindigdingdingdingdingdingdingdingdingdingdingdingdignin'
    # repo = Repo()
    # repo.RegisterAccount('', 'gemb1225', '13045537833', '109')
    args = {"repo_name_id": "167","repo_number_id": "109","add_count": "9","time_delay": "3"}  # cate_id是仓库号，发中文问题
    o.action(d,z, args)









