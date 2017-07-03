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

        runLock = int( args['run_lock'] )
        cateId = args['repo_save_id']
        totalList = self.repo.GetNUmberNormalTotal( cateId )
        normalTotal = int( totalList[0]['total'] )

        if normalTotal < runLock:
            z.toast( '库内未使用号码低于' + args['run_lock'] + '，开始拉号码' )

            str = d.info  # 获取屏幕大小等信息
            height = str["displayHeight"]
            width = str["displayWidth"]
            d.press.home( )

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

            lock_count = 0
            while True:
                lock_count = lock_count + 1
                if lock_count > int( args['check_count'] ):
                    z.toast( '成功检存' + args['check_count'] + '次，结束' )
                    break

                cate_id = int( args["repo_number_id"] )  # 得到取号码的仓库号
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
                if d( text='详细资料' ).exists:
                    PhoneNumber = self.scode.GetPhoneNumber( self.scode.WECHAT_REGISTER, WXnumber )  # 获取接码平台手机号码
                    if PhoneNumber is not None:
                        self.scode.defriendPhoneNumber( PhoneNumber, self.scode.WECHAT_REGISTER )  # 拉黑
                        saveCate = args['repo_save_id']
                        para = {"phoneNumber": WXnumber, 'x_01': "exist", 'x_02': '0',
                                'x_03': '2000-01-01 00:00:00',
                                'x_04': '0', 'x_05': '空', 'x_06': '2000-01-01 00:00:00', 'x_19': 'CheckXunMa',
                                'x_27': '0', 'x_28': '0'}
                        self.repo.PostInformation( saveCate, para )
                    d( descriptionContains='返回' ).click( )
                    d( descriptionContains='清除' ).click( )
                    z.sleep( 1 )


        else:
            z.toast( '库内未使用号码大于' + args['run_lock'] + '，模块无法运行' )



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
    args = {"repo_number_id": "175", 'repo_save_id': '189',"run_lock": "500", "check_count": "100"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
