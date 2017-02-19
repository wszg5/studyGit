# coding:utf-8
from uiautomator import Device
from Repo import *
from XunMa import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')




class RegisterAccount:
    def __init__(self):

        self.repo = Repo()
        self.XunMa = XunMa()

    def action(self, d,z, args):
        while True:
            d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()
            d.server.adb.cmd("shell", "pm clear com.tencent.mm").wait()  # 清除缓存
            # 将微信拉起来
            d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()
            time.sleep(8)
            if d(text='注册').exists:
                d(text='注册').click()

            d(textContains='例如').click()
            cate_id = args['repo_name_id']  # 得到昵称库的id
            Material = self.repo.GetMaterial(cate_id, 0, 1)  # 修改昵称
            wait = 1
            while wait == 1:
                try:
                    name = Material[0]['content']  # 从素材库取出的要发的材料
                    wait = 0
                except Exception:
                    d.server.adb.cmd("shell",
                                     "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
            z.input(name)

            d(textContains='手机号码').click()
            phoneNumber = self.XunMa.GetPhoneNumber('2251', 0)
            print(phoneNumber)
            z.input(phoneNumber)
            d(className='android.widget.LinearLayout',index=3).child(className='android.widget.EditText').click()
            d(textContains='密码').click()
            z.input('13141314abc')

            d(text='注册').click()
            d(text='确定').click()
            time.sleep(2)
            while d(textContains='正在验证').exists:
                time.sleep(2)

            code = self.XunMa.GetVertifyCode(phoneNumber,'2251',6)
            if '失败'==code:
                continue
            print(code)
            d(text='请输入验证码', className='android.widget.EditText').set_text(code)
            d(text='下一步', className='android.widget.Button').click()

            time.sleep(1.5)
            if d(text='不是我的，继续注册').exists:
                d(text='不是我的，继续注册').click()
                continue
            if d(textContains='不可频繁重复注册').exists:
                continue
            else:
                d(text='确定', className='android.widget.Button').click()
                print ('成功')
                time.sleep(20)
                break


def getPluginClass():
    return RegisterAccount

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # d(calssName='android.widget.EditText').click()
    # z.input('652466')
    # d.dump(compressed=False)
    args = {"repo_name_id": "38","repo_number_cate_id": "13", "repo_material_cate_id": "8", "gender": "女", "add_count": "9","time_delay": "3"}  # cate_id是仓库号，发中文问题
    o.action(d,z, args)