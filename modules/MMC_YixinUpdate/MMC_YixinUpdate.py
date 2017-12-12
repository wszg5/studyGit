# coding:utf-8
from __future__ import division
import base64
import logging
import re

from uiautomator import Device
from Repo import *
import os, time, datetime, random
import json

from zcache import cache
from zservice import ZDevice


class MMCYixinUpdate:
    def __init__(self):
        self.repo = Repo()

    def GetUnique(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 1000);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(00) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum



    def action(self, d, z,args):
        z.toast( "准备执行MMS版易信改资料" )
        z.sleep( 1 )
        z.toast( "正在ping网络是否通畅" )
        z.heartbeat( )
        i = 0
        while i < 200:
            i += 1
            ping = d.server.adb.cmd( "shell", "ping -c 3 baidu.com" ).communicate( )
            print( ping )
            if 'icmp_seq' and 'bytes from' and 'time' in ping[0]:
                z.toast( "网络通畅。开始执行：易信改资料" )
                break
            z.sleep( 2 )
        if i > 200:
            z.toast( "网络不通，请检查网络状态" )
            if (args["time_delay"]):
                z.sleep( int( args["time_delay"] ) )
            return
        # self.scode = smsCode( d.server.adb.device_serial( ) )
        z.heartbeat( )
        d.server.adb.cmd( "shell", "am force-stop im.yixin" ).communicate( )  # 强制停止
        d.server.adb.cmd( "shell","am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
        z.sleep( 10 )
        if d(textContains="停止运行").exists:
            if d(text="确定").exists:
                d( text="确定" ).click()
                d.server.adb.cmd( "shell", "am start -n im.yixin/.activity.WelcomeActivity" ).communicate( )  # 拉起来
                z.sleep(5)
        z.heartbeat( )
        if d( text="我", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).exists:
            z.toast( "登录状态正常" )
            d( text="我", resourceId="im.yixin:id/tab_title_label", className="android.widget.TextView" ).click()
        else:
            return
        if d(text="立即体验",resourceId="im.yixin:id/new_presented_resources_experience_btn").exists:
            d( text="立即体验", resourceId="im.yixin:id/new_presented_resources_experience_btn" ).click()
            z.sleep(1)

        str = d.info  # 获取屏幕大小等信息
        height = str["displayHeight"]
        width = str["displayWidth"]
        repo_material_cate_id2 = args["repo_material_cate_id2"]
        repo_material_cate_id = args["repo_material_cate_id"]
        repo_material_cate_id3 = args["repo_material_cate_id3"]
        z.heartbeat()
        if d(index=0,resourceId="im.yixin:id/self_profile").child(index=0,className="android.widget.LinearLayout").child(index=0,resourceId="im.yixin:id/nickname").exists:
            d( index=0, resourceId="im.yixin:id/self_profile" ).child( index=0,
                                                                       className="android.widget.LinearLayout" ).child(
                index=0, resourceId="im.yixin:id/nickname" ).click()
            if d(text="编辑名片",resourceId="im.yixin:id/edit_self_card").exists:
                d( text="编辑名片", resourceId="im.yixin:id/edit_self_card" ).click()
                if d( text="头像", resourceId="im.yixin:id/title_label" ).exists:
                    d( text="头像", resourceId="im.yixin:id/title_label" ).click( )
                    if d(text="从手机相册选择").exists:
                        d( text="从手机相册选择" ).click()
                        z.sleep(3)
                        z.heartbeat()
                        if d(index=0,resourceId="im.yixin:id/picker_image_folder_listView").child(index=0,className="android.widget.LinearLayout").child(index=0,resourceId="im.yixin:id/picker_photofolder_cover").exists:
                            d( index=0, resourceId="im.yixin:id/picker_image_folder_listView" ).child( index=0,
                                                                                                       className="android.widget.LinearLayout" ).child(
                                index=0, resourceId="im.yixin:id/picker_photofolder_cover" ).click()
                            z.sleep(1)
                            if d(index=0,resourceId="im.yixin:id/picker_images_gridview").child(index=0,className="android.widget.FrameLayout").exists:
                                d( index=0, resourceId="im.yixin:id/picker_images_gridview" ).child( index=0,
                                                                                                     className="android.widget.FrameLayout" ).click()
                                z.sleep(1)
                                if d(text="选取",resourceId="im.yixin:id/ok_btn").exists:
                                    d( text="选取", resourceId="im.yixin:id/ok_btn" ).click()
                                    z.sleep(1)
                                    z.heartbeat()
                z.heartbeat()
                if d( text="名字", resourceId="im.yixin:id/title_label" ).exists:
                    d( text="名字", resourceId="im.yixin:id/title_label" ).click( )
                    if d(resourceId="im.yixin:id/self_profile_modify_nick_new_nick",index=0).exists:
                        name = d(resourceId="im.yixin:id/self_profile_modify_nick_new_nick",index=0).info["text"].encode("utf-8")
                        Namelen = len(name)
                        for i in range(0,Namelen):
                            d.press.delete()
                        Material = self.repo.GetMaterial( repo_material_cate_id, 0, 1 )
                        if len( Material ) == 0:
                            d.server.adb.cmd( "shell",
                                              "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % repo_material_cate_id ).communicate( )
                            z.sleep( 10 )
                            return
                        message = Material[0]['content']  # 取出发送消息的内容
                        z.input( message )
                        z.sleep(1)
                        z.heartbeat()
                        if d( text="保存", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).exists:
                            d( text="保存", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).click( )
                z.heartbeat()
                if d( text="性别", resourceId="im.yixin:id/title_label" ).exists:
                    d( text="性别", resourceId="im.yixin:id/title_label" ).click( )
                    if d(text=args["gender"]).exists:
                        d( text=args["gender"] ).click()
                        z.sleep(1)
                        if not d( text="名字", resourceId="im.yixin:id/title_label" ).exists:
                            d.press.back()
                z.heartbeat()
                if d( text="地区", resourceId="im.yixin:id/title_label" ).exists:
                    d( text="地区", resourceId="im.yixin:id/title_label" ).click( )
                    if d(text="自定义",className="android.widget.TextView").exists:
                        d( text="自定义", className="android.widget.TextView" ).click()
                        if d(index=0,resourceId="im.yixin:id/self_profile_modify_region_other").exists:
                            address = d(index=0,resourceId="im.yixin:id/self_profile_modify_region_other").info["text"].encode("utf-8")
                            for i in range(0, len(address)):
                                d.press.delete()
                            Material2 = self.repo.GetMaterial( repo_material_cate_id2, 0, 1 )
                            if len( Material2 ) == 0:
                                d.server.adb.cmd( "shell",
                                                  "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % repo_material_cate_id2 ).communicate( )
                                z.sleep( 10 )
                                return
                            message2 = Material2[0]['content']  # 取出发送消息的内容
                            z.input( message2 )
                            z.sleep( 1 )
                            z.heartbeat( )
                            if d( text="保存", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).exists:
                                d( text="保存", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).click( )
                z.heartbeat()
                if d( text="签名", resourceId="im.yixin:id/title_label" ).exists:
                    d( text="签名", resourceId="im.yixin:id/title_label" ).click( )
                    if d(index=0,resourceId="im.yixin:id/self_profile_modify_signature_new_signature").exists:
                        signature = d(index=0,resourceId="im.yixin:id/self_profile_modify_signature_new_signature").info["text"].encode("utf-8")
                        for i in range( 0, len( signature ) ):
                            d.press.delete( )
                        Material3 = self.repo.GetMaterial( repo_material_cate_id3, 0, 1 )
                        if len( Material3 ) == 0:
                            d.server.adb.cmd( "shell",
                                              "am broadcast -a com.zunyun.zime.toast --es msg \"消息素材%s号仓库为空，等待中……\"" % repo_material_cate_id3 ).communicate( )
                            z.sleep( 10 )
                            return
                        message3 = Material3[0]['content']  # 取出发送消息的内容
                        z.input( message3 )
                        z.sleep( 1 )
                        z.heartbeat( )
                        if d( text="保存", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).exists:
                            d( text="保存", resourceId="im.yixin:id/action_bar_right_clickable_textview" ).click( )

        z.toast( "模块完成" )
        if (args["time_delay"]):
            time.sleep(int(args["time_delay"]))



def getPluginClass():
    return MMCYixinUpdate

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding("utf-8")

    clazz = getPluginClass()
    o = clazz()

    d = Device("d99e4b99")
    z = ZDevice("d99e4b99")

    args = {"time_delay":"3",
            "repo_material_cate_id":"139","gender":"男","repo_material_cate_id2":"139","repo_material_cate_id3":"139"}    #cate_id是仓库号，length是数量
    o.action( d, z, args )
