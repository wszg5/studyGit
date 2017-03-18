# coding:utf-8
from uiautomator import Device
from Repo import *
import time
from zservice import ZDevice


class TIMTempoAdviceAddFriends:
    def __init__(self):

        self.repo = Repo()


    def action(self, d, z, args):
        add_count = int(args['add_count'])  # 要添加多少人
        repo_number_cate_id = int(args["repo_number_id"])  # 得到取号码的仓库号
        numbers = self.repo.GetNumber(repo_number_cate_id, 0, add_count)  # 取出totalNumber条两小时内没有用过的号码
        print(len(numbers))
        if len(numbers) == 0:
            d.server.adb.cmd("shell",
                             "am broadcast -a com.zunyun.zime.toast --es msg \"QQ号码%s号仓库为空，等待中\"" % repo_number_cate_id).communicate()
            return
        list = numbers  # 将取出的号码保存到一个新的集合

        for i in range(0, add_count, +1):  # 总人数
            repo_material_cate_id = args["repo_material_cate_id"]
            Material = self.repo.GetMaterial(repo_material_cate_id, 0, 1)
            if len(Material) == 0:
                d.server.adb.cmd("shell","am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，没有取到消息\"" % repo_material_cate_id).communicate()
                return
            material = Material[0]['content']

            qq = list[i]

            d.server.adb.cmd("shell", 'am start -a android.intent.action.VIEW -d "mqqwpa://im/chat?chat_type=wpa\&uin=%s\&version=1\&src_type=web\&web_src=http:://114.qq.com"'%qq)   #咨询会话
            time.sleep(1)
            while d(text='TIM', className='android.widget.TextView').exists:
                d(text='TIM', className='android.widget.TextView').click()
                time.sleep(0.5)
                if d(text='仅此一次', className='android.widget.Button').exists:
                    d(text='仅此一次', className='android.widget.Button').click()

            time.sleep(1)
            d(text='加为好友', className='android.widget.TextView').click()
            time.sleep(2)
            if d(text='加为好友', className='android.widget.TextView', index=2).exists:  # 拒绝被添加好友的情况
                continue
            if d(text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText').exists:  # 可直接添加为好友的情况
                d(text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
                if d(resourceId='com.tencent.tim:id/name', text='添加失败，请勿频繁操作').exists:  # 操作过于频繁的情况
                    return
                continue
            if d(text='必填', resourceId='com.tencent.tim:id/name').exists:  # 需要验证时
                continue
            obj = d(resourceId='com.tencent.tim:id/name', index='3').info
            print(obj)
            obj = obj['text']
            length = len(obj)
            k = 0
            while k < length:
                length = length - 1
                d.press.delete()
            time.sleep(2)
            d(resourceId='com.tencent.tim:id/name', className='android.widget.EditText').click()  # 要发的消息
            z.input(material)
            d(text='下一步', resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
            d(text='发送', resourceId='com.tencent.tim:id/ivTitleBtnRightText').click()
            time.sleep(1)
            if d(resourceId='com.tencent.tim:id/name', text='添加失败，请勿频繁操作').exists:  # 操作过于频繁的情况
                return


        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))


def getPluginClass():
    return TIMTempoAdviceAddFriends

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()
    d = Device("HT529SK00384")
    # material=u'有空聊聊吗'
    z = ZDevice("HT529SK00384")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").wait()
    # d(resourceId='com.tencent.tim:id/name', className='android.widget.EditText').click()  # 要发的消息
    # z.input('豆腐坊')

    args = {"repo_number_cate_id": "43", "repo_material_cate_id": "36", "add_count": "9",
            "time_delay": "3"};  # cate_id是仓库号，length是数量
    o.action(d, z, args)