# coding:utf-8
import util
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *

class WXCheckDepostNormalNumber:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        z.heartbeat()
        self.scode = smsCode( d.server.adb.device_serial( ) )
        logger = util.logger

        runLock = int( args['run_lock'] )
        cateId = args['repo_can_use_number_id']
        logger.info(cateId)
        cateType = 'information'
        totalList = self.repo.GetNUmberNormalTotal( cateId,cateType )
        normalTotal = int( totalList[0]['total'] )



        if normalTotal < runLock:
            z.toast( '库内未使用号码低于' + args['run_lock'] + '，开始拉号码' )

            str = d.info  # 获取屏幕大小等信息
            height = str["displayHeight"]
            width = str["displayWidth"]
            d.press.home( )

            while True:
                if d( text='微信' ).exists:
                    d( text='微信' ).click( )
                    break
                d.swipe( width - 20, height / 2, 0, height / 2, 5 )

            while True:
                if d( text='发现' ) and d( text='我' ) and d( text='通讯录' ).exists:
                    break
                elif d(text='立刻安装').exists:
                    z.toast("出现更新弹框")
                    d(textContains='取消').click()
                    z.sleep(1.5)
                    d(text='是').click()
                else:
                    d( descriptionContains='返回', className='android.widget.ImageView' ).click( )
            d( description='更多功能按钮' ).click( )
            z.sleep( 1 )
            if d( text='添加朋友' ).exists:
                d( text='添加朋友' ).click( )
            else:
                d( description='更多功能按钮', className='android.widget.RelativeLayout' ).click( )
                z.sleep( 1 )
                d( text='添加朋友' ).click( )
            d( index='1', className='android.widget.TextView' ).click( )  # 点击搜索好友的输入框
            z.heartbeat( )

            lock_count = 0
            while True:
                lock_count = lock_count + 1
                if lock_count > int( args['check_count'] ):
                    z.toast( '成功检存' + args['check_count'] + '次，结束' )
                    break

                while True:
                    WXnumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER)  # 获取接码平台手机号码
                    if WXnumber is not None:
                        z.sleep(3)
                        self.scode.defriendPhoneNumber( WXnumber, self.scode.WECHAT_REGISTER )  # 拉黑
                        break
                z.input(WXnumber)
                d( textContains='搜索:' ).click( )
                z.heartbeat( )
                while d( textContains='正在查找' ).exists:
                    z.sleep( 2 )
                z.heartbeat( )
                if d( textContains='操作过于频繁' ).exists:
                    repo_check_frequency_id = args['repo_check_frequency_id']
                    self.repo.uploadPhoneNumber(WXnumber, repo_check_frequency_id )
                    if d( descriptionContains='清除', index=2 ).exists:
                        d( descriptionContains='清除', index=2 ).click( )
                    else:
                        d(resourceId='com.tencent.mm:id/b2q',index=2).click()

                    z.sleep( 1 )
                    # z.toast('操作过于频繁,模块停止运行')
                    continue

                z.sleep( 1 )
                if d( textContains='用户不存在' ).exists:
                    para = {"phoneNumber": WXnumber, 'x_01': "notExist", 'x_07': '2000-01-01 00:00:00', 'x_19': 'CheckXunMa'}
                    self.repo.PostInformation( cateId, para )
                    if d( descriptionContains='清除', index=2 ).exists:
                        d( descriptionContains='清除', index=2 ).click( )
                    else:
                        d(resourceId='com.tencent.mm:id/b2q',index=2).click()
                    z.sleep( 1 )
                    continue
                if d( textContains='状态异常' ).exists:
                    repo_exception_id = args['repo_exception_id']
                    self.repo.uploadPhoneNumber( WXnumber,repo_exception_id )
                    if d( descriptionContains='清除', index=2 ).exists:
                        d( descriptionContains='清除', index=2 ).click( )
                    else:
                        d(resourceId='com.tencent.mm:id/b2q',index=2).click()
                    z.sleep(1)
                    continue
                z.heartbeat( )
                if d( text='详细资料' ).exists:
                    para = {"phoneNumber": WXnumber, 'x_01': "normalExist", 'x_07': '2000-01-01 00:00:00', 'x_19': 'CheckXunMa'}
                    self.repo.PostInformation( cateId, para )
                    d( descriptionContains='返回' ).click( )
                    if d( descriptionContains='清除', index=2 ).exists:
                        d( descriptionContains='清除', index=2 ).click( )
                    else:
                        d(resourceId='com.tencent.mm:id/b2q',index=2).click()
                    z.sleep( 1 )
        else:
            z.toast( '库内未使用号码大于' + args['run_lock'] + '，模块无法运行' )



def getPluginClass():
    return WXCheckDepostNormalNumber

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AVSK00885")
    z = ZDevice("HT4AVSK00885")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_can_use_number_id": "210",'repo_exception_id': '189','repo_check_frequency_id': '190', "run_lock": "500", "check_count": "100"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
