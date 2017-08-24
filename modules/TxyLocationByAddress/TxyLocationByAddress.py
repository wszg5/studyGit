# coding=utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *


class TxyLocationByAddress:
    def __init__(self):
        self.repo = Repo( )

    def action(self, d, z, args):
        z.toast("准备执行天下游模拟定位模块")
        d.server.adb.cmd( "shell", "am force-stop com.txy.anywhere" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.txy.anywhere/com.txy.anywhere.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 5 )
        z.heartbeat( )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        repo_address_id = args["repo_address_id"]
        address = self.repo.GetNumber( repo_address_id, 60, 1 )
        if len( address ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"地址库%s号仓库为空，没有取到消息\"" % repo_address_id ).communicate( )
            return
        address = address[0]['number']
        while not d(text="设置",className="android.widget.RadioButton").exists:
            z.sleep(2)

        obj1 = d(index=2,resourceId="com.txy.anywhere:id/rl_search_result",className="android.widget.LinearLayout").child(
            index=1,resourceId="com.txy.anywhere:id/tv_mapfrg_searchresult",className="android.widget.TextView")

        obj  = d(index=1,resourceId="com.txy.anywhere:id/lv_city",className="android.widget.ListView").child(index=1,resourceId="com.txy.anywhere:id/tv_city",className='android.widget.TextView')

        obj2 = d( index=1, resourceId="com.txy.anywhere:id/lv_search", className="android.widget.ListView" ).child(
            index=0, className="android.widget.LinearLayout" ).child( index=0, className="android.widget.LinearLayout" )
        obj3 = d( index=0, resourceId="com.txy.anywhere:id/rl_pin_startmockbtn_distanceLl",
                  className="android.widget.RelativeLayout" ).child(
            index=0, resourceId="com.txy.anywhere:id/iv_mapfrg_start_mock", className="android.widget.ImageView" )

        while obj1.exists:
            z.sleep(1)
            z.heartbeat()
            obj1.click()
        z.sleep(1)
        z.heartbeat()
        z.input(address)
        z.sleep(1)
        d(text="搜索",resourceId="com.txy.anywhere:id/btn_search",className="android.widget.Button").click()
        z.sleep(2)
        while (not obj.exists and not obj2.exists) and not obj3.exists:
            z.toast("该地点不存在")
            objtemp = d( index=0, className="android.widget.LinearLayout" ).child(index=0,className="android.widget.LinearLayout").child(
                index=1, resourceId="com.txy.anywhere:id/et_search", className="android.widget.EditText" )
            if objtemp.exists:
                z.sleep(1)
                z.heartbeat()
                obj.click()
                objtemp = objtemp.info["text"]
                lenth = len(objtemp)
                t = 0
                while t < lenth:
                    # z.heartbeat( )
                    d.press.delete( )
                    t = t + 1
                z.sleep(1)
                address2 = self.repo.GetNumber( repo_address_id, 60, 1 )
                if len( address ) == 0:
                    d.server.adb.cmd( "shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"地址库%s号仓库为空，没有取到消息\"" % repo_address_id ).communicate( )
                    return
                address2 = address2[0]['number']
                z.heartbeat()
                z.input(address2)
                z.sleep(1)
                z.heartbeat()
                d( text="搜索", resourceId="com.txy.anywhere:id/btn_search", className="android.widget.Button" ).click( )
            z.sleep(1)
        while obj.exists:
            z.sleep(1)
            z.heartbeat()
            obj.click()

        while obj2.exists:
            z.sleep(1)
            z.heartbeat()
            obj2.click()
            z.sleep(1)

        if obj3.exists:
            obj3.click( )
            z.sleep( 1 )
            z.heartbeat( )
        d.click( 100, 100 )
        z.toast("模块完成")
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return TxyLocationByAddress


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT524SK00685" )
    z = ZDevice( "HT524SK00685" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).wait( )
    args = {"repo_address_id": "224","time_delay": "3"}  # repo_name_id:QQ修改昵称仓库号，birthday_ xxx :年龄范围
    o.action( d, z, args )
    # a = o.WebViewBlankPages(d)
    # print(a)


