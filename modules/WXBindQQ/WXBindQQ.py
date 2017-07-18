# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXBindQQ:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(15)
        if d(text='我').exists:
           for i in range(1,3):
               d( text='我' ).click()
        z.sleep(3)
        d(text='设置').click()
        z.sleep( 3 )
        d(textContains='帐号与安全').click()
        z.sleep( 3 )
        d(text='QQ号').click()
        z.sleep(3)
        if not d(text='开始绑定').exists:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"该微信已绑定QQ号\"" ).communicate()
            d(descriptionContains='更多',className='android.widget.TextView').click()
            if d(text='解除绑定').exists:
                d( text='解除绑定' ).click()
                z.sleep(2)

            if d(text='开始解绑QQ').exists:
                d( text='开始解绑QQ' ).click()
                z.sleep(1.5)
            if d(text='确定解绑QQ?').exists:
                d(text='确定').click()
                z.sleep(2)
            d( text='QQ号' ).click()
            z.sleep( 3 )

        z.heartbeat( )
        cate_id = args["repo_cate_id"]
        time_limit = args['time_limit']
        numbers = self.repo.GetAccount( cate_id, time_limit, 1 )
        if len( numbers ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码%s号仓库为空，等待中\"" % cate_id ).communicate( )
            z.sleep(10)
            return
        QQNumber = numbers[0]['number']  # 即将登陆的QQ号
        QQPassword = numbers[0]['password']
        z.sleep( 1 )
        z.heartbeat( )
        d( text='开始绑定' ).click( )
        d( text='QQ号' ).set_text( QQNumber )
        d( className='android.widget.EditText', index=2 ).set_text( QQPassword )
        d( text='完成' ).click( )
        z.sleep( 3 )
        z.heartbeat( )

        while d( text='帐号或密码错误，请重新填写。' ).exists:
            d( text='确定' ).click( )
            editQQNumberObj = d( className='android.widget.EditText', index=0 )
            editQQPasswordObj = d( className='android.widget.EditText', index=2 )
            if editQQNumberObj.exists and editQQPasswordObj.exists:
                editQQPasswordObj.click( )
            else:
                d.click( 320, 230 )
            QQPasswordObj = \
                d( resourceId='com.tencent.mm:id/se', className='android.widget.EditText', index=2 )
            if QQPasswordObj.exists:
                QQPasswordObj.clear_text( )
            else:
                editQQPasswordObj.clear_text( )

            z.sleep( 2 )

            if editQQNumberObj.exists and editQQPasswordObj.exists:
                editQQNumberObj.click( )
            else:
                d.click( 320, 160 )

            QQNumberObj = \
                d( resourceId='com.tencent.mm:id/sd', className='android.widget.EditText', index=0 )
            if QQNumberObj.exists:
                QQNumberObj.clear_text( )
            else:
                editQQNumberObj.clear_text( )

            cate_id = args["repo_cate_id"]
            time_limit = args['time_limit']
            numbers = self.repo.GetAccount( cate_id, time_limit, 1 )
            if len( numbers ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码%s号仓库为空，等待中\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            QQNumber = numbers[0]['number']  # 即将登陆的QQ号
            QQPassword = numbers[0]['password']
            z.sleep( 1 )
            z.heartbeat( )
            d( text='QQ号' ).set_text( QQNumber )
            d( className='android.widget.EditText', index=2 ).set_text( QQPassword )
            d( text='完成' ).click( )
            z.sleep( 3 )
            if d( textContains='过于频繁' ).exists:
                break

        if d( text='已绑定。' ).exists:
            d( text='确定' ).click( )
            repo_bindQQ_id = args['repo_bindQQ_id']
            NUM_INFO = self.repo.GetInformationByDevice( repo_bindQQ_id, d.server.adb.device_serial( ) )
            phoneNumber = NUM_INFO[0]['phonenumber']
            BindQQ = QQNumber + ',' + QQPassword
            para = {"phoneNumber": phoneNumber, 'x_19': 'WXRegister', 'x_21': BindQQ}
            self.repo.PostInformation( repo_bindQQ_id, para )

        if d( textContains='过于频繁' ).exists:
            d( text='确定' ).click( )
            return

        if (args["time_delay"]):
            z.sleep( int( args["time_delay"] ) )



def getPluginClass():
    return WXBindQQ

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("9ef40375")
    z = ZDevice("9ef40375")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_cate_id": "132", "repo_bindQQ_id": "189", "time_limit": "0", "time_delay": "3"}   #cate_id是仓库号，length是数量
    o.action(d,z, args)