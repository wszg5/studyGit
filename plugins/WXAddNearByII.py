# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXAddNearByII:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)
        proportion = args['proportion']  #单双比例
        if proportion == '1:1':
            dan = 1
            shuang = 1
        elif proportion == '1:2':
            dan = 1
            shuang = 2
        else:
            dan = 2
            shuang = 1
        dan1 = dan
        shuang1 = shuang
        add_count = int(args['add_count'])
        countnum = 0
        while countnum<add_count:
            cate_id = args['repo_wxcade_id']
            wxid = self.repo.GetNumber(cate_id, 0, 1)  # 取出add_count条两小时内没有用过的号码
            if len(wxid) == 0:
                d.server.adb.cmd("shell","am broadcast -a com.zunyun.zime.toast --es msg \"第%s号号码仓库为空，等待中……\"" % cate_id).communicate()
                z.sleep(20)
                return
            z.heartbeat()
            id = wxid[0]['number']
            print(id)
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


            if  d(text='添加到通讯录').exists:
                d(text='添加到通讯录').click()
                if d(textContains='正在添加').exists:
                    z.sleep(1)
            else:
                continue
            z.sleep(2)
            if d(text='发消息').exists:
                danxiang = '单向'
                para = {'x_01': nickname, 'x_02': Gender, "x_20": id,"x_03":danxiang}
                self.repo.PostInformation( args["repo_cate_id"], para )
                z.toast( "%s入库完成" % nickname )
                if dan1>0:   #证明此次循环单向未运行完成
                    dan1 = dan1 - 1
                    continue
                else:
                    continue

            danxiang = '混合'
            para = {'x_01': nickname, 'x_02': Gender, "x_20": id, "x_03": danxiang}
            self.repo.PostInformation( args["repo_cate_id"], para )
            z.toast( "%s入库完成" % nickname )

            if dan1>0:    #将单的运行完之后再运行双的
                continue

            if shuang1>0:
                shuang1 = shuang1 -1
               # print(shuang1)
            else:
                dan1 = dan      #一次的比例运行完成恢复原有比例
                shuang1 = shuang
                continue


            z.heartbeat()
            '''
            判断性别与设定是否一致
            '''
            gender = args['gender']
            if gender != '不限':
                if Gender != gender:  # 看性别是否满足条件
                    z.toast('性别不符')
                    shuang1 = shuang1+1
                    continue
            obj = d( className='android.widget.ScrollView' ).child( className='android.widget.LinearLayout',
                                                                    index=0 ).child(
                className='android.widget.EditText' )  # 得到消息框内容
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
            countnum = countnum+1

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXAddNearByII

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

    args = {"repo_wxcade_id": "131","repo_cate_id":171,"add_count": "10",'gender':"不限",'proportion':'1:2',"repo_material_id": "39",'time_delay':"3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)


























