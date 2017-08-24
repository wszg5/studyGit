# coding=utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *


class TxyLocationByCoordinate:
    def __init__(self):
        self.repo = Repo( )

    def action(self, d, z, args):
        z.toast("准备执行天下游模拟坐标定位模块")
        d.server.adb.cmd( "shell", "am force-stop com.txy.anywhere" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.txy.anywhere/com.txy.anywhere.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 5 )
        z.heartbeat( )
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        repo_address_id = args["repo_address_id"]
        time = args["time"]
        address = self.repo.GetNumber( repo_address_id, time, 1 )
        if len( address ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"地址库%s号仓库为空，没有取到消息\"" % repo_address_id ).communicate( )
            return
        address = address[0]['number']
        xy = address.split(',')
        x = xy[0]
        y = xy[1]


        while not d(text="设置",className="android.widget.RadioButton").exists:
            z.sleep(2)

        obj1 = d(index=3,resourceId="com.txy.anywhere:id/ll_function",className="android.widget.LinearLayout").child(
            index=3,resourceId="com.txy.anywhere:id/iv_user_input",className="android.widget.ImageView")

        obj3 = d( index=0, resourceId="com.txy.anywhere:id/rl_pin_startmockbtn_distanceLl",
                  className="android.widget.RelativeLayout" ).child(
            index=0, resourceId="com.txy.anywhere:id/iv_mapfrg_start_mock", className="android.widget.ImageView" )

        while obj1.exists:
            z.sleep(1)
            z.heartbeat()
            obj1.click()
        z.sleep(1)
        # d(index=1,resourceId="com.txy.anywhere:id/ll_content",className="android.widget.LinearLayout").child(index=0,className="android.widget.EditText",resourceId="com.txy.anywhere:id/et_input_lng").click()
        d(text="经度")
        z.input(x)
        z.sleep(2)
        z.heartbeat()
        # d( index=1, resourceId="com.txy.anywhere:id/ll_content", className="android.widget.LinearLayout" ).child(
        #     index=1, className="android.widget.EditText", resourceId="com.txy.anywhere:id/et_input_lng" ).click()
        d(text="纬度").click()
        z.input( y )
        z.heartbeat()
        z.sleep(2)
        d(text="确定",resourceId="com.txy.anywhere:id/btn_positive").click()
        z.sleep(random.randint(3,5))
        if obj3.exists:
            obj3.click( )
            z.sleep( 1 )
            z.heartbeat( )
            d.click( 100, 100 )
            z.toast("模块完成")
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return TxyLocationByCoordinate


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
    args = {"repo_address_id": "225","time_delay": "3","time":"60"}  # repo_name_id:QQ修改昵称仓库号，birthday_ xxx :年龄范围
    o.action( d, z, args )
    # a = o.WebViewBlankPages(d)
    # print(a)


