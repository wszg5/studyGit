# coding:utf-8
import colorsys
import os

from PIL import Image
from smsCode import smsCode
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice

class NewMobilqqAddByAddressListII:

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

    def action(self, d,z, args):

        z.toast("开始执行：普通QQ通讯录加好友单选")
        self.scode = smsCode( d.server.adb.device_serial( ) )
        gender1 = args['gender']
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(10)
        z.heartbeat()
        if not d(text='消息', resourceId='com.tencent.mobileqq:id/name').exists:  # 到了通讯录这步后看号有没有被冻结
            return 2
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
            d(text='关闭').click()
            z.sleep(1)
        if d(text='主题装扮').exists:
            d(text='关闭').click()
        if d(text='马上绑定').exists:
            d(text='关闭').click()
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
                if j > 20:
                    z.toast('取不到手机号码')
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
                return
            z.sleep(7)
        if d(textContains='没有可匹配的').exists:
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
                return
        t = 0
        b = 0
        alreadyUsePhoneNumList = []
        EndIndex = int( args['EndIndex'] )
        while True:
            phoneNumList = []
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
                        phoneNumList.append( phoneNum )
            phoneNumList = list( set( phoneNumList ) )
            phoneNumList = list( set( phoneNumList ).difference( set( alreadyUsePhoneNumList ) ) )
            phoneNumList = sorted( phoneNumList )

            if len( phoneNumList ) == 0:
                if b > 3:
                    z.toast( "通讯录号码全部加完" )
                    break
                d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
                b += 1
                continue

            cate_id = args["repo_material_id"]
            Material = self.repo.GetMaterial( cate_id, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']  # 取出验证消息的内容
            z.sleep( 1 )
            z.heartbeat( )

            for number in phoneNumList:
                if t == EndIndex:
                    break
                if d( text=number ).exists:
                    alreadyUsePhoneNumList.append( number )  # 将已点击过的号码，暂时存放到新集合里
                    d( text=number ).click( )
                    z.sleep( 6 )
                    z.heartbeat( )

                    JudgeGender = d( className='android.widget.LinearLayout', index=1 ).child(
                        className='android.view.View',
                        resourceId='com.tencent.mobileqq:id/icon',
                        index=0 )
                    if JudgeGender.exists:
                        genderStr = \
                            d( className='android.widget.AbsListView' ).child( className='android.widget.LinearLayout',
                                                                               index=1 ).child(
                                className='android.widget.LinearLayout',
                                resourceId='com.tencent.mobileqq:id/name' ).child(
                                className='android.widget.LinearLayout', index=0 ).child(
                                className='android.widget.LinearLayout', index=1 ).child(
                                className='android.widget.TextView', resourceId='com.tencent.mobileqq:id/info',
                                index=1 ).info['text']
                        gender2 = genderStr[0]

                    if gender1 != '不限':
                        if gender1 == gender2:  # gender1是外界设定的，gender2是读取到的
                            d( text='加好友' ).click( )
                            z.sleep( 5 )
                            z.heartbeat( )
                            if d( text='加好友' ).exists and d( text='QQ电话' ).exists and d( text='发消息' ).exists:
                                break
                        else:
                            d( textContains='返回' ).click( )
                    else:
                        d( text='加好友' ).click( )
                        z.sleep( 5 )
                        z.heartbeat( )
                        if d( text='加好友' ).exists and d( text='QQ电话' ).exists and d( text='发消息' ).exists:
                            break

                    if d( textContains='添加好友' ).exists:
                        if not d( textContains='问题' ).exists:
                            obj = d( resourceId='com.tencent.mobileqq:id/name', className='android.widget.EditText',
                                     index=4 ).info[
                                'text']  # 将之前消息框的内容删除
                            lenth = len( obj )
                            mn = 0
                            while mn < lenth:
                                d.press.delete( )
                                mn = mn + 1
                            z.input( message )
                            z.sleep( 2 )
                            d( text='发送' ).click( )
                            t = t + 1
                            z.sleep( 3 )
                            if d( text='请求发送失败' ).exists:
                                d( text='确定' ).click( )
                                z.sleep( 1.5 )
                            d( textContains='返回' ).click( )
                        else:
                            d( textContains='取消' ).click( )
                            z.sleep( 3 )
                            d( textContains='返回' ).click( )

            if t == EndIndex:
                z.toast( "已经加满你设置的好友数，共" + args['EndIndex'] + "个" )
                break

            if d( text='加好友' ).exists and d( text='QQ电话' ).exists and d( text='发消息' ).exists:
                z.toast("此号今日已不能添加好友")
                break


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return NewMobilqqAddByAddressListII

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
    args = {"repo_material_id": "39", 'gender': "男", 'EndIndex': '5', "time_delay": "3"};  # cate_id是仓库号，length是数量
    o.action(d, z, args)



























