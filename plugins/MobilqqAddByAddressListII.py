# coding:utf-8
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class MobilqqAddByAddressListII:

    def __init__(self):
        self.repo = Repo()
        self.xuma = None
    def Bind(self, d,z):
        self.scode = smsCode(d.server.adb.device_serial())
        z.heartbeat()
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
            z.heartbeat()
            newStart = 0

            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(code)
            d(text='完成', resourceId='com.tencent.mobileqq:id/name').click()
            z.sleep(8)
            z.heartbeat()
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
        cate_id = args["repo_material_id"]  # ------------------
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        if len(Material) == 0:
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
            z.sleep(10)
            return
        message = Material[0]['content']  # 取出验证消息的内容

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
        z.heartbeat()
        if d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',index=2).exists:  # 检查到尚未 启用通讯录
            if d(text=' +null', resourceId='com.tencent.mobileqq:id/name').exists:
                d(text=' +null', resourceId='com.tencent.mobileqq:id/name').click()
                d(text='中国', resourceId='com.tencent.mobileqq:id/name').click()
            z.heartbeat()
            text = self.Bind(d,z)  # 未开启通讯录的，现绑定通讯录
            z.heartbeat()
            if text == 'false':  # 操作过于频繁的情况
                return
            z.sleep(7)
        if d(textContains='没有可匹配的').exists:
            return
        if d(text='匹配手机通讯录').exists:
            d(text='匹配手机通讯录').click()
            while not d(text='多选').exists:
                z.sleep(2)
        z.heartbeat()
        d(text='多选').click()
        while True:
            if d(text='#').exists:
                z.heartbeat()
                for m in range(0,12,+1):     #快速加好友从#号下面的
                    obj = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',
                                                                          index=m).child(className='android.widget.TextView').info
                    if obj['text']=='#':
                        break
                    else:
                        m = m+1
                        continue

                break
            else:         #当前页没有找到＃时滑页
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)
        z.heartbeat()
        set1 = set()
        i = m+1
        t = 0
        EndIndex = int(args['EndIndex'])         #------------------
        while t < EndIndex :
            obj = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i)  #滑动的条件
            if obj.exists:
                z.heartbeat()
                obj1 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=i)\
                    .child(className='android.widget.LinearLayout',index=2).child(className='android.widget.TextView')     #第i个内容存在并且是人的情况
                if obj1.exists:
                    obj1 = obj1.info
                    phone = obj1['text']
                    if phone in set1:
                        i = i+1
                        continue
                    else:
                        set1.add(phone)
                        print(phone)
                        obj5 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i)\
                            .child(className='android.widget.FrameLayout').child(text='等待验证')     #验证已经发过的情况
                        if obj5.exists:
                            z.heartbeat()
                            d(textContains='加好友').click()
                            obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
                            obj = obj['text']
                            lenth = len(obj)
                            mn = 0
                            while mn < lenth:
                                d.press.delete()
                                mn = mn + 1
                            z.input(message)
                            d(text='发送').click()
                            return
                        obj4 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i).child(className='android.widget.CheckBox')  #勾选框没被遮住的情况
                        if obj4.exists:
                            obj4.click()
                        else:
                            d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i).click()
                        i = i+1
                        t = t+1
                        continue    #--------------------------------------------
                else:

                    i = i+1
                    continue
            else:
                d.swipe(width / 2, height * 4 / 5, width / 2, height / 5)
                obj2 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout', index=i-1) \
                    .child(className='android.widget.LinearLayout', index=2).child(
                    className='android.widget.TextView')  # 结束条件
                if obj2.exists:
                    obj2 = obj2.info
                else:
                    obj2 = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i - 2) \
                        .child(className='android.widget.LinearLayout', index=2).child(
                        className='android.widget.TextView').info  # 结束条件
                EndPhone = obj2['text']
                if EndPhone in set1:
                    z.heartbeat()
                    d(textContains='加好友').click()
                    obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
                    obj = obj['text']
                    lenth = len(obj)
                    mn = 0
                    while mn < lenth:
                        d.press.delete()
                        mn = mn + 1
                    z.input(message)
                    d(text='发送').click()
                    return
                i = 1
                continue

        d(textContains='加好友').click()
        obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
        obj = obj['text']
        lenth = len(obj)
        mn = 0
        z.heartbeat()
        while mn < lenth:
            d.press.delete()
            mn = mn + 1
        z.input(message)
        d(text='发送').click()
        while d(textContains='发送').exists:
            time.sleep(2)
        time.sleep(6)
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqAddByAddressListII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AYSK00084")
    z = ZDevice("HT4AYSK00084")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id": "39",'EndIndex':'100',"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)






















