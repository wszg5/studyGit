# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class MobilqqAddFriendByCard:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z,args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        z.sleep(1.5)
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来

        z.sleep(6)
        cate_id1 = args["repo_material_cate_id"]
        add_count = int(args['add_count'])  # 要添加多少人



        for i in range (0,add_count,+1):            #总人数
            Material = self.repo.GetMaterial( cate_id1, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id1 ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']  # 取出验证消息的内容

            repo_number_cate_id = int( args["repo_number_cate_id"] )  # 得到取号码的仓库号

            numbers = self.repo.GetNumber( repo_number_cate_id, 120, 1 )  # 取出add_count条两小时内没有用过的号码
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % repo_number_cate_id ).communicate( )
                z.sleep( 10 )
                return
            z.heartbeat( )
            QQnumber = numbers[0]['number']
            print(QQnumber)
            z.sleep(1)

            z.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=person\&source=qrcode"'%QQnumber)  # qq名片页面
            z.sleep(10)

            # if d( textContains='下次默认' ).exists:
            #     d( textContains='下次默认' ).click( )

            if d(text='QQ').exists:
                d(text='QQ').click()
                z.sleep(0.5)

            d(text='加好友').click()
            z.sleep(2)
            z.heartbeat()
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
                z.input(message)
            d(text='发送').click()
            z.heartbeat()

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqAddFriendByCard

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cc0e9474")
    z = ZDevice("cc0e9474")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_cate_id":"119","repo_material_cate_id":"39","add_count":"3","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d, z, args)