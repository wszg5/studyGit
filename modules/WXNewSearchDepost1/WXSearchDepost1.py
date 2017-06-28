# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *

class WXSearchDepost1:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.press.home()

        while True:
            if d( text='微信' ).exists:
                d( text='微信' ).click( )
                break
            d.swipe( width - 20, height / 2, 0, height / 2, 5 )

        while True:
            if d( text='发现' ) and d( text='我' ) and d( text='通讯录' ).exists:
                break
            else:
                d( descriptionContains='返回', className='android.widget.ImageView' ).click( )
        d( description='更多功能按钮' ).click( )
        z.sleep( 1 )
        if d( text='添加朋友' ).exists:
            d( text='添加朋友' ).click( )
        else:
            d( description='更多功能按钮', className='android.widget.RelativeLayout' ).click( )
            z.sleep( 1 )
            d( text='添加朋友' ).click( )
        d( index='1', className='android.widget.TextView' ).click( )  # 点击搜索好友的输入框
        z.heartbeat( )
        add_count = int( args['add_count'] )
        account = 0
        while True:
            if account <= add_count:
                cate_id = int(args["repo_number_id"])  # 得到取号码的仓库号
                number_count = 1  # 每次取一个号码
                while True:
                    exist_numbers = self.repo.GetNumber( cate_id, 0, number_count, 'exist' )
                    print( exist_numbers )
                    remain = number_count - len( exist_numbers )
                    normal_numbers = self.repo.GetNumber( cate_id, 0, remain, 'normal' )
                    numbers = exist_numbers + normal_numbers
                    if len( numbers ) > 0:
                        break
                    d.server.adb.cmd( "shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，等待中\"" % cate_id ).communicate( )
                    z.sleep( 30 )
                WXnumber = numbers[0]['number']
                z.input( WXnumber )
                d( textContains='搜索:' ).click( )
                z.heartbeat( )
                while d( textContains='正在查找' ).exists:
                    z.sleep( 2 )
                z.heartbeat( )
                if d( textContains='操作过于频繁' ).exists:
                   break

                z.sleep( 1 )

                if d( textContains='用户不存在' ).exists:
                    d( descriptionContains='清除', index=2 ).click( )
                    z.sleep( 1 )
                    continue
                if d( textContains='状态异常' ).exists:
                    d( descriptionContains='清除', index=2 ).click( )
                    continue
                z.heartbeat( )
                if d(text='详细资料').exists:
                    saveCate = args['repo_save_id']
                    para = {"phoneNumber": WXnumber, 'x_01': "exist",'x_02':'0','x_03':'2000-01-01 00:00:00','x_04':'0','x_05':'空','x_06':'NO','x_19':'CheckXunMa','x_27': '0','x_28':'0'}
                    self.repo.PostInformation( saveCate, para )
                    d( descriptionContains='返回' ).click( )
                    d( descriptionContains='清除' ).click( )
                    z.sleep( 1 )
                    account = account + 1
                    continue
            else:
                break
        if (args["time_delay"]):
            z.sleep( int( args["time_delay"] ) )

def getPluginClass():
    return WXSearchDepost1

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK00608")
    z = ZDevice("HT54VSK00608")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "175", "add_count": "25",'repo_save_id':'182',"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)




















