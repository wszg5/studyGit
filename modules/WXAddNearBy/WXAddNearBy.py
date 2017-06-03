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
                Gender = '不限'
            nickname = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=1).child(className='android.widget.LinearLayout',index=0).child(className='android.widget.TextView')
            nickname = nickname.info['text']

            para = {'x_01': nickname, 'x_02': Gender,"x_20":id}
            self.repo.PostInformation( args["repo_cate_id"], para )
            z.toast( "%s入库完成" % nickname )

            gender = args['gender']
            if gender!='不限':
                if not d(description=gender).exists:
                    continue

            if  d(text='添加到通讯录').exists:
                d(text='添加到通讯录').click()
            else:
                continue
            z.sleep(2)
            forselect = args['forselect']
            if forselect=='单向':
                z.sleep(1)
                continue
            time.sleep(1)
            if d(text='发消息').exists:
                continue
            z.heartbeat()
            obj = d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout',index=0)\
                .child(className='android.widget.LinearLayout',index=0).child(className='android.widget.EditText')    #得到消息框内容
            obj1 = obj.info
            text = obj1['text']
            if len(text)>0:
                d.swipe(478, 193, 495, 211, 1)
            check = obj.info
            check = check['text']
            lenth = len(check)
            z.heartbeat()
            while lenth>0:
                d.press.delete()
                lenth = lenth-1

            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id).communicate()
                z.sleep(10)
                return
            message = Material[0]['content']  # 取出验证消息的内容
            z.input(message)
            z.heartbeat()
            d(text='发送').click()

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
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_wxcade_id": "131","repo_cate_id":171,"add_count": "10",'forselect':'单向','gender':'不限',"repo_material_id": "39",'time_delay':"3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
