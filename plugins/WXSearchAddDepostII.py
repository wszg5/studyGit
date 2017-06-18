# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *
from zcache import cache
import re
import logging
logging.basicConfig(level=logging.INFO)
class WXSearchAddDepostII:

    def __init__(self):
        self.repo = Repo()

    def timeinterval(self,d, z, args):
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => stringk
        logging.info( '现在的时间%s' % nowtime )

        d1 = datetime.datetime.strptime( nowtime, '%Y-%m-%d %H:%M:%S' )
        gettime = cache.get( '%s_WXSearchAddDepostII_time'%d.server.adb.device_serial() )
        #z.toast('获得的以前的时间是%s'%gettime)
        logging.info( '以前的时间%s' % gettime )
        if gettime != None:
            d2 = datetime.datetime.strptime( gettime, '%Y-%m-%d %H:%M:%S' )
            delta1 = (d1 - d2)
            # print( delta1 )
            delta = re.findall( r"\d+\.?\d*", str( delta1 ) )  # 将天小时等数字拆开
            day1 = int( delta[0] )
            hours1 = int( delta[1] )
            minutes1 = 0
            if 'days' in str( delta1 ):
                minutes1 = int( delta[2] )
                allminutes = day1 * 24 * 60 + hours1 * 60 + minutes1
            else:
                allminutes = day1 * 60 + hours1  # 当时间不超过天时此时天数变量成为小时变量
            logging.info( "day=%s,hours=%s,minutes=%s" % (day1, hours1, minutes1) )

            logging.info( '两个时间的时间差%s' % allminutes )
            set_time = int( args['set_time'] )  # 得到设定的时间
            if allminutes < set_time:  # 由外界设定
                z.toast( '该模块未满足指定时间间隔,程序结束' )
                return 'end'
        else:
            z.toast('尚未保存时间')

    def action(self, d,z, args):
        condition = self.timeinterval( d,z, args )
        if condition == 'end':
            z.sleep( 2 )
            return
        z.heartbeat()
        add_count = int(args['add_count'])

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
        account = 0
        while True:
            if account<add_count:
                cate_id = int(args["repo_number_id"])  # 得到取号码的仓库号
                number_count = 1                       #每次取一个号码
                while True:
                    exist_numbers = self.repo.GetNumber( cate_id, 0, number_count, 'exist' )
                    print( exist_numbers )
                    remain = number_count - len( exist_numbers )
                    normal_numbers = self.repo.GetNumber( cate_id, 0, remain, 'normal' )
                    numbers = exist_numbers + normal_numbers
                    if len( numbers ) > 0:
                        break
                    d.server.adb.cmd( "shell", "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，等待中\"" % cate_id ).communicate( )
                    z.sleep( 30 )
                WXnumber = numbers[0]['number']
                z.input(WXnumber)
                z.heartbeat()
                d(textContains='搜索:').click()
                while d(textContains='正在查找').exists:
                    z.sleep(2)
                if d(textContains='操作过于频繁').exists:
                    now = datetime.datetime.now( )
                    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => stringk
                    cache.set( '%s_WXSearchAddDepostII_time' % d.server.adb.device_serial( ), nowtime,None )
                    z.toast('模块结束，保存的时间是%s'%nowtime)
                    return
                z.sleep(2)
                if d(textContains='用户不存在').exists:
                    d(descriptionContains='清除',index=2).click()
                    z.sleep(1)
                    continue
                if d(textContains='状态异常').exists:
                    d(descriptionContains='清除', index=2).click()
                    continue
                z.heartbeat()

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
                '''
                得到搜索人的v1值
                '''
                serial = z.wx_userList( )
                ids = list( json.loads( serial ) )[0]  # 将字符串改为list样式
                print(ids)
                onlyInfo = args['onlyInfo']
                if onlyInfo=='是':
                    para = {"phoneNumber": WXnumber,'x_20': ids}
                    self.repo.PostInformation( args["repo_cate_id"], para )
                    z.toast( "%s入库完成" % WXnumber )
                    d( descriptionContains='返回' ).click( )
                    d( descriptionContains='清除' ).click( )
                    continue


                z.heartbeat()
                z.sleep(1)
                if d(text='添加到通讯录').exists:      #存在联系人的情况
                    d(text='添加到通讯录').click()
                    if d( textContains='正在添加' ).exists:
                        z.sleep( 1 )
                    if d(text='发消息').exists:
                        seltype = '单向'
                    else:
                        seltype = '混合'
                    para = {"phoneNumber": WXnumber, 'x_01': nickname, 'x_02': Gender, "x_03": area, "x_04": sign,'x_05': seltype,'x_20':ids}
                    print( '--%s--%s--%s--%s--%s' % (WXnumber, nickname, Gender, area, sign) )
                    self.repo.PostInformation( args["repo_cate_id"], para )
                    z.toast( "%s入库完成" % WXnumber )

                    gender = args['gender']
                    if gender != '不限':
                        if Gender != gender:  # 看性别是否满足条件
                            d( description='返回' ).click( )
                            d( description='返回' ).click( )
                            d( descriptionContains='清除' ).click()
                            para = {"phoneNumber": WXnumber, 'x_01': nickname, 'x_02': Gender, "x_03": area,"x_04": sign, 'x_05': seltype,'x_20':ids}
                            print( '--%s--%s--%s--%s--%s' % (WXnumber, nickname, Gender, area, sign) )
                            self.repo.PostInformation( args["repo_cate_id"], para )
                            z.toast( "%s入库完成" % WXnumber )
                            continue

                    if d(text='发消息').exists:
                        d( descriptionContains='返回' ).click( )
                        d( descriptionContains='清除' ).click( )
                        continue

                else:
                    continue
                z.sleep( 2 )

                obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
                obj = obj['text']
                lenth = len(obj)
                t = 0
                while t < lenth:
                    d.press.delete()
                    t = t + 1
                d(className='android.widget.EditText').click()
                z.input(message)
                d(text='发送').click()
                z.heartbeat()
                d(descriptionContains='返回').click()
                d(descriptionContains='清除').click()
                z.sleep(1)
                account = account+1
                continue
            else:
                break

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => stringk
        cache.set( '%s_WXSearchAddDepostII_time' % d.server.adb.device_serial( ), nowtime,None )
        #z.toast('模块结束，保存的时间是%s'%nowtime)
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXSearchAddDepostII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("8HVSMZKBEQFIBQUW")
    z = ZDevice("8HVSMZKBEQFIBQUW")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    #z.wx_openuserchat('v1_fdf20d0551660ab7f940af3e87f2d73ba5efccebfabd7e9adec3b5ca0439d025906825f5cf09d7598af10cd78927fcf1@stranger')
    args = {"repo_number_id": "44", "repo_cate_id":'171',"onlyInfo":"是",'set_time':'3',"repo_material_id": "39","add_count": "3", 'gender':"不限","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)
