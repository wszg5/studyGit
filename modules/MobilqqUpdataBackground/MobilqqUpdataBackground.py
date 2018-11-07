# coding:utf-8
from uiautomator import Device
import  time
from zservice import ZDevice


class MobilqqUpdataBackground:

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
        d(descriptionContains='点击更换背景').click()
        z.sleep( 1.5 )
        if not d(text='从手机相册选择').exists:
            d.press.back()
            time.sleep(1)
            if d(descriptionContains='点击更换背景').exists:
                d( descriptionContains='点击更换背景' ).click( )
                time.sleep(1)
        d( text='从手机相册选择' ).click()
        time.sleep(3)
        obj = d( className='com.tencent.widget.GridView' ).child( className='android.widget.RelativeLayout',
                                                                  index=0 )
        if obj.exists:
            obj.click()
            time.sleep(1)
            d(resourceId='com.tencent.mobileqq:id/name', text='完成').click()
            time.sleep(3)
            while d(text='上传中').exists:
                time.sleep(3)
        else:
            z.toast("没有图片")
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqUpdataBackground

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cc0e9474")
    z = ZDevice("cc0e9474")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)
    # obj = d( className='com.tencent.widget.GridView' ).child( className='android.widget.RelativeLayout',
    #                                                           index=0 )
    # if obj.exists:
    #     obj.click( )
    #     time.sleep( 1 )
    #     d( resourceId='com.tencent.mobileqq:id/name', text='完成' ).click( )
    #     time.sleep( 3 )
    #     while d( text='上传中' ).exists:
    #         time.sleep( 3 )
    # else:
    #     z.toast( "没有图片" )
