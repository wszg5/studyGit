# coding:utf-8
from uiautomator import Device
from Repo import *
from smsCode import smsCode
import time, string, datetime, random
from zservice import ZDevice


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
        PhoneNumber = '123456789'
        while True:
            nowTime = datetime.datetime.now( ).strftime( "%Y-%m-%d %H:%M:%S" );  # 生成当前时间
            NUM_INFO = self.repo.GetInformationByDevice( saveCate, PhoneNumber )
            x2 = NUM_INFO[0]['x05']
            if x2 is not None and x2 != '空':
                break
            d.press.home()
            d.server.adb.cmd("shell", "pm clear com.tencent.mm").communicate()  # 清除缓存，返回home页面

            while True:
                if d(text='微信').exists:
                    d(text='微信').click()
                    break
                d.swipe( width - 20, height / 2, 0, height / 2, 5 )

            z.sleep(8)
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

            if not d(text='中国').exists:
                d(textContains='地区').click()
                d.dump( compressed=False )
                d(className='android.support.v7.widget.LinearLayoutCompat',index=1).click()
                z.input('中')
                d(text='中国').click()

            d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout', index=2).child(
                className='android.widget.EditText', index=1).click()
            d(className='android.widget.ScrollView').child(className='android.widget.LinearLayout', index=2).child(
                className='android.widget.EditText', index=1).click.bottomright()
            z.heartbeat()


            information_cate_id = args['repo_information_id']
            numbers = self.repo.GetInformation(information_cate_id)
            if len(numbers) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"资料库%s号仓库为空，没有取到手机号\"" % cate_id ).communicate( )
                z.sleep(10)
                return
            z.heartbeat()

            number = numbers[0]['phonenumber']

            PhoneNumber = self.scode.GetPhoneNumber(self.scode.WECHAT_REGISTER,number)#获取接码平台手机号码

            if PhoneNumber is None:
                para = {"phoneNumber": number, 'x_01': "not_exist", 'x_19': 'WXRegister','x_20':d.server.adb.device_serial()}
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

            para = {"phoneNumber": PhoneNumber, 'x_19': 'WXRegister','x_20':d.server.adb.device_serial()}#对应微信手机号的设备号入库
            self.repo.PostInformation( saveCate, para )

            d(text='注册').click()

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
            para = {"phoneNumber": PhoneNumber, 'x_02': x_02,'x_03':nowTime, 'x_19': 'WXRegister'}
            self.repo.PostInformation( saveCate, para )
            d(text='请输入验证码').click()
            z.input(code)
            d(text='下一步', className='android.widget.Button').click()
            z.sleep(10)

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

                if d(text='你操作频率过快，请重新输入').exists:
                    d(text='确定').click
                    break

            d.dump(compressed=False)
            if d( textContains='看看手机通讯录' ).exists:
                d( text='是' ).click( )
                para = {"phoneNumber": PhoneNumber, 'x_19': 'WXRegister', 'x_26': '登陆状态YSE'}
                self.repo.PostInformation( saveCate, para )
                continue

            d.dump( compressed=False )
            if d(textContains='当前手机号一个月内已成功注册微信号').exists:
                d(text='确定')
                self.repo.DeleteInformation( saveCate, PhoneNumber )

            time.sleep(1.5)
            while True:
                z.sleep(5)
                d.dump( compressed=False )
                if d(text='是我的，立刻登录').exists:
                    d(text='是我的，立刻登录').click()
                    z.sleep(10)

                d.dump( compressed=False )
                if d( textContains='看看手机通讯录' ).exists:
                    d( text='是' ).click()
                    para = {"phoneNumber": PhoneNumber, 'x_19': 'WXRegister', 'x_26': '登陆状态YSE'}
                    self.repo.PostInformation( saveCate, para )
                    break

                d.dump( compressed=False )
                if d( textContains='有人正通过短信验证码' ).exists:
                    d( text='确定' ).click( )
                    break

                d.dump( compressed=False )
                if d(textContains='非法软件注册').exists:
                    d(text='取消').click()
                    self.repo.DeleteInformation(saveCate, PhoneNumber)
                    break

                d.dump( compressed=False )
                if d(text='该帐号长期未登录，为保护帐号安全，系统将其自动置为保护状态。点击确定按钮可立即激活帐号解除保护状态。').exists:
                    d(text='取消')
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
                if d(textContains='是否立即验证').exists:
                    d(text='确定').click()
                    z.sleep(10)


                if d(text='确认登录').exists:
                    x_27 = numbers[0]['x27'] + 1
                    para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_02':x_02, 'x_03': nowTime, 'x_19': 'WXRegister', 'x_27': x_27}
                    self.repo.PostInformation( saveCate, para )
                    break

                if d( description='通过扫码验证身份', className='android.view.View', index=1 ).exists:
                    para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_02':x_02, 'x_03':nowTime, 'x_19': 'WXRegister'}
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

                    z.sleep(3)

                    d.dump( compressed=False )
                    if d( textContains='看看手机通讯录' ).exists:
                        d( text='是' ).click( )
                        para = {"phoneNumber": PhoneNumber, 'x_19': 'WXRegister', 'x_26': '登陆状态YSE'}
                        self.repo.PostInformation( saveCate, para )

                    weixinhao = d( className='android.widget.LinearLayout', index=1 ).child( className='android.widget.TextView',index=1 ).info['text']
                    para = {"phoneNumber": PhoneNumber, 'x_01': "exist",'x_02':x_02, 'x_05': 'YES','x_19': 'WXRegister','x_20':d.server.adb.device_serial(),'x_21':password,'x_22':weixinhao,'x_26': '登陆状态YSE'}
                    self.repo.PostInformation( saveCate, para )
                    break


                if d(text='验证身份').exists:
                    x_04 = int( numbers[0]['x04'] ) + 1
                    para = {"phoneNumber": PhoneNumber,'x_04': x_04, 'x_19': 'WXRegister'}
                    self.repo.PostInformation( saveCate, para )
                    z.sleep(3)
                    x_value = ''
                    for i in range(1, 5):
                        if d(description='请选择你最近一次登录设备的名称').exists:
                            if d( resourceId='x0', className='android.widget.RadioButton' ).exists:
                                numberInfo = self.repo.GetInformation( information_cate_id, number )
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
                                    a = set( )
                                    a.add( x0_val )
                                    a.add( x1_val )
                                    a.add( x2_val )
                                    a.add( x3_val )
                                    a.add( x4_val )

                                    b = set( )
                                    for i in range( 7, 17 ):
                                        if i < 10:
                                            index = 'x0' + str( i )
                                            if numbers[0][index] is not None:
                                                b.add( numbers[0][index] )
                                            else:
                                                break
                                        else:
                                            index = 'x' + str( i )
                                            if numbers[0][index] is not None:
                                                b.add( numbers[0][index] )
                                            else:
                                                break

                                    for obj in a:
                                        c = set( )
                                        c.add( obj )
                                        flag = b.isdisjoint( c )
                                        if flag == True:
                                            if obj == x0_val:
                                                d( resourceId='x0', className='android.widget.RadioButton').click()
                                            if obj == x1_val:
                                                d( resourceId='x1', className='android.widget.RadioButton').click()
                                            if obj == x2_val:
                                                d( resourceId='x2', className='android.widget.RadioButton').click()
                                            if obj == x3_val:
                                                d( resourceId='x3', className='android.widget.RadioButton').click()
                                            if obj == x4_val:
                                                d( resourceId='x4', className='android.widget.RadioButton').click()

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
                                    a = set( )
                                    a.add( x0_val )
                                    a.add( x1_val )
                                    a.add( x2_val )
                                    a.add( x3_val )
                                    a.add( x4_val )

                                    b = set( )
                                    for i in range( 7, 17 ):
                                        if i < 10:
                                            index = 'x0' + str( i )
                                            if numbers[0][index] is not None:
                                                b.add( numbers[0][index] )
                                            else:
                                                break
                                        else:
                                            index = 'x' + str( i )
                                            if numbers[0][index] is not None:
                                                b.add( numbers[0][index] )
                                            else:
                                                break

                                    for obj in a:
                                        c = set( )
                                        c.add( obj )
                                        flag = b.isdisjoint( c )
                                        if flag == True:
                                            if obj == x0_val:
                                                d( className='android.widget.RadioButton', index=1 ).click( )
                                            if obj == x1_val:
                                                d( className='android.widget.RadioButton', index=2 ).click( )
                                            if obj == x2_val:
                                                d( className='android.widget.RadioButton', index=3 ).click( )
                                            if obj == x3_val:
                                                d( className='android.widget.RadioButton', index=4 ).click( )
                                            if obj == x4_val:
                                                d( className='android.widget.RadioButton', index=5 ).click( )

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
                                        z.sleep( 2 )
                            else:
                                d.swipe(440, 540, 450, 540, 5)
                                d.swipe(260, 630, 270, 630, 5)
                                z.sleep(2)


                        elif d(description='请从下面头像中选出两位你的好友').exists:
                            d(className='android.widget.ImageView',description='返回').click()
                            break
                        else:
                            yibushiObj_LTV = d(resourceId='x5', className='android.widget.RadioButton',descriptionContains='以上都不是')
                            yibushiObj_HTC = d(className='android.widget.RadioButton',descriptionContains='以上都不是', index=6)
                            if yibushiObj_LTV.exists:
                                d( resourceId='x5', className='android.widget.RadioButton',
                                   descriptionContains='以上都不是' ).click( )  # 以上都不是
                                d( resourceId='submitBtn', className='android.view.View',
                                   descriptionContains='下一步' ).click( )  # 下一步
                            elif yibushiObj_HTC.exists:
                                d( className='android.widget.RadioButton',descriptionContains='以上都不是',index=6).click()  # 以上都不是
                                d( className='android.view.View',descriptionContains='下一步' ).click( )  # 下一步
                            else:
                                d.swipe(440, 540, 450, 540, 5)
                                d.swipe(270, 630, 280, 630, 5)
                            z.sleep(2)

                z.sleep(5)

                if d(text='确认登录').exists:
                    para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_02':x_02, 'x_03': nowTime, 'x_19': 'WXRegister'}
                    self.repo.PostInformation( saveCate, para )
                    break

                if d(descriptionContains='验证失败', className='android.view.View', index=1).exists:
                    d(descriptionContains='关闭页面', className='android.view.View', index=3).click()
                    if x_value == '':
                        para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_02': x_02, 'x_04': x_04, 'x_05': '空', 'x_19': 'WXRegister'}
                    else:
                        for i in range( 7, 17 ):
                            if i<10:
                                index = 'x0' + str( i )
                                if numbers[0][index] is None:
                                    x_key = 'x_0' + str(i)
                                    break
                            else:
                                index = 'x' + str( i )
                                if numbers[0][index] is None:
                                    x_key = 'x_' + str(i)
                                    break
                        para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_02': x_02, 'x_04': x_04, 'x_05': '空',
                                x_key: x_value, 'x_19': 'WXRegister','x_20':d.server.adb.device_serial()}
                        print(para)
                    self.repo.PostInformation( saveCate, para )

                if d(descriptionContains='验证通过', className='android.view.View', index=1).exists:
                    d(descriptionContains='关闭页面', className='android.view.View', index=3).click()
                    if x_value == '':
                        x_value = 'YSE'
                    para = {"phoneNumber": PhoneNumber, 'x_01': "exist", 'x_02': x_02, 'x_04': x_04, 'x_05':x_value , 'x_19': 'WXRegister','x_20':d.server.adb.device_serial()}
                    self.repo.PostInformation( saveCate, para )

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












