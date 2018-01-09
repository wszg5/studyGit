# coding:utf-8
import os,re
import random
from zcache import cache
from uiautomator import Device
from Repo import *

from zservice import ZDevice


class GoogleKeyWord_2:
    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath(__file__)

    def timeCompare_this(self, start_time, stop_time, compare_time):
        if start_time == "" or stop_time == "":
            return False

        if compare_time is None:
            return False

        if not ":" in start_time:
            start_time = start_time + ":00"

        if not ":" in stop_time:
            stop_time = stop_time + ":00"

        if time.strptime(start_time, '%H:%M') < time.strptime(stop_time, '%H:%M'):
            if time.strptime(start_time, '%H:%M') < time.strptime(compare_time, '%H:%M') < time.strptime(stop_time,
                                                                                                         '%H:%M'):
                return True
            else:
                return False

        else:
            if time.strptime(start_time, '%H:%M') < time.strptime(compare_time, '%H:%M') < time.strptime("23:59",
                                                                                                         '%H:%M') or time.strptime(
                "00:00", '%H:%M') < time.strptime(compare_time, '%H:%M') < time.strptime(stop_time, '%H:%M'):
                return True
            else:
                return False

    def action(self, d, z, args):
        z.toast("Starting：Google Search")

        d.server.adb.cmd("shell", "pm clear com.android.chrome").communicate()  # 清除浏览器缓存

        z.heartbeat()
        while True:
            ping = d.server.adb.cmd("shell", "ping -c 3 google.com").communicate()
            z.toast("Checking network")

            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                break
            z.sleep(3)

        Str = d.info  # 获取屏幕大小等信息
        height = float(Str["displayHeight"])
        width = float(Str["displayWidth"])

        #z.generate_serial("com.android.chrome")  # 随机生成手机特征码
        #z.toast("Generate Phone serial information")

        # 取关键词
        material_KeyWords_id = args["material_KeyWords_id"]
        KeyWords_interval = args["KeyWords_interval"]
        materials = Repo().GetMaterial(material_KeyWords_id, KeyWords_interval, 1)
        if len(materials) == 0:
            z.toast(material_KeyWords_id + " warehouse is empty")
            z.sleep(10)
            return
        KeyWords = materials[0]["content"]
        BusinessName = materials[0]["name"]

        d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "http://www.google.com"')
        z.sleep(6)
        d.dump(compressed=False)
        z.heartbeat()
        if d(text='Accept & continue').exists:
            d(text="Accept & continue").click()
            z.sleep(5)

        if d(resourceId='com.android.chrome:id/terms_accept').exists:
            d(resourceId='com.android.chrome:id/terms_accept').click()
            z.sleep(5)

        if d(text='Next').exists:
            d(text="Next").click()
            z.sleep(5)

        if d(text='No Thanks').exists:
            d(text="No Thanks").click()
            z.sleep(5)

        if d(text='ไม่ ขอบคุณ').exists:
            d(text='ไม่ ขอบคุณ').click()
            z.sleep(5)


        j = 0
        while not (d(description="Google", className="android.widget.Image").exists or d(resourceId="hplogo").exists
                   or d(resourceId='lst-ib').exists or d(resourceId='tsbb').exists or d(resourceId='mib').exists
                   or d(description='Search', className='android.widget.Button').exists) :
            j += 1
            z.sleep(3)
            if j == 3:
                break
        if j == 3:
            z.toast("please check network or enable and disable TalkBack.")
            z.sleep(5)
            return

        z.heartbeat()
        if d(resourceId='lst-ib').exists:
            d(resourceId='lst-ib').click()
        elif d(resourceId='mib').exists:
            d(resourceId='mib').click()
        elif d(className='android.widget.EditText', index=0).exists:
            d(className='android.widget.EditText', index=0).click()
        else:
            z.toast("please enable and disable TalkBack.")

        # else:
        #     bounds = d(description="Google",className="android.widget.Image").info['bounds']
        #     d.click(int(bounds['left']) - 200, (int(bounds['bottom']) - int(bounds['top'])) / 2 + int(bounds['top']))
        z.sleep(2)

        z.input(KeyWords)
        z.sleep(2)
        z.heartbeat()

        if d(description='搜索', className='android.widget.Button').exists:
            d(description='搜索', className='android.widget.Button').click()
        elif d(description='ค้นหา', className='android.widget.Button').exists:
            d(description='ค้นหา', className='android.widget.Button').click()
        elif d(description='Search', className='android.widget.Button').exists:
            d(description='Search', className='android.widget.Button').click()
        elif d(resourceId='tsbb').exists:
            d(resourceId='tsbb').click()
            z.sleep(3)
            if d(resourceId='tsbb').exists:
                d(resourceId='tsbb').click()

        z.sleep(random.randint(5, 10))
        z.heartbeat()



        x = 0
        while True:

            if x >= int(args["slippage_count"]):
                z.toast("already finished page for " + args["slippage_count"])
                break

            x += 1
            z.toast("we are at page: %d" % x)
            while d(resourceId='com.android.chrome:id/infobar_close_button').exists:
                d(resourceId='com.android.chrome:id/infobar_close_button').click()
                z.sleep(2)

            for i in range(0, 5):
                if d(text="ใช้ภาษาภาษาไทยต่อไป").exists:
                    d(text="ใช้ภาษาภาษาไทยต่อไป").click()
                    z.sleep(2)

                if d(description="ใช้ภาษาภาษาไทยต่อไป").exists:
                    d(description="ใช้ภาษาภาษาไทยต่อไป").click()
                    z.sleep(2)

            d.dump(compressed=False)
            targetObj = d(descriptionContains=BusinessName)
            if not targetObj.exists:
                targetObj = d(textContains=BusinessName)
            if targetObj.exists:
                while True:
                    z.toast("Keyword found, try to scroll and click")
                    screen_d_before = d.dump(compressed=False)  # 点击前的屏幕内容
                    targetObj.click()
                    z.sleep(10)

                    screen_d_after = d.dump(compressed=False)  #点击后的屏幕内容

                    a1 = re.compile(r'\[-?\d*,-?\d*\]')
                    screen_d_before = a1.sub('', screen_d_before)
                    screen_d_after = a1.sub('', screen_d_after)
                    if (screen_d_before == screen_d_after):  #屏幕内容相同，继续滑动
                        d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                        continue
                    else:
                        break
                if args["if_slippage"] == "是":

                    for i in range(0, random.randint(1, 3)):  # 随机下翻页
                        d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                        z.sleep(2)
                        z.heartbeat()

                    d.swipe(width / 2, height / 7, width / 2, height * 6 / 7)  # 随机上翻页
                    z.sleep(2)

                z.heartbeat()
                for i in range(0, 5):
                    d.click(random.randint(int(width / 8), width), random.randint(int(height / 7), height))
                    z.sleep(5)

                z.sleep(random.randint(5, 10))
                z.heartbeat()

                break

            else:
                z.heartbeat()

                for i in range(0, 10):
                    z.toast("Keyword Not found, Scroll and Next pageing")

                    while d(resourceId='com.android.chrome:id/infobar_close_button').exists:
                        d(resourceId='com.android.chrome:id/infobar_close_button').click()
                        z.sleep(2)

                    for i in range(0, 5):
                        if d(text="ใช้ภาษาภาษาไทยต่อไป").exists:
                            d(text="ใช้ภาษาภาษาไทยต่อไป").click()
                            z.sleep(2)

                        if d(description="ใช้ภาษาภาษาไทยต่อไป").exists:
                            d(description="ใช้ภาษาภาษาไทยต่อไป").click()
                            z.sleep(2)

                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)

                    screen_d_before = d.dump(compressed=False)  # 点击前的屏幕内容

                    if d(description='下一页', className='android.view.View').exists:
                        d(description='下一页', className='android.view.View').click()
                        z.sleep(random.randint(3, 5))
                        z.heartbeat()
                    elif d(description='หน้าถัดไป', className='android.view.View').exists:
                        d(description='หน้าถัดไป', className='android.view.View').click()
                        z.sleep(random.randint(3, 5))
                        z.heartbeat()
                    elif d(resourceId='pnnext').exists:
                        d(resourceId='pnnext').click()
                        z.sleep(random.randint(3, 5))
                        z.heartbeat()
                        #print(d(resourceId='pnnext').info)
                    elif d(description='ถัดไป »').exists:
                        d(description='ถัดไป »').click()
                        z.sleep(random.randint(3, 5))
                        z.heartbeat()
                        #print(d(resourceId='pnnext').info)
                    else:
                        z.toast("No next page button found")
                        return;

                    screen_d_after = d.dump(compressed=False)  # 点击后的屏幕内容

                    a1 = re.compile(r'\[-?\d*,-?\d*\]')
                    screen_d_before = a1.sub('', screen_d_before)
                    screen_d_after = a1.sub('', screen_d_after)
                    if screen_d_before == screen_d_after:
                        continue
                    else:
                        break;  #设置循环值 i=10 ，直接跳出翻页循环

                z.heartbeat()



        now = datetime.datetime.now()
        nowtime = now.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun_new(self.mid)
        z.toast('模块结束，保存的时间是%s' % nowtime)

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return GoogleKeyWord_2


