# coding:utf-8
import os
import random
from zcache import cache
from uiautomator import Device
from Repo import *

from zservice import ZDevice


class GoogleKeyWord_1:
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
        count = 1
        while count < int(args["run_count"]):
            count += 1

            # start_time = args['start_time']
            # stop_time = args['stop_time']
            # try:
            #     if self.repo.timeCompare( start_time, stop_time ):
            #         run_interval = z.getModuleRunInterval_new( self.mid )
            #         if self.timeCompare_this(start_time, stop_time ,run_interval):
            #             z.toast( '时间:'+run_interval+'，模块搜索次数已满' )
            #             return
            #     else:
            #         z.toast( '不处于' + start_time + '～' + stop_time + '时间段内，模块不运行' )
            #         return
            # except:
            #     logging.exception( "exception" )
            #     z.toast( "输入时间格式有误" )
            #     return

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

            z.generate_serial("com.android.chrome")  # 随机生成手机特征码
            z.toast("Generate Phone serial information")

            # 取关键词
            material_KeyWords_id = args["material_KeyWords_id"]
            KeyWords_interval = args["KeyWords_interval"]
            materials = Repo().GetMaterial(material_KeyWords_id, KeyWords_interval, 1)
            if len(materials) == 0:
                z.toast(material_KeyWords_id + "号关键词仓库为空")
                return
            KeyWords = materials[0]["content"]
            BusinessName = materials[0]["name"]

            d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "http://www.google.com"')
            z.sleep(5)

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
            while not (d(description="Google", className="android.widget.Image").exists or d(resourceId="hplogo").exists ) :
                j += 1
                z.sleep(3)
                if j == 3:
                    z.toast("Network is very slow")
                    break
            if j == 3:
                return

            z.heartbeat()
            if d(resourceId='lst-ib').exists:
                d(resourceId='lst-ib').click()
            elif d(className='android.widget.EditText', index=0).exists:
                d(className='android.widget.EditText', index=0).click()

            # else:
            #     bounds = d(description="Google",className="android.widget.Image").info['bounds']
            #     d.click(int(bounds['left']) - 200, (int(bounds['bottom']) - int(bounds['top'])) / 2 + int(bounds['top']))
            z.sleep(1)

            z.input(KeyWords)
            z.sleep(random.randint(2, 4))
            z.heartbeat()

            if d(description='搜索', className='android.widget.Button').exists:
                d(description='搜索', className='android.widget.Button').click()
            elif d(description='ค้นหา', className='android.widget.Button').exists:
                d(description='ค้นหา', className='android.widget.Button').click()
            elif d(description='Search', className='android.widget.Button').exists:
                d(description='Search', className='android.widget.Button').click()
            elif d(resourceId='tsbb').exists:
                d(resourceId='tsbb').click()

            z.sleep(random.randint(8, 15))
            z.heartbeat()



            x = 1
            while True:
                z.toast("we are at page: %d" % x)
                while d(resourceId='com.android.chrome:id/infobar_close_button').exists:
                    d(resourceId='com.android.chrome:id/infobar_close_button').click()
                    z.sleep(2)


                if d(resourceId='com.android.chrome:id/url_bar', className='android.widget.EditText').exists:
                    urlStr1 = \
                        d(resourceId='com.android.chrome:id/url_bar', className='android.widget.EditText').info[
                            "text"]

                d.dump(compressed=False)
                if d(descriptionContains=BusinessName).exists:
                    d(descriptionContains=BusinessName).click()
                    z.sleep(10)

                    z.heartbeat()
                    d.swipe(width / 2, height / 7, width / 2, height * 2 / 7)

                    if d(resourceId='com.android.chrome:id/url_bar', className='android.widget.EditText').exists:
                        urlStr2 = \
                            d(resourceId='com.android.chrome:id/url_bar', className='android.widget.EditText').info[
                                "text"]

                    if urlStr1 == urlStr2:
                        d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                        continue



                    if args["if_slippage"] == "是":

                        for i in range(0, random.randint(1, 3)):  # 随机下翻页
                            d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                            z.sleep(2)
                            z.heartbeat()

                        d.swipe(width / 2, height / 7, width / 2, height * 6 / 7)  # 随机上翻页
                        z.sleep(2)
                        z.heartbeat()

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
                        while d(resourceId='com.android.chrome:id/infobar_close_button').exists:
                            d(resourceId='com.android.chrome:id/infobar_close_button').click()
                            z.sleep(2)

                        d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                        if d(resourceId='com.android.chrome:id/url_bar', className='android.widget.EditText').exists:
                            urlStr1 = d(resourceId='com.android.chrome:id/url_bar', className='android.widget.EditText').info["text"]
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
                        else:
                            z.toast("No next page button found")
                            return;


                        d.swipe(width / 2, height / 7, width / 2, height * 2 / 7)

                        if d(resourceId='com.android.chrome:id/url_bar', className='android.widget.EditText').exists:
                            urlStr2 = d(resourceId='com.android.chrome:id/url_bar', className='android.widget.EditText').info["text"]
                        if urlStr1 == urlStr2:
                            continue
                        else:
                            break




                    z.heartbeat()
                    if x == int(args["slippage_count"]):
                        z.toast("已经翻完" + args["slippage_count"] + "页")
                        break
                    else:
                        x += 1
                        continue

            if x == int(args["slippage_count"]):
                z.toast("No result，search again。")
                #nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #para = {"phoneNumber": KeyWords, "x_01": BusinessName, "x_02": "N", "x_20": nowTime}
                #self.repo.PostInformation(int(args['repo_information_id']), para)
                continue

            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            para = {"phoneNumber": KeyWords, "x_01": BusinessName, "x_02": "Y", "x_20": nowTime}
            self.repo.PostInformation(int(args['repo_information_id']), para)

        now = datetime.datetime.now()
        nowtime = now.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun_new(self.mid)
        z.toast('模块结束，保存的时间是%s' % nowtime)

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))


def getPluginClass():
    return GoogleKeyWord_1


if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("920121a870e384dd")
    z = ZDevice("920121a870e384dd")
    #z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").communicate()

    args = {'start_time': '16', 'stop_time': '16:10', "repo_information_id": "204", "material_KeyWords_id": "207",
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











