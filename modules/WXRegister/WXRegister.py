# coding:utf-8
from uiautomator import Device
from Repo import *
from smsCode import smsCode
import time, string, datetime, random
from zservice import ZDevice
import util


class WeiXinRegister:
    def __init__(self):
        self.repo = Repo( )
        self.xm = None
        self.cache_phone_key = 'cache_phone_key'

    def GenPassword(self, numOfNum=4, numOfLetter=4):
        # 选中numOfNum个数字
        slcNum = [random.choice(string.digits) for i in range(numOfNum)]
        # 选中numOfLetter个字母
        slcLetter = [random.choice(string.lowercase) for i in range(numOfLetter)]
        slcChar = slcLetter + slcNum
        genPwd = ''.join([i for i in slcChar])
        return genPwd

    def action(self, d,z, args):
        z.heartbeat()
        Str = d.info  # 获取屏幕大小等信息
        height = Str["displayHeight"]
        width = Str["displayWidth"]
        saveCate = args['repo_information_id']
        self.scode = smsCode(d.server.adb.device_serial())
        logger = util.logger
        while True:
            nowTime = datetime.datetime.now( ).strftime( "%Y-%m-%d %H:%M:%S" );  # 生成当前时间
            NUM_INFO = self.repo.GetInformationByDevice( saveCate, d.server.adb.device_serial() )
            x26 = NUM_INFO[0]['x26']
            if x26 == '登陆状态YSE':
                z.toast('该设备已成功注册微信号')
                break
            d.press.home()
            d.server.adb.cmd("shell", "pm clear com.tencent.mm").communicate()  # 清除缓存，返回home页面

            while True:
                if d(text='微信').exists:
                    d(text='微信').click()
                    break
                d.swipe( width - 20, height / 2, 0, height / 2, 5 )

            z.sleep(8)
            z.heartbeat()
            if d(text='注册').exists:
                d(text='注册').click()
            cate_id = args['repo_material_id']  # 得到昵称库的id
            Material = self.repo.GetMaterial(cate_id, 0, 1)  # 修改昵称
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                z.sleep(10)
                return
            z.heartbeat()
            name = Material[0]['content']  # 从素材库取出的要发的材料
            z.input(name)       #name

            d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout', index=2).child(
                className='android.widget.EditText', index=1).click()
            d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout', index=2).child(
                className='android.widget.EditText', index=1).click.bottomright()
            z.heartbeat()


            information_cate_id = args['repo_information_id']
            numbers = self.repo.GetInformation(information_cate_id)
            if len(numbers) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"资料库%s号仓库为空，没有取到手机号\"" % information_cate_id ).communicate( )
                z.sleep(10)
                return
            z.heartbeat()

            number = numbers[0]['phonenumber']

            PhoneNumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER,number)#获取接码平台手机号码
            # PhoneNumber = '13923977280'

            if PhoneNumber is None:
                x_28 = int(numbers[0]['x28']) - 1
                para = {"phoneNumber": number, 'x_01': "not_exist", 'x_19': 'WXRegister','x_28': x_28}
                self.repo.PostInformation(saveCate, para)
                z.toast('讯码查不无此号')
                continue

            z.heartbeat()
            print(PhoneNumber)
            z.input(PhoneNumber)
            d(className='android.widget.LinearLayout',index=3).child(className='android.widget.EditText').click()
            d(textContains='密码').click()
            z.heartbeat()
            password = self.GenPassword()
            z.input(password)
            print(password)
            print('↑ ↑ ↑ ↑ ↑ ↑ ↑　↑  上面是手机＋密码 ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ')
            z.heartbeat()

            d(text='注册').click()
            z.sleep(3)

            d.dump( compressed=False )
            if d(textContains='操作太频繁，请稍后再试').exists:
                para = {"phoneNumber": PhoneNumber, 'x_03': nowTime, 'x_19': 'WXRegister'}
                self.repo.PostInformation( saveCate, para )

            d(text='确定').click()

            d.dump( compressed=False )
            if d(textContains='正在验证').exists:
                z.sleep(35)
            z.heartbeat()

            code = self.scode.GetVertifyCode(PhoneNumber, self.scode.WECHAT_REGISTER)#获取接码验证码
            self.scode.defriendPhoneNumber(PhoneNumber,self.scode.WECHAT_REGISTER)
            if code == '':
                x_02 = int(numbers[0]['x02']) - 1
                para = {"phoneNumber": PhoneNumber, 'x_02': x_02,'x_03':nowTime, 'x_19': 'WXRegister'}
                self.repo.PostInformation( saveCate, para )
                z.toast(PhoneNumber + '手机号,获取不到验证码')
                continue
            z.heartbeat()
            print('验证码：'+code)
            x_02 = int( numbers[0]['x02'] ) + 1
            para = {"phoneNumber": PhoneNumber, 'x_02': x_02, 'x_19': 'WXRegister'}
            self.repo.PostInformation( saveCate, para )
            d(text='请输入验证码').click()
            z.input(code)
            d(text='下一步', className='android.widget.Button').click()
            z.sleep(10)
            z.heartbeat( )

            while d(text='验证码不正确，请重新输入').exists:
                d(text='确定').click()
                d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout',index=0).child(className='android.widget.LinearLayout',index=2).child(
                    className='android.widget.LinearLayout',index=0).child(className='android.widget.EditText', index=1).click.bottomright()
                # code = '596028'
                code = self.scode.GetVertifyCode(PhoneNumber, self.scode.WECHAT_REGISTER)
                self.scode.defriendPhoneNumber(PhoneNumber,self.scode.WECHAT_REGISTER)
                if code == '':
                    z.toast(PhoneNumber+'手机号,获取不到验证码')
                    break
                z.sleep(8)
                z.heartbeat()
                print(code)
                d(text='请输入验证码').click()
                z.input(code)
                d(text='下一步', className='android.widget.Button').click()
                z.sleep(3)
                if d(textContains='你操作频率过快').exists:
                    d(text='确定').click()
                    break

            d.dump(compressed=False)
            if d( textContains='看看手机通讯录' ).exists:
                d( text='是' ).click( )
                para = {"phoneNumber": PhoneNumber,'x_05': 'YES',  'x_19': 'WXRegister', 'x_20':d.server.adb.device_serial(), 'x_26': '登陆状态YSE'}
                self.repo.PostInformation( saveCate, para )

                z.sleep(15)
                z.heartbeat( )

                d.dump( compressed=False )
                if d( textContains='有人正通过短信验证码' ).exists:
                    d( text='确定' ).click( )
                continue

            d.dump( compressed=False )
            if d(textContains='当前手机号一个月内已成功注册微信号').exists:
                d(text='确定')
                self.repo.DeleteInformation( saveCate, PhoneNumber )

            d.dump( compressed=False )
            if d( textContains='操作频率' ).exists:
                d( text='确定' ).click( )
                break

            time.sleep(1.5)
            n = 1
            while True:
                z.sleep(5)
                d.dump( compressed=False )
                if d(text='是我的，立刻登录').exists:
                    logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－是我的，立即登陆' )
                    n = n + 1
                    d(text='是我的，立刻登录').click()
                    if n == 1:
                        z.sleep(10)
                        z.heartbeat( )
                    else:
                        z.sleep(15)
                        z.heartbeat( )
                        n = 1

                d.dump( compressed=False )
                if d( textContains='看看手机通讯录' ).exists:
                    logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－是我的，立即登陆的　　　　通讯录匹配' )
                    d( text='是' ).click()
                    para = {"phoneNumber": PhoneNumber,'x_05': 'YES',  'x_19': 'WXRegister', 'x_26': '登陆状态YSE','x_20':d.server.adb.device_serial()}
                    self.repo.PostInformation( saveCate, para )

                    z.sleep(10)
                    z.heartbeat( )

                    d.dump(compressed=False )
                    if d(textContains='有人正通过短信验证码' ).exists:
                        logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－有人正通过短信验证码' )
                        d(text='确定' ).click( )
                    break

                d.dump(compressed=False)
                if d(text='声纹验证').exists:
                    d(className='android.widget.ImageView', description='返回').click()
                    x_27 = int( numbers[0]['x27'] ) + 1
                    para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_02': x_02, 'x_03': nowTime,
                            'x_19': 'WXRegister', 'x_27': x_27}
                    self.repo.PostInformation( saveCate, para )
                    break


                d.dump( compressed=False )
                if d(textContains='非法软件注册').exists:
                    d(text='取消').click()
                    self.repo.DeleteInformation(saveCate, PhoneNumber)
                    break

                d.dump( compressed=False )
                if d(text='该帐号长期未登录，为保护帐号安全，系统将其自动置为保护状态。点击确定按钮可立即激活帐号解除保护状态。').exists:
                    d(text='取消').click()
                    self.repo.DeleteInformation( saveCate, PhoneNumber )
                    break

                d.dump( compressed=False )
                if d(textContains='帐号有异常').exists:
                    d(text='取消').click()
                    self.repo.DeleteInformation( saveCate, PhoneNumber )
                    break

                d.dump( compressed=False )
                if d(textContains='限制登录').exists:
                    d(text='取消').click()
                    self.repo.DeleteInformation( saveCate, PhoneNumber )
                    break

                d.dump( compressed=False )
                if d(textContains='长期没有登陆，帐号已被收回').exists:
                    d(text='取消').click()
                    self.repo.DeleteInformation( saveCate, PhoneNumber )
                    break

                d.dump( compressed=False )
                if d(textContains='相同手机号不可频繁重复注册微信帐号').exists:
                    d(text='确定').click()
                    self.repo.DeleteInformation( saveCate, PhoneNumber )
                    break

                d.dump( compressed=False )
                if d(textContains='你操作频率过快').exists:
                    d(text='确定').click()
                    break

                d.dump( compressed=False )
                if d(textContains='是否立即验证').exists:
                    d(text='确定').click()
                    z.sleep(10)
                    z.heartbeat( )


                if d(text='确认登录').exists:
                    x_27_number = self.repo.GetInformation( information_cate_id, number )
                    x_27 = int(x_27_number[0]['x27']) + 1
                    para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_02':x_02, 'x_03': nowTime, 'x_19': 'WXRegister', 'x_27': x_27}
                    self.repo.PostInformation( saveCate, para )
                    break



                d.dump( compressed=False )
                if d(text='设置密码').exists:
                    d(className='android.widget.LinearLayout', index=2).child(className='android.widget.EditText', index=1).click()
                    z.input(password)
                    z.sleep(2)
                    d(className='android.widget.LinearLayout', index=4).child(className='android.widget.EditText', index=1).click()
                    z.input(password)
                    d(text='完成').click()

                    z.sleep(15)
                    z.heartbeat( )

                    d.dump( compressed=False )
                    if d(textContains='看看手机通讯录').exists:
                        logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－设置密码时的　　　　通讯录匹配' )
                        d( text='是' ).click( )
                        para = {"phoneNumber": PhoneNumber,'x_05': 'YES', 'x_19': 'WXRegister','x_20':d.server.adb.device_serial(), 'x_26': '登陆状态YSE'}
                        self.repo.PostInformation( saveCate, para )
                        z.sleep(15)
                        z.heartbeat( )

                        d.dump( compressed=False )
                        if d( textContains='有人正通过短信验证码' ).exists:
                            d( text='确定' ).click( )

                    d.dump( compressed=False )
                    if d( textContains='你的操作频繁过快，请稍后重试' ).exists:
                        d( text='确定' ).click( )
                        para = {"phoneNumber": PhoneNumber,'x_05': 'YES',  'x_19': 'WXRegister', 'x_20': d.server.adb.device_serial( ), 'x_21': password,
                                'x_26': '登陆状态YSE'}
                        self.repo.PostInformation( saveCate, para )
                        z.sleep( 15 )
                        z.heartbeat( )

                        d.dump( compressed=False )
                        if d( textContains='有人正通过短信验证码' ).exists:
                            d( text='确定' ).click( )

                    weixinhao = d( className='android.widget.LinearLayout', index=1 ).child( className='android.widget.TextView',index=1 ).info['text']
                    para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_05': 'YES','x_19': 'WXRegister','x_20':d.server.adb.device_serial(),'x_21':password,'x_22':weixinhao,'x_26': '登陆状态YSE'}
                    self.repo.PostInformation( saveCate, para )
                    logger.info( para )
                    break


                if d(text='验证身份').exists:
                    x_04_number = self.repo.GetInformation( information_cate_id, number )
                    x_04 = int( x_04_number[0]['x04'] ) + 1
                    para = {"phoneNumber": PhoneNumber,'x_04': x_04, 'x_19': 'WXRegister'}
                    self.repo.PostInformation( saveCate, para )
                    logger.info(para)
                    logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－验证身份，答题次数' )
                    z.sleep(3)
                    x_value = ''

                    for i in range(1, 6):
                        yibushiObj_LTV = d( resourceId='x5', className='android.widget.RadioButton',
                                            descriptionContains='以上都不是' )
                        yibushiObj_HTC = d( className='android.widget.RadioButton', descriptionContains='以上都不是',
                                            index=6 )

                        if i != 1:
                            if not yibushiObj_HTC or yibushiObj_LTV.exists:
                                break

                        if d(description='请选择你最近一次登录设备的名称').exists:
                            if d( resourceId='x0', className='android.widget.RadioButton' ).exists:
                                numberInfo = self.repo.GetInformation(information_cate_id, number)
                                if numberInfo[0]['x07'] is not None:
                                    x0_val = d( resourceId='x0', className='android.widget.RadioButton' ).info[
                                        'contentDescription']
                                    x1_val = d( resourceId='x1', className='android.widget.RadioButton' ).info[
                                        'contentDescription']
                                    x2_val = d( resourceId='x2', className='android.widget.RadioButton' ).info[
                                        'contentDescription']
                                    x3_val = d( resourceId='x3', className='android.widget.RadioButton' ).info[
                                        'contentDescription']
                                    x4_val = d( resourceId='x4', className='android.widget.RadioButton' ).info[
                                        'contentDescription']

                                    trues = repo.GetTrueAnswer( saveCate, number, x0_val, x1_val, x2_val, x3_val, x4_val)
                                    true = trues[0]['x07']

                                    if true == x0_val:
                                        d( resourceId='x0', className='android.widget.RadioButton' ).click( )
                                        d( resourceId='submitBtn', className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if true == x1_val:
                                        d( resourceId='x1', className='android.widget.RadioButton' ).click( )
                                        d( resourceId='submitBtn', className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if true == x2_val:
                                        d( resourceId='x2', className='android.widget.RadioButton' ).click( )
                                        d( resourceId='submitBtn', className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if true == x3_val:
                                        d( resourceId='x3', className='android.widget.RadioButton' ).click( )
                                        d( resourceId='submitBtn', className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if true == x4_val:
                                        d( resourceId='x4', className='android.widget.RadioButton' ).click( )
                                        d( resourceId='submitBtn', className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                else:
                                    number = random.randint( 1, 5 )
                                    if number == 1:
                                        x_value = d( resourceId='x0', className='android.widget.RadioButton' ).info[
                                            'contentDescription']
                                        d( resourceId='x0', className='android.widget.RadioButton' ).click( )
                                        d( resourceId='submitBtn', className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 2:
                                        x_value = d( resourceId='x1', className='android.widget.RadioButton' ).info[
                                            'contentDescription']
                                        d( resourceId='x1', className='android.widget.RadioButton' ).click( )
                                        d( resourceId='submitBtn', className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 3:
                                        x_value = d( resourceId='x2', className='android.widget.RadioButton' ).info[
                                            'contentDescription']
                                        d( resourceId='x2', className='android.widget.RadioButton' ).click( )
                                        d( resourceId='submitBtn', className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 4:
                                        x_value = d( resourceId='x3', className='android.widget.RadioButton' ).info[
                                            'contentDescription']
                                        d( resourceId='x3', className='android.widget.RadioButton' ).click( )
                                        d( resourceId='submitBtn', className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 5:
                                        x_value = d( resourceId='x4', className='android.widget.RadioButton' ).info[
                                            'contentDescription']
                                        d( resourceId='x4', className='android.widget.RadioButton', ).click( )
                                        d( resourceId='submitBtn', className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                            elif d(className='android.widget.RadioButton', index=1).exists:
                                numberInfo = self.repo.GetInformation( information_cate_id, number )
                                if numberInfo[0]['x07'] is not None:
                                    x0_val = d(className='android.widget.RadioButton', index=1).info[
                                        'contentDescription']
                                    x1_val = d(className='android.widget.RadioButton', index=2).info[
                                        'contentDescription']
                                    x2_val = d(className='android.widget.RadioButton', index=3).info[
                                        'contentDescription']
                                    x3_val = d(className='android.widget.RadioButton', index=4).info[
                                        'contentDescription']
                                    x4_val = d(className='android.widget.RadioButton', index=5).info[
                                        'contentDescription']

                                    trues = repo.GetTrueAnswer( saveCate, number, x0_val, x1_val, x2_val, x3_val,
                                                                x4_val )
                                    true = trues[0]['x07']

                                    if true == x0_val:
                                        d( className='android.widget.RadioButton', index=1 ).click( )
                                        d( className='android.view.View', descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep(2)
                                    if true == x1_val:
                                        d( className='android.widget.RadioButton', index=2 ).click( )
                                        d( className='android.view.View', descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if true == x2_val:
                                        d( className='android.widget.RadioButton', index=3 ).click( )
                                        d( className='android.view.View', descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if true == x3_val:
                                        d( className='android.widget.RadioButton', index=4 ).click( )
                                        d( className='android.view.View', descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if true == x4_val:
                                        d( className='android.widget.RadioButton', index=5 ).click( )
                                        d( className='android.view.View', descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )

                                else:
                                    number = random.randint( 1, 5 )
                                    if number == 1:
                                        x_value = d( className='android.widget.RadioButton', index=1).info[
                                            'contentDescription']
                                        d(className='android.widget.RadioButton', index=1).click( )
                                        d(className='android.view.View',descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 2:
                                        x_value = d( className='android.widget.RadioButton', index=2 ).info[
                                            'contentDescription']
                                        d( className='android.widget.RadioButton', index=2 ).click( )
                                        d( className='android.view.View', descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 3:
                                        x_value = d( className='android.widget.RadioButton', index=3 ).info[
                                            'contentDescription']
                                        d( className='android.widget.RadioButton', index=3 ).click( )
                                        d( className='android.view.View', descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 4:
                                        x_value = d( className='android.widget.RadioButton', index=4 ).info[
                                            'contentDescription']
                                        d( className='android.widget.RadioButton', index=4 ).click( )
                                        d( className='android.view.View', descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 5:
                                        x_value = d( className='android.widget.RadioButton', index=5 ).info[
                                            'contentDescription']
                                        d( className='android.widget.RadioButton', index=5 ).click( )
                                        d( className='android.view.View', descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep(2)
                            else:
                                d.swipe(440, 540, 450, 540, 5)
                                d.swipe(260, 630, 270, 630, 5)
                                z.sleep(2)


                        elif d(description='请从下面头像中选出两位你的好友').exists:
                            logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－请从下面头像中选出两位你的好友' )
                            d(className='android.widget.ImageView',description='返回').click()
                            break
                        elif d( description='通过扫码验证身份', className='android.view.View', index=1 ).exists:
                            logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－通过扫码验证身份' )
                            x_27_number = self.repo.GetInformation( information_cate_id, number )
                            x_27 = int( x_27_number[0]['x27'] ) + 1
                            para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_03': nowTime, 'x_19': 'WXRegister',
                                    'x_27': x_27}
                            self.repo.PostInformation( saveCate, para )
                            logger.info( para )
                            break
                        else:

                            if yibushiObj_LTV.exists:
                                logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－乐视非设备号按钮点击' )
                                d( resourceId='x5', className='android.widget.RadioButton',
                                   descriptionContains='以上都不是' ).click( )  # 以上都不是
                                d( resourceId='submitBtn', className='android.view.View',
                                   descriptionContains='下一步' ).click( )  # 下一步
                            elif yibushiObj_HTC.exists:
                                logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－ＨＴＣ非设备号按钮点击' )
                                d( className='android.widget.RadioButton',descriptionContains='以上都不是',index=6).click()  # 以上都不是
                                d( className='android.view.View',descriptionContains='下一步' ).click( )  # 下一步
                            else:
                                logger.info('－－－－－－－－－－－－－－－－－－－－－－－－－－－－－非设备号滑动答题准备点击')
                                YZSB = d( descriptionContains='验证失败', className='android.view.View', index=1 )
                                YZTG = d( descriptionContains='验证通过', className='android.view.View', index=1 )
                                if not YZSB and YZTG.exists:
                                    d.swipe( 440, 540, 450, 540, 5 )
                                    d.swipe( 270, 630, 280, 630, 5 )
                                    logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－非设备号滑动答题已点击' )
                                logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－非设备号滑动答题点击结束' )
                            z.sleep(2)

                z.sleep(5)

                if d(text='确认登录').exists:
                    logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－进入身份验证后的确认登录' )
                    para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_03': nowTime, 'x_19': 'WXRegister'}
                    self.repo.PostInformation( saveCate, para )
                    logger.info(para )
                    break

                if d(descriptionContains='验证失败', className='android.view.View', index=1).exists:
                    logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－验证失败' )
                    d(descriptionContains='关闭页面', className='android.view.View', index=3).click()
                    if x_value == '':
                        para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_05': '空', 'x_19': 'WXRegister'}
                    else:
                        para = {"phoneNumber": PhoneNumber, 'x_01': "exist",
                                "x_key": x_value, 'x_19': 'WXRegister'}
                    self.repo.PostInformation( saveCate, para )
                    logger.info( para)

                if d(descriptionContains='验证通过', className='android.view.View', index=1).exists:
                    logger.info( '－－－－－－－－－－－－－－－－－－－－－－－－－－－－－验证通过' )
                    d(descriptionContains='关闭页面', className='android.view.View', index=3).click()
                    if x_value == '':
                        x_value = 'YSE'
                    para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_05':x_value , 'x_19': 'WXRegister'}
                    self.repo.PostInformation( saveCate, para )
                    logger.info(para)


            continue





def getPluginClass():
    return WeiXinRegister

if __name__ == "__main__":
    import sys
    reload( sys )
    sys.setdefaultencoding( 'utf8' )

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT544SK00366")#INNZL7YDLFPBNFN7
    z = ZDevice("HT544SK00366")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    'dingdingdingdingdindigdingdingdingdingdingdingdingdingdingdingdingdignin'
    repo = Repo()
    # repo.RegisterAccount('', 'gemb1225', '13045537833', '109')
    args = {"repo_information_id":"189","repo_material_id": "167"}  # cate_id是仓库号，发中文问题
    saveCate = args['repo_information_id']
    o.action(d,z, args)
    # para = {"phoneNumber": '13642744049', 'x_01': "exist", 'x_05': '空',
    #         "x_key": 'x_value', 'x_19': 'WXRegister'}
    # repo.PostInformation( saveCate, para )

    # para = {"phoneNumber": '13642744049', 'x_01': "exist", 'x_05': 'x_value', 'x_19': 'WXRegister'}
    # repo.PostInformation( saveCate, para )
    # print('')