if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("9201204840b3a4c5")
    z = ZDevice("9201204840b3a4c5")

    screen_d_after = d.dump(compressed=False)  # 点击后的屏幕内容

    a1 = re.compile(r'\[-?\d*,-?\d*\]')
    screen_d_after = a1.sub('', screen_d_after)
    #z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").communicate()

    args = {'start_time': '16', 'stop_time': '16:10', "repo_information_id": "204", "material_KeyWords_id": "216",
            "KeyWords_interval": "0", "run_count": "3", "slippage_count": "20", "if_slippage": "是", "time_delay": "3"};
    o.action(d, z, args)
    # obj = d( className='android.widget.Button' )
    # if obj.exists:
    #     obj =  d( className='android.widget.Button' ).info["bounds"]
    #     left = obj["left"]
    #     bottom = obj["bottom"]
    #     top = obj["top"]
    #     d.click(left-88,bottom - (bottom - top)/2)
    #     if obj.exists:
    #         d( className='android.widget.Button' ).left( className="android.widget.EditText" ).click()
    #         z.input("123")
    # d.server.adb.cmd( "shell", "pm clear com.android.chrome" ).communicate( )  # 清除浏览器缓存
    #
    # d.server.adb.cmd( "shell", 'am start -a android.intent.action.VIEW -d  http://www.google.cn/' )











