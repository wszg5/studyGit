# coding:utf-8
import datetime
import os
import random

from uiautomator import Device
from Repo import *
from zservice import ZDevice

class WeiXinAddFriends:

    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )


    def action(self, d,z, args):

        z.toast( "正在ping网络是否通畅" )
        while True:
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                break
            z.sleep( 2 )

        run_time_min = int( args['run_time_min'] )
        run_time_max = int( args['run_time_max'] )
        run_time = float( random.randint( run_time_min, run_time_max ) ) * 60
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast(u'模块在锁定时间内，无法运行')
            z.sleep(2)
            return

        start_time = args['start_time']
        stop_time = args['stop_time']
        try:
            if self.repo.timeCompare(start_time, stop_time):
                z.toast('处于' + start_time + '～' + stop_time + '时间段内，模块不运行')
                z.sleep(2)
                return
        except:
            logging.exception("exception")
            z.toast( "输入时间格式有误" )
            return

        z.heartbeat()
        z.toast("开始执行：微信搜索加好友")
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(8)

        d(description='更多功能按钮',className='android.widget.RelativeLayout').click()
        z.sleep(1)
        if d(text='添加朋友').exists:
            d(text='添加朋友').click()
        else:
            d(description='更多功能按钮', className='android.widget.RelativeLayout').click()
            z.sleep(1)
            d(text='添加朋友').click()
        z.heartbeat()
        d(index='1',className='android.widget.TextView').click()   #点击搜索好友的输入框
        account = 0
        add_count = int( args['add_count'] )
        while True:
            if account<add_count:
                cateid = args["repo_material_cate_id"]
                Material = self.repo.GetMaterial( cateid, 0, 1 )
                if len( Material ) == 0:
                    d.server.adb.cmd( "shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cateid ).communicate( )
                    z.sleep( 10 )
                    return
                message = Material[0]['content']  # 取出验证消息的内容

                cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
                numbers = self.repo.GetNumber(cate_id, 120, 1)  # 取出add_count条两小时内没有用过的号码
                if len(numbers) == 0:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"第%s号号码仓库为空，等待中……\"" % cate_id).communicate()
                    z.sleep(20)
                    return
                WXnumber = numbers[0]['number']
                z.input(WXnumber)
                z.heartbeat()
                d(textContains='搜索:').click()
                if d(textContains='操作过于频繁').exists:
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                    z.setModuleLastRun( self.mid )
                    z.toast( '模块结束，保存的时间是%s' % nowtime )
                    return
                z.sleep(2)
                if d(textContains='用户不存在').exists:
                    d( resourceId='com.tencent.mm:id/b4r', index=2 ).click( )
                    z.sleep(1)
                    continue
                if d(textContains='状态异常').exists:
                    d( resourceId='com.tencent.mm:id/b4r', index=2 ).click( )
                    continue
                z.heartbeat()
                gender = args['gender']
                if gender!='不限':
                    Gender = d(className='android.widget.LinearLayout', index=1).child(
                        className='android.widget.LinearLayout', index=0) \
                        .child(className='android.widget.LinearLayout', index=0).child(
                        className='android.widget.ImageView')
                    if Gender.exists:
                        z.heartbeat()
                        Gender = Gender.info
                        Gender = Gender['contentDescription']
                        print(Gender)
                        if Gender!=gender:     #看性别是否满足条件
                            d(description='返回').click()
                            z.sleep(1.5)
                            d( resourceId='com.tencent.mm:id/b4r', index=2 ).click( )
                            continue
                    else:
                        d(description='返回').click()
                        z.sleep(1.5)
                        d( resourceId='com.tencent.mm:id/b4r', index=2 ).click( )
                        continue

                z.heartbeat()
                if d(text='添加到通讯录').exists:      #存在联系人的情况
                    d(text='添加到通讯录').click()
                    z.sleep(3)
                    if d(text='发消息').exists:
                        d( descriptionContains='返回' ).click( )
                        z.sleep( 1 )
                        d( resourceId='com.tencent.mm:id/b4r', index=2 ).click( )
                        z.sleep( 1 )
                        continue
                    obj = d(className='android.widget.EditText', resourceId='com.tencent.mm:id/cl9').info  # 将之前消息框的内容删除
                    obj = obj['text']
                    lenth = len(obj)
                    t = 0
                    while t < lenth:
                        d.press.delete()
                        t = t + 1
                    d(className='android.widget.EditText', resourceId='com.tencent.mm:id/cl9').click()
                    z.input(message)
                    if args["set_remark"] == "是":
                        d( className='android.widget.EditText', resourceId='com.tencent.mm:id/clc' ).click( )
                        z.input(WXnumber)
                    d(text='发送').click()
                    z.heartbeat()
                    d(descriptionContains='返回').click()
                    z.sleep( 1 )
                    d(resourceId='com.tencent.mm:id/b4r', index=2).click()
                    z.sleep(1)
                    account = account+1
                    continue
                else:
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 1 )
                    d( resourceId='com.tencent.mm:id/b4r', index=2 ).click( )
                    z.sleep( 1 )
                    continue
            else:
                break

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WeiXinAddFriends

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
    args = {"repo_number_cate_id": "44", "repo_material_cate_id": "39", 'run_time_min': '0', 'run_time_max': '0', 'start_time': '', 'stop_time': '', "add_count": "3","set_remark": "是", 'gender': "不限",  "time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d, z, args)
