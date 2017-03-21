# coding:utf-8
import threading
import time
from PIL import Image
from uiautomator import Device
import re,subprocess
from Repo import *
from imageCode import imageCode
import time, datetime, random
from zservice import ZDevice
from slot import slot
import os


class EIMLogin:
    def __init__(self):
        self.type = 'eim'
        self.repo = Repo()
        self.slot = slot(self.type)

    def action(self, d,z, args):
        z.heartbeat()
        cate_id = args["repo_cate_id"]     #仓库号
        time_limit = args['time_limit']      #登录不用eim
        while True:
            slotnum = self.slot.getSlot(d, time_limit)  # 没有空卡槽，取time_limit小时没用过的卡槽
            while slotnum == 0:  # time_limit小时没用过的卡槽为空的情况
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"无间隔时间段未用,等待中\"").communicate()
                z.sleep(30)
                slotnum = self.slot.getSlot(d, time_limit)

            d.server.adb.cmd("shell", "pm clear com.tencent.mobileqq").communicate()  # 清除缓存
            z.set_mobile_data(False)
            z.sleep(3)
            getSerial = self.repo.Getserial(cate_id, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, slotnum))  # 得到之前的串号
            z.heartbeat()
            if len(getSerial) == 0:  # 之前的信息保存失败的话
                d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"获取串号失败\"").communicate()
                continue
            else:
                getSerial = getSerial[0]['imei']  # 如果信息保存成功但串号没保存成功的情况
                print('卡槽切换时的sereial%s' % getSerial)
                if getSerial is None:  # 如果串号为空，重新获取
                   continue
                else:
                    z.generateSerial(getSerial)  # 将串号保存
            z.heartbeat()
            self.slot.restore(d, slotnum,"com.tencent.mobileqq")  # 有２小时没用过的卡槽情况，切换卡槽
            d.server.adb.cmd("shell", "am broadcast -a com.zunyun.zime.toast --es msg \"切换为%s号卡槽\""%slotnum).communicate()

            print("切换为" + str(slotnum))
            z.set_mobile_data(True)
            z.sleep(8)

            d.server.adb.cmd("shell",
                             "am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.SplashActivity").communicate()  # 拉起来
            while d(textContains='正在更新').exists:
                z.sleep(2)
            z.heartbeat()
            z.sleep(10)
            if d(text='搜索', resourceId='com.tencent.mobileqq:id/name').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, slotnum)  # 得到切换后的QQ号
                QQnumber = obj['info']  # info为QQ号
                self.slot.backup(d, slotnum, QQnumber)  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo(cate_id, 'using', QQnumber, getSerial, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, slotnum))  # 仓库号，状态，QQ号，备注设备id_卡槽id
                break
            elif d(textContains='消息').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, slotnum)  # 得到切换后的QQ号
                QQnumber = obj['info']  # info为QQ号
                self.slot.backup(d, slotnum, QQnumber)  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo(cate_id, 'using', QQnumber, getSerial, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, slotnum))  # 仓库号，状态，QQ号，备注设备id_卡槽id
                break
            elif d(text='主题装扮').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, slotnum)  # 得到切换后的QQ号
                QQnumber = obj['info']  # info为QQ号
                self.slot.backup(d, slotnum, QQnumber)  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo(cate_id, 'using', QQnumber, getSerial, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, slotnum))  # 仓库号，状态，QQ号，备注设备id_卡槽id
                break
            elif d(text='启用').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, slotnum)  # 得到切换后的QQ号
                QQnumber = obj['info']  # info为QQ号
                self.slot.backup(d, slotnum, QQnumber)  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo(cate_id, 'using', QQnumber, getSerial, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, slotnum))  # 仓库号，状态，QQ号，备注设备id_卡槽id
                break
            elif d(text='马上绑定').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, slotnum)  # 得到切换后的QQ号
                QQnumber = obj['info']  # info为QQ号
                self.slot.backup(d, slotnum, QQnumber)  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo(cate_id, 'using', QQnumber, getSerial, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, slotnum))  # 仓库号，状态，QQ号，备注设备id_卡槽id
                break
            elif d(text='马上升级').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, slotnum)  # 得到切换后的QQ号
                QQnumber = obj['info']  # info为QQ号
                self.slot.backup(d, slotnum, QQnumber)  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo(cate_id, 'using', QQnumber, getSerial, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, slotnum))  # 仓库号，状态，QQ号，备注设备id_卡槽id
            elif d(text='寻找好友').exists:
                z.heartbeat()
                obj = self.slot.getSlotInfo(d, slotnum)  # 得到切换后的QQ号
                QQnumber = obj['info']  # info为QQ号
                self.slot.backup(d, slotnum, QQnumber)  # 设备信息，卡槽号，QQ号
                self.repo.BackupInfo(cate_id, 'using', QQnumber, getSerial, '%s_%s_%s' % (d.server.adb.device_serial(), self.type, slotnum))  # 仓库号，状态，QQ号，备注设备id_卡槽id
                break
            else:         #切换失败的情况
                continue

        print(QQnumber)
        if (args["time_delay"]):
            z.sleep(int(args["time_delay"]))
def getPluginClass():
    return EIMLogin

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49YSK01576")
    z = ZDevice("HT49YSK01576")
    d.server.adb.cmd("shell", "ime set com.zunyun.qk/.ZImeService").communicate()
    # d.dump(compressed=False)
    # slot = slot('eim')
    # d(resourceId='com.tencent.eim:id/name', className='android.widget.Button').click()
    # slot.restore(d, 2)  # 有２小时没用过的卡槽情况，切换卡槽

    # z.input('gfdc')
    args = {"repo_cate_id":"34","time_limit":"30","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d,z, args)