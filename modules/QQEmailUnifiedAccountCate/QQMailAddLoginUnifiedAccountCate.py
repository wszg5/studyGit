# coding:utf-8
import base64
import os
import random
import re

import requests

from uiautomator import Device
from Repo import *
from util import logger
from zservice import ZDevice
from PIL import Image

from imageCode import imageCode
from smsCode import smsCode


class QQMailAddLoginUnifiedAccountCate:
    def __init__(self):
        self.repo = Repo()
        self.type = 'qqmail'
        self.domain = '192.168.1.108:8888'
        # self.port = 8888

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 1000)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

    def input(self,z,height,text):
        if height>=888:
            z.input(text)
        else:
            z.cmd( "shell", "am broadcast -a ZY_INPUT_TEXT --es text \\\"%s\\\"" % text )

    def palyCode(self, d, z, picObj):
        self.scode = smsCode(d.server.adb.device_serial())
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))
        icode = imageCode()
        im_id = ""
        code = ""
        for i in range(0, 2):  # 打码循环
            if i > 0:
                icode.reportError(im_id)
            obj = picObj.info
            obj = obj['bounds']  # 验证码处的信息
            left = obj["left"]  # 验证码的位置信息
            top = obj['top']
            right = obj['right']
            bottom = obj['bottom']

            d.screenshot(sourcePng)  # 截取整个输入验证码时的屏幕

            img = Image.open(sourcePng)
            box = (left, top, right, bottom)  # left top right bottom
            region = img.crop(box)  # 截取验证码的图片

            img = Image.new('RGBA', (right - left, bottom - top))
            img.paste(region, (0, 0))

            img.save(codePng)
            time.sleep(1)
            with open( codePng, 'rb' ) as f:
                # file = f.read()
                file = "data:image/jpeg;base64," + base64.b64encode( f.read( ) )
                da = {"IMAGES": file}
                path = "/ocr.index"
                headers = {"Content-Type": "application/x-www-form-urlencoded",
                           "Connection": "Keep-Alive"}
                conn = httplib.HTTPConnection( "162626i1w0.51mypc.cn", 10082, timeout=30 )
                time.sleep( 0.5)
                params = urllib.urlencode( da )
                conn.request( method="POST", url=path, body=params, headers=headers )
                time.sleep( 1 )
                response = conn.getresponse( )
                if response.status == 200:
                    code = response.read( )
                    break
                else:
                    continue
                # print data
            # im = open(codePng, 'rb')
            #
            # codeResult = icode.getCode(im, icode.CODE_TYPE_4_NUMBER_CHAR, 60)
            #
            # code = codeResult["Result"]
            # im_id = codeResult["Id"]
            os.remove(sourcePng)
            os.remove(codePng)
            z.heartbeat()
            break
            # if code.isalpha() or code.isisdigitv() or code.isalnum():
            #     break
            # else:
            #     continue

        return code

    def action(self, d,z,args):
        # z.toast("正在ping网络是否通畅")
        # i = 0
        # while i < 200:
        #     i += 1
        #     ping = d.server.adb.cmd("shell", "ping -c 3 baidu.com").communicate()
        #     print(ping)
        #     if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
        #         z.toast(u"网络通畅。开始执行：QQ邮箱登录 无卡槽" )
        #         break
        #     z.sleep(2)
        # if i > 200:
        #     z.toast(u"网络不通，请检查网络状态" )
        #     return
        Str = d.info  # 获取屏幕大小等信息
        height = int( Str["displayHeight"] )
        width = int( Str["displayWidth"] )
        z.heartbeat( )
        z.heartbeat( )
        z.generate_serial( "com.tencent.androidqqmail" )  # 随机生成手机特征码
        d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
        time.sleep(1)
        for t in range(2):
            d.dump( compressed=False )
            if d( text="收件箱​",className="android.widget.TextView" ).exists:
                if d(textContains="密码错误，请重新输入").exists:
                    z.toast("密码错误，请重新输入")
                    return
                else:
                    z.toast( "状态正常，继续执行" )
                    break
            else:
                if d( text="温馨提示​", className="android.widget.TextView" ).exists:
                    d( text="确定", className="android.widget.Button" ).click( )
                    z.sleep( 1 )
                    break
                elif d(text="收件人：").exists and d(text="写邮件").exists:
                    flag1 = True
                    break
                elif d(text="取消​",resourceId='com.tencent.androidqqmail:id/a5',index=0).exists:
                    d( text="取消​", resourceId='com.tencent.androidqqmail:id/a5',index=0 ).click()
                    time.sleep(1)
                    if d(text="离开",className="android.widget.Button").exists:
                        d( text="离开", className="android.widget.Button" ).click()
                        time.sleep(1)
                    if d( text="收件箱​", className="android.widget.TextView" ).exists:
                        if d( textContains="密码错误，请重新输入" ).exists:
                            z.toast( "密码错误，请重新输入" )
                            return
                        else:
                            z.toast( "状态正常，继续执行" )
                            break

                elif d(index=1,text="写邮件​",className="android.widget.TextView").exists:
                    d.click(60/720 * width,198/1280 * height)
                    flag1 = True
                    break
                else:
                    if t>=1:
                        z.toast( "状态异常，跳过此模块" )
                        return
                    else:
                        d.server.adb.cmd( "shell", "am force-stop com.tencent.androidqqmail" ).communicate( )  # 强制停止
                        d.server.adb.cmd( "shell",
                                          "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                        time.sleep( 5 )
        if d( text="收件箱​", className="android.widget.TextView" ).exists:
            if d( textContains="密码错误，请重新输入" ).exists:
                z.toast( "密码错误，请重新输入" )
                return
            else:
                z.toast( "状态正常，继续执行" )
        else:
            z.toast("状态不正常")
            return

        if d( description="写邮件和设置等功能" ).exists:
            d( description="写邮件和设置等功能" ).click( )
            z.sleep( 0.5 )
            if d( text="设置" ).exists:
                d( text="设置" ).click( )
                time.sleep(0.5)
                d(text="添加帐户​").click()
                time.sleep(2)

        z.heartbeat( )
        try:
            for x in range(2):
                if d( resourceId='com.tencent.androidqqmail:id/ea' ).exists:  # 选择QQ邮箱点击进入登陆页面
                    d( resourceId='com.tencent.androidqqmail:id/ea' ).click( )
                    z.sleep( 1 )
                    break
                # if d(resourceId='com.tencent.androidqqmail:id/ea').exists:  # 选择QQ邮箱点击进入登陆页面
                #     d(resourceId='com.tencent.androidqqmail:id/ea').click()
                #     z.sleep(1)
                #     break
                else:
                    d.server.adb.cmd( "shell",
                                      "am start -n com.tencent.androidqqmail/com.tencent.qqmail.LaunchComposeMail" ).communicate( )  # 拉起QQ邮箱
                    time.sleep( 25 )
                    continue


            if d(text='帐号密码登录').exists:
                d(text='帐号密码登录').click()

            # random_code = args['random_code']
            if d( resourceId='com.tencent.androidqqmail:id/bi' ).exists:  # 输入邮箱帐号
                domain = args['domain']
                if domain:
                    if 'http' not in domain:
                        self.domain = 'http://' + domain
                    else:
                        self.domain = domain
                    # domain = re.sub( r'https?\://', '', domain )
                    # domainArr = domain.split(':')
                    # if len(domainArr)>1:
                    #     self.domain = domainArr[0]
                    #     self.port = domainArr[1]
                    # else:
                    #     self.domain = domainArr[0]
                    #     self.port = 80
                else:
                    z.toast("参数错误，格式如：192.168.1.102:8888")
                    time.sleep(3)
                    return
                accounts = self.get_accont( args['repo_account_id'], int( args['account_time_limit'] ),
                                                 1 )  # 去仓库获取QQ邮箱帐号
                # accounts = self.repo.GetAccount( args['repo_account_id'], int( args['account_time_limit'] ),
                #                                  1 )  # 去仓库获取QQ邮箱帐号
                if len( accounts ) == 0:
                    z.toast( u"帐号库为空" )
                    return

                account = accounts[0]['number']
                password = accounts[0]['password']

                # account = '1006329641'
                # password = '13141314AAb'


                d( resourceId='com.tencent.androidqqmail:id/bi' ).set_text(account)
                # self.input( z,height,account )
            else:
                z.toast("判断不出来界面")
                return

            if d(resourceId='com.tencent.androidqqmail:id/bs').exists:  # 输入邮箱密码
                d( resourceId='com.tencent.androidqqmail:id/bs' ).set_text(password)
                # self.input(random_code,z,password)

            if d(resourceId='com.tencent.androidqqmail:id/a_').exists:  # 点击登录按钮
                d( resourceId='com.tencent.androidqqmail:id/a_' ).click()

            z.sleep(8)
            while True:
                if d(textContains="验证中"):
                    time.sleep(3)
                else:
                    break
            if d(resourceId='com.tencent.androidqqmail:id/h').exists:  # 判断是否要填写独立密码
                # self.input(random_code,z,"Abc" + account)
                d( resourceId='com.tencent.androidqqmail:id/h' ).set_text("Abc" + account)
                z.sleep(1)
                if d(text='确定').exists:
                    d(text='确定').click()
                z.sleep(5)

            while d(resourceId='com.tencent.androidqqmail:id/a16').exists:  # 出现验证码
                picObj = d(resourceId='com.tencent.androidqqmail:id/a19', index=0)
                code = self.palyCode(d, z, picObj)
                if code == "":
                    return False
                d( resourceId='com.tencent.androidqqmail:id/a17' ).set_text(code)
                # self.input(random_code,z,code)
                if d( resourceId='com.tencent.androidqqmail:id/a_' ).exists:  # 点击登录按钮
                    d( resourceId='com.tencent.androidqqmail:id/a_' ).click( )
                z.sleep(8)

            if d(resourceId='com.tencent.androidqqmail:id/h').exists:  # 判断是否要填写独立密码
                # self.input(random_code,z,"Abc" + account)
                d( resourceId='com.tencent.androidqqmail:id/h' ).set_text("Abc" + account)
                z.sleep(1)
                if d(text='确定').exists:
                    d(text='确定').click()
                z.sleep(5)


            z.sleep(12)
            z.heartbeat()
            if d(textContains='你有多个应用同时收到').exists:
                d(text='确定').click()
                z.sleep(2)

            if d(text='收件箱​').exists:
                z.toast(u"登录成功。退出模块")
                # d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
                return True
            elif d(text='完成​').exists:
                d( text='完成​' ).click()
                time.sleep(1)
                z.toast( u"登录成功。退出模块" )
                # d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
                return True
            else:
                if d(textContains='帐号或密码错误').exists:
                    z.toast(u"帐号或密码错误")
                    againCount = int(args["againCount"])
                    for ac in range(againCount):
                        result = self.againLogin(account,password,d,z,height,"")
                        if result is True:
                            z.toast("跳出模块")
                            return
                    else:
                        z.toast( u"一直登陆出现密码错误,跳出该帐号")

                    # self.repo.BackupInfo(args["repo_account_id"], 'frozen', account, '', '')  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                elif d(textContains="未开启IMAP服务").exists:
                    z.toast( u"未开启IMAP服务，标记为异常" )
                    self.backup_info( args["repo_account_id"], 'exception', account, '','' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                elif d(text='当前网络不可用').exists:
                    z.toast('当前网络不可用,跳出模块')
                    return True
                self.action(d,z,args)

        except Exception as e:
            # print e
            logging.exception("exception")
            z.toast(u"程序出现异常，模块退出")
            z.toast(u'错误信息为:%s'%str(e))
            d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
            return False

    def againLogin(self,account,password,d,z,height,random_code):
        if d(text="确定",className="android.widget.Button").exists or d(text="重新输入",className="android.widget.Button").exists:
            if d(text="确定",className="android.widget.Button").exists:
                d( text="确定", className="android.widget.Button" ).click()
            else:
                d( text="重新输入", className="android.widget.Button" ).click()
            time.sleep(1)
            # self.input( random_code,z, password)
            d( resourceId='com.tencent.androidqqmail:id/bs' ).set_text( password )
            time.sleep(1)
            if d(resourceId='com.tencent.androidqqmail:id/a_').exists:  # 点击登录按钮
                d( resourceId='com.tencent.androidqqmail:id/a_' ).click()
                time.sleep(5)
            while True:
                if d(textContains="验证中"):
                    time.sleep(3)
                else:
                    break
            if d(resourceId='com.tencent.androidqqmail:id/h').exists:  # 判断是否要填写独立密码
                # self.input(random_code,z,"Abc" + account)
                d( resourceId='com.tencent.androidqqmail:id/h' ).set_text("Abc" + account)
                z.sleep(1)
                if d(text='确定').exists:
                    d(text='确定').click()
                z.sleep(5)

            while d(resourceId='com.tencent.androidqqmail:id/a16').exists:  # 出现验证码
                picObj = d(resourceId='com.tencent.androidqqmail:id/a19', index=0)
                code = self.palyCode(d, z, picObj)
                if code == "":
                    return False
                d( resourceId='com.tencent.androidqqmail:id/a17' ).set_text(code)
                # self.input(random_code,z,code)
                if d( resourceId='com.tencent.androidqqmail:id/a_' ).exists:  # 点击登录按钮
                    d( resourceId='com.tencent.androidqqmail:id/a_' ).click( )
                z.sleep(8)

            if d(resourceId='com.tencent.androidqqmail:id/h').exists:  # 判断是否要填写独立密码
                # self.input(random_code,z,"Abc" + account)
                d( resourceId='com.tencent.androidqqmail:id/h' ).set_text("Abc" + account)
                z.sleep(1)
                if d(text='确定').exists:
                    d(text='确定').click()
                z.sleep(5)

            if d(textContains='你有多个应用同时收到').exists:
                d(text='确定').click()
                z.sleep(2)

            if d(text='收件箱​').exists:
                z.toast(u"登录成功。退出模块")
                # d.server.adb.cmd("shell", "am force-stop com.tencent.androidqqmail").wait()  # 强制停止
                return True
            else:
                if d(textContains='帐号或密码错误').exists:
                    z.toast(u"帐号或密码错误")
                    return False
                elif d(textContains="未开启IMAP服务").exists:
                    z.toast( u"未开启IMAP服务，标记为异常" )
                    self.backup_info( args["repo_account_id"], 'exception', account, '','' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                    return False
                elif d(text='当前网络不可用').exists:
                    z.toast('当前网络不可用,跳出模块')
                    return True

    def get_accont(self, cateId, interval, limit, condition="", recover=""):
        path = "/repo_api/account/pick?status=%s&cate_id=%s&interval=%s&limit=%s&condition=%s&recover=%s" % (
        "normal", cateId, interval, limit, condition, recover)
        url = self.domain + path
        response = requests.get(url)
        # conn = httplib.HTTPConnection( self.domain, self.port, timeout=30 )
        # conn.request( "GET", path )
        # response = conn.getresponse( )
        if response.status_code == 200:
            data = response.text
            numbers = json.loads( data )
            if numbers == [] and recover != '':
                path = "/repo_api/account/pick?status=%s&cate_id=%s&interval=%s&limit=%s&condition=%s&recover=%s" % (
                    "normal", cateId, interval, limit, condition, recover)
                url = self.domain + path
                response = requests.get( url )
                if response.status_code == 200:
                    data = response.text
                    numbers = json.loads( data )
            return numbers
        else:
            path = "/repo_api/account/pick?status=%s&cate_id=%s&interval=%s&limit=%s&condition=%s&recover=%s" % (
                "normal", cateId, interval, limit, condition, recover)
            url = self.domain + path
            response = requests.get( url )
            if response.status_code == 200:
                data = response.text
                numbers = json.loads( data )
                return numbers
            else:
                return []

    def get_material(self, cateId, interval, limit, wid=''):    #wid是用来发微信朋友圈的
        path = "/repo_api/material/pick?status=normal&cate_id=%s&interval=%s&limit=%s&wid=%s" % (cateId,interval,limit,wid)
        url = self.domain + path
        response = requests.get( url )
        if response.status_code == 200:
            data = response.text
            numbers = json.loads( data )
            return numbers
        else:
            return []

    def backup_info(self, cateId, status, Number, IMEI, remark):  # 仓库号，状态，QQ号，备注设备id_卡槽id
        # path = "/repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % (cateId,status,Number,IMEI,remark)
        # conn = httplib.HTTPConnection(self.domain, self.port, timeout=30)
        # conn.request("GET",path)
        data = {"cate_id": cateId, "status": status, 'Number': Number, 'IMEI': IMEI, "cardslot": remark}
        path = "/repo_api/account/statusInfo"
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Connection": "Keep-Alive"};
        url = self.domain + path
        response = requests.post( url, data, headers=headers )
        # print response.status_code

    def write_cate(self,qqNumber,numberCateId,cate_id):
        # qqNumber = '2879127010'
        # numberCateId = '407'
        path = "/repo_api/account/getAccountNumber?QQNumber=%s&cate_id=%s" % (qqNumber, numberCateId)
        url = self.domain + path
        response = requests.get( url )
        data = response.text
        numbers = json.loads( data )
        password = numbers[0]['password']
        print password

        data = {"QQNumber": qqNumber, "QQPassword": password, 'PhoneNumber': None, 'cate_id': cate_id,
                'status': 'normal', 'IMEI': None, "cardslot": None}
        path = "/repo_api/register/numberInfo"
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Connection": "Keep-Alive"}
        url = self.domain + path
        response = requests.post( url, data, headers=headers )


def getPluginClass():
    return QQMailAddLoginUnifiedAccountCate

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("37f7b82f")
    z = ZDevice("37f7b82f")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "413", "account_time_limit": "15","againCount":"10",'domain':"http://192.168.1.102:8888"}
    # d.dump( 'test.xml' )
    # o.palyCode(d,z,"dsa")
    o.action(d, z, args)
