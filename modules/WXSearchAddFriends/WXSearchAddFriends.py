# coding:utf-8
import os

from uiautomator import Device
from Repo import *
import datetime
from zservice import ZDevice
from Inventory import *
import logging
logging.basicConfig(level=logging.INFO)

class WXSearchAddFriends:

    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath(__file__)

    def action(self, d,z, args):
        run_time = float( args['run_time'] ) * 60
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return
        z.heartbeat()

        cate_id = args["repo_material_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        if len(Material) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % cate_id).communicate()
            z.sleep(10)
            return
        message = Material[0]['content']  # 取出验证消息的内容

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(5)

        d(description='更多功能按钮',className='android.widget.RelativeLayout').click()
        z.sleep(1)
        if d(text='添加朋友').exists:
            d(text='添加朋友').click()
        else:
            d(description='更多功能按钮', className='android.widget.RelativeLayout').click()
            z.sleep(1)
            d(text='添加朋友').click()
        z.heartbeat()
        d(index='1',className='android.widget.TextView').click()   #点击搜索好友的输入框
        counter = 0
        while True:
            cate_id = int( args["repo_number_id"] )  # 得到取号码的仓库号
            number_count = 1  # 每次取一个号码
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
            WXnumber = numbers[0]['number']
            z.input( WXnumber )
            z.heartbeat( )
            z.sleep( 3 )
            d(textContains='搜索:', className='android.widget.TextView').click()
            z.sleep( 8 )
            often_count = int(args['often_count'])

            if d( textContains='操作过于频繁').exists:
                counter = counter + 1
                if counter > often_count:
                    counter = 0
                    break
                else:
                    d( descriptionContains='清除' ).click( )
                    self.repo.uploadPhoneNumber( WXnumber, args['save_often_number_id'] )
                    z.toast( '频繁手机号入库成功' )
                    continue
            z.sleep( 2 )
            if d( textContains='用户不存在' ).exists:
                d( descriptionContains='清除', index=2 ).click( )
                z.sleep( 1 )
                continue
            if d( textContains='状态异常' ).exists:
                d( descriptionContains='清除', index=2 ).click( )
                continue
            z.heartbeat( )

            Gender = d( className='android.widget.LinearLayout', index=1 ).child(
                className='android.widget.LinearLayout' ).child( className='android.widget.ImageView',
                                                                 index=1 )  # 看性别是否有显示
            if Gender.exists:
                Gender = Gender.info
                Gender = Gender['contentDescription']
            else:
                Gender = '空'
            z.heartbeat( )
            nickname = d( className='android.widget.ListView' ).child( className='android.widget.LinearLayout',
                                                                       index=1 ) \
                .child( className='android.widget.LinearLayout', index=1 ).child(
                className='android.widget.TextView' )
            if nickname.exists:
                nickname = nickname.info['text']
            else:
                nickname = '空'
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
            z.heartbeat()

            v1s = z.wx_userList()
            if len(v1s) != 2:
                v1 = list(json.loads(v1s))[0] # 将字符串改为list样式
            else:
                v1 = '空'

            gender = args['gender']
            if gender != '不限':
                if Gender != gender:  # 看性别是否满足条件
                    if d( text='添加到通讯录' ).exists:  # 存在联系人的情况
                        d( text='添加到通讯录' ).click( )
                        if d( text='发消息' ).exists:
                            seltype = '单向'
                        else:
                            seltype = '双向'

                    if v1 == '空':
                        v1s1 = z.wx_userList( )
                        if len( v1s1 ) != 2:
                            v1 = list( json.loads( v1s1 ) )[0]  # 将字符串改为list样式

                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='清除' ).click( )

                    para = {"phoneNumber": WXnumber, 'x_01': nickname, 'x_02': Gender, "x_03": area,
                            "x_04": sign,
                            "x_05": seltype, 'x_20': v1}
                    print( '--%s--%s--%s--%s--%s' % (WXnumber, nickname, Gender, area, sign) )
                    self.repo.PostInformation( args["repo_information_id"], para )
                    z.toast( "%s入库完成" % WXnumber )
                    continue

            if d( text='设置备注和标签' ).exists:
                d( text='设置备注和标签' ).click( )
                z.sleep( 3 )
                beizhuObj = d( className='android.widget.EditText', index=1 )
                if beizhuObj.exists:
                    z.input( WXnumber )
                    d( text='保存' ).click( )
                    z.sleep( 3 )

            z.heartbeat()
            if d(text='添加到通讯录').exists:  # 存在联系人的情况
                d( text='添加到通讯录' ).click( )
                if d( text='发消息' ).exists:
                    seltype = '单向'
                else:
                    seltype = '双向'

                if v1 == '空':
                    v1s2 = z.wx_userList()
                    if len( v1s2 ) != 2:
                        v1 = list( json.loads( v1s2 ) )[0]  # 将字符串改为list样式

                para = {"phoneNumber": WXnumber, 'x_01': nickname, 'x_02': Gender, "x_03": area, "x_04": sign,
                        "x_05": seltype, 'x_20': v1}
                print( '--%s--%s--%s--%s--%s' % (WXnumber, nickname, Gender, area, sign) )
                self.repo.PostInformation( args["repo_information_id"], para )
                z.toast( "%s入库完成" % WXnumber )
                if d( text='发消息' ).exists:
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='返回' ).click( )
                    z.sleep( 3 )
                    d( descriptionContains='清除' ).click( )
                    continue
            else:
                continue
            z.sleep( 2 )

            obj = d( className='android.widget.EditText' ).info  # 将之前消息框的内容删除
            obj = obj['text']
            lenth = len( obj )
            t = 0
            while t < lenth:
                d.press.delete( )
                t = t + 1
            d( className='android.widget.EditText' ).click( )
            z.input( message )
            d( text='发送' ).click( )
            z.heartbeat( )
            d( descriptionContains='返回' ).click( )
            z.sleep( 1.5 )
            d( descriptionContains='清除' ).click( )
            z.sleep( 1 )
            continue


        now = datetime.datetime.now()
        nowtime = now.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun(self.mid)
        z.toast('模块结束，保存的时间是%s' % nowtime)

def getPluginClass():
    return WXSearchAddFriends

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("5959d2f3")
    z = ZDevice("5959d2f3")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_id": "44", "repo_information_id":'204', "repo_material_id": "39", "often_count":"3","save_often_number_id":"172", 'gender': "男", "run_time": "1"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)

