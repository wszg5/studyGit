# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXSaveId:

    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        d.server.adb.cmd("shell", "am force-stop com.ss.android.article.news").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.ss.android.article.news/com.ss.android.article.news.activity.SplashActivity").communicate()  # 将微信拉起来
        z.sleep(7)
        d(text='问答').click()
        condition = args['condition']
        d(text=condition).click()
        endIndex = int(args['EndIndex'])
        i = 1
        t = 0
        z.heartbeat()
        while True:
            if t<endIndex:
                clickCondition = d(className='android.widget.ListView').child(className='android.widget.RelativeLayout',index=i)
                if clickCondition.exists:
                    z.heartbeat()
                    if clickCondition.child(textContains='点击刷新').exists:
                        i = i+1
                        continue
                    clickCondition.click()
                    z.sleep(3)

                    cate_id = args["repo_material_id"]
                    Material = self.repo.GetMaterial(cate_id, 0, 1)
                    if len(Material) == 0:
                        d.server.adb.cmd("shell",
                                         "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                        z.sleep(10)
                        return
                    message = Material[0]['content']  # 取出验证消息的内容
                    z.heartbeat()
                    # d(text='发表').click()
                    if d(text='我来说两句').exists:
                        d(text='我来说两句').click()
                        z.input(message)
                        d(text='发表').click()
                        d.press.back()
                        i = i+1
                        t = t+1
                        continue

                    z.heartbeat()
                    d(textContains='写评论').click()
                    z.input(message)
                    d.swipe(452, 825, 519, 829)     #发表按钮无法定位
                    z.sleep(1)
                    d.press.back()
                    if d(textContains='写评论').exists:    #遇到图片类型的
                        d.press.back()
                    i = i+1
                    print(t)
                    t = t+1
                    z.heartbeat()

                else:
                    str = d.info  # 获取屏幕大小等信息
                    width = str["displayWidth"]
                    clickCondition = d(className='android.widget.ListView')
                    obj = clickCondition.info
                    obj = obj['visibleBounds']
                    top = int(obj['top'])
                    bottom = int(obj['bottom'])
                    y = bottom - top
                    d.swipe(width / 2, y, width / 2, 0)
                    i = 1
            else:
                d(text=condition).click()
                z.sleep(6)
                t = 0
                i = 1



        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXSaveId

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"repo_material_id": "48", 'condition': "热点", 'EndIndex': '7', "time_delay": "3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)
