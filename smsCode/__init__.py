# coding:utf-8


from dbapi import dbapi
from smsCode.client_hellotrue import client_hellotrue
from smsCode.client_jyzszp import client_jyzszp
from smsCode.client_xunma import client_xunma
from zcache import cache




class smsCode:


    def __init__(self, serial):
        self.platform = dbapi.GetSetting("sms_platform")
        if self.platform == 'xunma':
            self.platform = "xunma";
        elif self.platform == 'hellotrue':  #爱乐赞
            self.platform = "hellotrue";
        else:
            self.platform = "jyzszp"; #玉米

        self.username = dbapi.GetSetting("%s_user"%self.platform);
        self.password = dbapi.GetSetting("%s_password" % self.platform);

        if self.username is None or self.password is None:
            if not cache.get("EMPTY_SMS_CODE_USER_PASS"):
                cache.set("EMPTY_SMS_CODE_USER_PASS", True)
                dbapi.log_error("", "没有设置接码帐号密码","没有设置接码帐号密码")
                return

        if self.platform == 'xunma':
            self.client = client_xunma(serial, self.username, self.password)
        elif self.platform == 'hellotrue':  #爱乐赞
            self.client = client_hellotrue(serial , self.username, self.password)
        else:
            self.client = client_jyzszp(serial, self.username, self.password) #玉米


        self.WECHAT_REGISTER = "wechat_register";
        self.QQ_CONTACT_BIND = "qq_contact_bind";
        self.QQ_REGISTER = "qq_register";
        self.ALIPAY_REGISTER = "alipay_register";



    def GetPhoneNumber(self, itemId, times=0):
        return self.client.getPhoneNumber(itemId, times)


    def GetVertifyCode(self, number, itemId, length=6):
        return self.client.GetVertifyCode(number, itemId, length)

    def ReleasePhone(self, phoneNumber, itemId):
        return self.client.releasePhone(phoneNumber, itemId)





if __name__ == "__main__":
    ic = smsCode( )
    print ic.getCode(im, ic.CODE_TYPE_4_NUMBER_CHAR)
    print ic.reportError("5104838994")
