# coding:utf-8
import colorsys

from PIL import Image

from smsCode import smsCode
from uiautomator import Device
from Repo import *
import os, time, datetime, random
import util
from zservice import ZDevice


class QLCheckDepo:

    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def Bind(self, d,z):
        self.scode = smsCode(d.server.adb.device_serial())
        newStart = 1
        while newStart < 3:
            GetBindNumber = self.scode.GetPhoneNumber(self.scode.QQ_CONTACT_BIND)
            print(GetBindNumber)
            z.sleep(2)
            d(text='请输入你的手机号码', className='android.widget.EditText')
            z.input(GetBindNumber)  # GetBindNumber
            z.heartbeat()
            z.sleep(1)
            d(text='下一步').click()
            z.sleep(3)
            if d(text='下一步', resourceId='com.tencent.mobileqq:id/name', index=2).exists:  # 操作过于频繁的情况
                return 'false'

            if d(text='确定', resourceId='com.tencent.qqlite:id/phone_bind_changeqq_confirm_btn').exists:  # 提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d(text='确定', resourceId='com.tencent.qqlite:id/phone_bind_changeqq_confirm_btn').click()

            try:
                code = self.scode.GetVertifyCode(GetBindNumber, self.scode.QQ_CONTACT_BIND, '4')
                if d(text='启用').exists:
                    d(resourceId='com.tencent.qqlite:id/ivTitleBtnLeft').click()
            except:
                if d(text='启用').exists:
                    d(resourceId='com.tencent.qqlite:id/ivTitleBtnLeft').click()

                if d(text='验证手机号码').exists:
                    d(text='验证手机号码').click()
                    z.sleep(1)

                obj = d(resourceId='com.tencent.qqlite:id/number_edit', className='android.widget.EditText', index=2)
                if obj.exists:
                    deltext = obj.info['text']

                if deltext != '':
                    for i in range(len(deltext)):
                        d.press.delete()
                newStart += 1
                continue

            d(resourceId='com.tencent.qqlite:id/code_edit').click()
            z.input(code)
            z.heartbeat()
            d(text='下一步').click()
            z.sleep(5)

            if d(text='“QQ”想访问你的通讯录').exists:
                d(text='好').click()

            if d(textContains='没有可匹配的').exists:
                return 'false'

            if code != '':
                break

        if newStart >= 3:
            return 'false'

        return 'true'

    def action(self, d, z, args):
        z.toast( "正在ping网络是否通畅" )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ轻聊版通讯录检存" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast("网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return

        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.qqlite" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep(8)
        z.heartbeat()

        if d(text='消息').exists:  # 到了通讯录这步后看号有没有被冻结
            z.toast("状态正常，继续执行")
        else:
            z.toast("状态异常，跳过此模块")
            return

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d(text="联系人",className="android.widget.TextView").click()
        if d(description="通讯录").exists:
            d(description="通讯录").click()
        z.sleep(1)

        if d(text='启用').exists:
            d(text='启用').click()
            z.sleep(1)

        if d(text=' +null', resourceId='com.tencent.qqlite:id/country_code_txt').exists:
            d(text=' +null', resourceId='com.tencent.qqlite:id/country_code_txt').click()
            d(text='中国', resourceId='com.tencent.qqlite:id/country_name_txt').click()
            z.sleep(1)

        if d(text='验证手机号码').exists:
            bind_result = self.Bind(d, z)
            if bind_result == 'false':
                z.toast("接不到验证码")
                return

            z.sleep(int(args['time_delay1']))
            z.heartbeat()

        if d(text='匹配通讯录').exists:
            d(text='匹配通讯录').click()

        alreadyClickBtnArr = []
        judge = 0
        while True:

            for i in range(0, 9):
                obj = d(resourceId='com.tencent.qqlite:id/contact_pdlv').child(className='android.widget.RelativeLayout', index=i).child(resourceId='com.tencent.qqlite:id/name_text')
                if obj.exists:
                    alreadyClickBtn = obj.info['text']
                    if alreadyClickBtn in alreadyClickBtnArr:
                        continue
                    else:
                        z.heartbeat()
                        alreadyClickBtnArr.append(alreadyClickBtn)

                        obj.click()

                        number = d(resourceId='com.tencent.qqlite:id/common_xlistview').child(
                            resourceId='com.tencent.qqlite:id/info_card_header').child(resourceId='com.tencent.qqlite:id/info_layout').child(
                            resourceId='com.tencent.qqlite:id/nick_layout').child(resourceId='com.tencent.qqlite:id/info_card_nick').info['text']

                        gender = ''
                        age = ''
                        area = ''
                        infoObj = d(resourceId='com.tencent.qqlite:id/common_xlistview').child(
                            resourceId='com.tencent.qqlite:id/info_card_header').child(resourceId='com.tencent.qqlite:id/info_layout').child(
                            resourceId='com.tencent.qqlite:id/info_card_info', index=2)

                        if infoObj.exists:
                            gender = infoObj.info['text'][0]
                            age = infoObj.info['text'][2:5]
                            area = infoObj.info['text'][5:len(infoObj.info['text'])]

                        nick = d(resourceId='com.tencent.qqlite:id/common_xlistview').child(
                            resourceId='com.tencent.qqlite:id/info_card_more_layout').child(className='android.widget.LinearLayout', index=0).child(
                            resourceId='com.tencent.qqlite:id/info', index=1).info['text']

                        para = {"phoneNumber": number, 'x_01': gender, 'x_02': age, 'x_03': area, 'x_04': nick}
                        self.repo.PostInformation(args['repo_cate_id'], para)

                        if d(resourceId='com.tencent.qqlite:id/ivTitleBtnLeft').exists:
                            d(resourceId='com.tencent.qqlite:id/ivTitleBtnLeft').click()



            if len(alreadyClickBtnArr) > judge:
                judge = len(alreadyClickBtnArr)
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 6)
            else:
                break

        if args["time_delay"]:
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return QLCheckDepo

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("465b4e4b")
    z = ZDevice("465b4e4b")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # print(d.dump(compressed=False))
    args = {'repo_cate_id': "349","time_delay1": "1", "time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)

    pass