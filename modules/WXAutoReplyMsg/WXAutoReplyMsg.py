# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from zcache import cache
import re
import logging
logging.basicConfig(level=logging.INFO)

class WXAutoReplyMsg:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)

        msg_count = int(args['msg_count'])

        while True:
            if d( text='发现' ).exists and d( text='我' ).exists and d( text='通讯录' ).exists:
                d(text='微信').click()
                break
            else:
                d( descriptionContains='返回', className='android.widget.ImageView' ).click( )
        z.sleep(2)
        if d(text='腾讯新闻').exists:
            d(text='腾讯新闻').long_click()
            z.sleep(2)
            if d( text='删除该聊天' ).exists:
                d( text='删除该聊天' ).click( )

        if d(text='微信团队').exists:
            d( text='微信团队' ).long_click()
            z.sleep( 2 )
            if d( text='删除该聊天' ).exists:
                d( text='删除该聊天' ).click( )

        i = 0
        while True:
            i = i + 1
            nearObj = d(className='android.widget.ListView', index=0).child(className='android.widget.LinearLayout', index=i).child(
                className='android.widget.RelativeLayout',index=0).child(className='android.widget.TextView', index=1)
            if nearObj.exists:
                nearObj.click()
                z.sleep(1.5)
                for i in range( 0, msg_count ):
                    cate_id = args["repo_material_id"]
                    Material = self.repo.GetMaterial( cate_id, 0, 1 )
                    if len( Material ) == 0:
                        d.server.adb.cmd( "shell",
                                          "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id ).communicate( )
                        z.sleep( 10 )
                        return
                    message = Material[0]['content']  # 取出发送消息的内容
                    d( className='android.widget.EditText' ).click( )
                    z.input( message )
                    z.sleep( 1 )
                    d( text='发送' ).click( )
                d( descriptionContains='返回' ).click()
                z.sleep(1.5)
                d( className='android.widget.ListView', index=0 ).child( className='android.widget.LinearLayout',
                                                                         index=i ).long_click()
                if d(text='删除该聊天').exists:
                    d(text='删除该聊天').click()
                z.sleep( 1 )
            else:
                if i > 18:
                    z.sleep(3)
                    i = 0
                continue


def getPluginClass():
    return WXAutoReplyMsg

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("5959d2f3")
    z = ZDevice("5959d2f3")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id": "200", "msg_count": "1"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
