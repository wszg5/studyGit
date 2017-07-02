# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *


class WXSearchDepost1PP:
    def __init__(self):
        self.repo = Repo()

    def action(self, d, z, args):
        z.heartbeat()
        d.press.home()
        if d( text='微信' ).exists:
            d( text='微信' ).click( )
        else:
            # d.swipe( width - 20, height / 2, 0, height / 2, 5 )
            z.toast( '该页面没有微信' )
            z.sleep( 2 )
            return
        z.sleep( 5 )

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

        while True:
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
                saveCate = args['repo_save_exist_id']
                self.repo.uploadPhoneNumber( WXnumber, saveCate )
                d( descriptionContains='清除' ).click( )

                continue

            z.sleep( 1 )

            if d( textContains='用户不存在' ).exists:
                saveCate = args['repo_save_not_exist_id']
                self.repo.uploadPhoneNumber( WXnumber, saveCate )
                d( descriptionContains='清除', index=2 ).click( )
                z.sleep( 1 )
                continue
            if d( textContains='状态异常' ).exists:
                saveCate = args['repo_save_exist_id']
                self.repo.uploadPhoneNumber( WXnumber, saveCate )
                d( descriptionContains='清除', index=2 ).click( )
                continue
            z.heartbeat( )

            saveCate = args['repo_save_exist_id']
            self.repo.uploadPhoneNumber( WXnumber ,saveCate )

            d( descriptionContains='返回' ).click( )
            d( descriptionContains='清除' ).click( )
            z.sleep( 1 )
            continue

        if (args["time_delay"]):
            z.sleep( int( args["time_delay"] ) )


def getPluginClass():
    return WXSearchDepost1PP


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz( )
    d = Device( "HT53ASK00088" )
    z = ZDevice( "HT53ASK00088" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).communicate( )
    args = {"repo_number_id": "181",'repo_save_exist_id': '175',"repo_save_not_exist_id": "183",
            "time_delay": "3"}  # cate_id是仓库号，length是数量
    o.action( d, z, args )






















