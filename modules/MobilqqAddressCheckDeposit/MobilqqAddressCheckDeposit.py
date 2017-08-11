# coding:utf-8
import colorsys
import os

from PIL import Image
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class MobilqqAddressCheckDeposit:

    def __init__(self):
        self.repo = Repo()
        self.xuma = None

    def GetUnique(self):
        nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" );  # 生成当前时间
        randomNum = random.randint( 0, 1000 );  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str( 00 ) + str( randomNum );
        uniqueNum = str( nowTime ) + str( randomNum );
        return uniqueNum

    def Gender(self, d, obj):

        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        if obj.exists:
            obj = obj.info
            obj = obj['bounds']  # 验证码处的信息
            left = obj["left"]  # 验证码的位置信息
            top = obj['top']
            right = obj['right']
            bottom = obj['bottom']

            d.screenshot( sourcePng )  # 截取整个输入验证码时的屏幕

            img = Image.open( sourcePng )
            box = (left, top, right, bottom)  # left top right bottom
            region = img.crop( box )  # 截取验证码的图片
            # show(region)    #展示资料卡上的信息
            image = region.convert( 'RGBA' )
            # 生成缩略图，减少计算量，减小cpu压力
            image.thumbnail( (200, 200) )
            max_score = None
            dominant_color = None
            for count, (r, g, b, a) in image.getcolors( image.size[0] * image.size[1] ):
                # 跳过纯黑色
                if a == 0:
                    continue
                saturation = colorsys.rgb_to_hsv( r / 255.0, g / 255.0, b / 255.0 )[1]
                y = min( abs( r * 2104 + g * 4130 + b * 802 + 4096 + 131072 ) >> 13, 235 )
                y = (y - 16.0) / (235 - 16)
                # 忽略高亮色
                if y > 0.9:
                    continue

                score = (saturation + 0.1) * count
                if score > max_score:
                    max_score = score
                    dominant_color = (r, g, b)  # 红绿蓝
            # print("---------------------------------------------------------------------------")
            # print(dominant_color)
            return dominant_color

    def Bind(self, d,z):
        circle = 0
        self.scode = smsCode( d.server.adb.device_serial( ) )
        newStart = 1
        while newStart == 1:
            GetBindNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )
            print( GetBindNumber )
            z.sleep( 2 )
            d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText' ).set_text(
                GetBindNumber )  # GetBindNumber
            z.heartbeat( )
            z.sleep( 1 )
            d( text='下一步' ).click( )
            z.sleep( 3 )
            if d( text='下一步' ).exists:  # 操作过于频繁的情况
                return 'false'

            if d( text='确定' ).exists:  # 提示该号码已经与另一个ｑｑ绑定，是否改绑,如果请求失败的情况
                d( text='确定', ).click( )
            z.heartbeat( )
            code = self.scode.GetVertifyCode( GetBindNumber, self.scode.QQ_CONTACT_BIND, '4' )
            d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText' ).set_text( code )
            print( code )
            newStart = 0
            if d( text='请输入短信验证码' ).exists:
                if circle < 4:
                    z.toast( '没有接收到验证码' )
                    d( textContains='返回' ).click( )
                    if d( text='确定' ).exists:
                        d( text='返回' ).click( )
                        z.sleep( 1 )
                    d( description='删除 按钮' ).click( )
                    circle = circle + 1
                    newStart = 1
                    continue
                else:
                    z.toast( '程序结束' )
                    print( circle )
                    return 'false'
            z.heartbeat( )
            d( text='完成', resourceId='com.tencent.mobileqq:id/name' ).click( )
            z.sleep( 10 )
            if d( textContains='没有可匹配的' ).exists:
                return 'false'

        return 'true'

    def bindPhoneNumber(self,z,d):
        z.toast( "点击开始绑定" )
<<<<<<< HEAD
<<<<<<< HEAD
        self.scode = smsCode( d.server.adb.device_serial( ) )
=======
>>>>>>> fc75ece82dfa7a15da2e8ec009f8387c3a7d2a50
=======
        self.scode = smsCode( d.server.adb.device_serial( ) )
