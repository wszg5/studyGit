# coding:utf-8
from uiautomator import Device
from Repo import *
import os, time, datetime, random




class NearbyAddFriends:
    def __init__(self):

        self.repo = Repo()

    def action(self, d, args):
        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").wait()
        # 将微信拉起来
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").wait()
        for i in range(50, 110):
            time.sleep(1)
            print 'not exist'
            if d(text='发现', resourceId='com.tencent.mm:id/ble').exists:
                print 'exist'
                time.sleep(5)
                # d(clickable='true', index=2, className='android.widget.RelativeLayout').click()
                d(text='发现', resourceId='com.tencent.mm:id/ble').click()
                time.sleep(2)
                d(text='附近的人', resourceId='android:id/title').click()
                break

        time.sleep(1)
        if d(text='下次不提示', className='android.widget.CheckBox').exists:
            d(text='下次不提示', className='android.widget.CheckBox').click()
            d(text='确定', className='android.widget.Button').click()
        #添加附近的人
        time.sleep(3)
        str = d.info
        height = str["displayHeight"]
        width = str["displayWidth"]
        t = 0
        for i in range(1, 15):
            print i
            time.sleep(2)

            if d(resourceId='com.tencent.mm:id/bq2', index=0).child(className='android.widget.LinearLayout',clickable='true', index=i-t).exists:
                d(resourceId='com.tencent.mm:id/bq2', index=0).child(className='android.widget.LinearLayout',clickable='true', index=i - t).click()
                time.sleep(2)
                if (d(description='女', resourceId='com.tencent.mm:id/abd').exists):
                    d(text='打招呼', resourceId='com.tencent.mm:id/ab0').click()
                    d(resourceId='com.tencent.mm:id/c4i', index=1).set_text('c85965263')
                    d(resourceId='com.tencent.mm:id/g9', text='发送').click()
                    time.sleep(1)
                    d(description='返回', resourceId='com.tencent.mm:id/gq').click()
                    print '男'
                else:
                    print '返回'
                    d(description='返回', resourceId='com.tencent.mm:id/gq').click()
                    continue

            else:
                t += i
                d.swipe(width / 2, height * 3 / 5, width / 2, height / 5)
                d.swipe(width / 2, height * 3 / 5, width / 2, height / 5)
                # EndIndex = EndIndex-i
                i = 0
                continue

def getPluginClass():
    return NearbyAddFriends

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49XSK01883")
    d.dump(compressed=False)
    args = {"repo_number_cate_id": "13", "repo_material_cate_id": "8", "gender": "女", "add_count": "9","time_delay": "3"}  # cate_id是仓库号，发中文问题
    o.action(d, args)