# coding:utf-8
import os
import random
from zcache import cache
from uiautomator import Device
from Repo import *

from zservice import ZDevice


class BaiDuKeyWordSearch:
    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )

    def timeCompare_this(self, start_time, stop_time, compare_time):
        if start_time == "" or stop_time == "":
            return False

        if compare_time is None:
            return False

        if not ":" in start_time:
            start_time = start_time + ":00"

        if not ":" in stop_time:
            stop_time = stop_time + ":00"

        if time.strptime( start_time, '%H:%M' ) < time.strptime( stop_time, '%H:%M' ):
            if time.strptime( start_time, '%H:%M' ) < time.strptime( compare_time, '%H:%M' ) < time.strptime( stop_time, '%H:%M'):
                return True
            else:
                return False

        else:
            if time.strptime( start_time, '%H:%M' ) < time.strptime( compare_time, '%H:%M' ) < time.strptime( "23:59",
                                                                                                         '%H:%M' ) or time.strptime(
                "00:00", '%H:%M') < time.strptime( compare_time, '%H:%M') < time.strptime( stop_time, '%H:%M' ):
                return True
            else:
                return False

    def CTSim(self, d, z, args):
        z.toast( "准备执行天下游模拟坐标定位模块" )
        d.server.adb.cmd( "shell", "pm clear com.txy.anywhere" ).communicate( )  # 清除缓存
        z.sleep(1)
        d.server.adb.cmd( "shell",
                          "am start -n com.txy.anywhere/com.txy.anywhere.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep(5)
        z.heartbeat()
        if d(text='允许').exists:
            d(text='允许').click()

        repo_address_id = args["repo_address_id"]
        time = args["time"]
        address = self.repo.GetNumber( repo_address_id, time, 1, "normal", "NO" )
        if len( address ) == 0:
            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"地址库%s号仓库为空，没有取到消息\"" % repo_address_id ).communicate( )
            return
        address = address[0]['number']
        xy = address.split( ',' )
        x = xy[0]
        y = xy[1]

        while not d( text="设置", className="android.widget.RadioButton" ).exists:
            z.sleep( 2 )

        obj1 = d( index=3, resourceId="com.txy.anywhere:id/ll_function",
                  className="android.widget.LinearLayout" ).child(
            index=3, resourceId="com.txy.anywhere:id/iv_user_input", className="android.widget.ImageView" )

        obj3 = d( index=0, resourceId="com.txy.anywhere:id/rl_pin_startmockbtn_distanceLl",
                  className="android.widget.RelativeLayout" ).child(
            index=0, resourceId="com.txy.anywhere:id/iv_mapfrg_start_mock", className="android.widget.ImageView" )

        while obj1.exists:
            z.sleep( 1 )
            z.heartbeat( )
            obj1.click( )
        z.sleep( 1 )
        d( text="经度" )
        z.input( x )
        z.sleep( 2 )
        z.heartbeat( )
        d( text="纬度" ).click( )
        z.input( y )
        z.heartbeat( )
        z.sleep( 2 )
        d( text="确定", resourceId="com.txy.anywhere:id/btn_positive" ).click( )
        z.sleep( random.randint( 3, 5 ) )
        if obj3.exists:
            obj3.click( )
            z.sleep( 1 )
            z.heartbeat( )
            d.click( 100, 100 )
            z.toast( "定位完成" )

        if (args["time_delay1"]):
            z.sleep( int( args["time_delay1"] ) )


    def action(self, d, z, args):
        z.toast( "开始执行：百度关键词搜索" )
        count = 0
        while count < int(args["run_count"]):
            count += 1

            # start_time = args['start_time']
            # stop_time = args['stop_time']
            # try:
            #     if self.repo.timeCompare( start_time, stop_time ):
            #         run_interval = z.getModuleRunInterval_new( self.mid )
            #         if self.timeCompare_this(start_time, stop_time ,run_interval):
            #             z.toast( '时间:'+run_interval+'，模块搜索次数已满' )
            #             return
            #     else:
            #         z.toast( '不处于' + start_time + '～' + stop_time + '时间段内，模块不运行' )
            #         return
            # except:
            #     logging.exception( "exception" )
            #     z.toast( "输入时间格式有误" )
            #     return

            d.server.adb.cmd( "shell", "pm clear com.android.chrome" ).communicate( )  # 清除浏览器缓存

            d.server.adb.cmd( "shell", "settings put global airplane_mode_on 1" ).communicate( )
            d.server.adb.cmd( "shell",
                              "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true" ).communicate( )
            z.sleep( 3 )
            d.server.adb.cmd( "shell", "settings put global airplane_mode_on 0" ).communicate( )
            d.server.adb.cmd( "shell",
                              "am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false" ).communicate( )

            z.heartbeat( )
            z.toast("正在ping网络是否通畅")
            while True:
                ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
                print(ping)
                if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                    break
                z.sleep( 2 )

            # self.CTSim( d, z, args )  # 模拟定位

            # 获取手机IP
            IPList = d.server.adb.cmd( "shell", "curl http://ipecho.net/plain" ).communicate( )
            IP = IPList[0]

            Str = d.info  # 获取屏幕大小等信息
            height = float( Str["displayHeight"] )
            width = float( Str["displayWidth"] )

            z.generate_serial( "com.android.chrome" )  # 随机生成手机特征码
            z.toast( "随机生成手机特征码" )

            # 取关键词
            material_KeyWords_id = args["material_KeyWords_id"]
            KeyWords_interval = args["KeyWords_interval"]
            materials = Repo().GetMaterial( material_KeyWords_id, KeyWords_interval, 1 )
            if len(materials) == 0:
                z.toast(material_KeyWords_id + "号关键词仓库为空")
                return
            KeyWords = materials[0]["content"]
            BusinessName = materials[0]["name"]

            # 取发送消息
            material_msg_id = args["material_msg_id"]
            Msg_interval = args["Msg_interval"]
            materials = Repo().GetMaterial( material_msg_id, Msg_interval, 1 )
            if len( materials ) == 0:
                z.toast( material_msg_id + "号消息仓库为空" )
                return
            MsgArray = materials[0]["content"].split("｜")
            randomtime = args["time_delay3"].split( "~" )  # 发消息随机间隔时间

            d.server.adb.cmd( "shell", 'am start -a android.intent.action.VIEW -d "http://www.baidu.com"' )
            z.sleep( 8 )

            z.heartbeat()
            if d( text='接受并继续' ).exists:
                d( text="接受并继续" ).click( )
                z.sleep(2)
                if d( text="不用了" ).exists:
                    d( text="不用了" ).click( )
                z.sleep( 8 )

            if d(text="允许",resourceId="com.android.chrome:id/button_primary",className="android.widget.Button").exists:
                d( text="允许", resourceId="com.android.chrome:id/button_primary",className="android.widget.Button" ).click()
                z.sleep(1)

            z.heartbeat()
            if d(className='android.widget.EditText', resourceId='index-kw').exists:
                d(className='android.widget.EditText', resourceId='index-kw').click()
            else:
                bounds = d( description='百度一下', className='android.widget.Button', resourceId='index-bn').info['bounds']
                d.click(int(bounds['left']) - 200, (int(bounds['bottom']) - int(bounds['top'])) / 2 + int(bounds['top']))
            z.sleep(1)

            z.input(KeyWords)
            z.sleep(random.randint(1, 5))
            z.heartbeat()

            if d( description='百度一下', className='android.widget.Button', resourceId='index-bn').exists:
                d( description='百度一下', className='android.widget.Button', resourceId='index-bn' ).click()

            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            para = {"phoneNumber": KeyWords, "x_01": IP, "x_20": nowTime}
            self.repo.PostInformation(int(args['repo_information_id']), para)

            z.sleep(random.randint(15, 20))

            z.heartbeat()
            btnList = ["匿名回复",'立即回复','匿名咨询']
            existBtnList = []
            x = 0
            while True:
                x += 1
                if d( description=BusinessName ).exists:
                    d( description=BusinessName ).click( )
                    z.sleep(random.randint(30, 40))
                    z.heartbeat()

                    for btn in btnList:
                        if d( description=btn ).exists:
                            existBtnList.append( btn )

                    if len( existBtnList ) > 0 or x > 6:
                        break
                    else:
                        d.swipe( width / 2, height * 6 / 7, width / 2, height / 7 )

                else:
                    if x > 6:
                        break
                    d.swipe( width / 2, height * 6 / 7, width / 2, height / 7 )

            if len( existBtnList ) == 0:
                z.toast("这个关键词没有找到相应商家")
                continue

            for i in range(0, random.randint(1, 3)):  # 随机下翻页
                d.swipe( width / 2, height * 6 / 7, width / 2, height / 7 )
                z.sleep(2)
                z.heartbeat()

            # for i in range(0, random.randint(1)):  # 随机上翻页
            #     d.swipe( width / 2, height / 7, width / 2, height * 6 / 7 )
            #     z.sleep( 2 )
            #     z.heartbeat()

            for existBtn in existBtnList:
                if d(description=existBtn).exists:
                    d(description=existBtn).click()
                    z.sleep(3)
                    z.heartbeat()
                    if d( className='android.widget.Button' ).exists:
                        for Msg in MsgArray:
                            if d(className='android.widget.EditText').exists:
                                d(className='android.widget.EditText').click()

                                z.input(Msg)
                                z.heartbeat()

                            if d(className='android.widget.Button').exists:
                                d(className='android.widget.Button').click()
                            z.sleep(random.randint(int(randomtime[0]),int(randomtime[1])))
                            z.heartbeat()
                        para = {"phoneNumber": KeyWords, "x_01": IP, "x_02": "Y", "x_20": nowTime}
                        self.repo.PostInformation( int( args['repo_information_id'] ), para )
                        break


        now = datetime.datetime.now()
        nowtime = now.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun_new(self.mid)
        z.toast('模块结束，保存的时间是%s' % nowtime)

        if (args["time_delay2"]):
            z.sleep( int( args["time_delay2"] ) )



def getPluginClass():
    return BaiDuKeyWordSearch

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("7HQWC6U8A679SGAQ")
    z = ZDevice("7HQWC6U8A679SGAQ")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_information_id": "277", "repo_address_id": "124", "material_KeyWords_id": "212", "material_msg_id":"270", 'start_time': '16', 'stop_time': '16:10', "KeyWords_interval": "0",
            "Msg_interval": "0","run_count": "5","time_delay3": "10~15", "time_delay1": "3","time_delay2": "3","time":"60"};
    o.action(d, z, args)
    # obj = d( className='android.widget.Button' )
    # if obj.exists:
    #     obj =  d( className='android.widget.Button' ).info["bounds"]
    #     left = obj["left"]
    #     bottom = obj["bottom"]
    #     top = obj["top"]
    #     d.click(left-88,bottom - (bottom - top)/2)
    #     if obj.exists:
    #         d( className='android.widget.Button' ).left( className="android.widget.EditText" ).click()
    #         z.input("123")
    # d.server.adb.cmd( "shell", "pm clear com.android.chrome" ).communicate( )  # 清除浏览器缓存
    #
    # d.server.adb.cmd( "shell", 'am start -a android.intent.action.VIEW -d  http://www.google.cn/' )



