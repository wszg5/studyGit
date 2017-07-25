# coding:utf-8
from uiautomator import Device
from Repo import *
from smsCode import smsCode
import time, string, datetime, random
from zservice import ZDevice
import util

class WeiXinCloseUnnecessary:
    def __init__(self):
        self.repo = Repo( )


    def action(self, d, z, args):
        for i in range(2,15):
            if d(classname='android.widget.LinearLayout',resourceId='com.tencent.mm:id/i_',package='com.tencent.mm',index=1).exists:
                d( classname='android.widget.LinearLayout', resourceId='com.tencent.mm:id/i_', package='com.tencent.mm',index=1 ).click()
            d( className='android.widget.ListView' ).child( className='android.widget.LinearLayout', index=i ).click()
            if d( text='摇一摇' ).exists or d( text='附近的人' ).exists or d( text='群发助手' ).exists:
                if d( text='停用' ).exists:
                    d.click( 30, 72 )
            else:
                d.drag(30,72,500,500)
                if d( text='停用' ).exists:
                    # 点击'停用'
                    d( text='停用' ).click( )
                    z.sleep( 1 )
                    if d( textContains='停用该功能' ).exists:
                        # 点击'清空并停用'
                        d( text='清空' ).click( )
                        z.sleep( 5 )
                    if d( text='启用该功能' ).exists:
                        # 返回到功能界面，继续进行下一个功能的关闭
                        d.click( 30, 72 )
                        z.sleep( 1 )
                elif d( text='启用该功能' ).exists:
                    d.click( 30, 72 )
                    z.sleep( 1 )




def getPluginClass():
    return WeiXinCloseUnnecessary

if __name__ == "__main__":
    import sys
    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT54VSK00608" )  # INNZL7YDLFPBNFN7
    z = ZDevice( "HT54VSK00608" )
    # z.server.install()
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).communicate( )
    'dingdingdingdingdindigdingdingdingdingdingdingdingdingdingdingdingdignin'
    repo = Repo( )
    # repo.RegisterAccount('', 'gemb1225', '13045537833', '109')
    args = {"repo_information_id": "189", "repo_material_id": "167"}  # cate_id是仓库号，发中文问题
    saveCate = args['repo_information_id']
    o.action( d, z, args )