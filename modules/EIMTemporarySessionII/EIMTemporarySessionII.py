# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class EIMTemporarySessionII:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        totalNumber = int(args['totalNumber'])  # 要给多少人发消息
        cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        numbers = self.repo.GetNumber(cate_id, 0, totalNumber)  # 取出totalNumber条两小时内没有用过的号码
        if len(numbers) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % cate_id).communicate()
            z.sleep(10)
            return

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)
        z.sleep(15)
        z.heartbeat()
        for i in range (0,totalNumber,+1):
            cate_id = args["repo_material_cate_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                z.sleep(10)
                return
            message = Material[0]['content']  # 取出验证消息的内容

            QQnumber = list[i]['number']
            z.sleep(1)

            z.heartbeat()
            d.server.adb.cmd("shell",
                             'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=wpa\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % QQnumber)  # 临时会话发企业QQ）
            z.sleep(2)
            z.heartbeat()
            if d(text='企业QQ').exists:
                d(text='企业QQ').click()
                z.sleep(0.5)
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()

            if d(textContains='沟通的权限').exists:
                d.server.adb.cmd("shell",
                                 'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=wpa\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % QQnumber)  # 临时会话发企业QQ）
                z.heartbeat()
                z.sleep(1)
                if d(text='企业QQ').exists:
                    d(text='企业QQ').click()
                    if d(text='仅此一次').exists:
                        d(text='仅此一次').click()

            if d(className='android.widget.EditText').exists:
                d(className='android.widget.EditText').click()
                z.input(message)

            d(text='发送').click()


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return EIMTemporarySessionII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52ESK00321")
    z = ZDevice("HT52ESK00321")

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_cate_id":"119","repo_material_cate_id":"39","totalNumber":"20","time_delay":"3"};    #cate_id是仓库号，length是数量
    # z.openQQChat(154343346)   QQTemporarySession

    o.action(d, z,args)

