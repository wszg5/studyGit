# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXAddAddressList:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)
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
                GenderFrom = args['gender']     #-------------------------------外界设定的性别
                if GenderFrom !='不限':
                    if Gender != GenderFrom:  #如果性别不符号的情况
                        danxiang = '性别不符'
                        para = {"phone": phonenumber, 'qq_nickname': name, 'sex': Gender, "city": area, "x_01": sign,"x_02":danxiang}
                        self.repo.PostInformation( args["repo_cate_id"], para )
                        z.toast( "%s入库完成" % phonenumber )
                        d(description='返回').click()
                        i = i+1
                        continue

                z.heartbeat()
                if d(text='添加到通讯录').exists:
                    d(text='添加到通讯录').click()
                    if d( textContains='正在添加' ).exists:
                        z.sleep( 1 )
                    time.sleep(1)
                    if d(text='发消息').exists:
                        danxiang = '单向'
                        para = {"phone": phonenumber, 'qq_nickname': name, 'sex': Gender, "city": area, "x_01": sign,"x_02":danxiang}
                        self.repo.PostInformation( args["repo_cate_id"], para )
                        z.toast( "%s入库完成" % phonenumber )
                        d(description='返回').click()
                        i = i+1
                        continue

                elif d(text='通过验证').exists:
                    d(text='通过验证').click()
                    d(description='返回').click()
                    danxiang = '未知'
                    para = {"phone": phonenumber, 'qq_nickname': name, 'sex': Gender, "city": area, "x_01": sign,"x_02": danxiang}
                    self.repo.PostInformation( args["repo_cate_id"], para )
                    z.toast( "%s入库完成" % phonenumber )
                    d( description='返回' ).click( )
                    i = i + 1
                    continue

                else:
                    danxiang = '未知'
                    para = {"phone": phonenumber, 'qq_nickname': name, 'sex': Gender, "city": area, "x_01": sign,"x_02": danxiang}
                    self.repo.PostInformation( args["repo_cate_id"], para )
                    z.toast( "%s入库完成" % phonenumber )
                    d(description='返回').click()
                    i = i+1
                    continue

                danxiang = '非单项'       #有添加到通讯录且非单项的情况
                para = {"phone": phonenumber, 'qq_nickname': name, 'sex': Gender, "city": area, "x_01": sign,"x_02": danxiang}
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

                    continue

            else:
                if change==0:   #一次还没有点击到人
                    if i==1:    #通讯录没有人的情况
                        return
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    i = 1
                    continue
                else:
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    endterm = d(className='android.widget.LinearLayout', index=i-1).child(className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).child(textContains='微信:')
                    time.sleep(0.5)
                    if endterm.exists:
                        endterm = endterm.info
                        name1 = endterm['text']      #判断是否已经到底
                        if name1 in set1:
                            if (args["time_delay"]):
                                z.sleep( int( args["time_delay"] ) )
                            return
                    i = 1
                    continue


def getPluginClass():
    return WXAddAddressList

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

    args = {"repo_material_id": "39",'EndIndex':'100','repo_cate_id':'171','gender':"女","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)

































