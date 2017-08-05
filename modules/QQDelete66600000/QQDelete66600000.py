#coding=utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *

class QQDelete66600000:
    def __init__(self):
        self.repo = Repo()

    def action(self,d,z,args):
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).wait( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).wait( )  # 将qq拉起来
        time.sleep(3)
        z.heartbeat( )
        d(index=0,resourceId="com.tencent.mobileqq:id/et_search_keyword",descriptionContains="搜索",className="android.widget.EditText").click()
        time.sleep(1)
        QQNumber = args["QQNumber"]
        z.input(QQNumber)
        if d(index=1,className="android.widget.RelativeLayout").exists:
            z.heartbeat( )
            d(index=1,className="android.widget.RelativeLayout").click()
            d(index=0,resourceId = "com.tencent.mobileqq:id/ivTitleBtnRightImage",descriptionContains="聊天设置",className="android.widget.ImageView").click()
            d( index=3, text="删除好友" ).click( )
            d( index=0, text="删除好友" ).click( )
        else:
            d(text="取消").click()
def getPluginClass():
    return QQDelete66600000


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT53XSK00427" )
    z = ZDevice( "HT53XSK00427" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).wait( )
    args = { "QQNumber":"66600000",}    #repo_name_id:QQ修改昵称仓库号，ｇｅｎｄｅｒ为默认性别
    o.action( d, z, args )