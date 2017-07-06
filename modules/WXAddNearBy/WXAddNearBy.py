# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *

class WXAddNearBy:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)
        add_count = int(args['add_count'])
        for i in range(add_count):
            cate_id = args['repo_wxcade_id']
            wxid = self.repo.GetNumber(cate_id, 0, 1)  # 取出add_count条两小时内没有用过的号码
            if len(wxid) == 0:
                d.server.adb.cmd("shell","am broadcast -a com.zunyun.zime.toast --es msg \"第%s号号码仓库为空，等待中……\"" % cate_id).communicate()
                z.sleep(20)
                return
            z.heartbeat()
            id = wxid[0]['number']
            z.wx_openuserchat(id)
            z.heartbeat()
            d(description='聊天信息').click()
            d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=1).child(className='android.widget.RelativeLayout',index=0).click()  #点击搜索到的好友头像到添加界面
            while d(textContains='v1').exists:
                z.sleep(1)

            if d(description='男').exists:
                Gender = '男'
            elif d(description='女').exists:
                Gender = '女'
            else:
                Gender = '未知'

            nickname = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=1).child(className='android.widget.LinearLayout',index=0).child(className='android.widget.TextView')
            nickname = nickname.info['text']

            if d(text='添加到通讯录').exists:
                d(text='添加到通讯录').click()
                z.sleep(3)
                if d( text='发消息' ).exists:
                    para = {'phoneNumber': nickname, 'x_01': Gender, 'x_02': '单向', 'x_03': id}
                    self.repo.PostInformation( args["repo_cate_id"], para )
                    z.toast( "%s入库完成" % nickname )
                else:
                    para = {'phoneNumber': nickname, 'x_01': Gender, 'x_02': '双向', 'x_03': id}
                    self.repo.PostInformation( args["repo_cate_id"], para )
                    z.toast( "%s入库完成" % nickname )
            else:
                continue

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXAddNearBy

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_wxcade_id": "131","repo_cate_id":"171","add_count": "10",'time_delay':"3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
