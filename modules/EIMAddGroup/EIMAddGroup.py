# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class EIMAddGroup:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):

        totalNumber = int(args['totalNumber'])  # 要给多少人发消息

        cate_id = int(args["repo_number_id"])  # 得到取号码的仓库号

        numbers = self.repo.GetNumber(cate_id, 0, totalNumber)  # 取出totalNumber条两小时内没有用过的号码
        if len(numbers)==0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\""%cate_id).communicate()
            time.sleep(10)
            return
        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)
        time.sleep(15)

        for i in range (0,totalNumber,+1):
            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                time.sleep(10)
                return
            message = Material[0]['content']

            QQnumber = list[i]['number']
            time.sleep(1)

            d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=group&source=qrcode"'%QQnumber )  # 群页面
            time.sleep(2)

            if d(text='企业QQ').exists:
                d(text='企业QQ').click()
                time.sleep(0.5)
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()

            obj = d(className='android.widget.RelativeLayout',index=5).child(className='android.widget.TextView',index=1).info
            member = obj['text']
            member = filter(lambda ch: ch in '0123456789', member)
            member = int(member)
            if member==0:
                continue
            d(text='加入该群').click()
            time.sleep(1)
            if d(text='加入该群').exists:
                continue
            obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
            obj = obj['text']
            lenth = len(obj)
            m = 0
            while m < lenth:
                d.press.delete()
                m = m + 1
            z.input(message)
            d(text='发送').click()

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return EIMAddGroup

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()

    args = {"repo_number_id":"119","repo_material_id":"39","totalNumber":"20","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

