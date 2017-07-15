# coding:utf-8
import datetime
import os


from uiautomator import Device
from Repo import *
from zservice import ZDevice
from random import choice
import logging
logging.basicConfig(level=logging.INFO)


class WXSearchAddFriendsByV1:

    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath(__file__)

    def action(self, d,z, args):
        run_time = float( args['run_time'] ) * 60
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return

        z.heartbeat()

        count = 1
        while True:
            wayList = ['3','6','13','15','17','18','30','39']

            if count > int(args['add_count']):
                z.toast(args['add_count']+'个好友已加完')
                break

            cateId = args['repo_material_id']
            Material = self.repo.GetMaterial( cateId, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']  # 从素材库取出的要发的材料
            z.sleep( 1 )

            cate_id = args['repo_number_id']
            infoList = self.repo.GetNumber(cate_id, 0, 1)
            if len(infoList) == 0:
                z.toast(cate_id+'号仓库为空，没有取到ｖ１值')
                return
            v1 = infoList[0]['number']

            if args['add_friend_way'] == '随机':
                indexStr = choice(wayList)
            else:
                indexStr = args['add_friend_way']

            z.wx_openuser_v1(v1, indexStr)
            z.sleep(3)

            z.heartbeat()
            if d( text='添加到通讯录' ).exists:
                d( text='添加到通讯录' ).click( )
                z.sleep( 5 )

            if d(text='发消息').exists:
                count = count + 1
                danshuang = '单向'

            if d(text='验证申请').exists:
                count = count + 1
                danshuang = '双向'
                deltext = d(className='android.widget.EditText', index=1).info  # 将之前消息框的内容删除
                deltext = deltext['text']
                lenth = len(deltext)
                m = 0
                while m < lenth:
                    d.press.delete()
                    m = m + 1
                z.heartbeat()
                d(className='android.widget.EditText', index=1).click()
                z.input(message)
                z.sleep(2)

                d(text='发送').click()
                z.sleep(1)
                d(description='返回').click()

            if d(text='确定').exists:
                d(text='确定').click()

            para = {"x_05": danshuang, 'x_20': v1}
            self.repo.PostInformation( args["repo_information_id"], para )
            z.toast( "%s入库完成" )

            if d(descriptionContains='返回').exists:
                d(descriptionContains='返回').click()

            if (args["time_delay"]):
                z.sleep(int(args["time_delay"]))

        now = datetime.datetime.now()
        nowtime = now.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun(self.mid)
        z.toast('模块结束，保存的时间是%s' % nowtime)


def getPluginClass():
    return WXSearchAddFriendsByV1

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("5959d2f3")
    z = ZDevice("5959d2f3")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "202", "repo_information_id": "204", "repo_material_id": "39", "add_count": "3", 'run_time':'0', "add_friend_way":"随机", "time_delay": "5"}    #cate_id是仓库号，length是数量
    o.action(d, z, args)
