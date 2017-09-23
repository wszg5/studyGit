# coding:utf-8
import os

import re

from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *

class WXImpContactAddFriend:

    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )

    def GetUnique(self):
        nowTime = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" );  # 生成当前时间
        randomNum = random.randint( 0, 1000 );  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str( 00 ) + str( randomNum );
        uniqueNum = str( nowTime ) + str( randomNum );
        return uniqueNum

    # 导入通讯录
    def ImpContact(self, d, z, args):
        z.heartbeat( )
        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        filename = os.path.join( base_dir, "%s.txt" % (self.GetUnique( )) )

        number_count = int( args['number_count'] )
        cate_id = args["repo_imp_number_id"]
        while True:
            exist_numbers = self.repo.GetNumber( cate_id, 0, number_count, 'exist' )
            print( exist_numbers )
            remain = number_count - len( exist_numbers )
            normal_numbers = self.repo.GetNumber( cate_id, 0, remain, 'normal' )
            numbers = exist_numbers + normal_numbers
            if len( numbers ) > 0:
                break

            d.server.adb.cmd( "shell",
                              "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，等待中\"" % cate_id ).communicate( )
            z.sleep( 30 )

        if numbers:
            file_object = open( filename, 'w' )
            lines = ""
            pname = ""
            for number in numbers:
                if number["name"] is None:
                    pname = number["number"]
                else:
                    pname = number["name"]
                lines = "%s%s----%s\r" % (lines, pname, number["number"])

            file_object.writelines( lines )
            file_object.close( )
            # isclear = args['clear']
            isclear = '是'
            if isclear == '是':
                d.server.adb.cmd( "shell", "pm clear com.android.providers.contacts" ).communicate( )

            # d.server.adb.cmd("shell", "am", "start", "-a", "zime.clear.contacts").communicate()
            d.server.adb.cmd( "push", filename, "/data/local/tmp/contacts.txt" ).communicate( )
            d.server.adb.cmd( "shell", "am", "start", "-n", "com.zunyun.zime/.ImportActivity", "-t", "text/plain",
                              "-d",
                              "file:////data/local/tmp/contacts.txt" ).communicate( )

            # d.server.adb.cmd("shell", "am broadcast -a com.zunyun.import.contact --es file \"file:///data/local/tmp/contacts.txt\"").communicate()
            os.remove( filename )

            out = d.server.adb.cmd( "shell",
                                    "dumpsys activity top  | grep ACTIVITY" ).communicate( )[0].decode( 'utf-8' )
            while out.find( "com.zunyun.zime/.ImportActivity" ) > -1:
                z.heartbeat( )
                out = d.server.adb.cmd( "shell",
                                        "dumpsys activity top  | grep ACTIVITY" ).communicate( )[0].decode(
                    'utf-8' )
                z.sleep( 5 )

        if (args["import_time_delay"]):
            z.sleep( int( args["import_time_delay"] ) )

    def action(self, d,z, args):
        run_time = float( args['run_time'] ) * 60
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return

        self.ImpContact( d, z, args )  # 导入通讯录
        z.heartbeat( )
        z.sleep( 8 )
        z.toast( "开始执行：微信通讯录加好友+导入模块  尊云专用" )

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.press.home( )
        z.sleep(2)
        if d( text='微信' ).exists:
            d( text='微信' ).click( )
        else:
            # d.swipe( width - 20, height / 2, 0, height / 2, 5 )
            z.toast( '该页面没有微信' )
            z.sleep( 2 )
            return
        z.sleep( 5 )
        while True:
            if d( text='发现' ).exists and d( text='我' ).exists and d( text='通讯录' ).exists:
                break
            else:
                d( descriptionContains='返回', className='android.widget.ImageView' ).click( )

        d( description='更多功能按钮' ).click( )
        d( textContains='添加朋友' ).click( )
        d( textContains='手机联系人' ).click( )
        if d( text='添加手机联系人' ).exists:
            d( text='添加手机联系人' ).click( )
        if d(text='绑定手机号').exists:
            z.toast("此微信号没有绑定手机号，模块退出")
            return
        while d( textContains='正在获取' ).exists:
            z.sleep( 3 )
        z.heartbeat( )
        set1 = set( )
        change = 0
        i = 0
        t = 0
        endcon = 0
        EndIndex = int( args['EndIndex'] )  # ------------------
        while True:
            cate_id = args["repo_material_id"]  # ------------------
            Material = self.repo.GetMaterial( cate_id, 0, 1 )
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id ).communicate( )
                z.sleep( 10 )
                return
            message = Material[0]['content']  # 从素材库取出的要发的材料
            z.sleep( 1 )
            wxname = d( className='android.widget.ListView' ).child( className='android.widget.LinearLayout', index=i ) \
                .child( className='android.widget.LinearLayout' ).child( className='android.widget.LinearLayout',
                                                                         index=1 ).child( textContains='微信:' )  # 得到微信名
            if wxname.exists:
                '''
                得到电话号
                '''
                phone = d( className='android.widget.ListView' ).child( className='android.widget.LinearLayout',
                                                                        index=i ).child(
                    className='android.widget.LinearLayout' ).child( className='android.widget.LinearLayout',
                                                                     index=1 ).child(
                    className='android.widget.TextView', index=0 )
                phonenumber = phone.info['text']

                z.heartbeat( )

                alreadyAdd = d( className='android.widget.ListView' ).child( className='android.widget.LinearLayout',
                                                                             index=i ).child(
                    className='android.widget.LinearLayout', index=0 ).child( className='android.widget.FrameLayout',
                                                                              index=2 ).child(
                    text='已添加' )  # 该编号好友已经被添加的情况
                if alreadyAdd.exists:
                    i = i + 1
                    continue

                change = 1  # 好友存在且未被添加的情况出现，change值改变
                '''
                微信名
                '''
                wxname = wxname.info
                name = wxname['text']
                z.heartbeat( )
                if name in set1:  # 判断是否已经给该人发过消息
                    i = i + 1
                    continue
                else:
                    set1.add( name )
                endcon = 1
                d( className='android.widget.ListView', index=0 ).child( className='android.widget.LinearLayout',
                                                                         index=i ). \
                    child( className='android.widget.LinearLayout' ).child( className='android.widget.LinearLayout',
                                                                            index=1 ).click( )  # 点击第i个人
                '''
                得到性别
                '''
                Gender = d( className='android.widget.LinearLayout', index=1 ).child(
                    className='android.widget.LinearLayout', index=0 ).child( className='android.widget.ImageView',
                                                                              index=1 )  # 看性别是否有显示
                if Gender.exists:
                    z.heartbeat( )
                    Gender = Gender.info
                    Gender = Gender['contentDescription']
                else:
                    Gender = '空'

                z.heartbeat( )
                if d( text='地区' ).exists:
                    for k in range( 3, 10 ):
                        if d( className='android.widget.ListView' ).child( className='android.widget.LinearLayout',
                                                                           index=k ).child(
                            className='android.widget.LinearLayout', index=0 ).child( text='地区' ).exists:
                            break
                    area = d( className='android.widget.ListView' ).child( className='android.widget.LinearLayout',
                                                                           index=k ).child(
                        className='android.widget.LinearLayout', index=0 ). \
                        child( className='android.widget.LinearLayout', index=1 ).child(
                        className='android.widget.TextView' ).info['text']
                else:
                    area = '空'
                z.heartbeat( )
                if d( text='个性签名' ).exists:
                    for k in range( 3, 10 ):
                        if d( className='android.widget.ListView' ).child( className='android.widget.LinearLayout',
                                                                           index=k ).child(
                            className='android.widget.LinearLayout', index=0 ).child( text='个性签名' ).exists:
                            break
                    sign = d( className='android.widget.ListView' ).child( className='android.widget.LinearLayout',
                                                                           index=k ).child(
                        className='android.widget.LinearLayout', index=0 ). \
                        child( className='android.widget.LinearLayout', index=1 ).child(
                        className='android.widget.TextView' ).info['text']
                else:
                    sign = '空'

                print( '%s--%s--%s--%s--%s' % (phonenumber, name, Gender, sign, area) )

                serial = z.wx_userList( )
                ids = ''
                if len( serial ) != 2:
                    ids = list( json.loads( serial ) )[0]  # 将字符串改为list样式
                    print( ids )

                if d( text='社交资料' ).exists:
                    d( text='社交资料' ).click( )
                    z.sleep( 3 )
                    SJZL1 = d( resourceId='android:id/summary', className='android.widget.TextView', index=0 ).info[
                        'text']
                    d( descriptionContains='返回', className='android.widget.ImageView' ).click( )
                    z.sleep( 3 )
                SJZL = re.split( " ", SJZL1 )

                if d( text='设置备注和标签' ).exists:
                    d( text='设置备注和标签' ).click( )
                    z.sleep( 3 )
                    beizhuObj = d( className='android.widget.EditText', index=1 )
                    if beizhuObj.exists:
                        if SJZL[0] != SJZL[1]:
                            deltext = beizhuObj.info  # 将之前消息框的内容删除
                            deltext = deltext['text']
                            lenth = len( deltext )
                            m = 0
                            while m < lenth:
                                d.press.delete( )
                                m = m + 1
                            z.input( SJZL1 )
                        if SJZL[0] == SJZL[1]:
                            z.input( SJZL[1] )
                        d( text='保存' ).click( )
                        z.sleep( 3 )
                        # d( descriptionContains='返回', className='android.widget.ImageView' ).click( )
                        # z.sleep(3)

                z.heartbeat( )
                if d( text='添加到通讯录' ).exists:
                    d( text='添加到通讯录' ).click( )
                    if d( textContains='正在添加' ).exists:
                        z.sleep( 1 )
                    time.sleep( 1 )
                    if d( text='发消息' ).exists:
                        danxiang = '单向'
                        para = {"phoneNumber": phonenumber, 'x_01': name, 'x_02': Gender, "x_03": area, "x_04": sign,
                                "x_05": danxiang, 'x_20': ids}
                        self.repo.PostInformation( args["repo_save_information_id"], para )
                        z.toast( "%s入库完成" % phonenumber )
                        d( description='返回' ).click( )
                        i = i + 1
                        continue

                elif d( text='通过验证' ).exists:
                    d( text='通过验证' ).click( )
                    d( description='返回' ).click( )
                    danxiang = '未知'
                    para = {"phoneNumber": phonenumber, 'x_01': name, 'x_02': Gender, "x_03": area, "x_04": sign,
                            "x_05": danxiang, 'x_20': ids}
                    self.repo.PostInformation( args["repo_save_information_id"], para )
                    z.toast( "%s入库完成" % phonenumber )
                    d( description='返回' ).click( )
                    i = i + 1
                    continue

                else:
                    danxiang = '未知'
                    para = {"phoneNumber": phonenumber, 'x_01': name, 'x_02': Gender, "x_03": area, "x_04": sign,
                            "x_05": danxiang, 'x_20': ids}
                    self.repo.PostInformation( args["repo_save_information_id"], para )
                    z.toast( "%s入库完成" % phonenumber )
                    d( description='返回' ).click( )
                    i = i + 1
                    continue

                danxiang = '双向'  # 有添加到通讯录且非单向的情况
                para = {"phoneNumber": phonenumber, 'x_01': name, 'x_02': Gender, "x_03": area, "x_04": sign,
                        "x_05": danxiang, 'x_20': ids}
                self.repo.PostInformation( args["repo_save_information_id"], para )
                z.toast( "%s入库完成" % phonenumber )
                GenderFrom = args['gender']  # -------------------------------外界设定的性别
                if GenderFrom != '不限':
                    if Gender != GenderFrom:  # 如果性别不符号的情况
                        # para = {"phoneNumber": phonenumber, 'x_01': name, 'x_02': Gender, "x_03": area, "x_04": sign,
                        #         "x_05": danxiang}
                        # self.repo.PostInformation( args["repo_save_information_id"], para )
                        # z.toast( "%s入库完成" % phonenumber )
                        z.toast( '性别不符' )
                        d( description='返回' ).click( )
                        d( description='返回' ).click( )
                        i = i + 1
                        continue
                z.sleep( 1 )
                if t < EndIndex:
                    deltext = d( className='android.widget.EditText', index=1 ).info  # 将之前消息框的内容删除
                    deltext = deltext['text']
                    lenth = len( deltext )
                    m = 0
                    while m < lenth:
                        d.press.delete( )
                        m = m + 1
                    z.heartbeat( )
                    d( className='android.widget.EditText', index=1 ).click( )
                    z.input( message )  # ----------------------------------------
                    z.sleep( 2 )

                    d( text='发送' ).click( )
                    z.sleep( 1 )
                    d( description='返回' ).click( )
                    i = i + 1
                    t = t + 1
                    continue
                else:
                    d( description='返回' ).click( )
                    d( description='返回' ).click( )
                    z.toast( '已经成功向' + args['EndIndex'] + '个好友发送添加验证请求' )
                    break

            else:
                if change == 0:  # 一次还没有点击到人
                    if i == 1:  # 通讯录没有人的情况
                        now = datetime.datetime.now( )
                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                        z.setModuleLastRun( self.mid )
                        z.toast( '模块结束，保存的时间是%s' % nowtime )

                        return
                    d.swipe( width / 2, height * 6 / 7, width / 2, height / 7 )
                    i = 1
                    continue
                else:
                    if endcon == 0:
                        z.toast( '全部发送完成' )

                        now = datetime.datetime.now( )
                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                        z.setModuleLastRun( self.mid )
                        z.toast( '模块结束，保存的时间是%s' % nowtime )

                        if (args["time_delay"]):
                            z.sleep( int( args["time_delay"] ) )
                        return
                    d.swipe( width / 2, height * 6 / 7, width / 2, height / 7 )
                    i = 1
                    endcon = 0

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )

        if (args["time_delay"]):
            z.sleep( int( args["time_delay"] ) )

def getPluginClass():
    return WXImpContactAddFriend

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A1SK02114")
    z = ZDevice("HT4A1SK02114")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_imp_number_id": "113", 'run_time': '1', 'number_count': '15', "import_time_delay": "30",
            "repo_material_id": "39", 'EndIndex': '3', 'repo_save_information_id': '197', 'gender': "不限",
            "time_delay": "3"}  # cate_id是仓库号，length是数量
    o.action(d,z, args)

































