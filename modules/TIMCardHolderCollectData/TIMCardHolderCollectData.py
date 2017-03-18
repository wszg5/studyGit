# coding:utf-8
from uiautomator import Device
from Repo import *
from Inventory import *
import os, time, datetime, random
from zservice import ZDevice


class TIMCardHolderCollectData:
    def __init__(self):

        self.repo = Repo()
        self.inventory = Inventory()


    def action(self, d, z, args):

        d.server.adb.cmd("shell", "am force-stop com.tencent.tim").communicate()  # 强制停止
        d.server.adb.cmd("shell","am start -n com.tencent.tim/com.tencent.mobileqq.activity.SplashActivity").wait()  # 拉起来

        time.sleep(1)
        d(index=2, className='android.widget.FrameLayout').click()
        d(text='名片夹', className='android.widget.TextView').click()

        if d(text='添加第一张名片', className='android.widget.TextView').exists:
            d(text='添加第一张名片', className='android.widget.TextView').click()
            d(text='从相册选择', className='android.widget.TextView').click()

            time.sleep(1)
            d(index=0, className='android.widget.ImageView').click()
            d(text='确定', className='android.widget.Button').click()
            time.sleep(2)
            d(text='完成', className='android.widget.TextView').click()

            time.sleep(3)
            d(index=1, className='android.widget.RelativeLayout').child(index=1,className='android.widget.ImageView').click()
            while 1:
                self.collectData(args)
        else:
            d(index=1, className='android.widget.RelativeLayout').child(index=1,className='android.widget.ImageView').click()
            while 1:
                self.collectData(args)

        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

    def collectData(self,args,status=True):
        cate_id = args["repo_number_cate_id"]
        collect_count = int(args['collect_count'])  # 要扫描多少人
        count = self.repo.GetNumber(cate_id, 0, collect_count)

        d(text='编辑', className='android.widget.TextView').click()
        d(text='添加手机号', className='android.widget.TextView').click()
        d(text='添加手机号', className='android.widget.TextView').click()
        for i in range(0,len(count)/3 + 1):

            for j in range(0,3):
                if i * 3 + j > len(count)-1:
                    status = False
                    break
                if not d(text='填写号码', className='android.widget.EditText', index=j).exists:
                    d(className='android.widget.RelativeLayout', index=4).child(className='android.widget.EditText', index=j).clear_text()
                    time.sleep(0.5)

                text = count[i * 3 + j]['number']
                print text
                d(text='填写号码', className='android.widget.EditText', index=j).set_text(text)
                time.sleep(0.5)

                if j==2 or i * 3 + j==len(count)-1:
                    d(text='完成', className='android.widget.TextView').click()

            if status==False:
                break

            str = d.info                        # 获取屏幕大小等信息
            height = str["displayHeight"]
            width = str["displayWidth"]
            d.swipe(width / 2, height * 5 / 6, width / 2, height*2/ 4, 10)

            for k in range(0, 3):
                obj1 = d(index=2, className='android.widget.LinearLayout').child(index=k, className='android.widget.RelativeLayout').child(index=2, className='android.widget.TextView')
                if obj1.exists:
                    obj = obj1.info
                    number = obj["text"]
                    para = {"phone": int(number)}
                    self.inventory.postData(para)
                    print '-----------'
                else:
                    break
            print '结束扫描'
            d(text='编辑', className='android.widget.TextView').click()
            time.sleep(0.5)
            for k in range(0, 3):
                obj = d(className='android.widget.RelativeLayout', index=4).child(className='android.widget.EditText',index=k)
                if obj.exists:
                    obj.clear_text()
                    time.sleep(0.5)
                else:
                    break

        d(text='完成', className='android.widget.TextView').click()


def getPluginClass():
    return TIMCardHolderCollectData

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT52ESK00321")
    # material=u'有空聊聊吗'
    z = ZDevice("HT52ESK00321")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_cate_id": "44","collect_count": "12", "time_delay": "3"};  # cate_id是仓库号，length是数量
    o.action(d, z, args)
    # d(className='android.widget.RelativeLayout', index=4).child(className='android.widget.EditText',index=0).clear_text()


