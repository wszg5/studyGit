# coding:utf-8
from uiautomator import Device
import  time
from zservice import ZDevice

class MobilqqPicModify:

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)
        z.heartbeat()
        d(description='帐户及设置').click()
        z.sleep(1.5)
        d(descriptionContains='等级：').click()
        z.sleep( 5 )
        d( text='编辑资料' ).click( )
        z.sleep( 1.5 )
        if d( text='编辑资料' ).exists:
            d.press.back( )
            time.sleep( 1 )
            if d( text='编辑资料' ).exists:
                d( text='编辑资料' ).click( )
                time.sleep( 2 )
        z.sleep( 1.5 )
        d(text='头像').click()
        z.sleep(3)
        d(text='从相册选择图片').click()
        z.sleep(3)
        forclick = d( className='com.tencent.widget.GridView' ).child( className='android.widget.RelativeLayout',
                                                                       index=0 )
        if forclick.exists:
            forclick.click( )
        z.heartbeat()
        z.sleep(1.5)
        d(textContains='完成').click()
        z.sleep(5)
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqPicModify

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cc0e9474")
    z = ZDevice("cc0e9474")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)

