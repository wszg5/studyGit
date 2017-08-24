# coding:utf-8
from slot import Slot
from uiautomator import Device
from Repo import *
from smsCode import smsCode
import time, string, datetime, random
from zservice import ZDevice
import util
from functools import reduce


class WeiXinRegister:
    def __init__(self):
        self.repo = Repo( )
        self.xm = None
        self.cache_phone_key = 'cache_phone_key'
        self.type = 'wechat'

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
        z.generate_serial( "com.tencent.mm" )  # 随机生成手机特征码
        z.toast( "随机生成手机特征码" )
        password = self.GenPassword( )
        while True:

            nowTime = datetime.datetime.now( ).strftime( "%Y-%m-%d %H:%M:%S" );  # 生成当前时间
            time_limit = int( args['time_limit'] )
            serial = d.server.adb.device_serial( )
            self.slot = Slot( serial, self.type )
            slotnum = self.slot.getEmpty( )  # 取空卡槽
            if slotnum == 0:  # 没有空卡槽的话
                slotObj = self.slot.getAvailableSlot( time_limit )  # 取空卡槽，取２小时没用过的卡槽
                if not slotObj is None:
                    slotnum = slotObj['id']
                print( slotnum )
                while slotObj is None:  # 2小时没用过的卡槽也为没有的情况
                    d.server.adb.cmd( "shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"QQ卡槽全满，无间隔时间段未用\"" ).communicate( )
                    z.heartbeat( )
                    z.sleep( 30 )
                    slotObj = self.slot.getAvailableSlot( time_limit )
                    if not slotObj is None:
                        slotnum = slotObj['id']
                z.heartbeat( )
                self.slot.restore( slotnum )  # 有time_limit分钟没用过的卡槽情况，切换卡槽
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"卡槽成功切换为" + slotnum + "号\"").communicate()
                d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
            else:
                d.press.home()
                d.server.adb.cmd("shell", "pm clear com.tencent.mm").communicate()  # 清除缓存，返回home页面

                while True:
                    if d( text='微信' ).exists:
                        d( text='微信' ).click( )
                        break
                    d.swipe( width - 20, height / 2, 0, height / 2, 5 )

                while not d( text='注册' ).exists:
                    z.toast( "等待 登录按钮　出现" )
                    d.dump( compressed=False )
                    z.sleep( 3 )

                if d( text='登录' ).exists:
                    d( text='登录' ).click( )

                z.sleep(2)
                if not d( text='中国' ).exists:
                    d( text='国家/地区' ).click( )
                    z.sleep(1.5)
                    d(resourceId='com.tencent.mm:id/aq').click( )
                    z.input( '中' )
                    d( text='中国' ).click( )

                information_cate_id = args['repo_information_id']
                numbers = self.repo.GetInformation( information_cate_id )
                if len( numbers ) == 0:
                    d.server.adb.cmd( "shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"资料库%s号仓库为空，没有取到手机号\"" % information_cate_id ).communicate( )
                    z.sleep( 10 )
                    return

                z.heartbeat( )
                number = numbers[0]['phonenumber']
                PhoneNumber = self.scode.GetPhoneNumber( self.scode.WECHAT_REGISTER, number )  # 获取接码平台手机号码
                if PhoneNumber is None:
                    self.repo.DeleteInformation( saveCate, number )
                    z.toast( '讯码查不无此号' )
                    continue

                z.heartbeat( )
                print( PhoneNumber )
                z.input( PhoneNumber )
                d( text='用短信验证码登录' ).click( )
                z.sleep( 1.5 )
                if d(text='下一步').exists:
                    d(text='下一步').click()
                    z.sleep( 1.5 )

                while d(text='确认手机号码').exists:
                    d( text='确定' ).click( )
                z.sleep( 3 )

                if d( textContains='正在验证' ).exists:
                    z.sleep( 35 )
                z.heartbeat( )

                code = self.scode.GetVertifyCode( PhoneNumber, self.scode.WECHAT_REGISTER )  # 获取接码验证码
                self.scode.defriendPhoneNumber(PhoneNumber,self.scode.WECHAT_REGISTER)
                if code == '':
                    self.repo.DeleteInformation( saveCate, PhoneNumber )
                    z.toast( PhoneNumber + '手机号,获取不到验证码' )
                    continue
                z.heartbeat( )
                print( '验证码：' + code )
                x_02 = int( numbers[0]['x02'] ) + 1
                para = {"phoneNumber": PhoneNumber, 'x_02': x_02, 'x_19': 'WXRegister'}
                self.repo.PostInformation( saveCate, para )
                d( text='请输入验证码' ).click( )
                d( text='请输入验证码' ).click( )
                z.input( code )
                z.sleep(2)
                d( text='下一步', className='android.widget.Button' ).click( )
                z.sleep(5)


                z.heartbeat( )
                if d( textContains='看看手机通讯录' ).exists:
                    d( text='是' ).click( )

                    para = {"phoneNumber": PhoneNumber, 'x_05': 'YES', 'x_19': 'WXRegister',
                            'x_20':str( slotnum ) + '_' + d.server.adb.device_serial( ), 'x_26': '登陆状态YSE'}
                    self.repo.PostInformation( saveCate, para )

                    z.sleep( 15 )
                    z.heartbeat( )

                    if d( textContains='如果这不是你本人操作，你的短信内容已经泄露。请检查手机是否被植入木马导致短信被转发。' ).exists:
                        d( text='确定' ).click( )
                    self.slot.backup( slotnum, str( slotnum ) + '_' + PhoneNumber )  # 卡槽号，手机号
                    continue

                if d( textContains='当前手机号一个月内已成功注册微信号' ).exists:
                    d( text='确定' )
                    self.repo.DeleteInformation( saveCate, PhoneNumber )

                if d( textContains='操作频率' ).exists:
                    d( text='确定' ).click( )
                    break

                z.sleep( 2 )
                n = 0
                while True:
                    z.sleep( 5 )
                    n = n + 1
                    if d( text='是我的，立刻登录' ).exists:
                        d( text='是我的，立刻登录' ).click( )
                        if n == 1:
                            z.sleep( 10 )
                            z.heartbeat( )
                        else:
                            z.sleep( 15 )
                            z.heartbeat( )

                    if d( text='下一步' ).exists:
                        d( text='下一步' ).click( )
                        z.sleep( 1.5 )

                    while d( text='确认手机号码' ).exists:
                        d( text='确定' ).click( )
                    z.sleep( 3 )

                    if d( textContains='看看手机通讯录' ).exists:
                        d( text='是' ).click( )
                        number_info = self.repo.GetInformation( saveCate, PhoneNumber )
                        if number_info[0]['x05'] is None:
                            para = {"phoneNumber": PhoneNumber, 'x_05': 'YES', 'x_19': 'WXRegister', 'x_26': '登陆状态YSE',
                                    'x_20':str( slotnum ) + '_' + d.server.adb.device_serial( )}
                        else:
                            para = {"phoneNumber": PhoneNumber, 'x_05': number_info[0]['x05'], 'x_19': 'WXRegister', 'x_26': '登陆状态YSE',
                                    'x_20':str( slotnum ) + '_' + d.server.adb.device_serial( )}
                        self.repo.PostInformation( saveCate, para )
                        self.slot.backup( slotnum, str( slotnum ) + '_' + PhoneNumber )  # 卡槽号，手机号

                        z.sleep( 10 )
                        z.heartbeat( )

                        if d( textContains='如果这不是你本人操作，你的短信内容已经泄露。请检查手机是否被植入木马导致短信被转发。' ).exists:
                            d( text='确定' ).click( )
                        break

                    if d( text='声纹验证' ).exists:
                        d( className='android.widget.ImageView', description='返回' ).click( )
                        x_27 = int( numbers[0]['x27'] ) + 1
                        para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_03': nowTime,
                                'x_19': 'WXRegister', 'x_27': x_27}
                        self.repo.PostInformation( saveCate, para )
                        break

                    if d( textContains='非法软件注册' ).exists:
                        d( text='取消' ).click( )
                        self.repo.DeleteInformation( saveCate, PhoneNumber )
                        break

                    if d( text='该帐号长期未登录，为保护帐号安全，系统将其自动置为保护状态。点击确定按钮可立即激活帐号解除保护状态。' ).exists:
                        d( text='取消' ).click( )
                        self.repo.DeleteInformation( saveCate, PhoneNumber )
                        break

                    if d( textContains='帐号有异常' ).exists:
                        d( text='取消' ).click( )
                        self.repo.DeleteInformation( saveCate, PhoneNumber )
                        break

                    if d( text='系统检测到帐号有被盗风险。为了你的帐号安全，新设备的登录请求会被拒绝。请使用常用设备登录微信。' ).exists:
                        d( text='确定' ).click( )
                        if n == 1:
                            continue
                        else:
                            break

                    if d( textContains='限制登录' ).exists:
                        d( text='取消' ).click( )
                        self.repo.DeleteInformation( saveCate, PhoneNumber )
                        break

                    if d( textContains='长期没有登陆，帐号已被收回' ).exists:
                        d( text='取消' ).click( )
                        self.repo.DeleteInformation( saveCate, PhoneNumber )
                        break

                    if d( textContains='相同手机号不可频繁重复注册微信帐号' ).exists:
                        d( text='确定' ).click( )
                        self.repo.DeleteInformation( saveCate, PhoneNumber )
                        break

                    if d( textContains='你操作频率过快' ).exists:
                        d( text='确定' ).click( )
                        break

                    while d( textContains='是否立即验证' ).exists:
                        d( text='确定' ).click( )
                    z.sleep( 10 )
                    z.heartbeat( )

                    if d( text='确认登录' ).exists:
                        if n == 1:
                            d( className='android.widget.ImageView', description='返回' ).click( )
                            z.sleep( 10 )
                            z.heartbeat( )
                            continue
                        elif n == 2:
                            self.repo.DeleteInformation( saveCate, PhoneNumber )
                        else:
                            para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_03': nowTime, 'x_19': 'WXRegister'}
                            self.repo.PostInformation( saveCate, para )
                        break

                    if d( text='设置密码' ).exists:
                        d( className='android.widget.LinearLayout', index=2 ).child(
                            className='android.widget.EditText', index=1 ).click( )
                        z.input( password )
                        z.sleep( 2 )
                        d( className='android.widget.LinearLayout', index=4 ).child(
                            className='android.widget.EditText', index=1 ).click( )
                        z.input( password )
                        d( text='完成' ).click( )

                        z.sleep( 15 )
                        z.heartbeat( )

                        if d( textContains='看看手机通讯录' ).exists:
                            d( text='是' ).click( )
                            para = {"phoneNumber": PhoneNumber, 'x_05': 'YES', 'x_19': 'WXRegister',
                                    'x_20': str( slotnum ) + '_' + d.server.adb.device_serial( ), 'x_21': password, 'x_26': '登陆状态YSE'}
                            self.repo.PostInformation( saveCate, para )
                            z.sleep( 15 )
                            z.heartbeat( )

                        if d( textContains='你的操作频繁过快，请稍后重试' ).exists:
                            d( text='确定' ).click( )
                            para = {"phoneNumber": PhoneNumber, 'x_05': 'YES', 'x_19': 'WXRegister',
                                    'x_20': str( slotnum ) + '_' +d.server.adb.device_serial( ), 'x_21': password,
                                    'x_26': '登陆状态YSE'}
                            self.repo.PostInformation( saveCate, para )
                            z.sleep( 15 )
                            z.heartbeat( )

                        if d( textContains='如果这不是你本人操作，你的短信内容已经泄露。请检查手机是否被植入木马导致短信被转发。' ).exists:
                            d( text='确定' ).click( )

                        self.slot.backup( slotnum, str( slotnum ) + '_' + PhoneNumber )  # 卡槽号，手机号

                        break

                    if d( text='验证身份' ).exists:
                        z.sleep( 3 )
                        if d( description='通过扫码验证身份', className='android.view.View', index=1 ).exists:
                            self.repo.DeleteInformation( saveCate, PhoneNumber )
                            break

                        if d( descriptionContains='验证失败', className='android.view.View' ).exists:
                            d( descriptionContains='关闭页面', className='android.view.View', index=3 ).click( )
                            if x_value != '':
                                para = {"phoneNumber": PhoneNumber, 'x_01': "exist", "x_key": x_value,
                                        'x_19': 'WXRegister'}
                            self.repo.PostInformation( saveCate, para )
                            break

                        if d( descriptionContains='验证通过', className='android.view.View' ).exists:
                            d( descriptionContains='关闭页面', className='android.view.View', index=3 ).click( )
                            if x_value == '':
                                x_value = 'YSE'
                            para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_05': x_value, 'x_19': 'WXRegister'}
                            self.repo.PostInformation( saveCate, para )
                            break

                        for i in range( 1, 6 ):

                            if i != 1:
                                yibushiObj_HTC = d( className='android.widget.RadioButton', descriptionContains='以上都不是')
                                if not yibushiObj_HTC.exists:
                                    break

                            if d( description='请选择你最近一次登录设备的名称' ).exists:
                                x_value = ''
                                if d( className='android.widget.RadioButton', index=1 ).exists:
                                    number = random.randint( 1, 5 )
                                    if number == 1:
                                        x_value = d( className='android.widget.RadioButton', index=1 ).info[
                                            'contentDescription'].replace( '\n\n', '' )
                                        d( className='android.widget.RadioButton', index=1 ).click( )
                                        d( className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 2:
                                        x_value = d( className='android.widget.RadioButton', index=2 ).info[
                                            'contentDescription'].replace( '\n\n', '' )
                                        d( className='android.widget.RadioButton', index=2 ).click( )
                                        d( className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 3:
                                        x_value = d( className='android.widget.RadioButton', index=3 ).info[
                                            'contentDescription'].replace( '\n\n', '' )
                                        d( className='android.widget.RadioButton', index=3 ).click( )
                                        d( className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 4:
                                        x_value = d( className='android.widget.RadioButton', index=4 ).info[
                                            'contentDescription'].replace( '\n\n', '' )
                                        d( className='android.widget.RadioButton', index=4 ).click( )
                                        d( className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                    if number == 5:
                                        x_value = d( className='android.widget.RadioButton', index=5 ).info[
                                            'contentDescription'].replace( '\n\n', '' )
                                        d( className='android.widget.RadioButton', index=5 ).click( )
                                        d( className='android.view.View',
                                           descriptionContains='下一步' ).click( )  # 下一步
                                        z.sleep( 2 )
                                else:
                                    if d( className='android.widget.RadioButton', descriptionContains='以上都不是' ).exists:
                                        d( className='android.widget.RadioButton',
                                           descriptionContains='以上都不是' ).click( )
                                        d( className='android.view.View', descriptionContains='下一步' ).click( )  # 下一步
                                    else:
                                        d.click( 410, 540 )
                                        d.click( 410, 640 )
                                    z.sleep( 2 )

                            elif d( description='请从下面头像中选出两位你的好友' ).exists:
                                d( className='android.widget.ImageView', description='返回' ).click( )
                                break
                            else:
                                if d( className='android.widget.RadioButton', descriptionContains='以上都不是').exists:
                                    d( className='android.widget.RadioButton', descriptionContains='以上都不是' ).click()
                                    d( className='android.view.View',descriptionContains='下一步' ).click( )  # 下一步
                                else:
                                    d.click( 410, 540 )
                                    d.click( 410, 640 )
                                z.sleep( 2 )

                        x_04_number = self.repo.GetInformation( information_cate_id, PhoneNumber )
                        x_04 = int( x_04_number[0]['x04'] ) + 1
                        para = {"phoneNumber": PhoneNumber, 'x_04': x_04, 'x_19': 'WXRegister'}
                        self.repo.PostInformation( saveCate, para )

                    z.sleep( 5 )

                    if d( text='确认登录' ).exists:
                        para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_03': nowTime, 'x_19': 'WXRegister'}
                        self.repo.PostInformation( saveCate, para )
                        break

                    if d( descriptionContains='验证失败', className='android.view.View' ).exists:
                        d( descriptionContains='关闭页面', className='android.view.View', index=3 ).click( )
                        if x_value == '':
                            para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_05': '空', 'x_19': 'WXRegister'}
                        else:
                            para = {"phoneNumber": PhoneNumber, 'x_01': "exist",
                                    "x_key": x_value, 'x_19': 'WXRegister'}
                        self.repo.PostInformation( saveCate, para )

                    if d( descriptionContains='验证通过', className='android.view.View' ).exists:
                        d( descriptionContains='关闭页面', className='android.view.View', index=3 ).click( )
                        if x_value == '':
                            x_value = 'YSE'
                        para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_05': x_value, 'x_19': 'WXRegister'}
                continue




def getPluginClass():
    return WeiXinRegister

if __name__ == "__main__":
    import sys
    reload( sys )
    sys.setdefaultencoding( 'utf8' )

    clazz = getPluginClass()
    o = clazz()
    d = Device("cda0ae8d")#INNZL7YDLFPBNFN7
    z = ZDevice("cda0ae8d")
    # z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    'dingdingdingdingdindigdingdingdingdingdingdingdingdingdingdingdingdignin'
    repo = Repo()
    # repo.RegisterAccount('', 'gemb1225', '13045537833', '109')
    args = {"repo_information_id": "191","time_limit": "120"}  # cate_id是仓库号，发中文问题
    o.action(d, z, args)














