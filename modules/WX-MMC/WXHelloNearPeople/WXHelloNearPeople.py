# coding:utf-8
import os
import random
from imp import reload

from uiautomator import Device
from Repo import *
import datetime
from zservice import ZDevice
import logging
logging.basicConfig(level=logging.INFO)

class WXHelloNearPeople:
    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath(__file__)

    def action(self, d, z, args):
        z.toast( "正在ping网络是否通畅" )
        while True:
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                break
            z.sleep( 2 )

        z.toast( "开始执行：微信附近人打招呼" )
        run_time_min = int( args['run_time_min'] )
        run_time_max = int( args['run_time_max'] )
        run_time = float( random.randint( run_time_min, run_time_max ) ) * 60
        run_interval = z.getModuleRunInterval(self.mid)
        if run_interval is not None and run_interval < run_time:
            z.toast( u'模块在锁定时间内，无法运行' )
            z.sleep(2)
            return

        start_time = args['start_time']
        stop_time = args['stop_time']
        try:
            if self.repo.timeCompare( start_time, stop_time ):
                z.toast( '处于' + start_time + '～' + stop_time + '时间段内，模块不运行' )
                z.sleep( 2 )
                return
        except:
            logging.exception( "exception" )
            z.toast( "输入时间格式有误" )
            return

        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(20)
        z.heartbeat()

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]


        while True:
            if d(text='发现').exists and d(text='我').exists and d(text='通讯录').exists:
                break
            else:
                d(descriptionContains='返回', className='android.widget.ImageView').click()

        z.sleep(2)
        for i in range(0, 2):
            d(text='发现').click()
            z.sleep(2)


        if d(text='附近的人').exists:
            d(text='附近的人').click()
            z.sleep(15)

        if d(textContains='开始查看').exists:
            d(textContains='开始查看').click()
            z.sleep(1.5)

        if d(textContains='下次不提示').exists:
            d(textContains='下次不提示').click()

        if d(text='确定').exists:
            d(text='确定').click()

        if d(textContains='提高微信定位精确度').exists:
            if d( textContains='下次不提示' ).exists:
                d( textContains='下次不提示' ).click( )

            d(text='跳过').click()
            z.sleep(1.5)

        if d(textContains='补充个人信息').exists:
            d(text='女').click()
            d(textContains='地区').click()
            z.sleep(3)
            d(className='android.widget.LinearLayout',index=1).child(className='android.widget.ImageView',index=0).click()
            z.sleep(1.5)
            d(text='下一步').click()

        if d(text='查看附近的人').exists:
            d(text='查看附近的人').click()
            z.sleep( 3 )

        while d(text='正在查找附近的人').exists:
            z.sleep(3)

        z.sleep(3)
        if d(textContains='暂时没有找到附近也使用该功能的人').exists:
            z.toast("暂时没有找到附近的人")
            now = datetime.datetime.now( )
            nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
            z.setModuleLastRun( self.mid )
            z.toast( '模块结束，保存的时间是%s' % nowtime )
            return

        d(descriptionContains='更多').click()
        z.sleep(1)
        d(text='附近打招呼的人').click()
        z.sleep(1)
        if d(text='查看更多').exists:
            d( text='查看更多' ).click()

        nearPeopleObj = d(className='android.widget.ListView',resourceId='com.tencent.mm:id/bb1').child(className='android.view.View',index=0)
        while True:
            if nearPeopleObj.exists:
                nearPeopleObj.click()
                if d(text='通过验证').exists:
                    d( text='通过验证' ).click()
                    z.sleep(1)
                if d(text='完成').exists:
                    d( text='完成' ).click()
                    z.sleep(5)
                if d(text='发消息').exists:
                    d(description='返回').click()
            else:
                d( description='返回' ).click( )
                break

        d(descriptionContains='更多').click()
        z.sleep(1)
        gender = args['gender']
        if gender == '男':
            d(text='只看男生').click()
            z.sleep(3)
        elif gender == '女':
            d(text='只看女生').click()
            z.sleep(3)
        else:
            d(text='查看全部').click()
            z.sleep(3)


        z.sleep(8)
        i = 0
        count = 0
        while True:
            count = count + 1
            if count > int(args['hello_count']):
                z.toast('已完成设置打招呼次数')
                break
            i = i + 1
            nearObj = d(className='android.widget.ListView', index=0).child(className='android.widget.LinearLayout', index=i)
            if nearObj.exists:
                if d(textContains='朋友不够多').exists:
                    continue
                nearObj.click()
                if d(text='打招呼').exists:
                    d(text='打招呼').click()
                    z.sleep(2)
                if d(text='向TA说句话打个招呼').exists:
                    cate_id = args['repo_material_id']
                    Material = self.repo.GetMaterial(cate_id, 0, 1)
                    Msg = Material[0]['content']
                    z.input(Msg)
                    z.sleep(1.5)
                d(text='发送').click()
                z.sleep(3)
                d(descriptionContains='返回', className='android.widget.ImageView').click()
                z.sleep(2)
            else:
                i = 1
                d.swipe(width / 2, height * 7 / 8, width / 2, height / 8)

        now = datetime.datetime.now()
        nowtime = now.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun(self.mid)
        z.toast('模块结束，保存的时间是%s' % nowtime)




def getPluginClass():
    return WXHelloNearPeople

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A1SK02114")
    z = ZDevice("HT4A1SK02114")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id": "40", "repo_number_id": "205", "hello_count": "3", 'gender': '女', 'run_time_min': '1', 'run_time_max': '3', 'start_time': '', 'stop_time': ''}    #cate_id是仓库号，length是数量
    o.action(d, z, args)
