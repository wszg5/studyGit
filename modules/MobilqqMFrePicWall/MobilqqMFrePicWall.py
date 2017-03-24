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
        d(description='快捷入口').click()
        d(textContains='加好友').click()
        d(textContains='附近的人').click()
        while not d(textContains='等级').exists:
            z.sleep(2)
        d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=2).click()
        while not d(text='编辑交友资料').exists:
            time.sleep(2)
        d(text='编辑交友资料').click()
        if d(text='立即编辑').exists:
            d(text='立即编辑').click()
        d(className='android.widget.FrameLayout', index=3).child(className='android.widget.ImageView', index=1).click()
        d(textContains='从手机相册选择').click()

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
    # d(className='android.widget.RelativeLayout', index=1).child(className='android.widget.RelativeLayout',index=1).click()
    args = {"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)

