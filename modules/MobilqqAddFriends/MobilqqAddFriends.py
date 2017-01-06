# coding:utf-8
from PIL.ImageShow import show
from requests import delete
from uiautomator import Device
from Repo import *
import os, time, datetime, random
import util
from PIL import Image
from zservice import ZDevice


class TIMAddFriends:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum




    def action(self, d,z, args):
        str = d.info  # 获取屏幕大小等信息
        print(str)
        height = str["displayHeight"]
        width = str["displayWidth"]

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        genderPng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))



        repo_material_cate_id = args["repo_material_cate_id"]
        Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
        wait = 1  # 判断素材仓库里是否由素材
        while wait == 1:
            try:
                material = Material[0]['content']  # 取出验证消息的内容
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到验证消息\"")

        add_count = int(args['add_count'])  # 要添加多少人

        repo_number_cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
        wait = 1
        while wait == 1:
            numbers = self.repo.GetNumber(repo_number_cate_id, 120, add_count)  # 取出add_count条两小时内没有用过的号码
            if "Error" in numbers:  #
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"仓库为空，没有取到号码\"")
                continue
            wait = 0

        list = numbers  # 将取出的号码保存到一个新的集合
        print(list)

        d.server.adb.cmd("shell", "am force-stop com.tencent.mobileqq").wait()  # 强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
        time.sleep(1)
        d(resourceId='com.tencent.mobileqq:id/name',description='快捷入口').click()
        time.sleep(1)
        if d(text='加好友',resourceId='com.tencent.mobileqq:id/name').exists:
            d(text='加好友',resourceId='com.tencent.mobileqq:id/name').click()
        else:
            d(resourceId='com.tencent.mobileqq:id/name', description='快捷入口').click()
            d(text='加好友',resourceId='com.tencent.mobileqq:id/name').click()
        time.sleep(3)
        d(text='QQ号/手机号/群/公众号', resourceId='com.tencent.mobileqq:id/name').click()
        d(text='QQ号/手机号/群/公众号', resourceId='com.tencent.mobileqq:id/et_search_keyword').click()
        d(text='QQ号/手机号/群/公众号', resourceId='com.tencent.mobileqq:id/et_search_keyword').set_text(list[0])  # 第一次添加的帐号 list[0]

        d(text='找人:', resourceId='com.tencent.mobileqq:id/name').click()
        time.sleep(2)


        for i in range(1,add_count,+1):                   #给多少人发消息
            numbers = list[i]
            print(numbers)
            time.sleep(1)
            if d(text='没有找到相关结果',className='android.widget.TextView').exists:                            #没有这个人的情况
                d(resourceId='com.tencent.mobileqq:id/ib_clear_text',description='清空').click()
                obj = d(text='QQ号/手机号/群/公众号', resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)  # 下次要添加的号码
                obj = d(text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)  # 下次要添加的号码
                d.press.enter()
                while d(text='正在搜索…',index=1).exists:                  #网速不行的情况，让它不停等待
                    time.sleep(1)
                continue
            time.sleep(2)

            if d(resourceId='com.tencent.mobileqq:id/title',text='人').exists:
                d(className='android.widget.AbsListView').child(index=1,resourceId='com.tencent.mobileqq:id/name').click()



            d.swipe(width / 2, height * 3 / 6, width / 2, height / 6);
            d(text='加好友',resourceId='com.tencent.mobileqq:id/txt').click()
            time.sleep(1)

            if d(text='加好友',resourceId='com.tencent.mobileqq:id/txt').exists:                        #拒绝被添加为好友的情况
                time.sleep(1)
                d(text='返回',resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft').click()
                d(resourceId='com.tencent.mobileqq:id/ib_clear_text', description='清空').click()
                obj = d(text='QQ号/手机号/群/公众号', resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)  # 要改为从库里取------------------------------
                obj = d(text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)
                time.sleep(1)
                d.press.enter()
                while d(text='正在搜索…', index=1).exists:
                    time.sleep(1)
                continue
            time.sleep(1)


            if d(text='必填',resourceId='com.tencent.mobileqq:id/name').exists:                     #要回答问题的情况
                d(text='返回',resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft').click()
                time.sleep(1)
                d(text='返回',resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft').click()
                d(resourceId='com.tencent.mobileqq:id/ib_clear_text', description='清空').click()
                obj = d(text='QQ号/手机号/群/公众号', resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)  # 下次要添加的号码-
                obj = d(text='网络查找人',resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)
                time.sleep(1)
                d.press.enter()
                while d(text='正在搜索…', index=1).exists:
                    time.sleep(1)
                continue

            time.sleep(1)
            obj = d(text='发送',resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText')            #不需要验证可直接添加为好友的情况
            if obj.exists:
                obj.click()
                if d(text='添加失败，请勿频繁操作',resourceId='com.tencent.mobileqq:id/name').exists:
                    return
                d(text='返回', resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft').click()
                d(resourceId='com.tencent.mobileqq:id/ib_clear_text', description='清空').click()
                obj = d(text='QQ号/手机号/群/公众号', resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)  # 要改为从库里取-------------------------------
                obj = d(text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword')
                if obj.exists:
                    obj.set_text(numbers)
                d.press.enter()
                while d(text='正在搜索…', index=1).exists:
                    time.sleep(1)
                continue

            time.sleep(2)
            obj = d(className='android.widget.EditText', resourceId='com.tencent.mobileqq:id/name').info           #将之前消息框的内容删除
            obj = obj['text']
            lenth = len(obj)
            t = 0
            while t < lenth:
                d.press.delete()
                t = t + 1

            d(className='android.widget.EditText',resourceId='com.tencent.mobileqq:id/name').click()   #发送验证消息  material
            z.input(material)
            d(text='下一步',resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText').click()
            d(text='发送',resourceId='com.tencent.mobileqq:id/ivTitleBtnRightText').click()
            if d(text='添加失败，请勿频繁操作', resourceId='com.tencent.mobileqq:id/name').exists:
                return
            d(text='返回',resourceId='com.tencent.mobileqq:id/ivTitleBtnLeft').click()
            d(resourceId='com.tencent.mobileqq:id/ib_clear_text',description='清空').click()
            obj = d(text='QQ号/手机号/群/公众号', resourceId='com.tencent.mobileqq:id/et_search_keyword')
            if obj.exists:
                obj.set_text(numbers)
            obj = d(text='网络查找人', resourceId='com.tencent.mobileqq:id/et_search_keyword')
            if obj.exists:
                obj.set_text(numbers)
            d.press.enter()
            while d(text='正在搜索…', index=1).exists:
                time.sleep(1)

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
    return TIMAddFriends

if __name__ == "__main__":

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A3SK00853")
    z = ZDevice("HT4AVSK01106")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # print(d.dump(compressed=False))
    args = {"repo_number_cate_id":"13","repo_material_cate_id":"8","add_count":"9","time_delay":"3"};    #cate_id是仓库号，length是数量
    util.doInThread(runwatch, d, 0, t_setDaemon=True)
    o.action(d,z, args)