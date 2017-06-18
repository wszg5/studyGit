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
            d.server.adb.cmd("shell", "pm clear com.tencent.mm").communicate()  # 清除缓存，返回home页面
            d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate() #使用命令唤起微信
            z.sleep(8)
            d(text='注册').click()
            z.sleep(1)
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
            if d(textContains='手机号码').exists:
                d(textContains='手机号码').click()
            else:
                d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout',index=2).child(className='android.widget.EditText',index=1).click()
                d.swipe(474,327,500,329)
            z.heartbeat()
            while True:
                PhoneNumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER)
                z.heartbeat()
                print(PhoneNumber)
                if PhoneNumber.startswith('17'):
                    break
                else:
                    self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER)
            # backNumber = 0
            # while True:
            #     if backNumber==0:
            #         PhoneNumber = self.xuma.GetPhoneNumber('2251')
            #         PhoneNumber = cache.popSet(self.cache_phone_key)
            #         if PhoneNumber is None:
            #             d.server.adb.cmd("shell",
            #                              "am broadcast -a com.zunyun.zime.toast --es msg \"缓存中没有号码\"" ).communicate()
            #             z.sleep(10)
            #             return
            #         print(PhoneNumber)
            #         print('-------------------------------上面是仓库里的号码')
            #         backNumber = self.xm.MatchPhoneNumber(PhoneNumber, '2251')  # 判断从库里取出的是否可用，当backNumber为０时不可用
            #         print(backNumber)
            #         print('-------------------------------------上面是backNumber')
            #     else:
            #         break
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
            while d(textContains='正在验证').exists:
                z.sleep(2)
            z.heartbeat()
            code = self.scode.GetVertifyCode(PhoneNumber, self.scode.WECHAT_REGISTER)
            self.scode.defriendPhoneNumber(PhoneNumber,self.scode.WECHAT_REGISTER)
            z.heartbeat()
            if '失败'==code:
                continue
            print(code)
            d(text='请输入验证码').click()
            z.input(code)
            d(text='下一步', className='android.widget.Button').click()

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
                print ('成功')
                z.sleep(20)


def getPluginClass():
    return WeiXinRegister

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    clazz = getPluginClass()
    o = clazz()
    d = Device("9ddbd665")
    z = ZDevice("9ddbd665")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    'dingdingdingdingdindigdingdingdingdingdingdingdingdingdingdingdingdignin'
    # repo = Repo()
    # repo.RegisterAccount('', 'gemb1225', '13045537833', '109')
    args = {"repo_name_id": "167","repo_number_id": "109","add_count": "9","time_delay": "3"}  # cate_id是仓库号，发中文问题
    o.action(d,z, args)









