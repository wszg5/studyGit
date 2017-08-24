# coding:utf-8
from uiautomator import Device
import  time,threading
from zservice import ZDevice
import random
import re
from Repo import *

class MobilqqUpdatePicWall:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.toast( "准备执行QQ交友资料修改" )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ交友资料修改" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.mobileqq" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        z.heartbeat( )
        if d( text="消息" ).exists:
            z.toast( "卡槽状态正常，继续执行" )
        else:
            z.toast( "卡槽状态异常，跳过此模块" )
            return

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        z.heartbeat()
        if d(text='绑定手机号码').exists:
            d(text='关闭').click()
        if d(textContains='匹配').exists:
            d.press.back()
        # d(description='快捷入口').click()
        # d( descriptionContains='快捷入口' ).click( )
        # d(text='加好友/群').click()
        z.heartbeat()
        while not d(text='附近的人',className="android.widget.TextView").exists:
            if d(index=2,text="动态",className="android.widget.TextView").exists:
               d(index=2,text="动态",className="android.widget.TextView").click()
            z.sleep(1)
            z.heartbeat()
            if d(index=1,text="附近",className="android.widget.TextView").exists:
                z.sleep(1)
                z.heartbeat()
                d(index=1,text="附近",className="android.widget.TextView").click()
        # d(text='附近的人',className="android.widget.TextView").click()
        tempnum = 0
        objtemp = d( index=2, className="android.widget.LinearLayout" ).child( index=0,className="android.widget.LinearLayout",resourceId="com.tencent.mobileqq:id/name" ).child(
            index="0", className="android.widget.RelativeLayout" ).child(index=0,className="android.widget.ImageView",resourceId="com.tencent.mobileqq:id/icon")
        while True:
            if objtemp.exists:
                z.sleep(1)
                break
            else:
                z.sleep( 2 )
                if tempnum == 4:
                    break
                else:
                    tempnum = tempnum + 1
        # d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=2).click()
        # z.sleep(5)
        while objtemp.exists:
            z.sleep(1)
            z.heartbeat()
            objtemp.click()
        forwait = 0
        while True:
            if d(text='附近点赞升级啦').exists:
                d( text='知道了' ).click( )
                break
            else:
                z.sleep(1)
                if forwait == 4:
                    break
                else:
                    forwait = forwait+1

        while not d(text='编辑交友资料').exists:
            time.sleep(2)
        z.sleep(1)
        z.heartbeat()
        d(text='编辑交友资料',className="android.widget.Button").click()
        if d(text='立即编辑').exists:
            d(text='立即编辑').click()
            z.sleep(2)

        # if d( className='android.widget.FrameLayout', index=3 ).child( className='android.widget.ImageView',index=1 ).exists:
        #     z.heartbeat( )
        #     d( className='android.widget.FrameLayout', index=3 ).child( className='android.widget.ImageView',index=1 ).click( )
        topobj = d( index=0, className="android.widget.LinearLayout" ).child( index=0,resourceId="com.tencent.mobileqq:id/name",className="android.widget.RelativeLayout" ).child(
            index=1, resourceId="com.tencent.mobileqq:id/name", className="android.widget.RelativeLayout" )
        for m in range( 0, 12 ):
            if topobj.exists or d(className="android.widget.FrameLayout",description="添加图片").exists:
                if d(className="android.widget.FrameLayout",description="添加图片").exists:
                    z.heartbeat()
                    d( className="android.widget.FrameLayout", description="添加图片" ).click()
                else:
                    topobj.click( )
                # for m in range(0,12):
                z.heartbeat()
                d(text='从手机相册选择图片',className="android.widget.TextView").click()
                time.sleep(2)
                if d(className='com.tencent.widget.GridView').child(className='android.widget.RelativeLayout',index=m).exists:
                    d(className='com.tencent.widget.GridView').child(className='android.widget.RelativeLayout', index=m).click()
                else:
                    z.toast('手机不足12张图片')
                    if d(text="取消",resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText").exists:
                        d(text="取消",resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText").click()
                    break
                rangee = d(className='android.widget.RelativeLayout', index=0).child(className='android.widget.RelativeLayout',index=1).child(className='android.view.View').info['bounds']
                x1 = rangee['left']     #缩小图片
                y1 = rangee['top']
                x2 = rangee['right']
                y2 = rangee['bottom']
                print(rangee)
                d(className='android.view.View').gesture((x1, y1), (x1, y1)).to((x2, y2), (x2, y2))
                d(text='完成').click()
                z.sleep(2)
                z.heartbeat()
                if not d(description='添加图片').exists:
                   break
                z.heartbeat()
            else:
                picnum = d( textContains='上传真实照片' ).right( className='android.widget.TextView', index=1 )
                if picnum.exists:
                    picnum = picnum.info["text"]
                    picnum = re.findall( r"\d+\.?\d*", picnum )
                    if int(picnum[0])<12:
                        d( description='添加图片' ).click( )
                        d( textContains='从手机相册选择图片' ).click( )
                    capic = int(picnum[0])
                    for a in (12,capic,-1):
                        if d( className='com.tencent.widget.GridView' ).child( className='android.widget.RelativeLayout',index=a ).exists:
                            d( className='com.tencent.widget.GridView' ).child( className='android.widget.RelativeLayout',index=a ).click()
                        else:
                            z.toast( '手机不足12张图片' )
                            if d( text="取消", resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText" ).exists:
                                d( text="取消", resourceId="com.tencent.mobileqq:id/ivTitleBtnRightText" ).click( )
                            break
        z.sleep(2)
        z.heartbeat()
        nickname = d( text='交友昵称' ).right( className='android.widget.EditText', index=1 )
        lenname = len( nickname.info['text'] )
        nickname.click( )
        t = 0
        while t < lenname:
            d.press.delete( )
            t = t + 1
        cate_id = args["repo_name_id"]
        Material = self.repo.GetMaterial( cate_id, 0, 1 )
        if len( Material ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id ).communicate( )
            z.sleep( 10 )
            return
        name = Material[0]['content']  # 取出验证消息的内容
        z.input( name )
        d.swipe( width / 2, height * 7 / 8, width / 2, height / 8 )
        z.sleep( 2 )
        gender = '女'
        if not d( text=gender ).exists:
            d( text='男' ).click( )
            d.swipe( width / 2, height * 3 / 4, width / 2, height / 4 )
            d( text='完成' ).click( )
            z.sleep( 1 )
        z.heartbeat( )
        d( text='生日' ).right( className='android.widget.EditText' ).click( )  # 设置年份
        setyear = random.randint( 1996, 2000 )
        print( 'setyear是%s' % setyear )
        nowyear = d( textContains='年', index='3' ).info['text']
        nowyear = int( re.findall( r"\d+\.?\d*", nowyear )[0] )
        if setyear < nowyear:
            num = nowyear - setyear
            for i in range( 0, num ):
                d( textContains='年', index=2 ).click( )
        else:
            num = setyear - nowyear
            for i in range( 0, num ):
                d( textContains='年', index=4 ).click( )

        setmonth = random.randint( 1, 12 )  # 设置月份
        print( 'setmonth是%s' % setmonth )
        nowmonth = d( textContains='月', index='3' ).info['text']
        nowmonth = int( re.findall( r"\d+\.?\d*", nowmonth )[0] )

        if setmonth < nowmonth:
            num = nowmonth - setmonth
            for i in range( 0, num ):
                d( textContains='月', index=2 ).click( )
        else:
            num = setmonth - nowmonth
            for i in range( 0, num ):
                if d( textContains='月', index=4 ).exists:
                    d( textContains='月', index=4 ).click( )
                else:
                    d( textContains='月', index=3 ).click( )

        setday = random.randint( 1, 30 )  # 设置月份
        print( 'setday是%s' % setday )
        nowday = d( textContains='日', index='3' ).info['text']
        nowday = int( re.findall( r"\d+\.?\d*", nowday )[0] )
        if setday < nowday:
            num = nowday - setday
            for i in range( 0, num ):
                d( textContains='日', index=2 ).click( )
        else:
            num = setday - nowday
            for i in range( 0, num ):
                if d( textContains='日', index=4 ).exists:
                    d( textContains='日', index=4 ).click( )
                else:
                    d( textContains='月', index=3 ).click( )

        d( text='完成' ).click( )
        z.heartbeat( )
        if d( text='想对附近的人说点什么' ).exists:
            d( text='交友宣言' ).right( className='android.widget.EditText' ).click( )
            cate_id = args["repo_declaration_id"]
            Material = self.repo.GetMaterial( cate_id, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"素材%s号仓库为空，没有取到交友宣言\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            Fredeclaration = Material[0]['content']  # 取出验证消息的内容
            z.input( Fredeclaration )
            d( text='返回' ).click( )

        if d( textContains='你的情感状态' ).exists:
            d( textContains='你的情感状态' ).click( )
            d( text='保密' ).click( )
            d( text='完成' ).click( )

        if d( text='选择职业，发现同行' ).exists:
            d( text='选择职业，发现同行' ).click( )
            d.swipe( width / 2, height * 4 / 5, width / 2, height / 6 )
            d( text='其他职业' ).click( )

        if d( text='填写公司，发现同事' ).exists:
            d( text='填写公司，发现同事' ).click( )
            cate_id = args["repo_company_id"]
            Material = self.repo.GetMaterial( cate_id, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"素材%s号仓库为空，没有取到公司名\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            company = Material[0]['content']  # 取出验证消息的内容
            z.input( company )

        d.swipe( width / 2, height * 5 / 6, width / 2, height / 6 )
        z.heartbeat( )
        if d( textContains='填写学校' ).exists:
            d( textContains='填写学校' ).click( )
            while not d( textContains='发现校友' ).exists:
                time.sleep( 2 )
            cate_id = args["repo_school_id"]
            Material = self.repo.GetMaterial( cate_id, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            school = Material[0]['content']  # 取出验证消息的内容
            z.input( school )
            d( text='返回' ).click( )
        time.sleep( 3 )
        # if d(text="选择故乡,发现老乡").exists:
        #     d( text="选择故乡,发现老乡" ).click()
        #     if d(text="国家",className="android.widget.TextView").exists:
        #         d( text="国家", className="android.widget.TextView" ).click()
        #         d(text="中国",className='android.widget.TextView').click()
        #     if d(text="省市",className="android.widget.TextView").exists:
        #         d( text="省市", className="android.widget.TextView" ).click()
        #
        d.swipe( width / 2, height * 7 / 8, width / 2, height / 7 )
        if d( text='喜欢的电影' ).exists:
            d( text='喜欢的电影' ).click( )
            for i in range( 0, 8 ):
                select = random.randint( 0, 6 )
                d( className='android.widget.ListView' ).child( className='android.widget.RelativeLayout',
                                                                index=select ).click( )
                if i == 3:
                    d.swipe( width / 2, height * 7 / 8, width / 2, height / 7 )
            d( text='返回' ).click( )

        if d( text='喜欢的明星' ).exists:
            d( text='喜欢的明星' ).click( )
            for i in range( 0, 8 ):
                d( className='android.widget.ListView' ).child( className='android.widget.RelativeLayout',
                                                                index=i ).click( )
            d( text='返回' ).click( )
        z.heartbeat( )
        d.swipe( width / 2, height * 7 / 8, width / 2, height / 7 )
        if d( text='喜欢的游戏' ).exists:
            d( text='喜欢的游戏' ).click( )
            for i in range( 0, 8 ):
                select = random.randint( 0, 7 )
                d( className='android.widget.ListView' ).child( className='android.widget.RelativeLayout',
                                                                index=select ).click( )
                if i == 3:
                    d.swipe( width / 2, height * 7 / 8, width / 2, height / 7 )
            d( text='返回' ).click( )
        z.heartbeat( )
        d.swipe( width / 2, height * 7 / 8, width / 2, height / 7 )
        if d( text='去过的地方' ).exists:
            d( text='去过的地方' ).click( )
            for i in range( 0, 8 ):
                select = random.randint( 0, 8 )
                d( className='android.widget.ListView' ).child( className='android.widget.RelativeLayout',
                                                                index=select ).click( )
                if i == 3:
                    d.swipe( width / 2, height * 7 / 8, width / 2, height / 7 )
            d( text='返回' ).click( )

        if d( text='爱吃的美食' ).exists:
            d( text='爱吃的美食' ).click( )
            z.sleep( 2 )
            for i in range( 0, 8 ):
                select = random.randint( 0, 9 )
                d( className='android.widget.ListView' ).child( className='android.widget.RelativeLayout',
                                                                index=select ).click( )
                if i == 3:
                    d.swipe( width / 2, height * 7 / 8, width / 2, height / 7 )
            d( text='返回' ).click( )

        if d( text='常用的品牌' ).exists:
            d( text='常用的品牌' ).click( )
            z.sleep( 2 )
            for i in range( 0, 8 ):
                select = random.randint( 0, 9 )
                d( className='android.widget.ListView' ).child( className='android.widget.RelativeLayout',
                                                                index=select ).click( )
                if i == 3:
                    d.swipe( width / 2, height * 7 / 8, width / 2, height / 7 )
            d( text='返回' ).click( )
        z.heartbeat( )
        d.swipe( width / 2, height * 5 / 6, width / 2, height / 7 )
        if d( text='喜欢的运动' ).exists:
            d( text='喜欢的运动' ).click( )
            z.sleep( 2 )
            for i in range( 0, 8 ):
                select = random.randint( 0, 9 )
                d( className='android.widget.ListView' ).child( className='android.widget.RelativeLayout',
                                                                index=select ).click( )
                if i == 3:
                    d.swipe( width / 2, height * 7 / 8, width / 2, height / 7 )
            d( text='返回' ).click( )

        d( text='完成' ).click( )
        z.sleep( 2 )
        if d( text='发布资料' ).exists:
            d( text='发布资料' ).click( )

        seconds = 30
        while seconds > 0:
            seconds = seconds - 5
            z.heartbeat( )
            z.sleep( 5 )
            z.toast( "等待资料上传完成" )
            if d( textContains='编辑交友资料' ).exists:
                z.sleep(1)
                z.heartbeat()
                break
            if d( textContains='资料完整度' ).exists:
                z.sleep( 1 )
                z.heartbeat( )
                d(description="关闭",className="android.widget.ImageButton").click()
                break
        if d(text="完成").exists:
            d(text="完成").click()

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return MobilqqUpdatePicWall

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4AVSK00885")
    z = ZDevice("HT4AVSK00885")
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").communicate()

    args = {"repo_name_id":"139","repo_declaration_id":"140","repo_company_id":"141","repo_school_id":"142","time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)