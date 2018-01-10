# coding:utf-8
import os,re
import random
from zcache import cache
from uiautomator import Device
from Repo import *

from zservice import ZDevice


class ChromeSwitcher:
    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath(__file__)


    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def GetChromeAgent(self):
        d = dict()
        d['SONY_Xperia X_UC_11.5.1.944'] = 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36'
        d['vivo_X7_ANDROID_Internal'] = 'Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 5.1.1)'
        d['HUAWEI_MATE7_ANDROID_INTERNAL'] = 'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-CN; HUAWEI MT7-TL00 Build/HuaweiMT7-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.3.8.909 Mobile Safari/537.36'
        return d
        #agent['Sumsung_Chrome_55.66'] = ''
        #agent['Sumsung_Chrome_56.66'] = ''
        #agent['Sumsung_Chrome_57.66'] = ''

    def action(self, d, z, args):

        d.server.adb.cmd("shell", "am force-stop com.android.chrome").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "pm clear com.android.chrome").communicate()  # 清除浏览器缓存
        agents = self.GetChromeAgent()
        from random import choice
        key = choice(agents.keys())
        value = agents[key]

        d.press.home()
        z.toast("Change Browser to %s" % key)

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        filename = os.path.join(base_dir, "%s.txt"%(self.GetUnique()) )
        file_object = open(filename, 'w')

        # 取User-agent关键词
        #material_KeyWords_id = args["material_KeyWords_id"]
        #KeyWords_interval = args["KeyWords_interval"]
        #materials = Repo().GetMaterial(material_KeyWords_id, KeyWords_interval, 1)
        #if len(materials) == 0:
         #   z.toast(material_KeyWords_id + " chrome user-agentnwarehouse is empty")
          #  z.sleep(10)
           # return
        #content = materials[0]["content"]
        #agentName = materials[0]["name"]

        #z.toast("Get agent for : %s" % agentName)

        content = 'chrome --user-agent="%s"' % value
        file_object.writelines(content)
        file_object.close()
        d.server.adb.cmd("push", filename, "/data/local/tmp/chromeagent.txt").communicate()

        z.cmd("shell", "'rm -rf /data/local/chrome-command-line'")
        z.cmd("shell", "su -c 'cp -F /data/local/tmp/chromeagent.txt /data/local/chrome-command-line'")
        d.server.adb.cmd("shell", "su -c 'chmod -R 777 /data/local/chrome-command-line'").wait()

        d.server.adb.cmd("shell", "am force-stop com.android.chrome").communicate()  # 将微信强制停止



        z.heartbeat()
        while True:
            ping = d.server.adb.cmd("shell", "ping -c 3 google.com").communicate()
            z.toast("Checking network")

            print(ping)
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                break
            z.sleep(3)


        if args["Check_Result"] == 'Yes' :
            d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "http://www.user-agent.cn"')
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

        z.sleep(int(args['time_delay']))


def getPluginClass():
    return ChromeSwitcher


if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("920121a870e384dd")
    z = ZDevice("920121a870e384dd")
    #d.server.adb.cmd("shell", "am force-stop com.android.chrome").communicate()  # 将微信强制停止

    screen_d_after = d.dump(compressed=False)  # 点击后的屏幕内容

    a1 = re.compile(r'\[-?\d*,-?\d*\]')
    screen_d_after = a1.sub('', screen_d_after)
    #z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").communicate()

    args = {'start_time': '16', 'stop_time': '16:10', "repo_information_id": "204", "material_KeyWords_id": "207",
            "KeyWords_interval": "0", "run_count": "3", "slippage_count": "20", "Check_Result": "Yes", "time_delay": "3"};
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











