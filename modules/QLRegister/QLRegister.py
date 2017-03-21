# coding:utf-8
import string
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from PIL import Image

class QLRegister:
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
        d.server.adb.cmd("shell", "pm clear com.tencent.qqlite").communicate()  # 清除缓存
        d.server.adb.cmd("shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 将qq拉起来
        time.sleep(8)
        # cateId = args['repo_cate_id']
        # nickNameList = self.repo.GetMaterial(cateId, 0, 1)
        # nickName = nickNameList[0]["content"]
        # nickName = nickName.encode("utf-8")
        # d(text='昵称', className='android.widget.EditText').click()
        # z.input(nickName)
        d(text='新用户').click()
        count = args['add_count']
        time.sleep(1)
        condition = 0
        while condition<count:
            z.heartbeat()
            phoneNumber = self.scode.GetPhoneNumber(self.scode.QQ_REGISTER)
            z.input(phoneNumber)
            d(text='下一步').click()
            time.sleep(4)

            if d(textContains='已绑定其他QQ号码').exists:
                d(text='取消').click()


            if d(description='用QQ浏览器​打开').exists:
                d(description='向上导航').click()

            obj = d(className='android.widget.EditText', index=2)
            if obj.exists:
                z.heartbeat()
                obj = obj.info
                obj = obj['bounds']  # 验证码处的信息
                left = obj["left"]  # 验证码的位置信息
                top = obj['top']
                right = obj['right']
                bottom = obj['bottom']
                height = bottom - top
                width = right - left
                y = height / 2 + top
                d.swipe(width + 150, y, width + 200, y, 1)
                continue
            if not '手机号码' in obj:   #当一键删除失败时一个个删除
                lenth = len(obj)
                t = 0
                while t<lenth:
                    d.press.delete()
                    t = t+1

            z.heartbeat()
            verifycode = self.scode.GetVertifyCode(phoneNumber, self.scode.QQ_CONTACT_BIND)
            z.input(verifycode)

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return QLRegister

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    z.input('177751880')
    z.input('13141314abcd')
    args = {"repo_number_id": "44","repo_material_id": "118","add_count": "100","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)




















