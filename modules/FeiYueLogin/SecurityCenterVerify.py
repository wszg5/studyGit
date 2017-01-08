# coding:utf-8
from uiautomator import Device
from Repo import *
from XunMa import *
import time




class SecurityCenterVerify:
    def __init__(self):
        self.repo = Repo()
        self.XunMa = XunMa()

    def action(self, d, args):
        d.server.adb.cmd("shell", "pm clear com.tencent.tokenntxu").wait()  # 清除缓存
        d.server.adb.cmd("shell","am start -n com.tencent.tokenntxu/com.tencent.tokenntxu.ui.LogoActivity").wait()  # 拉起来
        time.sleep(3)
        d(resourceId='com.tencent.tokenntxu:id/account_bind_qqface',index=0).click()
        d(resourceId='com.tencent.tokenntxu:id/account_bind_qqface_center', index=0, className='android.widget.ImageView').click()
        d(resourceId='com.tencent.tokenntxu:id/wtlogin_with_account_psw',text='账号密码登录').click()




def getPluginClass():
    return SecurityCenterVerify

if __name__ == "__main__":
    clazz = getPluginClass()
    o = clazz()
    d = Device("HT49XSK01883")
    args = {"repo_cate_id":"131","length":"50","time_delay":"3"};    #cate_id是仓库号，length是数量
    o.action(d, args)
