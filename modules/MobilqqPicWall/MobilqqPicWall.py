# coding:utf-8
from uiautomator import Device
import  time
from zservice import ZDevice

class MobilqqPicWall:

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)
        z.heartbeat()
        d(description='帐户及设置').click()
        d(descriptionContains='等级：').click()
        d(text='上传照片').click()
        d(text='从手机相册选择').click()
        z.sleep(3)
        for i in range(0,9):
            forclick = d(className='com.tencent.widget.GridView').child(className='android.widget.RelativeLayout',index=i).\
                child(className='android.widget.RelativeLayout',index=1).child(className='android.widget.CheckBox')
            if forclick.exists:
                forclick.click()
        z.heartbeat()

        d(textContains='确定').click()

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqPicWall

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)

