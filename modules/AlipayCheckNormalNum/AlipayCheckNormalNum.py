# coding:utf-8
from uiautomator import Device
from Repo import *
from zservice import ZDevice
from smsCode import smsCode

class AlipayCheckNormalNum:
    def __init__(self):
        self.repo = Repo()
        self.__apk_pkgname = 'com.eg.android.AlipayGphone'

    def CheckLogined(self,d, z ):
        z.toast( "检测是否已有支付宝帐号登录" )
        z.cmd("shell", "am force-stop com.eg.android.AlipayGphone")  # 强制停止
        z.cmd("shell", "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin")
        z.sleep(15)
        if d(textContains='口碑').exists:
            return True
        return False

    def action(self, d, z, args):
        z.heartbeat()
        if self.CheckLogined(d, z) :
            z.toast("检测到已经登录，结束运行")
            return

        z.toast( "没有检测到登陆帐号，继续运行" )
        z.sleep(1.5)
        z.generate_serial( "com.eg.android.AlipayGphone" )  # 随机生成手机特征码
        z.toast( "随机生成手机特征码" )

        repo_number_id = args["repo_number_id"] #取手机号的仓库
        repo_normal_id = args["repo_normal_id"] #保存正常号的仓库
        repo_frozen_id = args["repo_frozen_id"] #保存冻结号的仓库
        repo_not_exist_id = args["repo_not_exist_id"] #保存不存在号的仓库

        z.heartbeat( )
        d.server.adb.cmd( "shell", "pm clear com.eg.android.AlipayGphone" ).communicate( )  # 清除缓存
        d.server.adb.cmd( "shell",
                          "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin" ).communicate( )  # 拉起来

        while not d( resourceId='com.ali.user.mobile.security.ui:id/registerButton' ).exists:
            z.toast( "等待 新用户注册 按钮出现" )
            d.dump( compressed=False )
            z.sleep( 5 )

        if d( text='登录' ).exists:
            d( resourceId='com.ali.user.mobile.security.ui:id/loginButton' ).click( )
            z.sleep( 3 )

        while True:
            number_count = 1  # 每次取一个号码
            exist_numbers = self.repo.GetNumber( repo_number_id, 0, number_count, 'exist' )
            print( exist_numbers )
            remain = number_count - len( exist_numbers )
            normal_numbers = self.repo.GetNumber( repo_number_id, 0, remain, 'normal' )
            numbers = exist_numbers + normal_numbers
            if len( numbers ) > 0:
                PhoneNumber = numbers[0]['number']
            else:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，等待中\"" % repo_number_id ).communicate( )
                break

            if d( resourceId='com.ali.user.mobile.security.ui:id/userAccountInput' ).exists:
                d( resourceId='com.ali.user.mobile.security.ui:id/userAccountInput' ).click( )
            z.input( PhoneNumber )

            if d( text='忘记密码？' ).exists:
                d( text='忘记密码？' ).click( )

            while not d( text='找回登录密码' ).exists:
                z.toast( "等待页面出现" )
                d.dump( compressed=False )
                z.sleep( 3 )
                if d(text='加载失败').exists:
                    d( resourceId='com.alipay.mobile.nebula:id/h5_lv_nav_back_loading' ).click( )
                    break
            z.sleep( 5 )

            if d( description='下一步' ).exists:
                d( description='下一步' ).click( )

            z.sleep( 3 )
            if d( description='能', className='android.widget.Button' ).exists:
                self.repo.uploadPhoneNumber( PhoneNumber, repo_normal_id, "N" )
            elif d( text='确认' ).exists:
                d( text='确认' ).click( )
                self.repo.uploadPhoneNumber( PhoneNumber, repo_frozen_id, "N" )
            else:
                self.repo.uploadPhoneNumber( PhoneNumber, repo_not_exist_id, "N" )
            z.toast( "入库成功" )
            d( resourceId='com.alipay.mobile.nebula:id/h5_lv_nav_back_loading' ).click( )
            d( className='android.widget.EditText',resourceId='com.ali.user.mobile.security.ui:id/content').click( )
            d( description='清空输入内容', resourceId='com.ali.user.mobile.security.ui:id/clearButton').click( )

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
    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").wait()
    args = {"repo_number_id": "223", "repo_normal_id": "222","repo_frozen_id": "221", "repo_not_exist_id": "220", "time_delay": "3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)

