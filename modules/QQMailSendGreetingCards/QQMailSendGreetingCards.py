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
    
    def input(self,z,height,text):
        if height>888:
            z.input(text)
        else:
            z.cmd( "shell", "am broadcast -a ZY_INPUT_TEXT --es text \\\"%s\\\"" % text )

    def action(self, d, z, args):
        # z.toast(u"正在ping网络是否通畅")
        # i = 0
        # while i < 200:
        #     i += 1
        #     ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
        #     print(ping)
        #     if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
        #         z.toast(u"网络通畅。开始执行：QQ邮箱发送贺卡")
        #         break
        #     z.sleep(2)
        # if i > 200:
        #     z.toast(u"网络不通，请检查网络状态")
        #     return

        z.heartbeat()
        d.server.adb.cmd("shell", "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail").communicate()  # 拉起QQ邮箱

        Str = d.info  # 获取屏幕大小等信息
        height = int(Str["displayHeight"])
        width = int(Str["displayWidth"])
        #
        # z.sleep(5)
        # z.heartbeat()


        for t in range(2):
            d.dump( compressed=False )
            if d( text="收件箱​",className="android.widget.TextView" ).exists:
                if d(textContains="密码错误，请重新输入").exists:
                    z.toast("密码错误，请重新输入")
                    return
                else:
                    z.toast( "状态正常，继续执行" )
                    break
            else:
                if d( text="温馨提示​", className="android.widget.TextView" ).exists:
                    d( text="确定", className="android.widget.Button" ).click( )
                    z.sleep( 1 )
                    break
                elif d(text="取消​",resourceId='com.tencent.androidqqmail:id/a5',index=0).exists:
                    d( text="取消​", resourceId='com.tencent.androidqqmail:id/a5',index=0 ).click()
                    time.sleep(1)
                    if d(text="离开",className="android.widget.Button").exists:
                        d( text="离开", className="android.widget.Button" ).click()
                        time.sleep(1)
                    if d( text="收件箱​", className="android.widget.TextView" ).exists:
                        if d( textContains="密码错误，请重新输入" ).exists:
                            z.toast( "密码错误，请重新输入" )
                            return
                        else:
                            z.toast( "状态正常，继续执行" )
                            break
                elif d(text="收件人：").exists and d(text="写邮件").exists:
                    flag1 = True
                    break
                elif d(index=1,text="写邮件​",className="android.widget.TextView").exists:
                    d.click(60/720 * width,198/1280 * height)
                    flag1 = True
                    break
                else:
                    if t>=1:
                        z.toast( "状态异常，跳过此模块" )
                        return
                    else:
                        d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
                        d.server.adb.cmd( "shell",
                                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        time.sleep( 5 )
        if d(text='贺卡​').exists and d(text='收件箱​').exists:  # 检测是否有邮箱登录
            if d( textContains="密码错误，请重新输入" ).exists:
                z.toast( "密码错误，请重新输入" )
                return
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

                z.sleep(2)
                z.heartbeat()
                nameFlag = args["nameFlag"]
                if nameFlag=="署名":
                    if d(resourceId='com.tencent.androidqqmail:id/l8').exists:  # 点击编辑署名
                        d(resourceId='com.tencent.androidqqmail:id/l8').click()

                        z.sleep(2)
                        delText = d(className='android.widget.EditText').info['text']  # 将之前消息框的内容删除
                        for i in range(len(delText)):
                            d.press.delete()

                        materials = self.getMaterial(args["repo_material_sign_id"], 0, 1)  # 去仓库获取主题内容
                        material = materials[0]['content']
                        self.input(z,height,material)

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
                if sendPeCount>0:
                    while len(numbers) == 0:
                        numbers = self.repo.GetNumber(args["repo_number_id"], 0, sendPeCount)  # 去仓库获取号码
                        if len(numbers) == 0:
                            if args["nuberLoop"] == "循环":
                                self.repo.UpdateNumberStauts( "", args["repo_number_id"], "normal" )
                                numbers = self.repo.GetNumber( args["repo_number_id"], 120, sendCount )
                                if len( numbers ) == 0:
                                    z.toast( "%s号仓库没有号码" % args["repo_number_id"] )
                                    return
                            else:
                                d.server.adb.cmd( "shell","am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % args["repo_number_id"] ).communicate( )
                                z.sleep( 10 )
                                return

                for s in range(len(numbers)):  # 发送给多少人
                    number = numbers[s]['number']
                    self.input(z,height,number+" ")
                    # d(resourceId='com.tencent.androidqqmail:id/px').click()
                    # d(resourceId='com.tencent.androidqqmail:id/nc').click()
                themeFlag = args["themeFlag"]
                if themeFlag=="是":
                    if d(resourceId='com.tencent.androidqqmail:id/px').exists:  # 主题设置
                        d(resourceId='com.tencent.androidqqmail:id/px').click()
                        deltext = d(resourceId='com.tencent.androidqqmail:id/px').info['text']  # 将之前消息框的内容删除
                        for i in range(len(deltext)):
                            d.press.delete()

                    materials = self.getMaterial(args["repo_material_themes_id"], 0, 1)  # 去仓库获取主题内容
                    material = materials[0]['content']
                    self.input(z,height,material)

                if d(resourceId='com.tencent.androidqqmail:id/a_').exists:  # 点击发送按钮
                    d(resourceId='com.tencent.androidqqmail:id/a_').click()
                    # time.sleep(3)
                if c < sendCount-1:
                    if args["time_delay"]:
                        z.sleep(int(args["time_delay"]))
                        z.heartbeat()

            d.server.adb.cmd( "shell",
                              "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
            time.sleep(1)
            if d( text="收件箱​", className="android.widget.TextView" ).exists:
                d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
                time.sleep(2)
            elif d( text="群邮件​", resourceId="com.tencent.androidqqmail:id/t0" ).exists:
                pass
            else:
                return
            if not d(text="待发送​").exists:
                return

            if d(descriptionContains="待发送有").exists and d(descriptionContains="封未读的邮件").exists:
                obj = d(descriptionContains="待发送有")
                if obj.exists:
                    text = obj.info['contentDescription']
                    num = text.split("待发送有")[1].split("封未读的邮件")[0]
                    failCount = int(args["failCount"])
                    if int(num)>=failCount:
                        z.toast("有%s个待发送,跳出模块"%num)
                        accountObj = d( resourceId="com.tencent.androidqqmail:id/ac", textContains="@",
                                        className="android.widget.TextView" )
                        account = accountObj.info["text"]
                        if "@qq.com" in account or "@163.com" in account:
                            account = account.split("@")[0]
                        self.repo.BackupInfo( args["account_cateId"], 'exception', account, '' , '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                return
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
    d = Device("9cae944e")
    z = ZDevice("9cae944e")
    # Str = d.info  # 获取屏幕大小等信息
    # height = Str["displayHeight"]
    # width = Str["displayWidth"]
    # o.input(z,height,"fdsfs发的三分1345")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "44", "repo_material_themes_id": "52", "repo_material_sign_id": "100",
         "send_count": "3", "send_num_of_pe": "5", "time_delay": "3","nameFlag":"署名","themeFlag":"否","account_cateId":"358","failCount":"4","nuberLoop":"循环"}
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

