# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class MobilqqPraiseII:
    def __init__(self):
        self.repo = Repo()


    def action(self, d,z,args):
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        z.sleep(8)
        z.heartbeat()
        d(description='快捷入口').click()
        d(textContains='加好友').click()
        d(textContains='附近的人').click()
        while not d(textContains='等级').exists:
            z.sleep(2)
        getGender = args['gender']
        if getGender !='不限':
            d(resourceId='com.tencent.mobileqq:id/ivTitleBtnRightImage').click()
            d(text='筛选附近的人').click()
            d(text=getGender).click()
            d(text='完成').click()
            while not d(textContains='等级').exists:
                z.sleep(2)
        z.heartbeat()
        prisenum = int(args['prisenum'])
        concernnum = int(args['concernnum'])
        textnum = int(args['textnum'])
        count = max(prisenum, concernnum, textnum)
        t = 0
        i = 3
        while t<count:
            forClick = d(className='android.widget.AbsListView').child(className='android.widget.LinearLayout',index=i).child(className='android.widget.RelativeLayout')
            if forClick.child(className='android.widget.LinearLayout',index=2).exists:
                z.heartbeat()
                if forClick.child(text='直播中').exists:
                    i = i+1
                    continue

                forClick.click()

                while not d(textContains='关注').exists:
                    z.sleep(2)
                    if d(text='知道了').exists:
                        d(text='知道了').click()
                if t<prisenum:
                    praise = 0
                    z.heartbeat()
                    while praise<10:
                        if d(descriptionContains='赞').exists:
                            z.heartbeat()
                            d(descriptionContains='赞').click()
                            if d(text='取消').exists:      #当点赞够次超数的时候
                                d(text='取消').click()
                                praise = 10       #表明点赞已够次数，将点赞结束掉
                            praise = praise+1
                        else:
                            praise = 10  # 无法赞的情况
                            continue
                z.sleep(2)
                if t<concernnum:
                    if d(text='关注').exists:
                        d(text='关注').click()

                if t<textnum:
                    d(text='发消息').click()
                    z.sleep(1)
                    if d(text='发消息').exists:
                        z.toast('无法发消息')
                        d(text='返回').click()
                        i = i + 1
                        t = t + 1
                        continue

                    d(className='android.widget.EditText').click()
                    cate_id = args["repo_material_id"]
                    Material = self.repo.GetMaterial(cate_id, 0, 1)
                    if len(Material) == 0:
                        d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                        z.sleep(10)
                        return
                    message = Material[0]['content']
                    z.input(message)
                    d(text='发送').click()


                d(text='返回').click()
                i = i+1
                t = t+1

            elif d(className='android.widget.AbsListView').child(className='android.widget.RelativeLayout',index=i).child(text='广告').exists:  #被点击条件不存在的情况
                z.heartbeat()
                i =i+1
                continue
            else:
                str = d.info  # 获取屏幕大小等信息
                width = str["displayWidth"]
                clickCondition = d(className='android.widget.AbsListView')
                obj = clickCondition.info
                obj = obj['visibleBounds']
                top = int(obj['top'])
                bottom = int(obj['bottom'])
                y = bottom - top
                d.swipe(width / 2, y, width / 2, 0)
                z.sleep(3)
                i = 1


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return MobilqqPraiseII

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49RSK01046")
    z = ZDevice("HT49RSK01046")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {"prisenum":"20","concernnum":"20","textnum":"20","repo_material_id":"39",'gender':"男","time_delay":"3"};    #cate_id是仓库号，length是数量

    o.action(d,z, args)
