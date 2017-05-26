# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class MobilqqAddGroupII:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        cate_id1 = args["repo_material_id"]


        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(1)
        d(resourceId='com.tencent.mobileqq:id/name', description='快捷入口').click()
        z.sleep(1)
        z.heartbeat()
        if d(textContains='加好友').exists:
            d(textContains='加好友').click()
        else:
            d(resourceId='com.tencent.mobileqq:id/name', description='快捷入口').click()
            d(textContains='加好友').click()
        z.sleep(2)
        d(text='找群').click()
        z.sleep(1)
        add_count = int(args['add_count'])  # 要添加多少人
        cate_id = int(args["repo_number_id"])  # 得到取号码的仓库号

        for i in range(add_count):
            Material = self.repo.GetMaterial( cate_id1, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']  # 取出验证消息的内容

            numbers = self.repo.GetNumber(cate_id, 120,1)  # 取出add_count条两小时内没有用过的号码
            if len(numbers) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % cate_id).communicate()
                z.sleep(10)
                return
            QQgroup = numbers[0]['number']
            d(textContains='QQ号/手机号').click()
            z.input(QQgroup)
            d(textContains='找群:').click()
            z.sleep(2)
            if d(textContains='没有找到相关结果').exists:
                d(description='清空').click()
                continue

            obj = d(descriptionContains='群成员').child(className='android.widget.LinearLayout',index=1).child(className='android.widget.TextView')
            if obj.exists:
                obj = obj.info
            else:
                d.swipe(width / 2, height * 5 / 6, width / 2, height / 4)
                if obj.exists:
                    obj = obj.info
                else:
                    continue
            z.heartbeat()
            member = obj['text']
            member = filter(lambda ch: ch in '0123456789', member)
            member = int(member)
            if member==0:
                continue
            d(text='申请加群').click()
            z.sleep(1)
            if d(text='申请加群').exists:
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
            z.sleep(1)
            if d(text='发送').exists:
                z.toast('操作频繁，程序结束')
                return
            z.sleep(2)
            d(text='关闭').click()
            d(description='清空').click()



        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqAddGroupII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id":"119","repo_material_id":"39","add_count":"3","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)

