# coding=utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *


class QQSearch:
    def __init__(self):
        self.repo = Repo()

    def action(self, d, z, args):
        z.heartbeat( )

        # runLock = int( args['run_lock'] )
        runLock = 500
        # cate_id = int( args["repo_number_id"] )
        cate_id = 190
        # saveCate = args['repo_save_exist_id']
        saveCate = 189
        # totalList = self.repo.GetNUmberNormalTotal( saveCate )
        # normalTotal = int( totalList[0]['total'] )
        normalTotal = 123

        if normalTotal < runLock:
            # z.toast( '库内未使用QQ号低于' + args['run_lock'] + '，开始检存' )
            d.press.home( )
            if d( text="QQ" ).exists:
                d( text="QQ" ).click( )
            else:

                z.toast( '该页面没有ＱＱ' )
                z.sleep( 2 )
                return
            z.sleep( 5 )
            while True:
                if d( text="消息" ) and d( text="联系人" ) and d( text="动态" ).exists:
                    d( text="消息" ).click( )
                    break
                if d( text="取消" ).exists:
                    d( text="取消" ).click( )
                elif d( descriptionContains="返回动态 按钮" ).exists:
                    d( descriptionContains="返回动态 按钮" ).click( )
                else:
                    d( text='返回', className='android.widget.TextView' ).click( )

            d( descriptionContains="快捷入口" ).click( )
            z.sleep( 1 )
            if d( text="加好友/群" ).exists:
                d( text="加好友/群" ).click( )
            else:
                d( descriptionContains="快捷入口", className="android.widget.ImageView" ).click( )
                z.sleep( 1 )
                d( text="加好友/群" ).click( )
            d( text='QQ号/手机号/群/公众号' ).click( )
            z.heartbeat( )

            repo_material_cate_id = args["repo_material_cate_id"]
            Material = self.repo.GetMaterial( repo_material_cate_id, 0, 1 )
            wait = 1
            while wait == 1:
                try:
                    material = Material[0]["content"]
                    wait = 0
                except Exception:
                    d.server.adb.cmd( "shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到验证消息\"" )
            repo_number_cate_id = int( args( "repo_number_cate_id" ) )
            add_count = int( args( "add_count" ) )
            wait = 1
            while wait == 1:
                numbers = self.repo.GetNumber( repo_number_cate_id, 120, add_count )
                if "Error" in numbers:
                    d.server.adb.cmd( "shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"" )
                    continue
                wait = 0
            list = numbers
            print( list )

            for i in range( 0, add_count, +1 ):
                numbers = list[i]
                d.server.adb.cmd( "shell",
                                  "am force-stop com.tencent.qqlite" ).wait( )
                d.server.adb.cmd( "shell",
                                  "am start-n com.tencent.qqlite/com.mobileqq.activity.SqlashActivity" ).wait( )
                time.sleep( 2 )
            d( text='QQ号/手机号/群/公众号' ).set_text( numbers )
            d( text='找人:' ).click( )

        else:
            z.toast( '库内未使用号码大于' + args['run_lock'] + '，模块无法运行' )


def getPluginClass():
    return QQSearch


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "36be646" )
    z = ZDevice( "36be646" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).communicate( )
    args = {"repo_number_cate_id": "62", 'repo_material_cate_id': '8', "gender": "女", "add_count": "10",
            "time_delay": "3"}

    o.action( d, z, args )