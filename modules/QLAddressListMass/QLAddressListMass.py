# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from RClient import *
from PIL import Image

class QLJudgeQQBind:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        str = d.info  # 获取屏幕大小等信息
        width = str["displayWidth"]
        height = str["displayHeight"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.qqlite").wait()  # 将qq强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 将qq拉起来
        time.sleep(8)
        d(text='联系人').click()
        d(text='通讯录').click()
        if d(text='匹配通讯录').exists:
            d(text='匹配通讯录').click()
            while not d(descriptionContains='发消息').exists:  #匹配通讯录存在延时
                time.sleep(2)

        add_count = int(args['add_count'])  # 给多少人发消息
        gender = args['gender']
        t = 0
        i = 0
        set1 = set()
        while t<add_count:
            forClick = d(className='android.view.View').child(className='android.widget.RelativeLayout',index=i).child(className='android.widget.TextView')
            if forClick.exists:
                savePhone = forClick.info
                savePhone = savePhone['text']
                if savePhone in set1:
                    i = i+1
                    continue
                set1.add(savePhone)
                forClick.click()
                if gender!='不限':
                    if not d(textContains=gender).exists:
                        i = i+1
                        continue
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
                # d(text='发送').click()
                d(description='向上导航').click()
                d(description='向上导航').click()
                i = i+1
                t = t+1
            else:
                if d(text='未启用通讯录的联系人').exists:    #到达未启用的那个人结束发消息
                    break
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 6)
                time.sleep(2)
                endcondition = d(className='android.view.View').child(className='android.widget.RelativeLayout', index=i-1).child(
                    className='android.widget.TextView').info
                endcondition = endcondition['text']
                if endcondition in set1:
                    break
                i = 0






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
    args = {"repo_material_id":"39",'gender':"女",'add_count':'20',"time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)




















