# coding:utf-8
from uiautomator import Device
from Repo import *
import time, datetime, random
from zservice import ZDevice
from Inventory import *

class WeiXinAddFriends:

    def __init__(self):
        self.repo = Repo()


    def action(self, d,z, args):

        d.server.adb.cmd("shell", "am force-stop com.tencent.mm").communicate()  # 将微信强制停止
        d.server.adb.cmd("shell", "am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI").communicate()  # 将微信拉起来
        time.sleep(7)

        d(description='更多功能按钮',className='android.widget.RelativeLayout').click()
        time.sleep(1)
        if d(text='添加朋友').exists:
            d(text='添加朋友').click()
        else:
            d(description='更多功能按钮', className='android.widget.RelativeLayout').click()
            time.sleep(1)
            d(text='添加朋友').click()
        d(index='1',className='android.widget.TextView').click()   #点击搜索好友的输入框

        add_count = int(args['add_count'])
        account = 0
        while True:
            if account<add_count:
                cate_id = int(args["repo_number_cate_id"])  # 得到取号码的仓库号
                numbers = self.repo.GetNumber(cate_id, 120, 1)  # 取出add_count条两小时内没有用过的号码
                if len(numbers) == 0:
                    d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"第%s号号码仓库为空，等待中……\"" % cate_id).communicate()
                    time.sleep(20)
                    return
                WXnumber = numbers[0]['number']
                z.input(WXnumber)
                d(textContains='搜索:').click()
                while d(textContains='正在查找').exists:
                    time.sleep(2)
                if d(textContains='操作过于频繁').exists:
                    return
                time.sleep(1)
                if d(textContains='用户不存在').exists:
                    d(descriptionContains='清除',index=2).click()
                    time.sleep(1)
                    continue
                if d(textContains='状态异常').exists:
                    d(descriptionContains='清除', index=2).click()
                    continue

                Gender = d(className='android.widget.LinearLayout', index=1).child(
                    className='android.widget.LinearLayout').child(className='android.widget.ImageView',index=1)  # 看性别是否有显示
                if Gender.exists:
                    Gender = Gender.info
                    Gender = Gender['contentDescription']
                else:
                    Gender = '空'

                nickname = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',
                                                                        index=1) \
                    .child(className='android.widget.LinearLayout', index=1).child(className='android.widget.TextView')
                if nickname.exists:
                    nickname = nickname.info['text']
                else:
                    nickname = '空'
                if d(text='地区').exists:
                    for k in range(3, 10):
                        if d(className='android.widget.ListView').child(className='android.widget.LinearLayout',
                                                                        index=k).child(
                                className='android.widget.LinearLayout', index=0).child(text='地区').exists:
                            break
                    area = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',
                                                                        index=k).child(
                        className='android.widget.LinearLayout', index=0). \
                        child(className='android.widget.LinearLayout', index=1).child(
                        className='android.widget.TextView').info['text']
                else:
                    area = '空'

                if d(text='个性签名').exists:
                    for k in range(3, 10):
                        if d(className='android.widget.ListView').child(className='android.widget.LinearLayout',
                                                                        index=k).child(
                                className='android.widget.LinearLayout', index=0).child(text='个性签名').exists:
                            break
                    sign = d(className='android.widget.ListView').child(className='android.widget.LinearLayout',
                                                                        index=k).child(
                        className='android.widget.LinearLayout', index=0). \
                        child(className='android.widget.LinearLayout', index=1).child(
                        className='android.widget.TextView').info['text']
                else:
                    sign = '空'

                para = {"phone": WXnumber, 'qq_nickname': nickname, 'sex': Gender, "city": area, "x_01": sign}
                print('--%s--%s--%s--%s--%s'%(WXnumber,nickname,Gender,area,sign))

                inventory = Inventory()
                con = inventory.postData(para)
                print(con)
                # if con != True:
                #     d.server.adb.cmd("shell",
                #                      "am broadcast -a com.zunyun.zime.toast --es msg \"消息保存失败……\"").communicate()
                #     time.sleep(10)
                #     return
                d(descriptionContains='返回').click()
                d(descriptionContains='清除').click()
                time.sleep(1)
                account = account+1
                continue
            else:
                break
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))

def getPluginClass():
    return WeiXinAddFriends

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT4A4SK00901")
    z = ZDevice("HT4A4SK00901")
    z.server.install()
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    args = {"repo_number_cate_id": "44", "add_count": "5", "time_delay": "3"}    #cate_id是仓库号，length是数量
    o.action(d,z, args)






















