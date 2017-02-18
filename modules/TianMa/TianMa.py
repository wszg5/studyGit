# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random
from zservice import ZDevice
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class WXReviseInfo:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        # d.server.adb.cmd("shell", "pm clear tianma.com.tianma").communicate()  # 清除缓存
        # d.server.adb.cmd("shell", "am force-stop tianma.com.tianma").wait()  # 强制停止
        # d.server.adb.cmd("shell", "am start -n tianma.com.tianma/tianma.com.tianma.view.StartActivity").communicate()  # 拉起来
        # time.sleep(7)
        d(text='请输入账号').child(className='android.widget.EditText').set_text('powerman')
        d(text='请输入密码').child(className='android.widget.EditText').set_text('13141314abc')



        # z.wx_action('openinfoui')
        # d(text='昵称').click()
        # obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
        # obj = obj['text']
        # lenth = len(obj)
        # m = 0
        # while m < lenth:
        #     d.press.delete()
        #     m = m + 1
        # cate_id = args['repo_name_id']     #得到昵称库的id
        # Material = self.repo.GetMaterial(cate_id, 0, 1)     #修改昵称
        # try:
        #     name = Material[0]['content']  # 从素材库取出的要发的材料
        # except Exception:
        #     d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
        # z.input(name)
        # d(text='保存').click()
        #
        # gender = args['gender']
        # d(text='性别').click()
        # d(text=gender).click()
        #
        # d(text='地区').click()
        # time.sleep(2)
        # d(className='android.widget.ListView').child(className='android.widget.LinearLayout',index=1).click()
        #
        # d(text='个性签名').click()
        # obj = d(className='android.widget.EditText').info  # 将之前消息框的内容删除
        # obj = obj['text']
        # lenth = len(obj)
        # m = 0
        # while m < lenth:
        #     d.press.delete()
        #     m = m + 1
        # cate_id = args['repo_persigned_id']
        # Material = self.repo.GetMaterial(cate_id, 0, 1)  # 修改个性签名
        # try:
        #     persigned = Material[0]['content']  # 从素材库取出的要发的材料
        #     wait = 0
        # except Exception:
        #     d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
        # z.input(persigned)
        # d(text='保存').click()


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return WXReviseInfo

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_name_id": "47",'repo_persigned_id':'48','gender':"男","time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)