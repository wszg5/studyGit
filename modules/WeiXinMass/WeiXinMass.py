# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WeiXinMass:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(4)
        cate_id = args["repo_material_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        if len(Material) == 0:
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
            z.sleep(10)
            return
        message = Material[0]['content']  # 取出验证消息的内容
        z.heartbeat()
        z.sleep(2)
        d(text='我').click()
        d(text='设置').click()
        d(text='通用').click()
        d(text='功能').click()
        d(text='群发助手').click()
        d(text='开始群发').click()
        if d(text='新建群发').exists:
            d(text='新建群发').click()
        elif d(text='新建群发').exists:
            d(text='新建群发').click()
        d(text='搜索').click()
        gender = args['gender']
        z.heartbeat()
        label = 'A'
        if gender !='不限':
            for i in range(0,26,+1):
                z.heartbeat()
                if gender == '男':
                    z.input(label+gender)
                    if d(textContains='没有找到').exists:
                        return
                    f = ord(label)
                    f = f + 1
                    label = chr(f)
                elif gender =='女':
                    z.input(label + gender)
                    if d(textContains='没有找到').exists:
                        return
                    f = ord(label)
                    f = f + 1
                    label = chr(f)
                z.heartbeat()
                d(text='全选').click()
                d(textContains='下一步').click()
                d(className='android.widget.EditText').click()
                z.input(message)
                d(text='发送').click()
                d(text='新建群发').click()
                d(text='搜索').click()
                continue
        else:
            for i in range(0, 26, +1):
                z.heartbeat()
                z.input(label + '女')
                if d(textContains='没有找到').exists:  # 没有找到的情况发男性
                    d(description='返回').click()
                    d(text='新建群发').click()
                    d(text='搜索').click()
                    break
                z.heartbeat()
                f = ord(label)
                f = f + 1
                label = chr(f)
                d(text='全选').click()
                d(textContains='下一步').click()
                d(className='android.widget.EditText').click()
                z.input(message)
                d(text='发送').click()
                d(text='新建群发').click()
                d(text='搜索').click()
                continue
            label = 'A'
            for i in range(0, 26, +1):
                z.heartbeat()
                z.input(label + '男')
                if d(textContains='没有找到').exists:  # 没有找到的情况发男性
                    d(description='返回').click()
                    d(text='新建群发').click()
                    d(text='搜索').click()
                    break
                f = ord(label)
                f = f + 1
                label = chr(f)
                d(text='全选').click()
                d(textContains='下一步').click()
                d(className='android.widget.EditText').click()
                z.input(message)
                d(text='发送').click()
                d(text='新建群发').click()
                d(text='搜索').click()
                continue
            label = 'A'
            for i in range(0, 26, +1):
                z.heartbeat()
                z.input(label + '妖')
                if d(textContains='没有找到').exists:  # 没有找到的情况发男性
                    return
                f = ord(label)
                f = f + 1
                label = chr(f)
                d(text='全选').click()
                d(textContains='下一步').click()
                d(className='android.widget.EditText').click()
                z.input(message)
                d(text='发送').click()
                d(text='新建群发').click()
                d(text='搜索').click()
                continue


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return WeiXinMass

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


    args = {"repo_material_id": "39","time_delay":"3",'gender':"不限",}    #cate_id是仓库号，length是数量
    o.action(d,z, args)






