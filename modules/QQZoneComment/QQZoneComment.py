# coding:utf-8
import base64
import os
import random
from uiautomator import Device
from Repo import *
from util import logger
from zservice import ZDevice
from PIL import Image

from imageCode import imageCode
from smsCode import smsCode

class QQZoneComment:
    def __init__(self):
        self.repo = Repo()
        self.type = 'qqmail'

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 1000)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

    def input(self,z,height,text,flag=True):
        if flag:
            if height>888:
                z.input(text)
            else:
                z.cmd( "shell", "am broadcast -a ZY_INPUT_TEXT --es text \\\"%s\\\"" % text )
        else:
            if height<=888:
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
            with open( codePng, 'rb' ) as f:
                # file = f.read()
                file = "data:image/jpeg;base64," + base64.b64encode( f.read( ) )
                da = {"IMAGES": file}
                path = "/ocr.index"
                headers = {"Content-Type": "application/x-www-form-urlencoded",
                           "Connection": "Keep-Alive"}
                conn = httplib.HTTPConnection( "162626i1w0.51mypc.cn", 10082, timeout=30 )
                params = urllib.urlencode( da )
                conn.request( method="POST", url=path, body=params, headers=headers )
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

    def login(self, d, z, args):
        z.generate_serial( "com.qzone" )  # 随机生成手机特征码
        d.server.adb.cmd( "shell",
                          "su -c 'rm -r -f /storage/emulated/0/tencent/QQmail'" )  # 删除/storage/emulated/0/tencent/QQmail文件夹
        time.sleep( 2 )
        d.server.adb.cmd( "shell", "pm clear com.qzone" ).communicate( )  # 清除QQ邮箱缓存
        d.server.adb.cmd( "shell",
                          "am start -n com.qzone/com.tencent.sc.activity.SplashActivity" ).communicate( )  # 拉起QQ邮箱
        z.sleep( 15 )
        z.heartbeat( )

        try:
            accounts = self.repo.GetAccount( args['repo_account_id'], int( args['account_time_limit'] ),
                                             1 )  # 去仓库获取QQ邮箱帐号
            if len( accounts ) == 0:
                z.toast( u"帐号库为空" )
                return

            account = accounts[0]['number']
            password = accounts[0]['password']
            # account = "17094558161"
            # password = "tifo5456"
            if d( resourceId="com.qzone:id/qqId" ).exists:
                d( resourceId="com.qzone:id/qqId" ).set_text( account )
                time.sleep( 1 )
                d( resourceId="com.qzone:id/passWord" ).set_text( password )
                time.sleep( 1 )
                d( resourceId="com.qzone:id/login_btn" ).click( )
                time.sleep( 5 )
                while True:
                    if d( textContains="正在处理..." ).exists:
                        time.sleep( 3 )
                    else:
                        break
                while d( resourceId='com.qzone:id/verifyImage' ).exists:  # 出现验证码
                    picObj = d( resourceId='com.qzone:id/verifyImage' )
                    code = self.palyCode( d, z, picObj )
                    if code == "":
                        return False
                    if d( resourceId='com.qzone:id/verifyInput' ).exists:
                        d( resourceId='com.qzone:id/verifyInput' ).set_text( code )
                    if d( resourceId='com.qzone:id/bar_right_button' ).exists:  # 点击登陆
                        d( resourceId='com.qzone:id/bar_right_button' ).click( )
                    z.sleep( 5 )
                z.heartbeat( )
                if d(text="该帐号被盗风险较高被暂时冻结，请前往安全中心查询或进行资金管理。").exists:
                    z.toast("该帐号被盗风险较高被暂时冻结，请前往安全中心查询或进行资金管理。")
                    self.repo.BackupInfo( args['repo_account_id'], 'frozen', account, '','' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
                    return False
                if d( resourceId="com.qzone:id/skip_button" ).exists:
                    d( resourceId="com.qzone:id/skip_button" ).click( )
                    time.sleep( 1 )
                    d.press.back( )
                    return True
                if d( resourceId="com.qzone:id/passWord" ).exists:
                    againCount = int(args["againCount"])
                    for i in range(againCount):
                        againResult = self.againLogin(account,password,d, args)
                        if againCount is True:
                            return True
                        elif againCount=="frozen":
                            return False
                    else:
                        return False


        except:
            return False

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
        while True:
            result = self.login(d,z,args)
            if result is True:
                break
        z.heartbeat( )
        if d(text="我的空间",resourceId="com.qzone:id/tab_name").exists:
            d( text="我的空间", resourceId="com.qzone:id/tab_name" ).click()
            time.sleep(3)
            if d(text="好友",resourceId="com.qzone:id/user_info_host_item_title").exists:
                d( text="好友", resourceId="com.qzone:id/user_info_host_item_title" ).click()
                time.sleep(2)
            else:
                d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
                time.sleep( 2 )
                if d( text="好友", resourceId="com.qzone:id/user_info_host_item_title" ).exists:
                    d( text="好友", resourceId="com.qzone:id/user_info_host_item_title" ).click( )
                    time.sleep( 2 )
                else:
                    print u"error"
            if d(resourceId="com.qzone:id/user_info_host_all_friends").exists:
                d( resourceId="com.qzone:id/user_info_host_all_friends" ).click()
                time.sleep(1)
            sendCount = int(args["sendCount"])
            count = 0
            while count < sendCount:
                z.heartbeat()
                if d(resourceId="com.qzone:id/friendListSearchText").exists:
                    repo_mail_cateId = args["repo_mail_cateId"]
                    numbers = self.repo.GetNumber( repo_mail_cateId, 120, 1 )
                    if len(numbers)==0:
                        d.server.adb.cmd( "shell",
                                          "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_mail_cateId ).communicate( )
                        z.sleep( 10 )
                        return
                    number = numbers[0]['number'].encode( "utf-8" )
                    # number = "342133515"
                    d( resourceId="com.qzone:id/friendListSearchText" ).set_text(number)
                    if d(resourceId="com.qzone:id/friendListItemNickName").exists:
                        d( resourceId="com.qzone:id/friendListItemNickName" ).click()
                        time.sleep(10)
                if d(text="没有权限访问该空间").exists:
                    z.toast("没有权限访问该空间")
                    # print "没有权限访问该空间"
                    self.repo.UpdateNumberStauts( number, repo_mail_cateId, "not_exist" )
                    for b in range( 2 ):
                        d.press.back( )
                        time.sleep( 1 )
                        if d( resourceId="com.qzone:id/edit_clear" ).exists:
                            d( resourceId="com.qzone:id/edit_clear" ).click( )
                            time.sleep( 1 )
                            break
                    continue
                # obj = d(resourceId="com.qzone:id/user_info_summary_bar_mood").child(index=0, className="android.widget.LinearLayout").child(resourceId="com.qzone:id/user_info_summary_bar_mood_count")
                z.heartbeat( )
                obj = d(resourceId="com.qzone:id/user_info_summary_bar_mood_count")
                if obj.exists:
                    num = obj.info["text"]
                    if num:
                        num = int(num)
                        if num>0:
                            if d(resourceId="com.qzone:id/text",text="加载更多").exists:
                                d( resourceId="com.qzone:id/text", text="加载更多" ).click()
                                time.sleep(2)
                            repo_material_cateId = args["repo_material_cateId"]
                            Material = self.repo.GetMaterial( repo_material_cateId, 0, 1 )
                            if len( Material ) == 0:
                                d.server.adb.cmd( "shell",
                                                  "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_material_cateId ).communicate( )
                                z.sleep( 10 )
                                return
                            message = Material[0]['content'].encode("utf-8")
                            if not d(text="评论",resourceId="com.qzone:id/feed_operation_comment").exists:
                                d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
                                time.sleep( 2 )
                                if not d( text="评论", resourceId="com.qzone:id/feed_operation_comment" ).exists:
                                    d.swipe( width / 2, height * 4 / 5, width / 2, height / 5 )
                                    time.sleep( 2 )
                                    if not d( text="评论", resourceId="com.qzone:id/feed_operation_comment" ).exists:
                                        z.toast("无法查看说说")
                                        for b in range( 2 ):
                                            d.press.back( )
                                            time.sleep( 1 )
                                            if d( resourceId="com.qzone:id/edit_clear" ).exists:
                                                d( resourceId="com.qzone:id/edit_clear" ).click( )
                                                time.sleep( 1 )
                                                break
                                        self.repo.UpdateNumberStauts(number, repo_mail_cateId, "not_exist")
                                        continue
                            if d(text="评论",resourceId="com.qzone:id/feed_operation_comment").exists:
                                d( text="评论", resourceId="com.qzone:id/feed_operation_comment" ).click()
                                time.sleep(1)
                                inputObj = d( index=2, resourceId="com.qzone:id/replyInput", className="android.widget.EditText" )
                                if inputObj.exists:
                                    inputObj.click()
                                    # d( index=2,resourceId="com.qzone:id/replyInput" ,className="android.widget.EditText").set_text(t)
                                    self.input(z,height,message)
                                    if inputObj.exists:
                                        inputText = inputObj.info["text"]
                                        if inputText:
                                            pass
                                        else:
                                            self.input( z, height, message, False)

                                    if d(resourceId="com.qzone:id/bar_right_button").exists:
                                        d( resourceId="com.qzone:id/bar_right_button" ).click()
                                        time.sleep(3)
                            count = count + 1
                            for b in range(2):
                                d.press.back()
                                time.sleep(1)
                                if d(resourceId="com.qzone:id/edit_clear").exists:
                                    d( resourceId="com.qzone:id/edit_clear" ).click()
                                    time.sleep(1)
                                    break
                        else:
                            for b in range(2):
                                d.press.back()
                                time.sleep(1)
                                if d(resourceId="com.qzone:id/edit_clear").exists:
                                    d( resourceId="com.qzone:id/edit_clear" ).click()
                                    time.sleep(1)
                                    break
                            self.repo.UpdateNumberStauts( number, repo_mail_cateId, "not_exist" )
                    else:
                        for b in range( 2 ):
                            d.press.back( )
                            time.sleep( 1 )
                            if d( resourceId="com.qzone:id/edit_clear" ).exists:
                                d( resourceId="com.qzone:id/edit_clear" ).click( )
                                time.sleep( 1 )
                                break
                        self.repo.UpdateNumberStauts(number, repo_mail_cateId, "not_exist")

                else:
                    for b in range( 2 ):
                        d.press.back( )
                        time.sleep( 1 )
                        if d( resourceId="com.qzone:id/edit_clear" ).exists:
                            d( resourceId="com.qzone:id/edit_clear" ).click( )
                            time.sleep( 1 )
                            break
                    self.repo.UpdateNumberStauts( number, repo_mail_cateId, "not_exist" )


    def againLogin(self,account,password, d, args):
        d( resourceId="com.qzone:id/passWord" ).set_text( password )
        time.sleep( 1 )
        d( resourceId="com.qzone:id/login_btn" ).click( )
        time.sleep( 5 )
        while True:
            if d( textContains="正在处理..." ).exists:
                time.sleep( 3 )
            else:
                break
        while d( resourceId='com.qzone:id/verifyImage' ).exists:  # 出现验证码
            picObj = d( resourceId='com.qzone:id/verifyImage' )
            code = self.palyCode( d, z, picObj )
            if code == "":
                return False
            if d( resourceId='com.qzone:id/verifyInput' ).exists:
                d( resourceId='com.qzone:id/verifyInput' ).set_text( code )
            if d( resourceId='com.qzone:id/bar_right_button' ).exists:  # 点击登陆
                d( resourceId='com.qzone:id/bar_right_button' ).click( )
            z.sleep( 5 )
        if d( text="该帐号被盗风险较高被暂时冻结，请前往安全中心查询或进行资金管理。" ).exists:
            z.toast( "该帐号被盗风险较高被暂时冻结，请前往安全中心查询或进行资金管理。" )
            self.repo.BackupInfo( args['repo_account_id'], 'frozen', account, '', '' )  # 仓库号,使用中,QQ号,设备号_卡槽号QQNumber
            return "frozen"
        if d( resourceId="com.qzone:id/skip_button" ).exists:
            d( resourceId="com.qzone:id/skip_button" ).click( )
            time.sleep( 1 )
            d.press.back( )
            return True
        if d( resourceId="com.qzone:id/passWord" ).exists:
            return False

def getPluginClass():
    return QQZoneComment

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT536SK03609")
    z = ZDevice("HT536SK03609")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_account_id": "250", "account_time_limit": "15","repo_mail_cateId": "228","repo_material_cateId":"227","againCount":"3","sendCount":"3"}
    # d.dump( 'test.xml' )
    # o.palyCode(d,z,"dsa")
    # d.server.adb.cmd( "shell", "pm clear com.qzone" ).communicate( )  # 清除QQ邮箱缓存
    # d.server.adb.cmd( "shell","am start -n com.qzone/com.tencent.feedback.eup.ConfirmDialog" ).communicate( )  # 拉起QQ邮箱
    # o.input( z, 888, "哈哈" )
    # d.server.adb.cmd( "shell", "am force-stop com.qzone" ).communicate( )  # 强制停止
    # d.server.adb.cmd( "shell", "am start -n com.qzone/com.tencent.sc.activity.SplashActivity" ).communicate( )  # 拉起QQ邮箱
    # time.sleep(3)
    # o.action(d, z, args)

    # o.repo.UpdateNumberStauts( "100085039", "372", "not_exist" )
