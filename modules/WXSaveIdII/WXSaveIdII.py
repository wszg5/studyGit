# coding:utf-8
from uiautomator import Device
from Repo import *
from zservice import ZDevice

class WXSaveIdII:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        wxcate_id = args['repo_wxcade_id1']
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
            while d(textContains='v1_').exists:   #要等昵称和性别显示出来
                z.sleep(2)


            z.sleep(2)
            if  d(text='添加到通讯录').exists:
                d(text='添加到通讯录').click()
                if d(textContains='正在添加').exists:
                    z.sleep(1)
            else:
                continue
            z.sleep(1)
            if d(text='发消息').exists:
                self.repo.uploadPhoneNumber(id, wxcate_id,'Y')
                continue
            else:
                continue

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXSaveIdII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_wxcade_id": "131","add_count": "10",'repo_wxcade_id1':172,'time_delay':"3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
