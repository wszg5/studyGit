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
        self.XunMa = XunMa()
        self.repo = Repo()
        self.headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "application/json", "Content-type": "application/xml; charset=utf=8"}

        self.domain = "192.168.1.88"
        self.port = 8888

    def action(self, d,z,args):
        cateId = args['repo_cate_id']
        numberCateId = args['muchNumber_cate_id']

        for registerQQ in range(1, 1000):

            d.server.adb.cmd("shell", "pm clear com.tencent.tim").communicate()  # 清除缓存
            d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            time.sleep(3)
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

            if k==35:
                continue
            time.sleep(2)

            if d(resourceId='com.tencent.tim:id/btn_register',index=1,text='新用户').exists:
                d(resourceId='com.tencent.tim:id/btn_register', index=1, text='新用户').click()
            time.sleep(2)


            phoneNumber = self.XunMa.GetPhoneNumber( '144')


            time.sleep(2)
            try:
                d(text='请输入你的手机号码', resourceId='com.tencent.tim:id/name').set_text(phoneNumber)
                time.sleep(1)
                d(text='下一步', resourceId='com.tencent.tim:id/name').click()

            except Exception:

                print '%s失败'%phoneNumber
                continue


            for j in range(1, 35):
                time.sleep(1)
                if d(text='请输入短信验证码', resourceId='com.tencent.tim:id/name').exists:
                    break
                if d(text='QQ注册', resourceId='com.tencent.tim:id/ivTitleName').exists:
                    continue

            time.sleep(3)
            # 关闭设备锁
            if d(description='开启设备锁，保障QQ帐号安全。', className='android.widget.CheckBox').exists:
                self.XunMa.ReleasePhone(phoneNumber)
                continue

            else:


                # data = self.XunMa.UploadPhoneNumber(phoneNumber, token)
                # if data == 0:
                #     print "************匹配号码失败**************"
                #     continue



                vertifyCode = self.XunMa.GetVertifyCode(phoneNumber,'144')  # 获取验证码




                if vertifyCode == "":
                    if d(text='重新发送', resourceId='com.tencent.tim:id/name').exists:
                        d(text='重新发送', resourceId='com.tencent.tim:id/name').click()
                        time.sleep(2)
                        print '重新发送'
                        vertifyCode = self.XunMa.GetVertifyCode(phoneNumber, '144')

                        if vertifyCode=='':
                            self.XunMa.ReleaseToken(phoneNumber)
                            print '验证码获取失败'
                            continue

                print vertifyCode
                d(text='请输入短信验证码', resourceId='com.tencent.tim:id/name').set_text(vertifyCode)

                time.sleep(1)
                d(text='下一步', resourceId='com.tencent.tim:id/name').click()
                time.sleep(2)

                try:
                    d(resourceId='com.tencent.tim:id/action_sheet_button',textContains='维持绑定').click()  # ****有问题，会crash****
                except Exception:
                    print ('维持绑定失败')
                    continue

                wait = 1
                while wait == 1:
                    nickNameList = self.GetMaterial(cateId, 0, 1)
                    if "Error" in nickNameList:  # 没有取到号码的时候
                        d.server.adb.cmd("shell",
                                         "am broadcast -a com.zunyun.qk.toast --es msg \"QQ号码%s号仓库为空，等待中\"" % cateId).communicate()
                        time.sleep(3)
                        continue
                    elif len(nickNameList) == 0:
                        d.server.adb.cmd("shell",
                                         "am broadcast -a com.zunyun.qk.toast --es msg \"QQ号码%s号仓库为空，等待中\"" % cateId).communicate()
                        time.sleep(1)
                        continue
                    wait = 0

                nickName = nickNameList[0]["content"].encode("utf-8")

                # nickName = ''
                # while nickName=='':
                #     nickName = full_name(last_names, first_names)
                #     continue


                d(text='昵称', className='android.widget.EditText').click()
                z.input(nickName)
                print nickName

                password = self.GenPassword()
                d(text='密码', className='android.widget.EditText').set_text(password)
                d(text='注册', resourceId='com.tencent.tim:id/btn_register').click()
                obj = d(index=1, className='android.widget.TextView', resourceId='com.tencent.tim:id/name').info
                qqNumber = obj["text"]
                # d(text='登录', className='android.widget.Button').click()
                # time.sleep(8)



            self.TIMUploadAccount(qqNumber, password, phoneNumber, numberCateId)
            # z.set_mobile_data(False)
            # time.sleep(6)
            # z.set_mobile_data(True)
            if (args["time_delay"]):
                time.sleep(int(args["time_delay"]))




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


    def TIMUploadAccount(self,qqNumber,password,phomeNumber, numberCateId):
        path = "/repo_api/register/numberInfo?QQNumber=%s&QQPassword=%s&PhoneNumber=%s&cate_id=%s" % (qqNumber,password,phomeNumber,numberCateId)
        conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        conn.request("GET",path)



    def makePassword(self,minlength=5,maxlength=25):
        length=random.randint(minlength,maxlength)
        letters=string.ascii_letters+string.digits
        # alphanumeric, upper and lowercase
        return ''.join([random.choice(letters) for _ in range(length)])

    def GenPassword(self):
        # 随机出数字的个数
        numOfNum = 4
        numOfLetter = 4
        # 选中numOfNum个数字
        slcNum = [random.choice(string.digits) for i in range(numOfNum)]
        # 选中numOfLetter个字母
        slcLetter = [random.choice(string.lowercase) for i in range(numOfLetter)]
        slcChar = slcLetter + slcNum
        genPwd = ''.join([i for i in slcChar])
        return genPwd



def getPluginClass():
    return TIMQQRegister

if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK01653")
    z = ZDevice("HT4A4SK01653")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # d.server.adb.cmd("shell", "am start -a android.intent.action.MAIN -n com.android.settings/.Settings").communicate()    #打开android设置页面

    # try:
    args = {"repo_cate_id": "33","muchNumber_cate_id":"32", "time_delay": "3"};
    o.action(d, z, args)


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



