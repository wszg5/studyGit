# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WeiXinMoments:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()  # 将微信拉起来
        time.sleep(7)

        z.wx_action('opensnsui')
        time.sleep(3)
        myname = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=0).child(
            className='android.widget.TextView').info
        myname = myname['text']
        d.swipe(width / 2, height * 4 / 5, width / 2, height / 4)
        time.sleep(1)

        i = 0
        t = 0
        EndIndex = int(args['EndIndex'])         #------------------
        while t < EndIndex :
            cate_id = args["repo_material_id"]   #------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            try:
                Material = Material[0]['content']  # 从素材库取出的要发的材料
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()

            obj = d(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=i).child(className='android.widget.FrameLayout').child(description='评论')   #首先看第i个人是否存在，
            if obj.exists:
                obj1 = d(className='android.widget.ListView').child(className='android.widget.FrameLayout', index=i).child(className='android.widget.LinearLayout',index=4)    #判断该好友是否有点赞评论
                if obj1.exists:  #给该好友评论的情况
                    getName = d(className='android.widget.FrameLayout', index=i).child(className='android.widget.LinearLayout',index=4).child(index=0,className='android.widget.TextView')
                    if getName.exists:
                        getName = getName.info
                        getName = getName['text']
                        if myname in getName:
                            i = i + 1
                            continue

                obj2 = d(className='android.widget.ListView').child(className='android.widget.FrameLayout', index=i).child(className='android.widget.LinearLayout',index=3)    #判断该好友是否有点赞评论,没有图片index会少一个
                if obj2.exists:  #给该好友评论的情况
                    getName1 = d(className='android.widget.FrameLayout', index=i).child(className='android.widget.LinearLayout',index=3).child(index=0,className='android.widget.TextView')
                    if getName1.exists:
                        getName1 = getName1.info
                        getName1 = getName1['text']
                        if myname in getName1:
                            i = i + 1
                            continue

                obj.click()
                if d(text='赞').exists:
                    d(text='赞').click()
                    time.sleep(0.5)
                else:                         #赞被屏幕遮住的情况
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    time.sleep(2)
                    if d(className='android.widget.FrameLayout', index=0).child(className='android.widget.FrameLayout', index='3').child(description='评论').exists:
                        i = 0
                    else:
                        i = 1
                    continue
                time.sleep(0.5)
                obj.click()
                d(text='评论').click()
                d(className='android.widget.EditText').click()
                z.input(Material)
                d(text='发送').click()
                i = i+1
                t = t+1
                continue
            else:

                obja = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=2).child(className='android.widget.LinearLayout')\
                    .child(className='android.widget.LinearLayout').child(className='android.widget.ImageView')
                if obja.exists:
                    return
                d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                time.sleep(2)
                obj = d(className='android.widget.ListView').child(className='android.widget.FrameLayout',
                                                                   index=0).child(
                    className='android.widget.FrameLayout').child(description='评论')
                if obj.exists:
                    i = 0
                    continue
                else:
                    i = 1
                    continue
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return WeiXinMoments

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()

    args = {"repo_material_id": "36",'EndIndex':'100',"time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)






