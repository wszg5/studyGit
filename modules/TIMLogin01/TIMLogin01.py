# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import os,re,subprocess
import util
from Repo import *
from RClient import *
import time, datetime, random
from slot import slot
from zservice import ZDevice

class TIMLogin01:

    def __init__(self):
        self.repo = Repo()
        self.slot = slot('tim')

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum


    def login(self,d,z,args):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        sourcePng = os.path.join(base_dir, "%s_s.png" % (self.GetUnique()))
        codePng = os.path.join(base_dir, "%s_c.png" % (self.GetUnique()))


        cate_id = args["repo_cate_id"]
        numbers = self.repo.GetAccount(cate_id, 120, 1)
        print(numbers)
        wait = 1
        while wait == 1:  # 判断仓库是否有东西
            try:
                QQNumber = numbers[0]['number']  # 即将登陆的QQ号
                wait = 0
            except Exception:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"仓库为空，没有取到号码\"")
                time.sleep(20)
        QQPassword = numbers[0]['password']
        time.sleep(1)
        t=1
        while t ==1:
            d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()  # 清除缓存
            d.server.adb.cmd("shell", "am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来
            time.sleep(3)
            for k in range(1, 35):
                time.sleep(1)
                if d(resourceId='com.tencent.tim:id/title', index=1, text='熟悉的QQ习惯').exists:
                    str = d.info  # 获取屏幕大小等信息
                    height = str["displayHeight"]
                    width = str["displayWidth"]
                    for i in range(0, 2):
                        d.swipe(width * 0.75, height * 0.5, width * 0.05, height * 0.5, 10)
                        time.sleep(1)
                    d(resourceId='com.tencent.tim:id/name', index=1, text='立即体验').click()
                    break

            if k == 35:
                continue
            time.sleep(2)
            d(text='QQ号登录',resourceId='com.tencent.tim:id/btn_login').click()

            d(className='android.widget.EditText',text='QQ号/手机号/邮箱').set_text(177751879)    #3001313499    3030327691   QQNumber
            d(resourceId='com.tencent.tim:id/password',description='密码 安全').set_text('13141314Abc')    #Bn2kJq5l
            d(text='登 录',resourceId='com.tencent.tim:id/login').click()
            while d(className='android.widget.LinearLayout').child(text='登录中',resourceId='com.tencent.tim:id/name').exists:
                time.sleep(1)
            # time.sleep(6)


            # d.watcher('success').when(text='搜索').when(resourceId='com.tencent.tim:id/name')

            # if d(text='搜索',resourceId='com.tencent.tim:id/name').exists:       #直接登陆成功的情况
            #     return  # 放到方法里改为return


            # if d(text='帐号无法登录', resourceId='com.tencent.eim:id/dialogTitle').exists:  # 帐号被冻结
            #     self.repo.SetAccount(cate_id, 'frozen', QQNumber)
            #     break

            if d(resourceId='com.tencent.tim:id/name', index='2', className="android.widget.EditText").exists:        #需要验证码的情况
                co = RClient()
                im_id = ""
                for i in range(0, 30, +1):         #打码循环
                    if i > 0:
                        co.rk_report_error(im_id)
                    obj = d(resourceId='com.tencent.tim:id/name', className='android.widget.ImageView')
                    obj = obj.info
                    print(obj)
                    obj = obj['bounds']  # 验证码处的信息
                    left = obj["left"]  # 验证码的位置信息
                    top = obj['top']
                    right = obj['right']
                    bottom = obj['bottom']

                    d.screenshot(sourcePng)  # 截取整个输入验证码时的屏幕

                    img = Image.open(sourcePng)
                    box = (left, top, right, bottom)  # left top right bottom
                    region = img.crop(box)  # 截取验证码的图片

                    img = Image.new('RGBA', (right - left, bottom - top))
                    img.paste(region, (0, 0))

                    img.save(codePng)
                    im = open(codePng, 'rb').read()

                    codeResult = co.rk_create(im, 3040)
                    code = codeResult["Result"]
                    im_id = codeResult["Id"]
                    os.remove(sourcePng)
                    os.remove(codePng)

                    d(resourceId='com.tencent.tim:id/name', index='2', className="android.widget.EditText").set_text(code)
                    time.sleep(1)
                    d(text='完成', resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
                    time.sleep(2)

                    if d(text='登 录').exists:  # 密码错误
                        self.repo.SetAccount(cate_id, 'locked', QQNumber)
                        break

                    if d(text='帐号无法登录', resourceId='com.tencent.tim:id/dialogTitle').exists:  # 帐号被冻结
                        self.repo.SetAccount(cate_id, 'frozen', QQNumber)
                        break
                    if d(text='身份过期',resourceId='com.tencent.tim:id/dialogTitle').exists:
                        break
                    #
                    if d(text='搜索',resourceId='com.tencent.tim:id/name').exists:
                        return  # 放到方法里改为return


            if d(text='搜索', resourceId='com.tencent.tim:id/name').exists:       #不需要验证码的情况
                # t=2
                return QQNumber # 放到方法里改为return
            if d(text='马上绑定').exists:
                # t=2
                return QQNumber


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

    def action1(self, d, z,args):
        time_limit = args['time_limit']
        cate_id = args["repo_cate_id"]

        name = self.slot.getEmpty(d)                    #取空卡槽
        print name
        while name ==0:
            name = self.slot.getSlot(d,time_limit)              #没有空卡槽，取２小时没用过的卡槽
            print '切换为'+str(name)
            while name == 0:                               #2小时没有用过的卡槽也为空的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"卡槽全满，无2小时未用\"").communicate()
                time.sleep(30)
                name = self.slot.getSlot(d,time_limit)

            z.set_mobile_data(False)
            time.sleep(3)
            self.slot.restore(d,name)                      #有２小时没用过的卡槽情况，切换卡槽
            z.set_mobile_data(True)
            time.sleep(8)

            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.qk.toast --es msg \"TIM卡槽成功切换成"+str(name)+"\"").communicate()
            time.sleep(1)

            d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            for k in range(1, 35):
                time.sleep(1)
                if d(resourceId='com.tencent.tim:id/title', index=1, text='熟悉的QQ习惯').exists:
                    str = d.info  # 获取屏幕大小等信息
                    height = str["displayHeight"]
                    width = str["displayWidth"]
                    for i in range(0, 2):
                        d.swipe(width * 0.75, height * 0.5, width * 0.05, height * 0.5, 10)
                        time.sleep(1)
                    d(resourceId='com.tencent.tim:id/name', index=1, text='立即体验').click()
                    break

            if k == 35:
                continue
            time.sleep(2)

            if d(text='消息',resourceId='com.tencent.tim:id/ivTitleName').exists:
                obj = self.slot.getSlotInfo(d,name)  #得到切换后的QQ号
                info = obj['info']  #info为QQ号
                self.repo.BackupInfo(cate_id,'using',info,'%s_%s'%(d.server.adb.device_serial(),name))  # 将登陆上的仓库cate_id,设备号d，卡槽号name，qq号info，备份到仓库
            else:
                info = self.login(d,z,args)                                             #帐号无法登陆则登陆,重新注册登陆
                self.slot.backup(d, name, info)  # 登陆之后备份,将备份后的信息传到后台　仓库号，状态，QQ号，备注设备id_卡槽id
                self.repo.BackupInfo(cate_id, 'using', info, '%s_%s'%(d.server.adb.device_serial(),name))  # 将登陆上的仓库cate_id,设备号d，卡槽号name，qq号info，备份到仓库


        else:                           #有空卡槽的情况
            # z.set_mobile_data(False)
            # time.sleep(3)
            # z.set_mobile_data(True)
            # time.sleep(8)
            info = self.login(d,z,args)
            self.slot.backup(d,name,info)          #设备信息，卡槽号，QQ号
            self.repo.BackupInfo(cate_id, 'using', info,'%s_%s'%(d.server.adb.device_serial(),name))     #仓库号,使用中,QQ号,设备号_卡槽号


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



    # def action(self, d, z, args):





# def runwatch(d, data):                                  #watcher除了点击还可以做什么，watcher到可以结束方法吗，可以改变参数吗
#     times = 120
#     while True:
#         if data == 1:
#             return True
#         # d.watchers.reset()
#         d.watchers.run()                      #强制运行所有watchers
#         times -= 1
#         if times == 0:
#             break
#         else:
#             time.sleep(0.5)

def getPluginClass():
    return TIMLogin01

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()

    d = Device("HT54VSK01061")
    z = ZDevice("HT54VSK01061")

    # slot = slot('tim')

    # slot.restore(d, 1)  # 有２小时没用过的卡槽情况，切换卡槽

    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_cate_id":"64","time_limit":"120","time_delay":"3"};    #cate_id是仓库号，length是数量
    # util.doInThread(runwatch, d, 0, t_setDaemon=True)

    o.action(d,z, args)
    # d.server.adb.cmd("shell", "pm clear com.taojin.dungeon.sy37").communicate()  # 清除缓存
    # d.server.adb.cmd("shell","am start -n com.taojin.dungeon.sy37/com.taojin.dungeon.MySplashActivity").communicate()  # 拉起来

    # while 1:
    #     time.sleep(0.44)
    #     d.click(100,150)
    #     d.click(270, 484)