>>>>>>> 4c63157369407566d32873cd3a6c7eb95f22cf16
        d( text='马上绑定' ).click( )
        while d( text='验证手机号码' ).exists:

            PhoneNumber = None
            j = 0
            while PhoneNumber is None:
                j += 1
                PhoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )  # 获取接码平台手机号码
                z.heartbeat( )
                if j > 20:
                    z.toast( '取不到手机号码' )
                    return "nothing"
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 4c63157369407566d32873cd3a6c7eb95f22cf16

            if not d( textContains='+86' ).exists:
                d( description='点击选择国家和地区' ).click( )
                if d( text='中国' ).exists:
                    d( text='中国' ).click( )
                else:
                    str = d.info  # 获取屏幕大小等信息
                    height = str["displayHeight"]
                    width = str["displayWidth"]
                    d.click(width * 5 / 12, height * 5 / 32)
                    z.sleep(1.5)
                    z.input('中国')
                    z.sleep(2)
                    d(text='+86').click()

<<<<<<< HEAD
=======
>>>>>>> fc75ece82dfa7a15da2e8ec009f8387c3a7d2a50
=======
>>>>>>> 4c63157369407566d32873cd3a6c7eb95f22cf16
            z.input( PhoneNumber )
            z.sleep( 1.5 )
            if d( text='下一步' ).exists:
                d( text='下一步' ).click( )
                z.sleep( 3 )
            if d( text='确定' ).exists:
                d( text='确定' ).click( )
                z.sleep( 2 )
            code = self.scode.GetVertifyCode( PhoneNumber, self.scode.QQ_CONTACT_BIND, '4' )  # 获取接码验证码
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_CONTACT_BIND )
            if code == '':
                z.toast( PhoneNumber + '手机号,获取不到验证码' )
                if d( text='返回' ).exists:
                    d( text='返回' ).click( )
                if not d( textContains='中国' ).exists:
                    if d( text='返回' ).exists:
                        d( text='返回' ).click( )
                if d( className='android.view.View', descriptionContains='删除' ).exists:
                    d( className='android.view.View', descriptionContains='删除' ).click( )
                continue
            z.heartbeat( )
            z.input( code )
            if d( text='完成' ).exists:
                d( text='完成' ).click( )
            z.sleep( 5 )
            break
        z.sleep( 1 )
    def action(self, d,z, args):
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：普通QQ通讯录匹配提取" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return

        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        cate_id = args['repo_number_id']

        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(10)
        z.heartbeat()

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 4c63157369407566d32873cd3a6c7eb95f22cf16
        loginStatusList = z.qq_getLoginStatus( d )
        if loginStatusList is None:
            z.toast( "登陆新场景，现无法判断登陆状态" )
            return
        loginStatus = loginStatusList['success']
        if loginStatus:
<<<<<<< HEAD
=======
        if d( text='消息' ).exists and d( text='联系人' ).exists and d( text='动态' ).exists:  # 到了通讯录这步后看号有没有被冻结
>>>>>>> fc75ece82dfa7a15da2e8ec009f8387c3a7d2a50
=======
>>>>>>> 4c63157369407566d32873cd3a6c7eb95f22cf16
            z.toast( "卡槽QQ状态正常，继续执行" )
        else:
            z.toast( "卡槽QQ状态异常，跳过此模块" )
            return

<<<<<<< HEAD
<<<<<<< HEAD
=======
        if not d(text='消息', resourceId='com.tencent.mobileqq:id/name').exists:  # 到了通讯录这步后看号有没有被冻结
            return 2
