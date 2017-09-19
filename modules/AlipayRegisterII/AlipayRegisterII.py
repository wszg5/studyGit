# coding:utf-8
from uiautomator import Device
from Repo import *
from zservice import ZDevice
from smsCode import smsCode

class AlipayRegisterII:
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
            z.toast("检测到已经登录，跳过注册")
            return

        z.toast( "没有检测到登陆帐号，继续注册" )
        z.sleep(1.5)
        z.generate_serial( "com.eg.android.AlipayGphone" )  # 随机生成手机特征码
        z.toast( "随机生成手机特征码" )

        self.scode = smsCode(d.server.adb.device_serial())
        while True:
            z.heartbeat()
            d.server.adb.cmd("shell", "pm clear com.eg.android.AlipayGphone").communicate()  # 清除缓存
            d.server.adb.cmd("shell", "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin").communicate()  # 拉起来

            while not d(resourceId='com.ali.user.mobile.security.ui:id/registerButton').exists:
                z.toast("等待 新用户注册 按钮出现")
                d.dump(compressed=False)
                z.sleep(5)

            if d(text='登录').exists:
                d(resourceId='com.ali.user.mobile.security.ui:id/loginButton').click()
                z.sleep(3)


            PhoneNumber = self.scode.GetPhoneNumber( self.scode.ALIPAY_REGISTER )
            if PhoneNumber is None:
                z.toast( "取不到手机号" )
                break

            if d(text='忘记密码？').exists:
                d(text='忘记密码？').click()

            while not d(text='找回登录密码').exists:
                z.toast( "等待页面出现" )
                d.dump( compressed=False )
                z.sleep(3)

            z.sleep(5)
            if d(description='请输入手机号/邮箱', className='android.widget.EditText').exists:
                d(description='请输入手机号/邮箱', className='android.widget.EditText').click()
                z.input(PhoneNumber)
                z.sleep(8)


            if d(description='下一步').exists:
                d(description='下一步').click()
                z.sleep(3)

            if d(description='能', className='android.widget.Button').exists:
                d(description='能', className='android.widget.Button').click()
                z.sleep(8)

                if d(descriptionContains='验证码').exists:
                    code = self.scode.GetVertifyCode( PhoneNumber, self.scode.ALIPAY_REGISTER, '4' )  # 获取接码验证码
                    self.scode.defriendPhoneNumber( PhoneNumber, self.scode.ALIPAY_REGISTER )
                    if code == '':
                        z.toast("获取不到验证码")
                        continue
                    z.input( code )
                    z.sleep( 16 )
                    if d( descriptionContains='暂不设置' ).exists:
                        d( descriptionContains='暂不设置' ).click()
                        z.sleep( 10 )
                        if d( textContains='口碑' ).exists:
                            z.sleep( 5 )
                            if d( description='关闭', className='android.widget.ImageView' ).exists:
                                d( description='关闭', className='android.widget.ImageView' ).click( )
                            z.toast( "成功登陆支付宝" )
                            break
                    else:
                        z.input( '13141314abc' )
                        z.sleep( 1.5 )
                        d( description='保存新密码' ).click( )
                        z.sleep( 1.5 )
                        if d( text='确认' ).exists:
                            d( text='确认' ).click( )
                        z.sleep( 10 )
                        if d( textContains='口碑' ).exists:
                            z.sleep( 5 )
                            if d( description='关闭', className='android.widget.ImageView' ).exists:
                                d( description='关闭', className='android.widget.ImageView' ).click( )
                            z.toast( "成功登陆支付宝" )
                            break

                else:
                    z.toast( "登陆支付宝失败" )
                    self.scode.defriendPhoneNumber( PhoneNumber, self.scode.ALIPAY_REGISTER )
                    continue
            else:
                if d(text='确认').exists:
                    d(text='确认').click()
                z.toast( "登陆支付宝失败" )
                self.scode.defriendPhoneNumber( PhoneNumber, self.scode.ALIPAY_REGISTER )
                continue

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return AlipayRegisterII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").wait()
    args = {"time_delay": "3"};    #cate_id是仓库号，length是数量
    o.action(d, z,args)
    #  z.cmd( "shell", "am force-stop com.eg.android.AlipayGphone" )  # 强制停止
    # z.cmd( "shell", "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin" )
    # if d( description='暂不设置，先进入支付宝' ).exists:
    #     d( className='android.widget.EditText', index=0 ).click( )
    #     z.input( '13141314abc' )
    #     z.sleep( 1.5 )
    #     d( description='保存新密码' ).click( )
    #     z.sleep( 1.5 )
    #     if d( text='确定' ).exists:
    #         d( text='确定' ).click( )
    #     z.sleep( 10 )
    #     if d( textContains='口碑' ).exists:
    #         z.toast( "成功登陆支付宝" )