# coding:utf-8
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class QLAddGroup:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ轻聊版唤醒加群 名片分享" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return

        totalNumber = int(args['totalNumber'])  # 唤醒加群次数
        for i in range (0,totalNumber,+1):
            cate_id = int( args["repo_number_id"] )  # 得到取号码的仓库号
            numbers = self.repo.GetNumber( cate_id, 0, 1 )  # 取出totalNumber条两小时内没有用过的号码
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            QQnumber = numbers[0]['number']
            z.sleep(2)

            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial( cate_id, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']
            z.sleep( 2 )

            d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqapi://card/show_pslcard?src_type=internal\&version=1\&uin=%s\&card_type=group&source=qrcode"'%QQnumber )  # 群页面
            z.sleep(2)
            z.heartbeat()
            if d(text='QQ轻聊版').exists:
                d(text='QQ轻聊版').click()
                time.sleep(0.5)
                if d(text='仅此一次').exists:
                    d(text='仅此一次').click()
                    z.sleep(2)

            if d(text='加入该群').exists:
                d(text='加入该群').click()

            obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
            obj = obj['text']
            lenth = len(obj)
            m = 0
            while m < lenth:
                d.press.delete()
                m = m + 1
            z.input(message)
            d(text='发送').click()
            z.heartbeat()
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return QLAddGroup

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT524SK00685")
    z = ZDevice("HT524SK00685")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_number_id":"229","repo_material_id":"39","totalNumber":"20","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)

