# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class MobilqqRouseAdd:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell",  "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        totalNumber = int(args['totalNumber'])  # 要给多少人发消息




        for i in range (0,totalNumber,+1):
            cate_id1 = args["repo_material_cate_id"]
            Material = self.repo.GetMaterial(cate_id1, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id1).communicate()
                z.sleep(10)
                return
            message = Material[0]['content']  # 取出验证消息的内容

            cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号
            numbers = self.repo.GetNumber( cate_id, 0, 1 )  # 取出totalNumber条两小时内没有用过的号码
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            z.heartbeat( )
            QQnumber = numbers[0]['number']
            z.sleep(1)
            z.heartbeat()
            d.server.adb.cmd("shell",
                             'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=crm\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"'%QQnumber )  # 临时会话
            z.sleep(2)
            z.heartbeat()
            if d(text='QQ').exists:
                d(text='QQ').click()
                time.sleep(0.5)
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()
            d(description='聊天设置').click()
            d(text='加为好友').click()
            z.heartbeat()
            z.sleep(2)
            if d(text='加为好友').exists:  # 拒绝被添加的轻况
                continue
            if d(text='输入答案').exists:
                continue
            if d(text='填写验证信息').exists:
                z.heartbeat()
                obj = d(className='android.widget.EditText',
                        resourceId='com.tencent.mobileqq:id/name').info  # 将之前消息框的内容删除
                obj = obj['text']
                lenth = len(obj)
                t = 0
                while t < lenth:
                    d.press.delete()
                    t = t + 1
                z.input(message)
            d(text='发送').click()

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqRouseAdd

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_number_cate_id":"119","repo_material_cate_id":"39","totalNumber":"4","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d, z,args)

