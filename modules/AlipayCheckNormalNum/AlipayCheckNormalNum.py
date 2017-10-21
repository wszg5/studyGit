# coding:utf-8
import logging

from uiautomator import Device
from Repo import *
from zservice import ZDevice
from smsCode import smsCode

class AlipayCheckNormalNum:
    def __init__(self):
        self.repo = Repo()
        self.__apk_pkgname = 'com.eg.android.AlipayGphone'

    def action(self, d, z, args):
        z.toast("开始：支付宝检测手机号模块")
        z.generate_serial( "com.eg.android.AlipayGphone" )  # 随机生成手机特征码
        z.toast( "随机生成手机特征码" )

        repo_number_id = args["repo_number_id"]  # 取手机号的仓库
        repo_normal_id = args["repo_normal_id"]  # 保存正常号的仓库
        repo_frozen_id = args["repo_frozen_id"]  # 保存冻结号的仓库
        repo_not_exist_id = args["repo_not_exist_id"]  # 保存不存在号的仓库

        z.heartbeat()
        d.server.adb.cmd( "shell", "pm clear com.eg.android.AlipayGphone" ).communicate( )  # 清除缓存
        z.sleep(1)
        d.server.adb.cmd( "shell",
                          "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin" ).communicate( )  # 拉起来

        z.sleep(2)
        while not d( resourceId='com.ali.user.mobile.security.ui:id/registerButton' ).exists:
            z.toast( "等待 新用户注册 按钮出现" )
            d.dump( compressed=False )
            z.sleep( 5 )
        z.sleep(3)
        z.heartbeat()

        if d( text='登录' ).exists:
            d( resourceId='com.ali.user.mobile.security.ui:id/loginButton' ).click( )
            z.sleep( 3 )

        while True:
            if not d( text='手机号/邮箱/淘宝会员名' ).exists:
                d( className='android.widget.EditText',
                   resourceId='com.ali.user.mobile.security.ui:id/content' ).click( )
                d( description='清空输入内容', resourceId='com.ali.user.mobile.security.ui:id/clearButton' ).click( )
            z.heartbeat( )
            number_count = 1  # 每次取一个号码
            exist_numbers = self.repo.GetNumber( repo_number_id, 120, number_count, 'exist', 'NO')
            print( exist_numbers )
            remain = number_count - len( exist_numbers )
            unknown_numbers = self.repo.GetNumber( repo_number_id, 120, remain, 'unknown', 'NO' )
            numbers = exist_numbers + unknown_numbers
            if len( numbers ) > 0:
                PhoneNumber = numbers[0]['number']
            else:
                normal_numbers = self.repo.GetNumber( repo_number_id, 120, number_count, 'normal', 'NO' )
                if len(normal_numbers) == 0:
                    d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，等待中\"" % repo_number_id ).communicate( )
                    break
                else:
                    PhoneNumber = normal_numbers[0]['number']
            self.repo.uploadNumberALiPay( PhoneNumber, repo_number_id, "unknown" )

            try:
                if d( resourceId='com.ali.user.mobile.security.ui:id/userAccountInput' ).exists:
                    d( resourceId='com.ali.user.mobile.security.ui:id/userAccountInput' ).click( )
                z.input( PhoneNumber )

                if d( text='忘记密码？' ).exists:
                    d( text='忘记密码？' ).click( )

                while not d( text='找回登录密码' ).exists:
                    z.toast( "等待页面出现" )
                    try:
                        d.dump(compressed=False)
                    except:
                        logging.exception("exception")
                    z.sleep( 3 )
                    if d( text='加载失败' ).exists:
                        d( resourceId='com.alipay.mobile.nebula:id/h5_tv_nav_back' ).click( )
                        break
                z.sleep( 5 )
                z.heartbeat()

                if d( description='下一步' ).exists:
                    d( description='下一步' ).click( )

                z.sleep( 5 )
                z.heartbeat()
                if d( description='能', className='android.widget.Button' ).exists:
                    self.repo.uploadPhoneNumber( PhoneNumber, repo_normal_id, "N" )
                    self.repo.uploadNumberALiPay(PhoneNumber, repo_number_id, "normal_exist")
                elif d( textContains='账户处于冻结状态' ).exists:
                    d( text='确认' ).click( )
                    self.repo.uploadPhoneNumber( PhoneNumber, repo_frozen_id, "N" )
                    self.repo.uploadNumberALiPay( PhoneNumber, repo_number_id, "frozen" )
                elif d(text='找回淘宝密码').exists:
                    d(text='取消').click()
                    self.repo.uploadPhoneNumber( PhoneNumber, repo_not_exist_id, "N" )
                    self.repo.uploadNumberALiPay( PhoneNumber, repo_number_id, "not_exist" )
                elif d( description='下一步',className='android.widget.Button').exists:
                    self.repo.uploadPhoneNumber( PhoneNumber, repo_not_exist_id, "N" )
                    self.repo.uploadNumberALiPay( PhoneNumber, repo_number_id, "not_exist" )
                else:
                    self.repo.uploadNumberALiPay( PhoneNumber, repo_number_id, "unknown" )
                z.toast( "入库成功" )
                for num in range( 1, 2 ):
                    d( resourceId='com.alipay.mobile.nebula:id/h5_tv_nav_back' ).click( )
                    if d( text='登录' ).exists:
                        z.sleep(1)
                        break
                d( className='android.widget.EditText',
                   resourceId='com.ali.user.mobile.security.ui:id/content' ).click( )
                d( description='清空输入内容', resourceId='com.ali.user.mobile.security.ui:id/clearButton' ).click( )
                if not d(text='手机号/邮箱/淘宝会员名').exists:
                    d( className='android.widget.EditText',
                       resourceId='com.ali.user.mobile.security.ui:id/content' ).click( )
                    d( description='清空输入内容', resourceId='com.ali.user.mobile.security.ui:id/clearButton' ).click( )
            except:
                logging.exception("exception")
                logging.error("error")
                self.repo.uploadNumberALiPay( PhoneNumber, repo_number_id, "unknown" )


        if (args["time_delay"]):
            z.sleep( int( args["time_delay"] ) )


def getPluginClass():
    return AlipayCheckNormalNum

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A1SK02114")
    z = ZDevice("HT4A1SK02114")
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").wait()
    args = {"repo_number_id": "223", "repo_normal_id": "222","repo_frozen_id": "221", "repo_not_exist_id": "220", "time_delay": "3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)

