# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WeiXinAddFriends:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        z.heartbeat()
        add_count = int(args['add_count'])

        cate_id = args["repo_material_cate_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        if len(Material) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id).communicate()
            z.sleep(10)
            return
        message = Material[0]['content']  # 取出验证消息的内容

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(5)

        d(description='更多功能按钮',className='android.widget.RelativeLayout').click()
        z.sleep(1)
        if d(text='添加朋友').exists:
            d(text='添加朋友').click()
        else:
            d(description='更多功能按钮', className='android.widget.RelativeLayout').click()
            z.sleep(1)
            d(text='添加朋友').click()
        z.heartbeat()
        d(index='1',className='android.widget.TextView').click()   #点击搜索好友的输入框
        account = 0
        while True:
            if account<add_count:
                cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
                numbers = self.repo.GetNumber(cate_id, 120, 1)  # 取出add_count条两小时内没有用过的号码
                if len(numbers) == 0:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"第%s号号码仓库为空，等待中……\"" % cate_id).communicate()
                    z.sleep(20)
                    return
                WXnumber = numbers[0]['number']
                z.input(WXnumber)
                z.heartbeat()
                d(textContains='搜索:').click()
                if d(textContains='操作过于频繁').exists:
                    return
                z.sleep(2)
                if d(textContains='用户不存在').exists:
                    d(descriptionContains='清除',index=2).click()
                    z.sleep(1)
                    continue
                if d(textContains='状态异常').exists:
                    d(descriptionContains='清除', index=2).click()
                    continue
                z.heartbeat()
                gender = args['gender']
                if gender!='不限':
                    Gender = d(className='android.widget.LinearLayout', index=1).child(
                        className='android.widget.LinearLayout', index=0) \
                        .child(className='android.widget.LinearLayout', index=0).child(
                        className='android.widget.ImageView')
                    if Gender.exists:
                        z.heartbeat()
                        Gender = Gender.info
                        Gender = Gender['contentDescription']
                        print(Gender)
                        if Gender!=gender:     #看性别是否满足条件
                            d(description='返回').click()
                            d(descriptionContains='清除').click()
                            continue
                    else:
                        d(description='返回').click()
                        d(descriptionContains='清除').click()
                        continue

                z.heartbeat()
                if d(text='添加到通讯录').exists:      #存在联系人的情况
                    d(text='添加到通讯录').click()
                    obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
                    obj = obj['text']
                    lenth = len(obj)
                    t = 0
                    while t < lenth:
                        d.press.delete()
                        t = t + 1
                    d(className='android.widget.EditText').click()
                    z.input(message)
                    d(text='发送').click()
                    z.heartbeat()
                    d(descriptionContains='返回').click()
                    d(descriptionContains='清除').click()
                    z.sleep(1)
                    account = account+1
                    continue
            else:
                break
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WeiXinAddFriends

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_cate_id": "44", "repo_material_cate_id": "39", "add_count": "3", 'gender':"女","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
