# coding:utf-8
import base64

from slot import Slot
from uiautomator import Device
from Repo import *
import os, time, datetime, random
import json
from zservice import ZDevice


class ImpContactALi:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum

    def CheckLogined(self,d, z ):
        z.toast( "检测是否已有支付宝帐号登录" )
        z.cmd("shell", "am force-stop com.eg.android.AlipayGphone")  # 强制停止
        z.cmd("shell", "am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin")
        z.sleep(15)
        if d(textContains='口碑').exists:
            if d( description='关闭', className='android.widget.ImageView' ).exists:
                d( description='关闭', className='android.widget.ImageView' ).click( )
            return True
        return False

    def CheckAddressBook(self,d, z ):
        z.toast( "检测通讯录是否正常" )
        d( description='通讯录' ).click( )
        if d( text='转到银行卡' ).exists:
            d( description='返回' ).click( )
            d( description='通讯录' ).click( )

        d( text='新的朋友' ).click( )
        d( text='添加手机联系人' ).click( )
        z.sleep(8)

        if d(textContains='账号违规').exists or d(textContains='该功能暂未对您开放').exists:
            d.server.adb.cmd( "shell", "pm clear com.eg.android.AlipayGphone" ).communicate( )  # 清除缓存
            return False
        return True


    def action(self, d,z, args):
        z.heartbeat()
        if self.CheckLogined(d, z) :
            if self.CheckAddressBook( d, z ):
                z.toast("检测到已经登录，开始导入")
            else:
                z.toast( "通讯录异常，结束模块" )
                return
        else:
            z.toast( "没有检测到登陆帐号，结束运行" )
            return


        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir, "tmp"))
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)
        filename = os.path.join(base_dir, "%s.txt"%(self.GetUnique()) )

        number_count = int(args['number_count'])
        cate_id = args["repo_cate_id"]
        while True:
            exist_numbers = self.repo.GetNumber(cate_id, 0, number_count, 'exist')
            print(exist_numbers)
            remain = number_count - len(exist_numbers)
            normal_numbers = self.repo.GetNumber(cate_id, 0, remain, 'normal')
            numbers = exist_numbers + normal_numbers
            if len(numbers)> 0:
                break

            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"电话号码%s号仓库为空，等待中\""%cate_id).communicate()
            z.sleep(30)

        if numbers:
            file_object = open(filename, 'w')
            lines = ""
            pname = ""
            for number in numbers:
                if number["name"] is None:
                    random_name = args['random_name']
                    if random_name == '是':
                        pname = z.phoneToName( number["number"] )
                    else:
                        pname = number["number"]
                else:
                    pname = number["name"]
                lines = "%s%s----%s\r" %(lines, pname, number["number"])

            file_object.writelines(lines)
            file_object.close()
            isclear = args['clear']
            if isclear=='是':
                d.server.adb.cmd("shell", "pm clear com.android.providers.contacts").communicate()

            #d.server.adb.cmd("shell", "am", "start", "-a", "zime.clear.contacts").communicate()
            d.server.adb.cmd("push", filename, "/data/local/tmp/contacts.txt").communicate()
            d.server.adb.cmd("shell", "am", "start", "-n", "com.zunyun.zime/.ImportActivity", "-t", "text/plain", "-d",
                             "file:////data/local/tmp/contacts.txt").communicate()


            #d.server.adb.cmd("shell", "am broadcast -a com.zunyun.import.contact --es file \"file:///data/local/tmp/contacts.txt\"").communicate()
            os.remove(filename)

            out = d.server.adb.cmd("shell",
                               "dumpsys activity top  | grep ACTIVITY").communicate()[0].decode('utf-8')
            while out.find("com.zunyun.zime/.ImportActivity") > -1:
                z.heartbeat()
                out = d.server.adb.cmd("shell",
                                   "dumpsys activity top  | grep ACTIVITY").communicate()[0].decode('utf-8')
                z.sleep(5)


        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return ImpContactALi

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("cda0ae8d")
    z = ZDevice("cda0ae8d")
#     pkg = 'com.tencent.mobileqq'
#     z.server.install()
#
#
#     slot = Slot('cda0ae8d', 'mobileqq')
#     print (slot.getSlots())
#     #slot.backup('1', 'slot_1')
#     #slot.restore('1')
#     print (z.qq_getLoginStatus(d))
#     z.generate_serial('com.tencent.mobileqq')
#     print(z.get_serial(pkg))
#     info = '{"buildManufacturer":"ZTE","buildModel":"ZTE G720C","buildSerial":"ytz0fad63hkensm","buildVersionRelease":"Android 2.2.3","empty":false,"settingsSecureAndroidId":"wwx31wo6hhxbkrw","telephonyGetDeviceId":"864948416091531","telephonyGetLine1Number":"+8615015541026","telephonyGetNetworkType":"12","telephonyGetSimSerialNumber":"84508614357292636763","telephonyGetSubscriberId":"48313995020377949279","wifiInfoGetMacAddress":"00:03:6C:6B:B2:EA","wifiInfoGetSSID":"TP-ZPBZEBM7"}'
#     z.set_serial(pkg, info)
#     source = '/tmp/xxx.png'
#     d.screenshot(source)
#     width = 540.0
#     height = 960.0
#     p =  { "x1":37/width, "y1":380/height, "x2":502/width, "y2":473/height}
#     z.img_crop(source, p)
#
#     out = d.server.adb.run_cmd('shell', 'ls')
#     z.input("xxx")
# #    d.server.adb.cmd("shell", "ime set com.zunyun.zime/.ZImeService").communicate()
#     z.server.install()
#
#     slot = Slot('FA53CSR02947', 'mobileqq')
#     print (slot.getSlots())
#     slot.backup('21', '22221111')
#
#     print (slot.getSlots())
#     slot.clear('21')
#
#     z.generateSerial();
#     #z.input("6565wv=1027&k=48KHKLm")
#
#
#     #d.server.adb.cmd("shell", "am", "start", "-a", "zime.clear.contacts").communicate()
#     d.server.adb.cmd("shell", "pm clear com.android.providers.contacts").communicate()
#     #d.server.adb.cmd("push", filename, "/data/local/tmp/contacts.txt").communicate()
#     d.server.adb.cmd("shell", "am", "start", "-n", "com.zunyun.zime/.ImportActivity", "-t", "text/plain", "-d",
#                      "/data/local/tmp/contacts.txt").communicate()

    # d.dump(compressed=False)


    args = {"repo_cate_id":"113",'number_count':'50',"random_name":"是","clear":"是","time_delay":"3"}    #cate_id是仓库号，length是数量

    o.action(d,z, args)
