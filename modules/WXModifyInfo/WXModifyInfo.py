# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXModifyInfo:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(15)
        if d(text='我').exists:
           for i in range(1,3):
               d(text='我').click()
           z.sleep( 3 )
           d.click( 270, 200 )

        z.sleep(3)
        d(descriptionContains='查看头像', className='android.view.View', resourceId='com.tencent.mm:id/hq').click()
        z.sleep(3)
        d(descriptionContains='更多',className='android.widget.TextView').click()
        z.sleep(3)
        d(text='从手机相册选择').click()

        if d(text='图片').exists:
            photoObj = d(className='android.widget.GridView').child(className='android.widget.RelativeLayout',resourceId='com.tencent.mm:id/ep',index=1)
            if photoObj.exists:
                photoObj.click()
            else:
                z.toast('本地相册没有图片')

        z.sleep(2)
        d(text='使用').click()

        z.sleep(8)
        if d(text='头像').exists:
            d.click(35,70)

        z.sleep(3)
        if d(text='昵称').exists:
            d(text='昵称').click()

        z.sleep(2)
        if d(text='更改名字').exists:
            textName = d( resourceId='com.tencent.mm:id/cib', className='android.widget.EditText' ).info['text']
            lenth = len( textName )
            mn = 0
            while mn < lenth:
                d.press.delete( )
                mn = mn + 1
            repo_material_name_id = args['repo_material_name_id']
            Material = self.repo.GetMaterial( repo_material_name_id, 0, 1 )  # 修改昵称
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_material_name_id ).communicate( )
                z.sleep( 10 )
            name = Material[0]['content']  # 从素材库取出的要发的材料
            z.input( name )

        d(text='保存').click()

        z.sleep(5)
        if d(text='性别').exists:
            d(text='性别').click()
            z.sleep(1)
            if d(text='性别').exists:
                gender = args['gender']
                d(text=gender).click()

        z.sleep(2)
        if d(text='地区').exists:
            d(text='地区').click()
            z.sleep(3)
        if d(text='选择地区').exists:
            d(resourceId='com.tencent.mm:id/bvs',className='android.widget.ImageView').click()
            z.sleep(1.5)

        if d(text='个性签名').exists:
            d(text='个性签名').click()
            z.sleep(1.5)

            textName = d( resourceId='com.tencent.mm:id/ib', className='android.widget.EditText' ).info['text']
            lenth = len( textName )
            mn = 0
            while mn < lenth:
                d.press.delete( )
                mn = mn + 1
            repo_material_sign_id = args['repo_material_sign_id']
            Material = self.repo.GetMaterial( repo_material_sign_id, 0, 1 )  # 修改昵称
            if len( Material ) == 0:
                d.server.adb.cmd( "shell",
                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_material_sign_id ).communicate( )
                z.sleep( 10 )
            sign = Material[0]['content']  # 从素材库取出的要发的材料
            z.input( sign )
            d(text='保存').click()
            z.sleep(5)


        if (args["time_delay"]):
            z.toast('个人信息设置完毕')
            z.sleep( int( args["time_delay"] ) )



def getPluginClass():
    return WXModifyInfo

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT53ASK00088")
    z = ZDevice("HT53ASK00088")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_material_name_id": "139", "repo_material_sign_id": "40", "gender":"女", "time_delay": "3"}   #cate_id是仓库号，length是数量
    o.action(d,z, args)

