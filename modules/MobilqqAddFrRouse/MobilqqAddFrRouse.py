# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MobilqqAddFrRouse:
    def __init__(self):
        self.repo = Repo()




    def action(self, d,z,args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(6)
        cate_id = args["repo_material_cate_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        try:
            material = Material[0]['content']  # 取出验证消息的内容
        except Exception:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id).communicate()

        add_count = int(args['add_count'])  # 要添加多少人

        repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            numbers = self.repo.GetNumber(repo_number_cate_id, 120, add_count)  # 取出add_count条两小时内没有用过的号码
            lenth = len(numbers)
            if "Error" in numbers:  #没有取到号码的时候
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"")
                continue
            elif lenth==0:
                continue
            wait = 0

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)

        for i in range (0,add_count,+1):            #总人数
            numbers = list[i]
            time.sleep(1)
            d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"'%numbers)  # qq名片页面
            time.sleep(2)
            if d(text='QQ').exists:
                d(text='QQ').click()
                time.sleep(0.5)
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()
            d(text='加好友').click()
            time.sleep(2)
            if d(text='加好友').exists:    #拒绝被添加的轻况
                continue
            if d(text='输入答案').exists:
                continue
            if d(text='填写验证信息').exists:
                obj = d(className='android.widget.EditText', resourceId='com.tencent.mobileqq:id/name').info  # 将之前消息框的内容删除
                obj = obj['text']
                lenth = len(obj)
                t = 0
                while t < lenth:
                    d.press.delete()
                    t = t + 1
                z.input(material)
            d(text='发送').click()


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqAddFrRouse

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    args = {"repo_number_cate_id":"38","repo_material_cate_id":"40","add_count":"9","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
