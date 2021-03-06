# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from zcache import cache
import re
import logging
logging.basicConfig(level=logging.INFO)

class WXAddAddressListP:

    def __init__(self):
        self.repo = Repo()

    def timeinterval(self, d,z, args):
        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        d1 = datetime.datetime.strptime( nowtime, '%Y-%m-%d %H:%M:%S' )
        logging.info( '现在的时间%s' % nowtime )
        gettime = cache.get( '%s_WXAddAddressList_time'%d.server.adb.device_serial() )
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
            z.toast( '尚未保存时间' )
    def action(self, d,z, args):
        condition = self.timeinterval(d, z, args )
        if condition == 'end':
            z.sleep( 2 )
            return
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.press.home()
        if d(text='微信').exists:
            d(text='微信').click()

        else:
            #d.swipe( width - 20, height / 2, 0, height / 2, 5 )
            z.toast('该页面没有微信')
            z.sleep(2)
            return
        z.sleep(5)
        while True:
            if d( text='发现' ) and d( text='我' ) and d( text='通讯录' ).exists:
                break
            else:
                d( descriptionContains='返回', className='android.widget.ImageView' ).click( )

        d(description='更多功能按钮').click()
        d(textContains='添加朋友').click()
        d(textContains='手机联系人').click()
        d(text='添加手机联系人').click()
        while d(textContains='正在获取').exists:
            z.sleep(3)
        z.heartbeat()
        set1 = set()
        change = 0
        i = 0
        t = 0
        endcon = 0
        EndIndex = int(args['EndIndex'])         #------------------
        while True :
            cate_id = args["repo_material_id"]   #------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                z.sleep(10)
                return
            message = Material[0]['content']  # 从素材库取出的要发的材料
            z.sleep(1)
            wxname = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=i)\
                .child(className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).child(textContains='微信:')     #得到微信名
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


                z.heartbeat()
                alreadyAdd = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=i).child(
                    className='android.widget.LinearLayout', index=0).child(className='android.widget.FrameLayout',index=2).child(text='已添加')  # 该编号好友已经被添加的情况
                if alreadyAdd.exists:
                    i = i+1
                    continue

                change = 1      #好友存在且未被添加的情况出现，change值改变
                '''
                微信名
                '''
                wxname = wxname.info
                name = wxname['text']
                z.heartbeat()
                if name in set1:    #判断是否已经给该人发过消息
                    i = i+1
                    continue
                else:
                    set1.add(name)
                print(name)
                endcon = 1
                d(className='android.widget.ListView',index=0).child(className='android.widget.LinearLayout',index=i).\
                    child(className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).click()      #点击第i个人
                '''
                得到性别
                '''
                Gender = d( className='android.widget.LinearLayout', index=1 ).child(
                    className='android.widget.LinearLayout' ).child( className='android.widget.ImageView',index=1 )  # 看性别是否有显示
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
                                className='android.widget.LinearLayout', index=0 ).child(text='个性签名').exists:
                            break
                    sign = d( className='android.widget.ListView' ).child( className='android.widget.LinearLayout',
                                                                           index=k ).child(
                        className='android.widget.LinearLayout', index=0 ). \
                        child( className='android.widget.LinearLayout', index=1 ).child(
                        className='android.widget.TextView' ).info['text']
                else:
                    sign = '空'

                print('%s--%s--%s--%s--%s'%(phonenumber,name,Gender,sign,area))


                z.heartbeat()
                if d(text='添加到通讯录').exists:
                    d(text='添加到通讯录').click()
                    if d( textContains='正在添加' ).exists:
                        z.sleep(1)
                    time.sleep(1)
                    if d(text='发消息').exists:
                        danxiang = '单向'
                        para = {"phoneNumber": phonenumber, 'x_01': name, 'x_02': Gender, "x_03": area, "x_04": sign,"x_05": danxiang}
                        self.repo.PostInformation( args["repo_cate_id"], para )
                        z.toast( "%s入库完成" % phonenumber )
                        d(description='返回').click()
                        i = i+1
                        continue

                elif d(text='通过验证').exists:
                    d(text='通过验证').click()
                    d(description='返回').click()
                    danxiang = '未知'
                    para = {"phoneNumber": phonenumber, 'x_01': name, 'x_02': Gender, "x_03": area, "x_04": sign,"x_05": danxiang}
                    self.repo.PostInformation( args["repo_cate_id"], para )
                    z.toast( "%s入库完成" % phonenumber )
                    d( description='返回' ).click( )
                    i = i + 1
                    continue

                else:
                    danxiang = '未知'
                    para = {"phoneNumber": phonenumber, 'x_01': name, 'x_02': Gender, "x_03": area, "x_04": sign,"x_05": danxiang}
                    self.repo.PostInformation( args["repo_cate_id"], para )
                    z.toast( "%s入库完成" % phonenumber )
                    d(description='返回').click()
                    i = i+1
                    continue

                danxiang = '非单项'       #有添加到通讯录且非单项的情况
                GenderFrom = args['gender']  # -------------------------------外界设定的性别
                if GenderFrom !='不限':
                    if Gender != GenderFrom:  #如果性别不符号的情况
                        para = {"phoneNumber": phonenumber, 'x_01': name, 'x_02': Gender, "x_03": area, "x_04": sign,"x_05":danxiang}
                        self.repo.PostInformation( args["repo_cate_id"], para )
                        z.toast( "%s入库完成" % phonenumber )
                        d(description='返回').click()
                        d( description='返回' ).click( )
                        i = i+1
                        continue

                para = {"phoneNumber": phonenumber, 'x_01': name, 'x_02': Gender, "x_03": area, "x_04": sign,"x_05": danxiang}
                self.repo.PostInformation( args["repo_cate_id"], para )
                z.toast( "%s入库完成" % phonenumber )
                z.sleep(1)
                if t<EndIndex:
                    deltext = d(className='android.widget.EditText', index=1).info  # 将之前消息框的内容删除
                    deltext = deltext['text']
                    lenth = len(deltext)
                    m = 0
                    while m < lenth:
                        d.press.delete()
                        m = m + 1
                    z.heartbeat()
                    d(className='android.widget.EditText', index=1).click()
                    z.input(message)       #----------------------------------------
                    d(text = '发送').click()
                    z.sleep(1)
                    d(description='返回').click()
                    i = i+1
                    t = t+1
                    continue
                else:
                    d( description='返回' ).click()
                    d( description='返回' ).click()
                    i = i + 1
                    continue

            else:
                if change==0:   #一次还没有点击到人
                    if i==1:    #通讯录没有人的情况
                        now = datetime.datetime.now( )
                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                        cache.set( '%s_WXAddAddressList_time' % d.server.adb.device_serial( ), nowtime, None )
                        z.toast( '模块结束，保存的时间是%s' % nowtime )

                        return
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    i = 1
                    continue
                else:
                    if endcon==0:
                        z.toast('全部发送完成')

                        now = datetime.datetime.now( )
                        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
                        cache.set( '%s_WXAddAddressList_time' % d.server.adb.device_serial( ), nowtime,None )
                        z.toast('模块结束，保存的时间是%s'%nowtime)

                        if (args["time_delay"]):
                            z.sleep( int( args["time_delay"] ) )
                        return
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    i = 1
                    endcon = 0



def getPluginClass():
    return WXAddAddressListP

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

    args = {"repo_material_id": "39",'EndIndex':'3','set_time':'0','repo_cate_id':'171','gender':"不限","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)

































