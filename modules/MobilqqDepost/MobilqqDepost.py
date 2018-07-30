# coding:utf-8


from smsCode import smsCode
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class MobilqqDepost:

    def __init__(self):
        self.repo = Repo()
        self.xuma = None

    def Bind(self, d,z):
        self.scode = smsCode(d.server.adb.device_serial())
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.scode.GetPhoneNumber(self.scode.QQ_CONTACT_BIND)
            print(GetBindNumber)
            z.sleep(2)
            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(
                GetBindNumber)  # GetBindNumber
            z.heartbeat()
            z.sleep(1)
            d(text='下一步').click()
            z.sleep(3)
            if d(text='下一步', resourceId='com.tencent.mobileqq:id/name', index=2).exists:  # 操作过于频繁的情况
                return 'false'

            if d(text='确定', resourceId='com.tencent.mobileqq:id/name',
                 index='2').exists:  # 提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d(text='确定', resourceId='com.tencent.mobileqq:id/name', index='2').click()

            code = self.scode.GetVertifyCode(GetBindNumber, self.scode.QQ_CONTACT_BIND, '4')
            newStart = 0

            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(code)
            z.heartbeat()
            d(text='完成', resourceId='com.tencent.mobileqq:id/name').click()
            z.sleep(5)
            if d(text='确定').exists:
                d(text='确定').click()

            while d(text='允许').exists:
                d(text='允许').click()
                z.sleep(5)

            if d(textContains='没有可匹配的').exists:
                return 'false'

        return 'true'

    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(6)
        z.heartbeat()
        if not d(text='消息', resourceId='com.tencent.mobileqq:id/name').exists:  # 到了通讯录这步后看号有没有被冻结
            return 2
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
            d(text='关闭').click()
            z.sleep(1)
        if d(text='主题装扮').exists:
            d(text='关闭').click()
        if d(text='马上绑定').exists:
            d(text='关闭').click()
        if d(text='通讯录').exists:
            d(text='关闭').click()
        d(description='快捷入口').click()
        d(textContains='加好友').click()
        d(text='添加手机联系人').click()

        z.sleep(3)
        if d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',index=2).exists:  # 检查到尚未 启用通讯录
            if d(text=' +null', resourceId='com.tencent.mobileqq:id/name').exists:
                d(text=' +null', resourceId='com.tencent.mobileqq:id/name').click()
                d(text='中国大陆', resourceId='com.tencent.mobileqq:id/name').click()
            z.heartbeat()
            text = self.Bind(d,z)  # 未开启通讯录的，现绑定通讯录
            z.heartbeat()
            if text == 'false':  # 操作过于频繁的情况
                return
            z.sleep(int(args['time_delay1']))

        z.heartbeat()
        if d(textContains='没有可匹配的').exists:
            return
        if d(text='匹配手机通讯录', resourceId='com.tencent.mobileqq:id/name').exists:
            d(text='匹配手机通讯录', resourceId='com.tencent.mobileqq:id/name').click()
            z.sleep(10)

        nickArr = []
        judge = 0
        g = 8
        while True:
            for i in range(0, g):
                z.heartbeat()
                obj = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=i).child(
                    className='android.widget.RelativeLayout', index=0).child(className='android.widget.LinearLayout', index=1).child(
                    resourceId='com.tencent.mobileqq:id/nickname')  #滑动的条件判断第i个人是否存在
                if obj.exists:
                    z.heartbeat()
                    nick = obj.info['text']
                    if nick in nickArr:
                        continue
                    else:
                        z.heartbeat()
                        nickArr.append(nick)
                        obj.click()

                        note = ''
                        nick = ''
                        gender = ''
                        age = ''
                        area = ''
                        number = ''

                        noteObj = d(resourceId='com.tencent.mobileqq:id/common_xlistview').child(className='android.widget.LinearLayout', index=0).child(
                            className='android.widget.LinearLayout', index=6).child(className='android.widget.TextView', resourceId='com.tencent.mobileqq:id/name', index=0
                                                                                    )
                        if noteObj.exists:
                            note = noteObj.info['text']

                        infoObj = d(resourceId='com.tencent.mobileqq:id/common_xlistview').child(className='android.widget.LinearLayout', index=1).child(
                            className='android.widget.LinearLayout', resourceId='com.tencent.mobileqq:id/name').child(className='android.widget.LinearLayout', index=0)

                        if infoObj.exists:
                            nick = infoObj.child(className='android.widget.LinearLayout', index=0).child(resourceId='com.tencent.mobileqq:id/info').info['text']

                            numberObj = infoObj.child(className='android.widget.LinearLayout', index=2).child(resourceId='com.tencent.mobileqq:id/info')
                            infoStr = infoObj.child(className='android.widget.LinearLayout', index=1).child(resourceId='com.tencent.mobileqq:id/info')
                            if numberObj.exists:
                                infoArr = infoStr.info['text'].split("  ")
                                gender = infoArr[0]
                                if len(infoArr) == 2:
                                    age = infoArr[1]
                                if len(infoArr) == 3:
                                    age = infoArr[1]
                                    area = infoArr[2]

                                number = numberObj.info['text'][3:len(numberObj.info['text'])]
                            else:
                                number = infoStr.info['text'][3:len(infoStr.info['text'])]

                        para = {"phoneNumber": number, 'x_01': gender, 'x_02': age, 'x_03': area, 'x_04': nick, 'x_05': note}
                        self.repo.PostInformation(args['repo_cate_id'], para)

                        if d(resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft').exists:
                            d(resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft').click()

                        time.sleep(1)
                        z.heartbeat()

            if len(nickArr) > judge:
                judge = len(nickArr)
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 6)
            else:
                if g == 8:
                    g = 12
                else:
                    break

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqDepost

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("465b4e4b")
    z = ZDevice("465b4e4b")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()


    args = {"repo_cate_id": "349", "time_delay1": "1", "time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)


    pass