>>>>>>> fc75ece82dfa7a15da2e8ec009f8387c3a7d2a50
=======
>>>>>>> 4c63157369407566d32873cd3a6c7eb95f22cf16
        if d( text='马上绑定' ).exists:
            result = self.bindPhoneNumber(z,d)
            if result == "nothing":
                return
        if d(text='主题装扮').exists:
            d(text='关闭').click()
        if d(text='马上绑定').exists:
            result = self.bindPhoneNumber( z, d )
            if result == "nothing":
                return
        if d(text='通讯录').exists:
            d(text='关闭').click()
        d(description='快捷入口').click()
        d(textContains='加好友').click()
        d(text='添加手机联系人').click()
        z.heartbeat()
        while d(text='验证手机号码').exists:

            PhoneNumber = None
            j = 0
            while PhoneNumber is None:
                j += 1
                PhoneNumber = self.scode.GetPhoneNumber( self.scode.QQ_CONTACT_BIND )  # 获取接码平台手机号码
                z.heartbeat()
                if j > 2:
                    z.toast('取不到手机号码')
                    if (args["time_delay"]):
                        z.sleep( int( args["time_delay"] ) )
                    return
            z.input( PhoneNumber )
            z.sleep( 1.5 )
            if d( text='下一步').exists:
                d( text='下一步').click()
                z.sleep( 3 )
            if d(text='确定').exists:
                d(text='确定').click()
                z.sleep(2)
            code = self.scode.GetVertifyCode( PhoneNumber, self.scode.QQ_CONTACT_BIND, '4')  # 获取接码验证码
            self.scode.defriendPhoneNumber( PhoneNumber, self.scode.QQ_CONTACT_BIND )
            if code == '':
                z.toast( PhoneNumber + '手机号,获取不到验证码' )
                if d(text='返回').exists:
                    d(text='返回').click()
                if not d(textContains='中国').exists:
                    if d( text='返回' ).exists:
                        d( text='返回' ).click( )
                if d(className='android.view.View', descriptionContains='删除').exists:
                    d( className='android.view.View', descriptionContains='删除' ).click( )
                continue
            z.heartbeat( )
            z.input(code)
            if d(text='完成').exists:
                d(text='完成').click()
            z.sleep(5)
            break

        if d(resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',index=2).exists:  # 检查到尚未 启用通讯录
            if d(text=' +null', resourceId='com.tencent.mobileqq:id/name').exists:
                d(text=' +null', resourceId='com.tencent.mobileqq:id/name').click()
                d(text='中国', resourceId='com.tencent.mobileqq:id/name').click()
            z.heartbeat()
            text = self.Bind(d,z)  # 未开启通讯录的，现绑定通讯录
            z.heartbeat()
            if text == 'false':  # 操作过于频繁的情况
                if (args["time_delay"]):
                    z.sleep( int( args["time_delay"] ) )
                return
            z.sleep(7)
        if d(textContains='没有可匹配的').exists:
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        if d(text='匹配手机通讯录').exists:
            d(text='匹配手机通讯录').click()
        z.heartbeat()
        z.sleep(5)

        obj1 = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                  index=2 ) \
            .child( className='android.widget.ImageView', index=0 )  # 判断第一次进通讯录是否有人
        if not obj1.exists:
            d(text='返回').click()
            z.sleep(1.5)
            d(text='添加手机联系人').click()
            if not obj1.exists:
                z.toast("该手机上没有联系人")
                if (args["time_delay"]):
                    z.sleep( int( args["time_delay"] ) )
                return

        overNumber1 = None
        while True:
            overNumber2 = None
            for k in range( 1, 15 ):
                obj2 = d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                          index=k ) \
                    .child( className='android.widget.ImageView', index=0 )  # 第i个内容存在并且是人的情况
                if obj2.exists:
                    getPhoneInfo = d( className='android.widget.AbsListView', resourceId='com.tencent.mobileqq:id/name',
                                      index=0 ).child(
                        className='android.widget.LinearLayout', index=k ).child(
                        className='android.widget.RelativeLayout', index=0 ).child(
                        className='android.widget.LinearLayout', index=1 ).child(
                        className='android.widget.TextView', index=0 )
                    if getPhoneInfo.exists:
                        phoneNum = getPhoneInfo.info['text']
                        self.repo.uploadPhoneNumber(phoneNum, cate_id)
                        overNumber2 = phoneNum

            if overNumber1 == overNumber2:
                z.toast("通讯录号码提取完毕，模块结束运行")
                break
            else:
                overNumber1 = overNumber2
                d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
                continue


        if (args["time_delay"]):
            z.sleep( int( args["time_delay"] ) )

def getPluginClass():
    return MobilqqAddressCheckDeposit

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A6SK01638")
    z = ZDevice("HT4A6SK01638")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "209", "time_delay": "3"};  # cate_id是仓库号，length是数量
    o.action(d, z, args)



























