# coding:utf-8
from uiautomator import Device
from Repo import *
import time, string, random
from zservice import ZDevice
from smsCode import smsCode

class AlipayRegister:
    def __init__(self):
        self.repo = Repo()
        self.xuma = None

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
        self.scode = smsCode(d.server.adb.device_serial())
        while True:
            d.server.adb.cmd("shell", "pm clear com.eg.android.AlipayGphone").communicate()  # 清除缓存
            # d.server.adb.cmd("shell", "am force-stop com.eg.android.AlipayGphone").wait()  # 强制停止
            d.server.adb.cmd("shell", "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin").communicate()  # 拉起来
            while not d(textContains='没有账号').exists:
                z.sleep(2)
            d(textContains='没有账号').click()
            cate_id = args['repo_name_id']  # 得到昵称库的id
            Material = self.repo.GetMaterial(cate_id, 0, 1)  # 修改昵称
            if len(Material) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                z.sleep(10)
                return
            name = Material[0]['content']  # 从素材库取出的要发的材料
            z.input(name)  # name
            z.heartbeat()
            d(text='中国大陆').click()
            d(text='中国大陆').click()
            d(className='android.widget.ScrollView').child(className='android.widget.RelativeLayout',index=2).click()
            d(description='清空输入内容').click()
            GetBindNumber = self.scode.GetPhoneNumber(self.scode.ALIPAY_REGISTER)

            z.input(GetBindNumber)
            z.heartbeat()
            d(className='android.widget.ScrollView').child(className='android.widget.RelativeLayout', index=3).click()
            password = self.GenPassword()
            z.input(password)
            d(text='注册').click()
            d(text='确定').click()

            code = self.xunma.GetVertifyCode(GetBindNumber, self.scode.ALIPAY_REGISTER)
            z.input(code)
            z.heartbeat()
            d(text='提交').click()
            z.sleep(5)
            if d(textContains='是我的').exists:
                d(textContains='是我的').click()
            if d(textContains='直接登录').exists:
                d(textContains='直接登录').click()
                cate_id = args['repo_number_id']
                self.repo.RegisterAccount('', password, GetBindNumber, cate_id)
                z.sleep(3)
            if d(textContains='没有账号').exists:
                z.heartbeat()
                continue
            else:
                break

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return AlipayRegister

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    # z.input('177751880')
    # z.input('13141314ABC')
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_name_id": "102","repo_number_id": "136","time_delay": "3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

