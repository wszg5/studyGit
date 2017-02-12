# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WeiXinAddFriends:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        add_count = int(args['add_count'])

        cate_id = args["repo_material_cate_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        wait = 1  # 判断素材仓库里是否由素材
        while wait == 1:
            try:
                material = Material[0]['content']  # 取出验证消息的内容
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id).communicate()
                time.sleep(20)

        cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            numbers = self.repo.GetNumber(cate_id, 120, add_count)  # 取出add_count条两小时内没有用过的号码
            lenth = len(numbers)
            if "Error" in numbers:  #
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"第%s号号码仓库为空，等待中……\"" % cate_id).communicate()
                time.sleep(20)
                continue
            if lenth == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"第%s号号码仓库为空，等待中……\"" % cate_id).communicate()
                time.sleep(20)
                continue
            wait = 0

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)

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
        for i in range(0,add_count,+1):
            print(i)
            d(text='搜索').set_text(list[i])       #ccnn527xj  list[i]
            d(textContains='搜索:').click()
            if d(textContains='操作过于频繁').exists:
                return
            time.sleep(2)
            if d(textContains='用户不存在').exists:
                d(descriptionContains='清除',index=2).click()
                time.sleep(1)
                continue
            gender = args['gender']
            if gender!='不限':
                obj = d(className='android.widget.ImageView', index=1, resourceId='com.tencent.mm:id/abr')  # 看性别是否有显示
                if obj.exists:
                    Gender = obj.info
                    Gender = Gender['contentDescription']
                    print(Gender)
                    if Gender==gender:     #看性别是否满足条件
                        print()
                    else:
                        d(description='返回').click()
                        d(descriptionContains='清除', index=2).click()
                        continue
                else:
                    d(description='返回').click()
                    d(descriptionContains='清除', index=2).click()
                    continue

            if d(text='添加到通讯录').exists:      #存在联系人的情况
                d(text='添加到通讯录').click()
                obj = d(className='android.widget.EditText',index=1).info  # 将之前消息框的内容删除
                obj = obj['text']
                lenth = len(obj)
                t = 0
                while t < lenth:
                    d.press.delete()
                    t = t + 1
                d(className='android.widget.EditText', index=1).click()
                z.input(material)
                d(text='发送').click()
                d(descriptionContains='返回').click()
                d(descriptionContains='清除', index=2).click()
                time.sleep(1)
                continue
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WeiXinAddFriends

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()


    args = {"repo_number_cate_id": "40", "repo_material_cate_id": "36", "add_count": "20", 'gender':"不限","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
