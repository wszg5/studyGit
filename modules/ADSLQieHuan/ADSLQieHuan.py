# coding:utf-8
import os

import time

from Repo import Repo


class ADSLQieHuan:
    def __init__(self):
        # a = os.system( "echo 1 | sudo -S poff" )
        # print a
        # b = os.system( "echo 1 | sudo -S pon dsl-provider" )
        # print b
        repo = Repo()
        sds = repo.GetPhantomJSParamInfo()
        sda = repo.GetPhantomJSTaskInfo()
        para = {"phoneNumber": "88888888888", 'x_04': 'NO', 'x_05': 'NO'}
        repo.PostInformation( "302", para )
        print



def getPluginClass():
    return ADSLQieHuan

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    clazz = getPluginClass()
    o = clazz()


