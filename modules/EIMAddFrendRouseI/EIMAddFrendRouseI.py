# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice


class EIMAddFrendRouseI:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        totalNumber = int(args['totalNumber'])  # 要给多少人发消息
        cate_id = int(args["repo_number_id"])  # 得到取号码的仓库号
        numbers = self.repo.GetNumber(cate_id, 0, totalNumber)  # 取出totalNumber条两小时内没有用过的号码
        if len(numbers)==0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码%s号仓库为空，等待中\""%cate_id).communicate()
            z.sleep(20)
            return
        list = numbers  # 将取出的号码保存到一个新的集合
        z.sleep(15)
        z.heartbeat()
        for i in range (0,totalNumber,+1):
            cate_id = args["repo_material_cate_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material)==0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                z.sleep(10)
                return
            message = Material[0]['content']
            QQnumber = list[i]['number']
            z.sleep(1)
            z.heartbeat()
            d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"'%QQnumber )  # qq名片页面
            z.sleep(2)

            if d(text='企业QQ').exists:
                d(text='企业QQ').click()
                z.sleep(0.5)
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()

            d(text='加好友').click()
            z.sleep(1)
            if d(text='加好友').exists:  # 拒绝被添加的情况

                continue
            z.sleep(2)
            if d(text='必填').exists:
                continue
            z.heartbeat()
            obj = d(className='android.widget.EditText').info  # 删除之前文本框的验证消息
            obj = obj['text']
            lenth = len(obj)
            t = 0
            while t < lenth:
                d.press.delete()
                t = t + 1
            z.sleep(1)
            z.input(message)
            d(text='下一步').click()
            d(text='发送').click()
            z.heartbeat()

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return EIMAddFrendRouseI

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").communicate()
    z.server.install()
    z.server.start()

    args = {"repo_number_id":"119","repo_material_cate_id":"39","totalNumber":"5","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

