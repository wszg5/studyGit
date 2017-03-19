# coding:utf-8
from PIL.ImageShow import show
from requests import delete
from uiautomator import Device
from Repo import *
import  time, datetime, random
import util
from PIL import Image
from zservice import ZDevice

class MobilqqAddFriends:
    def __init__(self):
        self.repo = Repo()

    def action(self, d,z, args):
        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        cate_id = args["repo_material_cate_id"]
        Material = self.repo.GetMaterial(cate_id, 0, 1)
        if len(Material) == 0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
            time.sleep(10)
            return
        message = Material[0]['content']  # 取出验证消息的内容

        add_count = int(args['add_count'])  # 要添加多少人

        cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        numbers = self.repo.GetNumber(cate_id, 120, add_count)  # 取出add_count条两小时内没有用过的号码
        if len(numbers)==0:
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码库%s号仓库为空，等待中\""%cate_id).communicate()
            time.sleep(10)
            return
        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)
        z.heartbeat()
        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").communicate()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
        time.sleep(1)
        d(resourceId='com.tencent.mobileqq:id/name',description='快捷入口').click()
        time.sleep(1)
        z.heartbeat()
        if d(textContains='加好友').exists:
            d(textContains='加好友').click()
        else:
            d(resourceId='com.tencent.mobileqq:id/name', description='快捷入口').click()
            d(textContains='加好友').click()
        time.sleep(3)
        d(className='android.widget.EditText',index=0).click()           #刚进来时点击 QQ号/手机号/群/公众号
        time.sleep(1)
        # d(className='android.widget.EditText',index=0).click()   #QQ号/手机号/群/公众号
        # d(className='android.widget.EditText').set_text(list[0]['number'])  # 第一次添加的帐号 list[0]
        z.input(list[0]['number'])
        time.sleep(0.5)
        d(text='找人:', resourceId='com.tencent.mobileqq:id/name').click()
        time.sleep(3)

        z.heartbeat()
        for i in range(1,add_count,+1):                   #给多少人发消息
            z.heartbeat()
            numbers = list[i]['number']
            print(numbers)
            time.sleep(1)
            if d(text='没有找到相关结果',className='android.widget.TextView').exists:                            #没有这个人的情况
                time.sleep(0.5)
                d(resourceId='com.tencent.mobileqq:id/ib_clear_text',description='清空').click()
                obj = d(className='android.widget.EditText',index=0)   #QQ号/手机号/群/公众号
                if obj.exists:
                    obj.set_text(numbers)  # 下次要添加的号码
                obj = d(text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)  # 下次要添加的号码
                d(textContains='找人').click()
                while d(text='正在搜索…',index=1).exists:                  #网速不行的情况，让它不停等待
                    time.sleep(1)
                continue
            time.sleep(1)
            z.heartbeat()
            d.swipe(width / 2, height * 4 / 6, width / 2, height / 6);
            d(text='加好友').click()
            time.sleep(3)

            if d(text='加好友').exists:                        #拒绝被添加为好友的情况
                time.sleep(1)
                d(text='返回',resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft').click()
                d(resourceId='com.tencent.mobileqq:id/ib_clear_text', description='清空').click()
                obj = d(className='android.widget.EditText',index=0)
                if obj.exists:
                    obj.set_text(numbers)  # 要改为从库里取------------------------------
                obj = d(text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)
                time.sleep(1)
                d(textContains='找人').click()
                while d(text='正在搜索…', index=1).exists:
                    time.sleep(1)
                continue
            time.sleep(0.5)

            z.heartbeat()
            if d(text='必填',resourceId='com.tencent.mobileqq:id/name').exists:                     #要回答问题的情况
                d(text='返回',resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft').click()
                time.sleep(1)
                d(text='返回',resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft').click()
                d(resourceId='com.tencent.mobileqq:id/ib_clear_text', description='清空').click()
                obj = d(className='android.widget.EditText',index=0)
                if obj.exists:
                    obj.set_text(numbers)  # 下次要添加的号码-
                obj = d(text='网络查找人',resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)
                time.sleep(1)
                d(textContains='找人').click()
                while d(text='正在搜索…', index=1).exists:
                    time.sleep(1)
                continue

            z.heartbeat()
            if d(textContains='问题').exists:            #要回答问题的情况
                d(text='取消').click()
                time.sleep(0.5)
                d(text='返回').click()
                d(resourceId='com.tencent.mobileqq:id/ib_clear_text', description='清空').click()
                obj = d(className='android.widget.EditText', index=0)
                if obj.exists:
                    obj.set_text(numbers)  # 下次要添加的号码-
                obj = d(text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)
                time.sleep(1)
                d(textContains='找人').click()
                while d(text='正在搜索…', index=1).exists:
                    time.sleep(1)
                continue

            z.heartbeat()
            time.sleep(0.5)
            obj = d(className='android.widget.EditText', resourceId='com.tencent.mobileqq:id/name').info  # 将之前消息框的内容删除
            obj = obj['text']
            lenth = len(obj)
            t = 0
            while t < lenth:
                d.press.delete()
                t = t + 1
            if d(className='android.widget.EditText',index=4).exists:
                z.input(message)
            obj = d(text='发送')            #不需要验证可直接添加为好友的情况
            if obj.exists:
                z.heartbeat()
                obj.click()
                if d(text='添加失败，请勿频繁操作',resourceId='com.tencent.mobileqq:id/name').exists:
                    return
                d(text='返回').click()
                d(description='清空').click()
                obj = d(className='android.widget.EditText',index=0)
                if obj.exists:
                    obj.set_text(numbers)  # 要改为从库里取-------------------------------
                obj = d(text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)
                d(textContains='找人').click()
                while d(text='正在搜索…', index=1).exists:
                    time.sleep(1)
                continue

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))






def runwatch(d, data):
    times = 120
    while True:
        if data == 1:
            return True
        # d.watchers.reset()
        d.watchers.run()
        times -= 1
        if times == 0:
            break
        else:
            time.sleep(0.5)

def getPluginClass():
    return MobilqqAddFriends

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    # print(d.dump(compressed=False))
    args = {"repo_number_cate_id":"119","repo_material_cate_id":"39","add_count":"15","time_delay":"3"};    #cate_id是仓库号，length是数量
    util.doInThread(runwatch, d, 0, t_setDaemon=True)
    o.action(d,z, args)