# coding:utf-8


from dbapi import dbapi
from imageCode.client_lianzong import client_lianzong
from imageCode.client_ruokuai import client_ruokuai
from zcache import cache


class imageCode:


    def __init__(self):
        self.platform = dbapi.GetSetting("image_platform")
        if self.platform == 'lianzong':
            self.platform = "lianzong";
        else:
            self.platform = "ruokuai";

        self.username = dbapi.GetSetting("%s_user"%self.platform);
        self.password = dbapi.GetSetting("%s_password" % self.platform);

        if self.username is None or self.password is None:
            if not cache.get("EMPTY_IMAGE_CODE_USER_PASS"):
                cache.set("EMPTY_IMAGE_CODE_USER_PASS", True)
                dbapi.log_error("", "没有设置打码帐号密码","没有设置打码帐号密码")
                return
        if self.platform == 'lianzong':
            self.client = client_lianzong(self.username, self.password)
        else:
            self.client = client_ruokuai(self.username, self.password)
        self.CODE_TYPE_4_NUMBER_CHAR = "4_number_char";




    def getCode(self, image, im_type, timeout=60):
        return self.client.getCode(image, im_type, timeout)


    def reportError(self, id):
        return self.client.reportError(id)


if __name__ == "__main__":
    ic = imageCode( )
    im = open("/home/zunyun/yzm.jpg", 'rb')
    print ic.getCode(im, ic.CODE_TYPE_4_NUMBER_CHAR)
    print ic.reportError("5104838994")
