# coding:utf-8
import os

from uiautomator import Device
from Repo import *
from zservice import ZDevice
import logging
logging.basicConfig(level=logging.INFO)

class WXAssignSearchAddFriends:

    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath(__file__)

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(5)

        d(description='更多功能按钮',className='android.widget.RelativeLayout').click()
        z.sleep(1)
        if d(text='添加朋友').exists:
            d(text='添加朋友').click()
        else:
            d(description='更多功能按钮', className='android.widget.RelativeLayout').click()
            z.sleep(1)
            d(text='添加朋友').click()
        z.heartbeat()
        d(index='1',className='android.widget.TextView').click()   #点击搜索好友的输入框

        cate_id = int( args["repo_number_id"] )  # 得到取号码的仓库号
        number_count = int( args['get_number'] )  # 每次取一个号码
        while True:
            exist_numbers = self.repo.GetNumber( cate_id, 8888, number_count, 'exist' )
            remain = number_count - len( exist_numbers )
            normal_numbers = self.repo.GetNumber( cate_id, 8888, remain, 'normal' )
            numbers = exist_numbers + normal_numbers
            if len( numbers ) > 0:
                break
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，结束运行\"" % cate_id ).communicate( )
            z.sleep( 30 )
        if len( numbers ) <= 0:
            return

        for i in range(len(numbers)):

            WXnumber = numbers[i]['number']
            z.input( WXnumber )
            z.heartbeat( )
            z.sleep( 3 )
            d( textContains='搜索:' ).click( )
            while d(textContains='正在查找联系人').exists:
                z.sleep(2)

            if d( textContains='操作过于频繁' ).exists:
                continue
                # return
            z.sleep( 2 )
            if d( textContains='用户不存在' ).exists:
                d( descriptionContains='清除', index=2 ).click( )
                z.sleep( 1 )
                continue
            if d( textContains='状态异常' ).exists:
                d( descriptionContains='清除', index=2 ).click( )
                continue
            z.heartbeat( )

            if d( text='设置备注和标签' ).exists:
                d( text='设置备注和标签' ).click( )
                z.sleep( 3 )
                beizhuObj = d( className='android.widget.EditText', index=1 )
                if beizhuObj.exists:
                    deltext = beizhuObj.info  # 将之前消息框的内容删除
                    deltext = deltext['text']
                    lenth = len( deltext )
                    m = 0
                    while m < lenth:
                        d.press.delete( )
                        m = m + 1
                    z.input( WXnumber )
                    d( text='保存' ).click( )
                    z.sleep( 3 )

            z.heartbeat( )
            if d( text='添加到通讯录' ).exists:  # 存在联系人的情况
                d( text='添加到通讯录' ).click( )

                if d( text='发消息' ).exists:
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='清除' ).click( )
                    continue
                elif d( text='验证申请' ).exists:
                    d( text='发送' ).click( )
                    z.sleep( 2 )
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 2 )
                    d( descriptionContains='清除' ).click( )
                    continue
                else:
                    if d( text='取消' ).exists:
                        d( text='取消' ).click( )
                        d( descriptionContains='返回' ).click( )
                        z.sleep( 3 )
                        d( descriptionContains='清除' ).click( )
                        continue

                    if d( text='确定' ).exists:
                        d( text='确定' ).click( )
                        d( descriptionContains='返回' ).click( )
                        z.sleep( 3 )
                        d( descriptionContains='清除' ).click( )
                        continue

                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='清除' ).click( )
                    continue
            elif d( text='发消息' ).exists:
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='清除' ).click( )
                    continue

def getPluginClass():
    return WXAssignSearchAddFriends

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "131","get_number": "10"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
