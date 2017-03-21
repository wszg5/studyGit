# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class QLJudgeQQBind:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "pm clear com.tencent.qqlite").communicate()  # 清除缓存
        d.server.adb.cmd("shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 将qq拉起来
        time.sleep(8)
        d(text='新用户').click()
        time.sleep(1)

        add_count = int(args['add_count'])  # 搜索号码的次数
        for i in range(0, add_count, +1):  # 总人数
            cate_id = args["repo_number_id"]
            number = self.repo.GetNumber(cate_id, 0, 1)
            if len(number) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"手机号码库%s号仓库为空，等待中\"" % cate_id).communicate()
                time.sleep(10)
                return
            PhoneNumber = number[0]['number']  # 取出验证消息的内容

            z.input(PhoneNumber)
            z.heartbeat()
            d(text='下一步').click()
            time.sleep(1.5)
            if d(textContains='已绑定其他').exists:
                z.heartbeat()
                SetCateId = args['repo_number_id1']
                self.repo.uploadPhoneNumber(PhoneNumber, SetCateId)  # 将有用的号传到库里
                d(text='取消').click()

            elif d(textContains='我知道了').exists:
                z.heartbeat()
                d(textContains='我知道了').click()
                SetCateId = args['repo_number_id1']
                self.repo.uploadPhoneNumber(PhoneNumber, SetCateId)  # 将有用的号传到库里

            else:
                d(description='向上导航').click()

            obj = d(className='android.widget.EditText', index=2)
            if obj.exists:
                obj = obj.info
                obj = obj['bounds']  # 验证码处的信息
                left = obj["left"]  # 验证码的位置信息
                top = obj['top']
                right = obj['right']
                bottom = obj['bottom']
                height = bottom - top
                width = right - left
                y = height / 2 + top
                d.swipe(width + 150, y, width + 200, y, 1)      #用来一键删除
            z.heartbeat()
            obj = d(className='android.widget.EditText').info   #当上马的一键删除无效时再单个删除
            obj = obj['text']
            if '手机号码' in obj:
                continue
            else:
                lenth = len(obj)
                t = 0
                while t<lenth:
                    d.press.delete()
                    t = t+1
            z.heartbeat()
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return QLJudgeQQBind

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
    args = {"repo_number_id": "44","repo_number_id1": "118","add_count": "100","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)




















