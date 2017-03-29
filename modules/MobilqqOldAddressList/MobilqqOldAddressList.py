# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
from smsCode import smsCode



class MobilqqOldAddressList:
    def __init__(self):
        self.repo = Repo()


    def Bind(self,d,z):
        self.scode = smsCode(d.server.adb.device_serial())
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.scode.GetPhoneNumber(self.scode.QQ_CONTACT_BIND)
            print(GetBindNumber)
            z.sleep(2)
            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(GetBindNumber)  #GetBindNumber
            z.heartbeat()
            z.sleep(2)
            d(text='下一步').click()
            z.sleep(3)
            if d(textContains='中国').exists:       #操作过于频繁的情况
                return 'false'

            if d(text='确定').exists:     #提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d(text='确定',).click()
                z.sleep(1)
                if d(text='确定').exists:
                    z.toast('请求失败，结束程序')
                    return 'false'
            z.heartbeat()
            code = self.scode.GetVertifyCode(GetBindNumber, self.scode.QQ_CONTACT_BIND, '4')
            newStart = 0
            d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText').set_text(code)
            z.heartbeat()
            d(text='下一步').click()
            z.sleep(2)
            if d(textContains='匹配手机通讯录').exists:
                d(text='好').click()
                time.sleep(10)
            self.scode.defriendPhoneNumber(GetBindNumber,self.scode.QQ_CONTACT_BIND)
            if d(textContains='匹配手机通讯录').exists:
                d(text='好').click()
                z.sleep(15)



        return 'true'

    def action(self, d,z, args):
        z.heartbeat()
        gender = args['gender']
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(9)
        if not d(text='搜索').exists:                    #到了通讯录这步后看号有没有被冻结
            return 2
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
            d(text='关闭').click()
            z.sleep(1)
        if d(text='匹配手机通讯录').exists:
            d(text='匹配手机通讯录').click()
        while d(textContains='正在发送').exists:
            time.sleep(2)
        time.sleep(4)
        d(className='android.widget.TabWidget').child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.ImageView',index=2).click()     #点击到联系人
        z.sleep(1)
        z.heartbeat()
        closecheck = d(className='android.view.View').child(className='android.widget.RelativeLayout',index=3).child(checked='true')
        if closecheck.exists:
            closecheck.click()
        if d(text='马上升级').exists:
            d(description='取消').click()
        closecheck = d(className='android.view.View').child(className='android.widget.FrameLayout', index=5).child(className='android.widget.ImageView')
        time.sleep(0.5)
        if not closecheck.exists:  # 通讯录下面没有好友的情况
            d(className='android.view.View').child(className='android.widget.RelativeLayout', index=4).click()    #点击展开
            time.sleep(0.5)
            if d(textContains='匹配手机通讯录').exists:
                d(text='好').click()
                z.sleep(3)
                d(className='android.view.View').child(className='android.widget.RelativeLayout',index=4).click()  # 点击展开
            if d(text='查看开启方法').exists:
                return
            time.sleep(0.5)
            if d(text='启用').exists:
                d(text='启用').click()
                while d(textContains='正在发送').exists:
                    z.sleep(2)
                z.sleep(6)
                d(text='返回').click()
                if not closecheck.exists:     #点击返回后通讯录收起来的情况
                    d(className='android.view.View').child(className='android.widget.RelativeLayout', index=4).click()

            if d(textContains='下线通知').exists:
                return

            if d(text='匹配手机通讯录',index=2).exists:
                d(text='匹配手机通讯录',index=2).click()
                z.sleep(6)
                while d(textContains='正在发送').exists:
                    z.sleep(2)
                d(className='android.view.View').child(className='android.widget.RelativeLayout', index=4).click()

            if d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',index=2).exists:  # 检查到尚未启用通讯录,有输入框的情况
                if d(text=' +null', resourceId='com.tencent.mobileqq:id/name').exists:
                    d(text=' +null', resourceId='com.tencent.mobileqq:id/name').click()
                    d(text='中国', resourceId='com.tencent.mobileqq:id/name').click()
                z.heartbeat()
                text = self.Bind(d,z)  # 未开启通讯录的，现绑定通讯录
                z.heartbeat()
                if text == 'false':  # 操作过于频繁的情况
                    return
                z.sleep(7)   #------------------------------
                closecheck = d(className='android.view.View').child(className='android.widget.FrameLayout', index=5).child(className='android.widget.ImageView')
                if not closecheck.exists:  #
                    d(className='android.view.View').child(className='android.widget.RelativeLayout', index=4).click()  # 点击展开
                    z.sleep(0.5)
                    if d(text='查看开启方法').exists:
                        return
                    if d(text='启用').exists:
                        d(text='启用').click()
                        z.sleep(6)
                        d(text='返回').click()
                        if not closecheck.exists:
                            d(className='android.view.View').child(className='android.widget.RelativeLayout', index=4).click()




        set1 = set()
        i = 5
        t = 1
        EndIndex = int(args['EndIndex'])
        while t < EndIndex+1:
            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                z.sleep(10)
                return
            message = Material[0]['content']  # 取出验证消息的内容
            forclick = d(className='android.widget.FrameLayout',index=i)
            if forclick.exists:
                z.heartbeat()
                z.sleep(0.3)
                forclick.click()
                z.sleep(0.5)
                if d(className='android.widget.FrameLayout',index=i).exists:   #结束条件，滑到底的情况
                    forclick.click()
                    if forclick.exists:
                        z.toast('程序结束')
                        break
                phone = d(className='android.widget.RelativeLayout', index=1).child(className='android.widget.LinearLayout',index=1).child(className='android.widget.TextView').info['text']
                if phone in set1:
                    d(text='返回').click()
                    i = i+1
                    continue
                set1.add(phone)
                if gender!='不限':
                    getgender = d(className='android.widget.RelativeLayout', index=1).child(className='android.widget.TextView',index=2)
                    if getgender.exists:
                        getgender = getgender.info['text']
                        if gender not in getgender:
                            i = i+1
                            d(text='返回').click()
                            continue
                    else:
                        i = i+1
                        d(text='返回').click()
                        continue
                d(text='发消息').click()
                time.sleep(0.5)
                if d(description='收起语音面板').exists:
                    d(text='文字输入').click()
                print(message)
                z.input(message)
                z.heartbeat()
                time.sleep(0.4)
                d(text='发送').click()
                i = i + 1
                t = t + 1
                while d(className='android.widget.ProgressBar').exists:
                    z.sleep(1)
                if d(description='重新发送').exists:
                   return
                d(textContains='消息').click()
                d(className='android.widget.TabWidget').child(className='android.widget.RelativeLayout', index=1).child(
                    className='android.widget.ImageView', index=2).click()  # 点击到联系人
            else:
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                i = 2
                continue


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqOldAddressList

if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_id":"100",'gender':"女",'EndIndex':'40',"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)
