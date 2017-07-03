# coding:utf-8


from dbapi import dbapi
from smsCode.client_hellotrue import client_hellotrue
from smsCode.client_xunma import client_xunma
from smsCode.client_jyzszp import client_jyzszp
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

        self.WECHAT_REGISTER = "wechat_register";
        self.QQ_CONTACT_BIND = "qq_contact_bind";
        self.QQ_REGISTER = "qq_register";
        self.QQ_TOKEN_BIND = "qq_token_bind";
        self.ALIPAY_REGISTER = "alipay_register";

        self.im_type_list={}
        self.im_type_list[self.WECHAT_REGISTER] = dbapi.GetSetting("%s_%s" % (self.platform,self.WECHAT_REGISTER));
        self.im_type_list[self.QQ_CONTACT_BIND] = dbapi.GetSetting("%s_%s" % (self.platform,self.QQ_CONTACT_BIND));
        self.im_type_list[self.QQ_REGISTER] = dbapi.GetSetting("%s_%s" % (self.platform,self.QQ_REGISTER));
        self.im_type_list[self.QQ_TOKEN_BIND] = dbapi.GetSetting("%s_%s" % (self.platform,self.QQ_TOKEN_BIND));
        self.im_type_list[self.ALIPAY_REGISTER] = dbapi.GetSetting("%s_%s" % (self.platform,self.ALIPAY_REGISTER));


        if self.platform == 'xunma':
            self.client = client_xunma(serial, self.username, self.password,self.im_type_list)
        elif self.platform == 'hellotrue':  #爱乐赞
            self.client = client_hellotrue(serial , self.username, self.password,self.im_type_list)
        else:
            self.client = client_jyzszp(serial, self.username, self.password,self.im_type_list) #玉米



    def GetPhoneNumber(self, itemId, phone=None, times=0):
        return self.client.GetPhoneNumber(itemId, phone, times)


    def GetVertifyCode(self, number, itemId, length=6):
        code = self.client.GetVertifyCode(number, itemId, int(length))
<<<<<<< HEAD
        if code == '':
            self.ReleasePhone(number, itemId)
=======
        #self.ReleasePhone(number, itemId)
>>>>>>> 5c4fae4c0fc124b9d07f40f29738e912357dafdc
        return code

    def ReleasePhone(self, phoneNumber, itemId):
        return self.client.ReleasePhone(phoneNumber, itemId)

    def defriendPhoneNumber(self, phoneNumber, itemId):
        return self.client.defriendPhoneNumber(phoneNumber,itemId)



if __name__ == "__main__":
    ic = smsCode( )
    #print ic.getCode(im, ic.CODE_TYPE_4_NUMBER_CHAR)
    #print ic.reportError("5104838994")
