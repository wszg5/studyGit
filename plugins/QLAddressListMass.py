# coding:utf-8
from uiautomator import Device
from Repo import *
from smsCode import smsCode
import time, datetime, random
from zservice import ZDevice
from PIL import Image

class QLAddressListMass:
    def __init__(self):
        self.repo = Repo()

    def Bind(self, d,z):
        self.scode = smsCode(d.server.adb.device_serial())
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.scode.GetPhoneNumber(self.scode.QQ_CONTACT_BIND)
            print(GetBindNumber)
            time.sleep(2)
            z.input(GetBindNumber)
            z.heartbeat()

            time.sleep(1)
            d(text='下一步').click()
            time.sleep(3)

            if d(text='确定').exists:  # 提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d(text='确定').click()
                if d(text='确定').exists:
                    return 'false'

            code = self.scode.GetVertifyCode(GetBindNumber, self.scode.QQ_CONTACT_BIND, '4')
            newStart = 0
            z.input(code)
            z.heartbeat()
            d(text='下一步').click()
            time.sleep(4)
            if d(textContains='访问你的通讯录').exists:
                d(text='好').click()
                time.sleep(5)

            if d(textContains='没有可匹配的').exists:
                return 'false'
            if d(textContains='验证短信').exists:    #验证码错误的情况
                return 'false'

        return 'true'

    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        width = str["displayWidth"]
        height = str["displayHeight"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.qqlite").wait()  # 将qq强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 将qq拉起来
        time.sleep(8)
        d(text='联系人').click()
        d(text='通讯录').click()
        time.sleep(1)
        if d(textContains='访问你的通讯录').exists:
            d(text='好').click()          #没有人的情况要判断
        if d(text='匹配通讯录').exists:
            d(text='匹配通讯录').click()
            while not d(descriptionContains='发消息').exists:  #匹配通讯录存在延时
                time.sleep(2)
        if d(text='启用').exists:
            d(text='启用').click()
            text = self.Bind(d,z)
            if text == 'false':  # 操作过于频繁的情况
                return
            time.sleep(3)
        z.heartbeat()
        add_count = int(args['add_count'])  # 给多少人发消息
        gender = args['gender']
        t = 0
        i = 0
        set1 = set()
        while t<add_count:
            forClick = d(className='android.view.View').child(className='android.widget.RelativeLayout',index=i).child(className='android.widget.TextView')
            print(i)
            time.sleep(1.5)
            if forClick.exists:
                z.heartbeat()
                savePhone = forClick.info
                savePhone = savePhone['text']
                if savePhone in set1:
                    i = i+1
                    continue
                set1.add(savePhone)
                print('保存的号码是%s'%savePhone)
                forClick.click()
                time.sleep(1)
                z.heartbeat()
                if gender!='不限':
                    if not d(textContains=gender).exists:
                        d(description='向上导航').click()
                        i = i+1
                        continue
                z.heartbeat()
                d(text='发消息').click()
                d(className='android.widget.EditText').click()
                cate_id = args["repo_material_id"]
                Material = self.repo.GetMaterial(cate_id, 0, 1)
                if len(Material) == 0:
                    d.server.adb.cmd("shell",
                                     "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                    time.sleep(10)
                    return
                message = Material[0]['content']  # 取出验证消息的内容
                z.input(message)
                z.heartbeat()
                d(text='发送').click()
                while d(className='android.widget.ProgressBar').exists:
                    time.sleep(1)
                if d(description='重新发送').exists:
                    return
                d(description='向上导航').click()
                d(description='向上导航').click()
                i = i+1
                t = t+1
            else:
                # g = i-1
                if d(text='未启用通讯录的联系人').exists:    #到达未启用的那个人结束发消息
                    break
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 6)
                time.sleep(2)
                # endcondition = d(className='android.view.View').child(className='android.widget.RelativeLayout', index=g).child(
                #     className='android.widget.TextView')
                # if endcondition.exists:
                #     endcondition = endcondition.info
                #     endcondition = endcondition['text']
                #     if endcondition in set1:
                #         print('结束时号码%s'%endcondition)
                #         break
                # else:
                #     endcondition = d(className='android.view.View').child(className='android.widget.RelativeLayout',index=g-1).child(className='android.widget.TextView').info
                #     endcondition = endcondition['text']
                #     if endcondition in set1:
                #         print('结束时号码%s'%endcondition)
                #         break
                # print('最后的人是%s'%endcondition)
                i = 1
                time.sleep(1)



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return QLAddressListMass

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id":"39",'gender':"女",'add_count':'100',"time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)




















