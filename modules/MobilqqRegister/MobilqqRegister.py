# coding:utf-8
from uiautomator import Device
from XunMa import *
from Repo import *
import time
from zservice import ZDevice
from random import choice
import string,random

class TIMQQRegister:
    def __init__(self):
        self.xunma = XunMa()
        self.repo = Repo()
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}

        self.domain = "192.168.1.88"
        self.port = 8888

    def action(self, d,z):

        for i in range(1, 1000):

            d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存
            d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            d(resourceId='com.tencent.mobileqq:id/btn_register', index=1, text='新用户').click()
            newStart = 1
            while newStart == 1:
                token = self.xunma.GetToken()
                try:
                    phoneNumber = self.xunma.GetPhoneNumber(token, '640')
                    newStart = 0
                except Exception:
                    time.sleep(2)

            d(text='请输入你的手机号码', resourceId='com.tencent.mobileqq:id/name').set_text(phoneNumber)
            d(text='下一步', resourceId='com.tencent.mobileqq:id/name').click()
            d(descriptionContains='马上去发短信',index=0).click()
            d(text='添加文本',resourceId='com.htc.sense.mms:id/msg_text_editor').set_text('zc')
            d(className='android.widget.ImageButton',index='1').click()




            for j in range(1, 35):
                time.sleep(1)
                if d(text='请输入短信验证码', resourceId='com.tencent.mobileqq:id/name').exists:
                    break

            time.sleep(1)
            # 关闭设备锁
            if d(description='开启设备锁，保障QQ帐号安全。', className='android.widget.CheckBox').exists:
                continue

            else:

                data = self.XunMa.UploadPhoneNumber(phoneNumber)
                if data == 0:
                    print ("************匹配号码失败**************")
                    continue

                try:
                    vertifyCode = self.XunMa.GetTIMManyCode(phoneNumber, token)  # 获取验证码
                except Exception:
                    print (Exception, ":")
                    continue


                if vertifyCode == "":
                    print ("************+++++++++验证码请求失败++++++**************")
                    continue
                d(text='请输入短信验证码', resourceId='com.tencent.mobileqq:id/name').set_text(vertifyCode)

                nickNameList = self.GetMaterial(56, 0, 1)
                if len(nickNameList)==0:
                    continue
                nickName = nickNameList[0]["content"]
                time.sleep(1)
                d(text='下一步', resourceId='com.tencent.mobileqq:id/name').click()
                time.sleep(2)

                try:
                    d(resourceId='com.tencent.mobileqq:id/action_sheet_button',textContains='维持绑定').click()  # ****有问题，会crash****
                except Exception:
                    print (Exception, ":")
                    continue

                print (nickName)
                d(text='昵称', className='android.widget.EditText').click()
                z.input(nickName)

                password = self.GenPassword(6)
                d(text='密码', className='android.widget.EditText').set_text(password)
                d(text='注册', resourceId='com.tencent.mobileqq:id/btn_register').click()
                obj = d(index=1, className='android.widget.TextView', resourceId='com.tencent.mobileqq:id/name').info
                qqNumber = obj["text"]
                d(text='登录', className='android.widget.Button').click()
                time.sleep(8)

                print (qqNumber)
                print (i)


            self.TIMUploadAccount(qqNumber, password, phoneNumber)
            z.set_mobile_data(False)
            time.sleep(8)
            z.set_mobile_data(True)




    def GetMaterial(self, cateId, interval, limit):
        path = "/repo_api/material/pick?status=normal&cate_id=%s&interval=%s&limit=%s" % (cateId,interval,limit)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)

        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            numbers = json.loads(data)
            return  numbers
        else:
            return "Error Getting material, Please check your repo"


    def TIMUploadAccount(self,qqNumber,password,phomeNumber):
        path = "/repo_api/register/numberInfo?QQNumber=%s&QQPassword=%s&PhoneNumber=%s" % (qqNumber,password,phomeNumber)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET",path)

    def GenPassword(self,length=8,chars=string.ascii_letters+string.digits):
        return ''.join([choice(chars) for i in range(length)])

    def makePassword(self,minlength=5,maxlength=25):
        length=random.randint(minlength,maxlength)
        letters=string.ascii_letters+string.digits
        # alphanumeric, upper and lowercase
        return ''.join([random.choice(letters) for _ in range(length)])



def getPluginClass():
    return TIMQQRegister

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    from zservice import ZDevice
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # d.server.adb.cmd("shell", "am start -a android.intent.action.MAIN -n com.android.settings/.Settings").communicate()    #打开android设置页面

    # try:
    o.action(d, z)
    # except Exception, e:
    #     print Exception, ":", e
    #     if d(className = 'android.widget.Button', text='确定').exists:
    #         d(className='android.widget.Button', text='确定').click()
    #         print 'TIM崩了'
    #         o.action(d, z)
    #     else:
    #         print '未知错误'
    #         o.action(d, z)

    # repo = Repo()
    # nickNameList = repo.GetMaterial(56, 0, 1)
    # nickName = nickNameList[0]["name"]
    # # nickName = str(nickName)
    # print nickName


