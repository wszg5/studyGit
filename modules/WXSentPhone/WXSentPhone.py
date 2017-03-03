# coding:utf-8
from uiautomator import Device
from Repo import *
from zservice import ZDevice
from XunMa import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WXSentPhone:

    def __init__(self):
        self.repo = Repo()
        self.xuma = None
    def action(self, d,z, args):
        self.xuma = XunMa(d.server.adb.device_serial())

        add_count = int(args['add_count'])
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()  # 将微信拉起来
        time.sleep(5)

        d(description='更多功能按钮',className='android.widget.RelativeLayout').click()
        time.sleep(1)
        if d(text='添加朋友').exists:
            d(text='添加朋友').click()
        else:
            d(description='更多功能按钮', className='android.widget.RelativeLayout').click()
            time.sleep(1)
            d(text='添加朋友').click()
        d(index='1',className='android.widget.TextView').click()   #点击搜索好友的输入框
        account = 0
        while True:
            if account<add_count:
                PhoneNumber = self.xuma.GetPhoneNumber('2251')
                print(PhoneNumber)
                d(text='搜索').click()
                z.input(PhoneNumber)
                d(textContains='搜索:').click()
                time.sleep(1)
                if d(textContains='状态异常').exists:
                    print('没用')
                    d(descriptionContains='清除').click()
                    continue
                time.sleep(0.5)
                if d(text='添加到通讯录').exists:
                    d(description='返回').click()
                    d(descriptionContains='清除').click()
                    continue
                if d(textContains='过于频繁').exists:
                    break
                SetCateId = args['repo_number_id']
                if not d(textContains='用户不存在'):

                    d(descriptionContains='清除').click()
                    continue
                self.repo.uploadPhoneNumber(PhoneNumber,SetCateId)    #将有用的号传到库里
                # cache.addSet('wxPhone',PhoneNumber)                     #将有用的号码保存到缓存
                # print(cache.popSet('wxPhone'))
                self.xuma.defriendPhoneNumber(PhoneNumber,'2251')       #将有用的号码拉黑
                d(descriptionContains='清除').click()
                account = account+1
                print('已到仓库')
            else:
                break

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXSentPhone

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()

    args = {"repo_number_id": "105","add_count": "100","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
