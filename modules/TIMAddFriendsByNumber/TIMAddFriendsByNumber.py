# coding:utf-8
import colorsys

from PIL import Image

from smsCode import smsCode
from uiautomator import Device
from Repo import *
import os, time, datetime, random
import util
from zservice import ZDevice


class TIMAddFriendsByNumber:

    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def Gender(self, d, z):
        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "tmp" ) )
        if not os.path.isdir( base_dir ):
            os.mkdir( base_dir )
        sourcePng = os.path.join( base_dir, "%s_s.png" % (self.GetUnique( )) )
        obj = d( resourceId='com.tencent.tim:id/name', className='android.widget.ImageView' )
        if obj.exists:
            z.heartbeat( )
            obj = obj.info
            obj = obj['bounds']  # 验证码处的信息
            left = obj["left"]  # 验证码的位置信息
            top = obj['top']
            right = obj['right']
            bottom = obj['bottom']

            d.screenshot( sourcePng )  # 截取整个输入验证码时的屏幕

            img = Image.open( sourcePng )
            box = (left, top, right, bottom)  # left top right bottom
            region = img.crop( box )  # 截取验证码的图片
            # show(region)    #展示资料卡上的信息
            image = region.convert( 'RGBA' )
            # 生成缩略图，减少计算量，减小cpu压力
            image.thumbnail( (200, 200) )
            max_score = None
            dominant_color = None
            for count, (r, g, b, a) in image.getcolors( image.size[0] * image.size[1] ):
                # 跳过纯黑色
                if a == 0:
                    continue
                saturation = colorsys.rgb_to_hsv( r / 255.0, g / 255.0, b / 255.0 )[1]
                y = min( abs( r * 2104 + g * 4130 + b * 802 + 4096 + 131072 ) >> 13, 235 )
                y = (y - 16.0) / (235 - 16)
                # 忽略高亮色
                if y > 0.9:
                    continue
                z.heartbeat( )
                score = (saturation + 0.1) * count
                if score > max_score:
                    max_score = score
                    dominant_color = (r, g, b)
            # print("---------------------------------------------------------------------------")
            # print(dominant_color)
            z.heartbeat( )
            if None == dominant_color:
                return '不限'
            red = dominant_color[0]
            blue = dominant_color[2]

            if red > blue:
                # print('女')
                return '女'
            else:
                # print('男')
                return '男'
        else:  # 没有基本资料的情况
            return '不限'



    def action(self, d, z,args):
        z.toast( "准备执行TIM搜索加好友模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：TIM加好友(搜索查找)" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.tim" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text='消息' ).exists:  # 到了通讯录这步后看号有没有被冻结
            z.toast( "卡槽TIM状态正常，继续执行" )
        else:
            z.toast( "卡槽TIM状态异常，跳过此模块" )
            return

        repo_material_cate_id = args["repo_material_cate_id"]       # 得到验证语的仓库号
        Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
        switch_card = args["switch_card"]
        gender1 = args['gender']
        wait = 1  # 判断素材仓库里是否由素材
        while wait == 1:
            try:
                material = Material[0]['content']  # 取出验证消息的内容
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到验证消息\"")
        add_count = int(args['add_count'])  # 要添加多少人
        repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            numbers = self.repo.GetNumber(repo_number_cate_id, 120, add_count)  # 取出add_count条两小时内没有用过的号码
            if "Error" in numbers:  #
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"")
                continue
            wait = 0
        list = numbers # 将取出的号码保存到一个新的集合
        # num = list[0]['number']
        QQnumber = numbers[0]['number']
        z.sleep(8)
        z.heartbeat( )
        d(resourceId='com.tencent.tim:id/name',description='快捷入口').click()
        z.heartbeat( )
        z.sleep( 2 )
        if d(text='加好友',resourceId='com.tencent.tim:id/name').exists:
            d(text='加好友',resourceId='com.tencent.tim:id/name').click()
            z.heartbeat( )
        else:
            z.heartbeat( )
            d(resourceId='com.tencent.tim:id/name', description='快捷入口').click()
            z.heartbeat( )
            d(text='加好友',resourceId='com.tencent.tim:id/name').click()
        z.sleep(3)
        z.heartbeat( )
        d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/name').click()
        d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword').click()
        z.heartbeat( )
        d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword').set_text(QQnumber)  # 第一次添加的帐号 list[0]
        z.heartbeat( )
        d( text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search' ).click( )
        z.sleep(2)
        count = 0
        while count<add_count:
            numbers = list[i]
            repo_material_cate_id = args["repo_material_cate_id"]  # 得到验证语的仓库号
            Material = self.repo.GetMaterial( repo_material_cate_id, 0, 1 )
            material = Material[0]['content']                         # 得到验证语
            numbers = self.repo.GetNumber( repo_number_cate_id, 120, add_count )    # 取出两小时内没有用过的号码
            list = numbers
            QQnumber = numbers[0]['number']
            z.heartbeat( )
            time.sleep(1)
            if d(text='没有找到相关结果',className='android.widget.TextView').exists:                            #没有这个人的情况
                z.heartbeat( )
                d(resourceId='com.tencent.tim:id/ib_clear_text',description='清空').click()
                obj = d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)  # 下次要添加的号码
                obj = d(text='网络查找人', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)  # 下次要添加的号码
                d(text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search').click()
                time.sleep(1)
                continue
            time.sleep(2)
            if d(text="申请加群").exists:
                d(resourceId="com.tencent.tim:id/ivTitleBtnLeft",description="返回按钮").click()
                d( resourceId='com.tencent.tim:id/ib_clear_text', description='清空' ).click( )
                obj = d( text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword' )
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text( QQnumber )  # 下次要添加的号码
                obj = d( text='网络查找人', resourceId='com.tencent.tim:id/et_search_keyword' )
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text( QQnumber )  # 下次要添加的号码
                d( text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search' ).click( )
                time.sleep( 1 )
                continue
            z.sleep(2)
            if d(className='android.widget.AbsListView').child(index=1,resourceId='com.tencent.tim:id/name').exists:      #在同一查条件有多个人
                z.heartbeat( )
                z.sleep( 2 )
                d(className='android.widget.AbsListView').child(index=1, resourceId='com.tencent.tim:id/name').click()
                z.sleep( 2 )
            z.sleep(1)
            z.heartbeat( )
            if gender1 != '不限':
                gender2 = self.Gender( d, z )
                z.heartbeat( )
                if gender1 == gender2:  # gender1是外界设定的，gender2是读取到的
                    z.sleep( 1 )
                else:
                    d( text='返回', resourceId='com.tencent.tim:id/ivTitleBtnLeft' ).click( )
                    z.sleep( 2 )
                    d( resourceId='com.tencent.tim:id/ib_clear_text', description='清空' ).click( )
                    obj = d( text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword' )
                    if obj.exists:
                        z.heartbeat( )
                        z.sleep( 2 )
                        obj.set_text( QQnumber )  # 要改为从库里取-------------------------------
                    obj = d( text='网络查找人', resourceId='com.tencent.tim:id/et_search_keyword' )
                    if obj.exists:
                        z.sleep( 2 )
                        obj.set_text(QQnumber )
                    d( text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search' ).click( )
                    continue
            z.heartbeat( )
            d(text='加好友',resourceId='com.tencent.tim:id/name').click()
            time.sleep(1)
            if d(text='加好友',resourceId='com.tencent.tim:id/name').exists:                        #拒绝被添加为好友的情况
                time.sleep(1)
                z.heartbeat( )
                d(text='返回',resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
                z.sleep( 2 )
                d(resourceId='com.tencent.tim:id/ib_clear_text', description='清空').click()
                z.sleep( 2 )
                obj = d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)  # 要改为从库里取------------------------------
                obj = d(text='网络查找人', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)
                time.sleep(1)
                d(text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search').click()
                continue
            time.sleep(2)
            if d(text="风险提示").exists:   #风险提示
                z.sleep(1)
                z.heartbeat()
                d(text="取消").click()
                z.sleep(1)
                d( text='返回', resourceId='com.tencent.tim:id/ivTitleBtnLeft' ).click( )
                z.sleep( 2 )
                d( resourceId='com.tencent.tim:id/ib_clear_text', description='清空' ).click( )
                obj = d( text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword' )
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text( QQnumber )  # 要改为从库里取-------------------------------
                obj = d( text='网络查找人', resourceId='com.tencent.tim:id/et_search_keyword' )
                if obj.exists:
                    z.sleep( 2 )
                    obj.set_text( QQnumber )
                d( text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search' ).click( )
                continue
            if d(text='必填',resourceId='com.tencent.tim:id/name').exists:                     #要回答问题的情况
                z.heartbeat( )
                z.sleep( 2 )
                d(text='返回',resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
                time.sleep(1)
                z.heartbeat( )
                d(text='返回',resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
                z.sleep( 2 )
                d(resourceId='com.tencent.tim:id/ib_clear_text', description='清空').click()
                obj = d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    z.sleep( 2 )
                    obj.set_text(QQnumber)  # 下次要添加的号码-
                obj = d(text='网络查找人',resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)
                time.sleep(1)
                d(text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search').click()
                continue
            time.sleep(1)
            z.heartbeat( )
            obj = d(text='发送',resourceId='com.tencent.tim:id/ivTitleBtnRightText')            #不需要验证可直接添加为好友的情况
            if obj.exists:
                z.sleep( 2 )
                obj.click()
                if d(text='添加失败，请勿频繁操作',resourceId='com.tencent.tim:id/name').exists:
                    # z.sleep( 1 )
                    # z.heartbeat( )
                    # d( text="确定", className="android.widget.TextView" ).click( )
                    # z.sleep( 1 )
                    # z.heartbeat( )
                    # d( text="返回", className="android.widget.TextView" ).click( )
                    z.toast( "频繁操作,跳出模块" )
                    return
                else:
                    print( str( QQnumber ) + "请求发送成功" )
                time.sleep(1)
                d(text='返回', resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
                z.sleep( 2 )
                d(resourceId='com.tencent.tim:id/ib_clear_text', description='清空').click()
                obj = d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)  # 要改为从库里取-------------------------------
                obj = d(text='网络查找人', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    z.sleep( 2 )
                    obj.set_text(QQnumber)
                d(text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search').click()
                continue
            time.sleep(2)
            obj = d(className='android.widget.EditText', resourceId='com.tencent.tim:id/name').info           #将之前消息框的内容删除
            obj = obj['text']
            lenth = len(obj)
            t = 0
            while t < lenth:
                d.press.delete()
                t = t + 1
            time.sleep(2)
            d(className='android.widget.EditText',resourceId='com.tencent.tim:id/name').click()   #发送验证消息  material
            z.input(material)
            if "是" in switch_card:
                if d( index=2, className="android.widget.CompoundButton", resourceId="com.tencent.tim:id/name" ).exists:
                    d( index=2, className="android.widget.CompoundButton", resourceId="com.tencent.tim:id/name" ).click( )
            d(text='下一步',resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
            z.sleep( 1 )
            d(text='发送',resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
            print( str(QQnumber) + "请求发送成功" )
            time.sleep(1)
            if d(text='添加失败，请勿频繁操作', resourceId='com.tencent.tim:id/name').exists:
                # z.sleep( 1 )
                # z.heartbeat( )
                # d( text="确定", className="android.widget.TextView" ).click( )
                # z.sleep( 1 )
                # z.heartbeat( )
                # d( text="返回", className="android.widget.TextView" ).click( )
                z.toast( "频繁操作,跳出模块" )
                return
            z.sleep( 2 )
            d(text='返回',resourceId='com.tencent.tim:id/ivTitleBtnLeft').click()
            z.sleep(2)
            d(resourceId='com.tencent.tim:id/ib_clear_text',description='清空').click()
            z.sleep( 2 )
            if count<add_count:
                obj = d(text='QQ号/手机号/邮箱/群/公众号', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    obj.click()
                    z.input(QQnumber)
                    z.sleep( 2 )
                obj = d(text='网络查找人', resourceId='com.tencent.tim:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(QQnumber)
                    z.sleep( 1 )
                d(text='搜索', resourceId='com.tencent.tim:id/btn_cancel_search').click()
            else:
                z.sleep( 2 )
                z.heartbeat( )
                d( text="取消",className="android.widget.Button" ).click( )
                z.sleep( 2 )
                d( text="返回", className="android.widget.TextView" ).click( )
            count = count + 1
            if count == add_count:
                print ("模块已完成")
                z.toast("模块已完成")
                break
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMAddFriendsByNumber

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # print(d.dump(compressed=False))
    args = {"repo_number_cate_id":"119","repo_material_cate_id":"39",'gender':"男","add_count":"5","time_delay":"3","switch_card":"N"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)