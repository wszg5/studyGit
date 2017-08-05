# coding:utf-8
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice


class TIMBind:
    def __init__(self):
        self.repo = Repo( )
        # self.xuma = XunMa( )
        self.xuma = None

    def action(self, d, z,args):
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.toast( "点击开始绑定" )
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        d( text='马上绑定' ).click( )
        while d( text='验证手机号码' ).exists:

            PhoneNumber = None
            j = 0
            while PhoneNumber is None:
                j += 1
                PhoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )  # 获取接码平台手机号码
                z.heartbeat( )
                if j > 20:
                    z.toast( '取不到手机号码' )
                    return "nothing"

            if not d( textContains='+86' ).exists:
                d( description='点击选择国家和地区' ).click( )
                if d( text='中国' ).exists:
                    d( text='中国' ).click( )
                else:
                    str = d.info  # 获取屏幕大小等信息
                    height = str["displayHeight"]
                    width = str["displayWidth"]
                    d.click( width * 5 / 12, height * 5 / 32 )
                    z.sleep( 1.5 )
                    z.input( '中国' )
                    z.sleep( 2 )
                    d( text='+86' ).click( )

            z.input( PhoneNumber )
            z.sleep( 1.5 )
            if d( text='下一步' ).exists:
                d( text='下一步' ).click( )
                z.sleep( 3 )
            if d( text='确定' ).exists:
                d( text='确定' ).click( )
                z.sleep( 2 )
            code = self.scode.GetVertifyCode( PhoneNumber, self.scode.QQ_CONTACT_BIND, '4' )  # 获取接码验证码
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_CONTACT_BIND )
            if code == '':
                z.toast( PhoneNumber + '手机号,获取不到验证码' )
                if d( text='返回' ).exists:
                    d( text='返回' ).click( )
                if not d( textContains='中国' ).exists:
                    if d( text='返回' ).exists:
                        d( text='返回' ).click( )
                if d( className='android.view.View', descriptionContains='删除' ).exists:
                    d( className='android.view.View', descriptionContains='删除' ).click( )
                continue
            z.heartbeat( )
            z.input( code )
            if d( text='完成' ).exists:
                d( text='完成' ).click( )
            z.sleep( 5 )
            break
        z.sleep( 1 )


def getPluginClass():
    return TIMBind

if __name__ == "__main__":
    clazz = getPluginClass()
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT54VSK01061" )
    z = ZDevice( "HT54VSK01061" )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).wait( )
    # d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # args = {"repo_cate_id": "132", "time_limit": "120", "time_limit1": "120",
    #         "time_delay": "3"}  # cate_id是仓库号，length是数量
    args = {"repo_material_id":"8","StartIndex":"0","EndIndex":"7","time_delay":"3"};
    # z.server.install( )
    o.action( d, z, args )
    # d.dump(compressed=False)
