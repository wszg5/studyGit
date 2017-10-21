# coding:utf-8
import os

from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice

class WXImpContactAddressAddFriend:

    def __init__(self):
        self.repo = Repo()
        self.mid = os.path.realpath( __file__ )

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum


    def impContact(self, d,z, args):
        z.heartbeat()
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
                        pname = z.phoneToName(number["number"])
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

            d.server.adb.cmd("push", filename, "/data/local/tmp/contacts.txt").communicate()
            d.server.adb.cmd("shell", "am", "start", "-n", "com.zunyun.zime/.ImportActivity", "-t", "text/plain", "-d",
                             "file:////data/local/tmp/contacts.txt").communicate()

            os.remove(filename)

            out = d.server.adb.cmd("shell",
                               "dumpsys activity top  | grep ACTIVITY").communicate()[0].decode('utf-8')
            while out.find("com.zunyun.zime/.ImportActivity") > -1:
                z.heartbeat()
                out = d.server.adb.cmd("shell",
                                   "dumpsys activity top  | grep ACTIVITY").communicate()[0].decode('utf-8')
                z.sleep(5)


    def action(self, d, z, args):
        run_time = float( args['run_time'] ) * 60
        run_interval = z.getModuleRunInterval( self.mid )
        if run_interval is not None and run_interval < run_time:
            z.toast( u'锁定时间还差:%d分钟' % int( run_time - run_interval ) )
            z.sleep( 2 )
            return

        start_time = args['start_time']
        stop_time = args['stop_time']
        try:
            if self.repo.timeCompare( start_time, stop_time ):
                z.toast('处于' + start_time + '～' + stop_time + '时间段内，模块不运行' )
                z.sleep( 2 )
                return
        except:
            logging.exception( "exception" )
            z.toast( "输入时间格式有误" )
            return

        self.impContact(d, z, args)

        z.heartbeat()
        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        z.sleep(7)
        d(description='更多功能按钮').click()
        d(textContains='添加朋友').click()
        d(text='手机联系人').click()
        d(text='添加手机联系人').click()
        while d(textContains='正在获取').exists:
            z.sleep(3)
        z.heartbeat()
        set1 = set()
        change = 0
        i = 0
        t = 0
        EndIndex = int(args['EndIndex'])         #------------------
        while t < EndIndex :
            cate_id = args["repo_material_id"]   #------------------
            Material = self.repo.GetMaterial(cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % cate_id).communicate()
                z.sleep(10)
                return
            message = Material[0]['content']  # 从素材库取出的要发的材料

            z.sleep(1)
            wxname = d(className='android.widget.ListView').child(className='android.widget.LinearLayout', index=i).child(className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).child(textContains='微信:')     #得到微信名
            if wxname.exists:
                z.heartbeat()
                alreadyAdd = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',
                                                                          index=i).child(
                    className='android.widget.LinearLayout', index=0).child(className='android.widget.FrameLayout',
                                                                            index=2).child(
                    text='已添加')  # 该编号好友已经被添加的情况
                if alreadyAdd.exists:
                    i = i+1
                    continue

                change = 1      #好友存在且未被添加的情况出现，change值改变
                wxname = wxname.info
                name = wxname['text']
                z.heartbeat()
                if name in set1:    #判断是否已经给该人发过消息
                    i = i+1
                    continue
                else:
                    set1.add(name)
                print(name)
                d(className='android.widget.ListView',index=0).child(className='android.widget.LinearLayout',index=i).\
                    child(className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).click()      #点击第i个人
                GenderFrom = args['gender']     #-------------------------------
                if GenderFrom !='不限':
                    Gender = d(className='android.widget.LinearLayout',index=1).child(className='android.widget.LinearLayout').child(className='android.widget.ImageView',index=1)      #看性别是否有显示
                    if Gender.exists:
                        z.heartbeat()
                        Gender = Gender.info
                        Gender = Gender['contentDescription']
                        if Gender !=GenderFrom:
                                     #如果性别不符号的情况
                            d(description='返回').click()
                            i = i+1
                            continue
                    else:                 #信息里没有显示出性别的话
                        d(description='返回').click()
                        i = i + 1
                        continue
                z.heartbeat()
                if d(text='添加到通讯录').exists:
                    d(text='添加到通讯录').click()
                    time.sleep(0.5)
                    if d(text='发消息').exists:
                        d(description='返回').click()
                        i = i+1
                        continue

                elif d(text='通过验证').exists:
                    d(text='通过验证').click()
                    d(description='返回').click()
                    i = i + 1
                    continue


                else:
                    d(description='返回').click()
                    i = i+1
                    continue
                z.sleep(1)
                deltext = d(className='android.widget.EditText', index=1).info  # 将之前消息框的内容删除
                deltext = deltext['text']
                lenth = len(deltext)
                m = 0
                while m < lenth:
                    d.press.delete()
                    m = m + 1
                z.heartbeat()
                d(className='android.widget.EditText', index=1).click()
                z.input(message)       #----------------------------------------
                d(text = '发送').click()
                z.sleep(1)
                d(description='返回').click()
                i = i+1
                t = t+1
                continue

            else:
                if change==0:   #一次还没有点击到人
                    if i==1:    #通讯录没有人的情况
                        return
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    i = 1
                    continue
                else:
                    d.swipe(width / 2, height * 6 / 7, width / 2, height / 7)
                    endterm = d(className='android.widget.LinearLayout', index=i-1).child(className='android.widget.LinearLayout').child(className='android.widget.LinearLayout',index=1).child(textContains='微信:')
                    time.sleep(0.5)
                    if endterm.exists:
                        endterm = endterm.info
                        name1 = endterm['text']      #判断是否已经到底
                        if name1 in set1:
                            return
                    i = 1
                    continue

        now = datetime.datetime.now( )
        nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
        z.setModuleLastRun( self.mid )
        z.toast( '模块结束，保存的时间是%s' % nowtime )

        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))

def getPluginClass():
    return WXImpContactAddressAddFriend

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A1SK02114")
    z = ZDevice("HT4A1SK02114")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()

    args = {'run_time': '1', 'start_time': '16.', 'stop_time': '8', "repo_material_id": "39", 'EndIndex': '100', 'gender': "女", "time_delay1": "3",
            "repo_cate_id": "113", 'number_count': '50', "random_name": "是", "clear": "是", "time_delay2": "3"}    #cate_id是仓库号，length是数量
    # o.action(d, z, args)
    repo = Repo()
    start_time = args['start_time']
    stop_time = args['stop_time']
    try:
        if repo.timeCompare(start_time,stop_time):
            print "dsds"
    except:
        logging.exception("exception")
        z.toast("输入时间格式有误")





































