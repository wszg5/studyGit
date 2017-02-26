# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class EIMAddFrendRouseI:
    def __init__(self):
        self.repo = Repo()




    def action(self, d,z, args):

        totalNumber = int(args['totalNumber'])  # 要给多少人发消息
        cate_id = int(args["repo_number_id"])  # 得到取号码的仓库号
        numbers = self.repo.GetNumber(cate_id, 0, totalNumber)  # 取出totalNumber条两小时内没有用过的号码
        print(len(numbers))
        if len(numbers)==0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码%s号仓库为空，等待中\""%cate_id).communicate()
            time.sleep(20)
            return
        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)
        time.sleep(15)

        for i in range (0,totalNumber,+1):
            cate_id = args["repo_material_cate_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material)==0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                time.sleep(10)
                return
            material = Material[0]['content']
            numbers = list[i]['number']
            time.sleep(1)

            d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"'%numbers )  # qq名片页面
            time.sleep(2)

            if d(text='企业QQ').exists:
                d(text='企业QQ').click()
                time.sleep(0.5)
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()

            d(text='加好友', resourceId='com.tencent.eim:id/txt').click()
            time.sleep(1)
            if d(text='加好友', resourceId='com.tencent.eim:id/txt').exists:  # 拒绝被添加的情况

                continue
            time.sleep(2)
            if d(text='必填', resourceId='com.tencent.eim:id/name').exists:
                continue

            obj = d(className='android.widget.EditText').info  # 删除之前文本框的验证消息
            obj = obj['text']
            lenth = len(obj)
            t = 0
            while t < lenth:
                d.press.delete()
                t = t + 1
            time.sleep(1)
            z.input(material)
            d(text='下一步', resourceId='com.tencent.eim:id/ivTitleBtnRightText').click()
            d(text='发送', resourceId='com.tencent.eim:id/ivTitleBtnRightText').click()



        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return EIMAddFrendRouseI

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").wait()
    z.server.install()
    z.server.start()

    args = {"repo_number_id":"119","repo_material_cate_id":"39","totalNumber":"5","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

