# coding:utf-8
from uiautomator import Device
from Repo import *
from zservice import ZDevice
import logging


#logging.basicConfig(level=logging.INFO)

class MobilqqMassTextII:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(6)
        if not d(text='消息').exists:  # 到了通讯录这步后看号有没有被冻结
            return 2
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
            d(text='关闭').click()
            z.sleep(1)

        d(className='android.widget.TabWidget', resourceId='android:id/tabs').child(
            className='android.widget.FrameLayout').child(className='android.widget.RelativeLayout').click()  # 点击到联系人
        z.sleep(4)

        z.heartbeat()
        if d(text='主题装扮').exists:
            d(text='关闭').click()
        if d(text='马上绑定').exists:
            d(text='关闭').click()

        d(className='android.widget.HorizontalScrollView').child(text='群').click()

        i = 2    #用来点击
        t = 0    #统计发送的人数
        set1 = set()
        gg = 0   #判断结束的条件
        EndIndex = int(args['EndIndex'])
        picnumber = int(args['picnumber'])   #发图片的个数
        while t<EndIndex:
            z.sleep( 1 )
            z.heartbeat( )
            if not d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=2).exists:   #看第一个群是否存在，如果不存在，则一个群都不存在
                z.toast('没有群存在')
                z.sleep(2)
                return
            clickinfo = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i).\
                child(className='android.widget.LinearLayout',index=1).child(className='android.widget.TextView')

            if clickinfo.exists:
                massname = clickinfo.info['text']
                if massname in set1:
                    i = i+1
                    continue
                else:
                    set1.add(massname)
                    logging.info(massname)
                    clickinfo.click()

                    z.sleep(1)
                    while not d(description='群资料卡').exists:
                        z.sleep(1)
                    if d(text='全员禁言中').exists:
                        d.press.back()
                        d( className='android.widget.TabWidget', resourceId='android:id/tabs' ).child(
                            className='android.widget.FrameLayout' ).child(
                            className='android.widget.RelativeLayout' ).click( )  # 点击到联系人
                        i = i+1
                        continue

                    try:
                        d(className='android.widget.RelativeLayout',index=0).child(className='android.widget.LinearLayout',index=5).\
                            child(className='android.widget.ImageView',index=1).click()  #点击图片按钮
                    except Exception:
                        d( className='android.widget.RelativeLayout', index=0 ).child(
                            className='android.widget.LinearLayout', index=6 ). \
                            child( className='android.widget.ImageView', index=1 ).click( )  # 点击图片按钮

                    judexist = d(className='android.widget.RelativeLayout',index=1).child(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=0)
                    if not judexist.exists:    #判断是否有图片
                        z.toast('没有图片')
                        z.sleep(2)
                        return
                    '''
                    发图片部分
                    '''
                    picsize = d( className='android.widget.RelativeLayout', index=1 ).child(
                        className='android.widget.AbsListView' ).info['bounds']      #得到图片的大小，为后面的滑动做准备
                    logging.info( picsize )
                    pictop = int( picsize['top'] )
                    picbottom = int( picsize['bottom'] )
                    picright = int( picsize['right'] ) - 10
                    hight = pictop + (picbottom - pictop) / 2
                    endcon = 0  # 判断滑动后是否还有图片
                    countpic = 0  # 用来点击图片
                    sentpic = 0  # 统计发送图片的个数
                    while sentpic < picnumber:
                        picclick = d( className='android.widget.RelativeLayout', index=1 ).child(
                            className='android.widget.AbsListView' ). \
                            child( className='android.widget.RelativeLayout', index=countpic ). \
                            child( className='android.widget.CheckBox', checked='false' )
                        if picclick.exists:
                            endcon = 1
                            picclick.click( )
                            sentpic = sentpic + 1
                            countpic = countpic + 1
                        else:
                            if countpic != 6:  # 为了解决滑动之后前一两个已被选定的情况
                                countpic = countpic + 1
                                continue
                            if endcon == 0:
                                z.toast( '没有更多图片' )
                                break
                            d.swipe( picright, hight, 0, hight )
                            z.sleep( 2 )
                            endcon = 0
                            countpic = 0

                    #d(className='android.widget.LinearLayout',index=1).child(textContains='发送').click()
                    gg = 1
                    d.press.back( )
                    d.press.back( )
                    d( className='android.widget.TabWidget', resourceId='android:id/tabs' ).child(
                        className='android.widget.FrameLayout' ).child(
                        className='android.widget.RelativeLayout' ).click( )  # 点击到联系人
                    i = i+1
                    t = t+1
                    continue
            else:
                if gg==0:
                    z.toast('全部发送完成')
                    z.sleep(2)
                    return
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 4 )
                z.sleep(3)
                gg = 0
                i = 1

        if (args["time_delay"]):
            z.sleep( int( args["time_delay"] ) )



def getPluginClass():
    return MobilqqMassTextII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4BLSK00255")
    z = ZDevice("HT4BLSK00255")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {'picnumber':'5','EndIndex':'30',"time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)












