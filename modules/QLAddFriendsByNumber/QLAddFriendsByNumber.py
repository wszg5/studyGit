# coding:utf-8
import colorsys

from PIL import Image

from smsCode import smsCode
from uiautomator import Device
from Repo import *
import os, time, datetime, random
import util
from zservice import ZDevice


class QLAddFriendsByNumber:

    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum


    def action(self, d, z,args):
        z.toast( "准备执行QQ轻聊版搜索加好友模块" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：QQ轻聊版加好友(搜索查找)" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop com.tencent.qqlite" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell",
                          "am start -n com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity" ).communicate( )  # 拉起来
        z.sleep( 8 )
        z.heartbeat( )

        if d( text='消息' ).exists:  # 到了通讯录这步后看号有没有被冻结
            z.toast( "卡槽状态正常，继续执行" )
        else:
            z.toast( "卡槽状态异常，跳过此模块" )
            return

        repo_material_cate_id = args["repo_material_cate_id"]       # 得到验证语的仓库号
        Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
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
        d( resourceId='com.tencent.qqlite:id/0', description='更多' ).click( )
        z.heartbeat( )
        z.sleep( 2 )
        if d( text='添加', resourceId='com.tencent.qqlite:id/action_sheet_button' ).exists:
            d( text='添加', resourceId='com.tencent.qqlite:id/action_sheet_button' ).click( )
        else:
            z.heartbeat( )
            d( resourceId='com.tencent.qqlite:id/0', description='更多' ).click( )
            z.heartbeat( )
            d( text='添加', resourceId='com.tencent.qqlite:id/action_sheet_button' ).click( )
        z.sleep(3)
        z.heartbeat( )
        d(text='QQ号/手机号/邮箱/群', resourceId='com.tencent.qqlite:id/0').click()
        z.heartbeat( )
        d(text='QQ号/手机号/邮箱/群', resourceId='com.tencent.qqlite:id/et_search_keyword').set_text(QQnumber)  # 第一次添加的帐号 list[0]
        z.heartbeat( )
        d( text='找人:', resourceId='com.tencent.qqlite:id/0' ).click( )
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
                d( resourceId='com.tencent.qqlite:id/ib_clear_text', description='清空搜索输入' ).click( )
                obj = d( text='QQ号/手机号/邮箱/群', resourceId='com.tencent.qqlite:id/et_search_keyword' )
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)  # 下次要添加的号码
                obj = d(text='网络查找人', resourceId='com.tencent.qqlite:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)  # 下次要添加的号码
                d( text='找人:', resourceId='com.tencent.qqlite:id/0' ).click( )
                time.sleep(1)
                continue
            time.sleep(2)
            if d(className='android.view.View').child(index=1,resourceId='com.tencent.qqlite:id/0',className="android.widget.RelativeLayout").exists:      #在同一查条件有多个人
                z.heartbeat( )
                z.sleep( 2 )
                d( className='android.view.View' ).child( index=1, resourceId='com.tencent.qqlite:id/0',className="android.widget.RelativeLayout" ).click()
                z.sleep( 2 )
            z.sleep(1)
            obj = d( index=1, resourceId="com.tencent.qqlite:id/0", className="android.widget.RelativeLayout" ).child(
                index=2, resourceId="com.tencent.qqlite:id/0", className="android.widget.TextView" )
            if obj.exists:
                obj = obj.info
                gender2 = obj["text"][0:1]
            else:
                gender2 = "不限"

            z.heartbeat( )
            if gender1 != '不限':
                z.heartbeat( )
                if gender1 == gender2:  # gender1是外界设定的，gender2是读取到的
                    z.sleep( 1 )
                else:
                    z.sleep(1)
                    d( text='个人资料').click( )
                    z.sleep( 2 )
                    if d( resourceId='com.tencent.qqlite:id/ib_clear_text', description='清空搜索输入' ).exists:
                        d( resourceId='com.tencent.qqlite:id/ib_clear_text', description='清空搜索输入' ).click( )
                    else:
                        d( text='个人资料' ).click( )
                    obj = d( text='QQ号/手机号/邮箱/群', resourceId='com.tencent.qqlite:id/et_search_keyword' )
                    if obj.exists:
                        z.heartbeat( )
                        z.sleep( 2 )
                        obj.set_text( QQnumber )  # 要改为从库里取-------------------------------
                    obj = d( text='网络查找人', resourceId='com.tencent.qqlite:id/et_search_keyword' )
                    if obj.exists:
                        z.sleep( 2 )
                        obj.set_text(QQnumber )
                    if d( text='找人:', resourceId='com.tencent.qqlite:id/0' ).exists:
                        d( text='找人:', resourceId='com.tencent.qqlite:id/0' ).click( )
                    else:
                        d(resourceId="com.tencent.qqlite:id/0",description="取消").click()
                        if d( resourceId='com.tencent.qqlite:id/ib_clear_text', description='清空搜索输入' ).exists:
                            d( resourceId='com.tencent.qqlite:id/ib_clear_text', description='清空搜索输入' ).click( )
                        else:
                            d( text='个人资料' ).click( )

                        obj = d( text='QQ号/手机号/邮箱/群', resourceId='com.tencent.qqlite:id/et_search_keyword' )
                        if obj.exists:
                            z.heartbeat( )
                            z.sleep( 2 )
                            obj.set_text( QQnumber )  # 要改为从库里取-------------------------------
                        obj = d( text='网络查找人', resourceId='com.tencent.qqlite:id/et_search_keyword' )
                        if obj.exists:
                            z.sleep( 2 )
                            obj.set_text( QQnumber )
                        if d( text='找人:', resourceId='com.tencent.qqlite:id/0' ).exists:
                            d( text='找人:', resourceId='com.tencent.qqlite:id/0' ).click( )
                    continue
            z.heartbeat( )
            d( text='加好友', className="android.widget.TextView" ).click( )
            time.sleep(1)
            if d(text='加好友').exists:                        #拒绝被添加为好友的情况
                time.sleep(1)
                z.heartbeat( )
                d(text='个人资料').click()
                z.sleep( 2 )
                d(resourceId='com.tencent.qqlite:id/ib_clear_text', description='清空搜索输入').click()
                z.sleep( 2 )
                obj =d(text='QQ号/手机号/邮箱/群', resourceId='com.tencent.qqlite:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)  # 要改为从库里取------------------------------
                obj = d(text='网络查找人', resourceId='com.tencent.qqlite:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)
                time.sleep(1)
                d( text='找人:', resourceId='com.tencent.qqlite:id/0' ).click( )
                continue
            time.sleep(2)
            if d(text="风险提示").exists:   #风险提示
                z.sleep(1)
                z.heartbeat()
                d(text="取消").click()
                z.sleep(1)
                d( text='个人资料' ).click( )
                z.sleep( 2 )
                d( resourceId='com.tencent.qqlite:id/ib_clear_text', description='清空搜索输入' ).click( )
                obj =d(text='QQ号/手机号/邮箱/群', resourceId='com.tencent.qqlite:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text( QQnumber )  # 要改为从库里取-------------------------------
                obj = d( text='网络查找人', resourceId='com.tencent.qqlite:id/et_search_keyword' )
                if obj.exists:
                    z.sleep( 2 )
                    obj.set_text( QQnumber )
                d( text='找人:', resourceId='com.tencent.qqlite:id/0' ).click( )
                continue
            if d(text='必填').exists:                     #要回答问题的情况
                z.heartbeat( )
                z.sleep( 2 )
                d(text='身份验证').click()
                z.sleep(1)
                z.heartbeat( )
                d( text='个人资料' ).click( )
                z.sleep( 2 )
                d( resourceId='com.tencent.qqlite:id/ib_clear_text', description='清空搜索输入' ).click( )
                obj = d(text='QQ号/手机号/邮箱/群', resourceId='com.tencent.qqlite:id/et_search_keyword')
                if obj.exists:
                    z.sleep( 2 )
                    obj.set_text(QQnumber)  # 下次要添加的号码-
                obj = d(text='网络查找人',resourceId='com.tencent.qqlite:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)
                time.sleep(1)
                d( text='找人:', resourceId='com.tencent.qqlite:id/0' ).click( )
                continue
            time.sleep(1)
            z.heartbeat( )
            obj = d(text='发送')            #不需要验证可直接添加为好友的情况
            if obj.exists:
                z.sleep( 2 )
                obj.click()
                if d(text='添加失败，请勿频繁操作').exists:
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
                d( resourceId='com.tencent.qqlite:id/ib_clear_text', description='清空搜索输入' ).click( )
                obj =d(text='QQ号/手机号/邮箱/群', resourceId='com.tencent.qqlite:id/et_search_keyword')
                if obj.exists:
                    z.heartbeat( )
                    z.sleep( 2 )
                    obj.set_text(QQnumber)  # 要改为从库里取-------------------------------
                obj = d(text='网络查找人', resourceId='com.tencent.qqlite:id/et_search_keyword')
                if obj.exists:
                    z.sleep( 2 )
                    obj.set_text(QQnumber)
                d( text='找人:', resourceId='com.tencent.qqlite:id/0' ).click( )
                continue
            time.sleep(2)
            obj = d( index=3, className="android.widget.EditText", resourceId="com.tencent.qqlite:id/0" ).info       #将之前消息框的内容删除
            obj = obj['text']
            lenth = len(obj)
            t = 0
            while t < lenth:
                d.press.delete()
                t = t + 1
            time.sleep(2)
            z.input(material)
            z.sleep(1)
            d(text='下一步').click()
            z.sleep( 1 )
            d(text='发送').click()
            print( str(QQnumber) + "请求发送成功" )
            time.sleep(1)
            if d(text='添加失败，请勿频繁操作', resourceId='com.tencent.qqlite:id/name').exists:
                # z.sleep( 1 )
                # z.heartbeat( )
                # d( text="确定", className="android.widget.TextView" ).click( )
                # z.sleep( 1 )
                # z.heartbeat( )
                # d( text="返回", className="android.widget.TextView" ).click( )
                print("频繁操作,跳出模块")
                z.toast( "频繁操作,跳出模块" )
                return
            z.sleep( 2 )
            d( resourceId='com.tencent.qqlite:id/ib_clear_text', description='清空搜索输入' ).click( )
            z.sleep( 2 )
            count = count + 1
            if count == add_count:
                print ("模块已完成")
                z.toast("模块已完成")
                break
            if count<add_count:
                obj =d(text='QQ号/手机号/邮箱/群', resourceId='com.tencent.qqlite:id/et_search_keyword')
                if obj.exists:
                    obj.click()
                    z.input(QQnumber)
                    z.sleep( 2 )
                obj = d(text='网络查找人', resourceId='com.tencent.qqlite:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(QQnumber)
                    z.sleep( 1 )
                d( text='找人:', resourceId='com.tencent.qqlite:id/0' ).click( )
            else:
                z.sleep( 2 )
                z.heartbeat( )
                d( text="取消",className="android.widget.Button" ).click( )
                z.sleep( 2 )
                d( text="返回", className="android.widget.TextView" ).click( )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return QLAddFriendsByNumber

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
    args = {"repo_number_cate_id":"119","repo_material_cate_id":"39",'gender':"男","add_count":"5","time_delay":"3"}    #cate_id是仓库号，length是数量
    o.action(d, z,args)