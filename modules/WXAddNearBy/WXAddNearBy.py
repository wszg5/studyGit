# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXSaveId:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(7)
        add_count = int(args['add_count'])
        for i in range(add_count):
            cate_id = args['repo_wxcade_id']
            wxid = self.repo.GetNumber(cate_id, 0, 1)  # 取出add_count条两小时内没有用过的号码
            if len(wxid) == 0:
                d.server.adb.cmd("shell",
                                 "am broadcast -a com.zunyun.zime.toast --es msg \"第%s号号码仓库为空，等待中……\"" % cate_id).communicate()
                time.sleep(20)
                return
            id = wxid[0]['number']
            z.wx_openuserchat(id)
            d(description='聊天信息').click()
            d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=1).child(className='android.widget.RelativeLayout',index=0).click()  #点击搜索到的好友头像到添加界面
            d(text='添加到通讯录').click()
            time.sleep(1.5)
            if d(text='发消息').exists:
                continue
            obj = d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout',index=0)\
                .child(className='android.widget.LinearLayout',index=0).child(className='android.widget.EditText')    #得到消息框内容
            obj1 = obj.info
            text = obj1['text']
            if len(text)>0:
                d.swipe(478, 193, 495, 211, 1)
            check = obj.info
            check = check['text']
            lenth = len(check)
            while lenth>0:
                d.press.delete()
                lenth = lenth-1

            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id).communicate()
                time.sleep(10)
                return
            message = Material[0]['content']  # 取出验证消息的内容
            z.input(message)
            d(text='发送').click()
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXSaveId

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_wxcade_id": "131","add_count": "10","repo_material_id": "39",'time_delay':"3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
