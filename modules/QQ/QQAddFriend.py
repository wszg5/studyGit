#coding=utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *

class QQAddFriend:
    def __init__(self):
        self.repo = Repo()

    def action(self,d,z,args):
        z.heartbeat( )

        runLock = int( args['run_lock'] )
        cate_id = int( args["repo_number_id"] )
        saveCate = args['repo_save_exist_id']
        # totalList = self.repo.GetNUmberNormalTotal( saveCate )
        # normalTotal = int( totalList[0]['total'] )
        normalTotal = 123

        if normalTotal < runLock:
            z.toast( '库内未使用QQ号低于' + args['run_lock'] + '，开始检存' )
            d.press.home( )
            if d(text="QQ").exists:
                d(text="QQ").click( )
            else:

                z.toast('该页面没有ＱＱ')
                z.sleep(2)
                return
            z.sleep(5)
            while True:
                if d(text="消息") and d(text="联系人") and d(text="动态").exists:
                    d( text="消息" ).click( )
                    break
                else:
                    if d(text="取消").exists:
                        d(text="取消").click()
                    elif d(descriptionContains="返回动态 按钮").exists:
                        d(descriptionContains="返回动态 按钮").click()
                    elif d(text="动态")and d(resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").exists:
                        d( text="动态" ) and d( resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click()
                    elif d(text="联系人")and d(resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").exists:
                        d( text="联系人" ) and d( resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft" ).click()
                    else:
                        d( text='返回', className='android.widget.TextView').click( )

            d( descriptionContains="快捷入口" ).click( )
            z.sleep(1)
            if d(text="加好友/群").exists:
                d(text="加好友/群").click()
            else:
                d( descriptionContains="快捷入口",className="android.widget.ImageView").click( )
                z.sleep(1)
                d(text="加好友/群").click()
            d(text='QQ号/手机号/群/公众号').click( )
            z.heartbeat( )

            lock_count = 0
            while True:
                lock_count = lock_count + 1
                if lock_count > int( args['check_count'] ):
                    z.toast( '成功检存' + args['check_count'] + '次，结束' )
                    break
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
                                      "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码%s号仓库为空，等待中\"" % cate_id ).communicate( )
                    z.sleep( 30 )
                QQnumber = numbers[0]['number']
                z.input( QQnumber )
                d( text='找人:').click( )
                z.heartbeat( )
                while d( textContains='正在查找' ).exists:
                    z.sleep( 2 )
                z.heartbeat( )
                if d( textContains='操作过于频繁' ).exists:
                    self.repo.uploadPhoneNumber( QQnumber, saveCate )
                    d( descriptionContains='清空' ).click( )

                    continue

                z.sleep( 1 )
                if d(text="没有找到相关结果").exists:
                    d( descriptionContains='清空', index=1 ).click( )
                    z.sleep( 1 )
                if d(text="加好友").exists:
                    d(text="加好友").click()

                if d( textContains='用户不存在' ).exists:
                    saveCate_not = args['repo_save_not_exist_id']
                    self.repo.uploadPhoneNumber( QQnumber, saveCate_not )
                    d( descriptionContains='清空', index=1 ).click( )
                    z.sleep( 1 )
                    continue
                if d( textContains='状态异常' ).exists:
                    self.repo.uploadPhoneNumber( QQnumber, saveCate )
                    d( descriptionContains='清空', index=1 ).click( )
                    continue
                z.heartbeat( )

                self.repo.uploadPhoneNumber( QQnumber, saveCate )

                d( descriptionContains='返回' ).click( )
                d( descriptionContains='清空' ).click( )
                z.sleep( 1 )
                continue

        else:
            z.toast( '库内未使用QQ号码大于' + args['run_lock'] + '，模块无法运行' )


    # if (args["time_delay"]):
    #     z.sleep( int( args["time_delay"] ) )


def getPluginClass():
    return QQAddFriend


if __name__ == "__main__":
    import sys

    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "36be646" )
    z = ZDevice( "36be646" )
    z.server.install( )
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).wait( )
    args = {"repo_number_id": "190", 'repo_save_exist_id': '189', "run_lock": "500", "check_count": "10",
            "repo_save_not_exist_id": "183"}  # cate_id是仓库号，length是数量
    o.action( d, z, args )













#