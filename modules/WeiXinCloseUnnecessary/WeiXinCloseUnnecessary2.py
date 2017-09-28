# coding:utf-8
from uiautomator import Device
from Repo import *
from smsCode import smsCode
import time, string, datetime, random
from zservice import ZDevice
import util

class WeiXinCloseUnnecessary2:
    def __init__(self):
        self.repo = Repo( )


    def action(self, d, z, args):
        #所有功能
        notUnnecessary = ['摇一摇','附近的人','群发助手','QQ离线助手', 'QQ邮箱提醒','语音记事本','腾讯新闻','视频聊天','语音输入','漂流瓶','通讯录同步助手','微信运动']
        while not (d(text='微信').exists and d(text='通讯录').exists and d(text='发现').exists and d(text='我').exists):
            #不再主界面，一直点击返回按钮的位置
            d.click(30, 72)
        # ‘微信’，‘通讯录’，‘发现’，‘我’按钮同时存在
        #点击‘我’按钮
        d( text='我' ).click()
        z.sleep( 1 )
        #判断‘设置’按钮是否存在
        if d( text='设置' ).exists:
            #点击‘设置’按钮
            d( text='设置' ).click()
            z.sleep(1)
            # 判断‘通用’按钮是否存在
        if d(text='通用').exists:
            # 点击‘通用’按钮
            d( text='通用' ).click()
            z.sleep( 1 )
            # 判断‘功能’按钮是否存在
        if d( text='功能' ).exists:
            # 点击‘功能’按钮
            d( text='功能' ).click()
            z.sleep( 1 )
            #循环对需要关闭的功能进行关闭
        for i in range(len(notUnnecessary)):
            #判断功能是否存在
            if d(text=notUnnecessary[i]).exists:
                #存在就点击它
                d(text=notUnnecessary[i] ).click()
                z.sleep( 1 )
                #如果'摇一摇','附近的人','群发助手'存在
                if d(text='摇一摇').exists or d(text='附近的人').exists or d(text='群发助手').exists:
                    if d(text='启用该功能').exists:
                        d( text='启用该功能' ).click()
                        z.sleep(3)
                    if d(text='停用').exists:
                        d.click( 30, 72 )
                else:
                    if d(text='停用').exists:
                        # 点击'停用'
                        d( text='停用' ).click()
                        z.sleep(1)
                        if d(textContains='停用该功能').exists:
                            #点击'清空并停用'
                            d(text='清空').click()
                            z.sleep(3)
                        if d( text='启用该功能' ).exists:
                            #返回到功能界面，继续进行下一个功能的关闭
                            d.click( 30, 72 )
                            z.sleep( 1 )
                    elif d(text='启用该功能').exists:
                            d.click( 30, 72 )
                            z.sleep( 1 )
            else:continue




def getPluginClass():
    return WeiXinCloseUnnecessary2

if __name__ == "__main__":
    import sys
    reload( sys )
    sys.setdefaultencoding( 'utf8' )
    clazz = getPluginClass( )
    o = clazz( )
    d = Device( "HT54VSK00608" )  # INNZL7YDLFPBNFN7
    z = ZDevice( "HT54VSK00608" )
    # z.server.install()
    d.server.adb.cmd( "shell", "ime set com.zunyun.qk/.ZImeService" ).communicate( )
    'dingdingdingdingdindigdingdingdingdingdingdingdingdingdingdingdingdignin'
    repo = Repo( )
    # repo.RegisterAccount('', 'gemb1225', '13045537833', '109')
    args = {"repo_information_id": "189", "repo_material_id": "167"}  # cate_id是仓库号，发中文问题
    saveCate = args['repo_information_id']
    o.action( d, z, args )