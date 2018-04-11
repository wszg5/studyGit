# coding:utf-8

import random
from uiautomator import Device
from Repo import *
from zservice import ZDevice


class QQMailSendGreetingCards:
    def __init__(self):
        self.repo = Repo()
        self.type = 'qqmail'

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 1000) # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

    def getMaterial(self, cateId, interval, limit=1):
        materials = []
        while len(materials) == 0:
            materials = self.repo.GetMaterial(cateId, interval, limit)  # 去仓库获取主题内容
            if len(materials) == 0:
                z.toast(u"素材库为空")
                z.sleep(30)
        return materials

    def action(self, d, z, args):
        z.toast(u"正在ping网络是否通畅")
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast(u"网络通畅。开始执行：QQ邮箱发送贺卡")
                break
            z.sleep(2)
        if i > 200:
            z.toast(u"网络不通，请检查网络状态")
            return

        z.heartbeat()
        d.server.adb.cmd("shell", "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail").communicate()  # 拉起QQ邮箱

        Str = d.info  # 获取屏幕大小等信息
        height = Str["displayHeight"]
        width = Str["displayWidth"]

        z.sleep(5)
        z.heartbeat()
        if d(text='贺卡​').exists and d(text='收件箱​').exists:  # 检测是否有邮箱登录
            d(text='贺卡​').click()
        else:
            z.toast(u"没有检测到QQ邮箱登录，模块退出。")
            return

        sendCount = 1
        if args['send_count']:
            sendCount = int(args['send_count'])

        try:
            for c in range(sendCount):  # 一个邮箱帐号发送贺卡多次

                cardIndex = random.randint(0, 2)  # 随机选择一个贺卡
                swipeDirectionArr = ["left", "right"]
                CIC = 0
                while CIC < cardIndex:
                    if CIC == 0:
                        d.swipe(width - 20, height / 2, 0, height / 2, 60)
                    else:
                        if swipeDirectionArr[random.randint(0, 1)] == "left":
                            d.swipe(width - 20, height / 2, 0, height / 2, 60)

                        if swipeDirectionArr[random.randint(0, 1)] == "right":
                            d.swipe(width - 20, height / 2, 0, height / 2, 60)
                    CIC += 1

                if d(resourceId='com.tencent.androidqqmail:id/o8').exists:  # 点击贺卡
                    d(resourceId='com.tencent.androidqqmail:id/o8').click()

                z.sleep(3)
                z.heartbeat()
                if d(resourceId='com.tencent.androidqqmail:id/l8').exists:  # 点击编辑署名
                    d(resourceId='com.tencent.androidqqmail:id/l8').click()

                    z.sleep(2)
                    delText = d(className='android.widget.EditText').info['text']  # 将之前消息框的内容删除
                    for i in range(len(delText)):
                        d.press.delete()

                    materials = self.getMaterial(args["repo_material_sign_id"], args["sign_material_time_limit"], 1)  # 去仓库获取主题内容
                    material = materials[0]['content']
                    z.input(material)

                    if d(resourceId='com.tencent.androidqqmail:id/a_').exists:  # 点击完成
                        d(resourceId='com.tencent.androidqqmail:id/a_').click()

                if d(className='android.widget.ImageView', index=0).exists:  # 点击发送贺卡进入发送页面
                    d(className='android.widget.ImageView', index=0).click()

                z.sleep(3)
                if d(resourceId='com.tencent.androidqqmail:id/nc').exists:  # 点击输入发送人
                    d(resourceId='com.tencent.androidqqmail:id/nc').click()

                sendPeCount = 1
                if args['send_num_of_pe']:
                    sendPeCount = int(args['send_num_of_pe'])

                numbers = []
                while len(numbers) == 0:
                    numbers = self.repo.GetNumber(args["repo_number_id"], args["number_time_limit"], sendPeCount)  # 去仓库获取号码
                    if len(numbers) == 0:
                        z.toast(u"号码库为空")
                        z.sleep(30)

                for s in range(len(numbers)):  # 发送给多少人
                    number = numbers[s]['number']
                    z.input(number)
                    d(resourceId='com.tencent.androidqqmail:id/px').click()
                    d(resourceId='com.tencent.androidqqmail:id/nc').click()

                if d(resourceId='com.tencent.androidqqmail:id/px').exists:  # 主题设置
                    d(resourceId='com.tencent.androidqqmail:id/px').click()
                    deltext = d(resourceId='com.tencent.androidqqmail:id/px').info['text']  # 将之前消息框的内容删除
                    for i in range(len(deltext)):
                        d.press.delete()

                materials = self.getMaterial(args["repo_material_themes_id"], args["them_material_time_limit"], 1)  # 去仓库获取主题内容
                material = materials[0]['content']
                z.input(material)

                if d(resourceId='com.tencent.androidqqmail:id/a_').exists:  # 点击发送按钮
                    d(resourceId='com.tencent.androidqqmail:id/a_').click()

                if args["time_delay"]:
                    z.sleep(int(args["time_delay"]))
                    z.heartbeat()
        except:
            logging.exception("exception")
            z.toast(u"程序中出现异常，模块退出")
            d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
            return



def getPluginClass():
    return QQMailSendGreetingCards

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("25424f9")
    z = ZDevice("25424f9")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "44", "repo_material_themes_id": "52", "repo_material_sign_id": "100", "number_time_limit": "120",
            "them_material_time_limit": "0", "sign_material_time_limit": "0", "send_count": "3", "send_num_of_pe": "2", "time_delay": "15"};
    o.action(d, z, args)

    # Str = d.info  # 获取屏幕大小等信息
    # height = Str["displayHeight"]
    # width = Str["displayWidth"]
    #
    # cardIndex = random.randint( 0, 2 )  # 随机选择一个贺卡
    # swipeDirectionArr = ["left", "right"]
    # CIC = 0
    # while CIC < cardIndex:
    #     if CIC == 0:
    #         d.swipe( width - 20, height / 2, 0, height / 2, 60 )
    #     else:
    #         directionIndex = random.randint( 0, 1 )
    #         swipeDirection = swipeDirectionArr[directionIndex]
    #         if swipeDirection == "left":
    #             d.swipe( 0, height / 2, width - 20, height / 2, 60 )
    #         if swipeDirection == "right":
    #             d.swipe( width - 20, height / 2, 0, height / 2, 60 )
    #     CIC += 1

    # slot = Slot(d.server.adb.device_serial(),'qqmail')
    # slot.clear(2)
    # d.server.adb.cmd( "shell", "pm clear com.tencent.androidqqmail" ).communicate( )  # 清除缓存
    # slot.restore( 1 )
    # d.server.adb.cmd( "shell",
    #                   "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱

