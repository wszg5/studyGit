# coding:utf-8
from XunMa import *
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class MobilqqAddByAddressListII:

    def __init__(self):
        self.repo = Repo()
        self.xuma = None

    def Bind(self, d):
        self.xuma = XunMa(d.server.adb.device_serial())
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.xuma.GetPhoneNumber('2113')
            print(GetBindNumber)
            time.sleep(2)
            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(
                GetBindNumber)  # GetBindNumber

            time.sleep(1)
            d(text='下一步').click()
            time.sleep(3)
            if d(text='下一步', resourceId='com.tencent.mobileqq:id/name', index=2).exists:  # 操作过于频繁的情况
                return 'false'

            if d(text='确定', resourceId='com.tencent.mobileqq:id/name',
                 index='2').exists:  # 提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d(text='确定', resourceId='com.tencent.mobileqq:id/name', index='2').click()

            code = self.xuma.GetVertifyCode(GetBindNumber, '2113', '4')
            newStart = 0

            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(code)
            d(text='完成', resourceId='com.tencent.mobileqq:id/name').click()
            time.sleep(5)
            if d(textContains='没有可匹配的').exists:
                return 'false'

        return 'true'

    def action(self, d,z, args):

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(6)

        if not d(text='消息', resourceId='com.tencent.mobileqq:id/name').exists:  # 到了通讯录这步后看号有没有被冻结
            return 2
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
            d(text='关闭').click()
            time.sleep(1)
        if d(text='主题装扮').exists:
            d(text='关闭').click()
        if d(text='马上绑定').exists:
            d(text='关闭').click()
        if d(text='通讯录').exists:
            d(text='关闭').click()
        d(description='快捷入口').click()
        d(textContains='加好友').click()
        d(text='添加手机联系人').click()
        time.sleep(3)
        if d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',index=2).exists:  # 检查到尚未 启用通讯录
            if d(text=' +null', resourceId='com.tencent.mobileqq:id/name').exists:
                d(text=' +null', resourceId='com.tencent.mobileqq:id/name').click()
                d(text='中国', resourceId='com.tencent.mobileqq:id/name').click()
            text = self.Bind(d)  # 未开启通讯录的，现绑定通讯录
            if text == 'false':  # 操作过于频繁的情况
                return
            time.sleep(7)
        if d(textContains='没有可匹配的').exists:
            return
        if d(text='匹配手机通讯录', resourceId='com.tencent.mobileqq:id/name').exists:
            d(text='匹配手机通讯录', resourceId='com.tencent.mobileqq:id/name').click()
            time.sleep(10)
        while True:
            if d(text='#').exists:
                for m in range(0,12,+1):     #快速加好友从#号下面的
                    obj = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',
                                                                          index=m).child(className='android.widget.TextView')
                    if not obj.exists:
                        continue
                    else:
                        obj = obj.info
                    if obj['text']=='#':
                        break
                    else:
                        m = m+1
                        continue

                break
            else:         #当前页没有找到＃时滑页
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)

        cate_id = args['repo_number_id']
        set1 = set()
        i = m+1
        t = 0
        bbb = 0

        while True :
            obj = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i)  #滑动的条件判断第i个人是否存在
            if obj.exists:
                obj1 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=i)\
                    .child(className='android.widget.LinearLayout').child(className='android.widget.TextView',textStartsWith='1')     #第i个内容存在并且是人的情况
                if obj1.exists:
                    obj1 = obj1.info
                    phone = obj1['text']
                    if phone in set1:
                        i = i+1
                        continue
                    else:
                        set1.add(phone)
                        self.repo.uploadPhoneNumber(phone,cate_id)
                        time.sleep(0.2)
                        bbb = bbb+1
                        print(bbb)
                        print(phone)
                else:
                    i = i+1
                    continue
            else:
                d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                time.sleep(2)
                obj2 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=i-1) \
                    .child(className='android.widget.LinearLayout').child(
                    className='android.widget.TextView',textStartsWith='1')  # 结束条件
                if obj2.exists:
                    obj2 = obj2.info
                else:
                    obj2 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i - 2) \
                        .child(className='android.widget.LinearLayout').child(
                        className='android.widget.TextView',textStartsWith='1').info  # 结束条件
                EndPhone = obj2['text']
                if EndPhone in set1:
                    break
                i = 1
                continue

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqAddByAddressListII

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


    args = {"repo_number_id": "106","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)

