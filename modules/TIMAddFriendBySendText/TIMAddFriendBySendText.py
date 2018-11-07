# coding:utf-8
import colorsys
import os

# from reportlab.graphics.shapes import Image
from PIL import Image

from smsCode import smsCode
from uiautomator import Device
from Repo import *
import  time, datetime, random
from zservice import ZDevice


class TIMAddFriendBySendText:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def action(self, d,z,args):
        z.toast( "准备执行TIM唤醒好友发消息加好友模块" )
        z.sleep(1)
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text="消息", resourceId="com.tencent.tim:id/ivTitleName" ).exists and not d( text="马上绑定",
                                                                                         className="android.widget.Button" ).exists:
            z.toast( "登录状态正常，继续执行" )
        else:
            if d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).exists:
                d( text="关闭", resourceId="com.tencent.tim:id/ivTitleBtnLeftButton" ).click( )
                z.sleep( 1 )
            elif d( text="消息", className="android.widget.TextView" ).exists and d( text="马上绑定",
                                                                                   className="android.widget.Button" ).exists:
                d( text="消息", className="android.widget.TextView" ).click( )
                z.sleep( 1 )
            elif d( text="返回" ).exists:
                d( text="返回" ).click( )
                z.sleep( 1 )

            else:
                z.toast( "登录状态异常，跳过此模块" )
                return
        z.heartbeat()

        cate_id1 = args["repo_material_cate_id"]
        all_counts = int(args['add_count'])  # 要添加多少人
        count = 1
        num = 0
        flag = False
        flag2 = False
        flag3 = True
        time_delay = args['time_delay']
        time_delay = int(time_delay)
        repo_number_cate_id2 = args['repo_number_cate_id2']
        random_code = args['random_code']
        friendCounts = int(args['friendCounts'])
        for friendCount in range(friendCounts):            #总人数
            repo_number_cate_id = args["repo_number_cate_id"]   # 得到取号码的仓库号
            numbers = self.repo.GetNumber( repo_number_cate_id, 120, 1 )  # 取出add_count条两小时内没有用过的号码
            # numbers = [{"number": '2872343938'}]
            if len( numbers ) == 0:
                if args["nuberLoop"] == "循环":
                    self.repo.UpdateNumberStauts( "", repo_number_cate_id, "normal" )
                    numbers = self.repo.GetNumber( repo_number_cate_id, 120, 1 )
                    if len( numbers ) == 0:
                        z.toast( "%s号仓库没有号码" % repo_number_cate_id )
                        return
                else:
                    d.server.adb.cmd( "shell",
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_number_cate_id ).communicate( )
                    z.sleep( 10 )
                    return
            z.heartbeat( )
            QQnumber = numbers[0]['number']
            # print(QQnumber)
            z.sleep(1)

            d.server.adb.cmd( "shell",'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=wpa\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % QQnumber )  # 临时会话
            z.sleep( random.randint( 2, 4 ) )
            if d(text='TIM').exists:
                z.heartbeat( )
                d(text='TIM').click()
                z.sleep(2)
                z.heartbeat()
                while d(text='仅此一次').exists:
                    z.heartbeat( )
                    d(text='仅此一次').click()
            for all_count in range(all_counts):
                QQnumber2 = ''
                if d(resourceId="com.tencent.tim:id/input").exists:
                    d( resourceId="com.tencent.tim:id/input" ).click()
                    numbers = self.repo.GetNumber( repo_number_cate_id2, 120, 1 )  # 取出add_count条两小时内没有用过的号码
                    # numbers = [{"number": '2088663682'}]
                    if len( numbers ) == 0:
                        if args["nuberLoop2"] == "循环":
                            self.repo.UpdateNumberStauts( "", repo_number_cate_id2, "normal" )
                            numbers = self.repo.GetNumber( repo_number_cate_id2, 120, 1 )
                            if len( numbers ) == 0:
                                z.toast( "%s号仓库没有号码" % repo_number_cate_id2 )
                                return
                        else:
                            d.server.adb.cmd( "shell",
                                              "am broadcast -a com.zunyun.zime.toast --es msg \"%s号仓库为空，没有取到消息\"" % repo_number_cate_id ).communicate( )
                            z.sleep( 10 )
                            return

                    QQnumber2 = numbers[0]['number']
                    self.input(random_code,z,'添加好友%s#'% QQnumber2)
                    if d(text="发送", resourceId='com.tencent.tim:id/fun_btn').exists:
                        d( text="发送", resourceId='com.tencent.tim:id/fun_btn' ).click()
                        time.sleep(time_delay)

                obj = d(resourceId="com.tencent.tim:id/listView1")
                text_index = 0
                for i in range(10):
                    if not obj.child(index=i).exists:
                        if i>0:
                            text_index = i - 1
                        break
                if obj.child( index=text_index ).child( resourceId='com.tencent.tim:id/chat_item_content_layout' ).exists:
                    reply_text = obj.child( index=text_index ).child(resourceId='com.tencent.tim:id/chat_item_content_layout').info['text'].encode("utf-8")
                    if '提交好友申请' in reply_text:
                        Material = self.repo.GetMaterial( cate_id1, 0, 1 )
                        if len( Material ) == 0:
                            d.server.adb.cmd( "shell",
                                              "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id1 ).communicate( )
                            z.sleep( 10 )
                            return
                        message = Material[0]['content']  # 取出验证消息的内容
                        self.input( random_code, z, '回复%s#%s' % (QQnumber2,message ))
                        if d( text="发送", resourceId='com.tencent.tim:id/fun_btn' ).exists:
                            d( text="发送", resourceId='com.tencent.tim:id/fun_btn' ).click( )
                            time.sleep( time_delay )
                            obj = d( resourceId="com.tencent.tim:id/listView1" )
                            text_index = 0
                            for i in range( 10 ):
                                if not obj.child( index=i ).exists:
                                    if i > 0:
                                        text_index = i - 1
                                    break

                            reply_text = obj.child( index=text_index ).child(
                                resourceId='com.tencent.tim:id/chat_item_content_layout' ).info['text'].encode( "utf-8" )
                            if '还不是我的好友，无法发送' in reply_text:
                                z.toast('还不是我的好友，无法发送')
                                break

                    elif '已经是我的好友了' in reply_text:
                        z.toast('TA已经是我的好友了，添加失败')
                    else:
                        z.toast("无回应...")
                        break

        z.toast( "模块完成" )

    def input(self,random_code,z,text):
        if random_code=="乱码":
            z.cmd( "shell", "am broadcast -a ZY_INPUT_TEXT --es text \\\"%s\\\"" % text )
        else:
            z.input(text)

def getPluginClass():
    return TIMAddFriendBySendText

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("37f7b82f")
    z = ZDevice("37f7b82f")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_cate_id":"407","repo_number_cate_id2":"407","repo_material_cate_id":"376",'friendCounts':"2","add_count":"3","time_delay":"3","random_code":"不乱码","nuberLoop":"循环","nuberLoop2":"不循环"}    #cate_id是仓库号，length是数量
    # o.repo.UpdateNumberStauts( "13856143219", "283", 'not_exist' )
    try:
        o.action( d, z, args )
    except :
       z.toast("模块异常")
    # d.server.adb.cmd( "shell",'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=crm\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % '2872343938' )  # 临时会话
    # QQnumber = '2872343938'
    # d.server.adb.cmd( "shell",'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=wpa\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"' % QQnumber )  # 临时会话