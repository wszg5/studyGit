# coding:utf-8
import os

import time
import sys
sys.path.append("/home/zunyun/workspace/TaskConsole")
from Repo import Repo


class ADSLQieHuan:
    def __init__(self):
     self.repo = Repo()

    def test(self):
        while True:
            numbers = self.repo.GetAccount("391", 0, 1)
            print u"woshihaoma: %s" % numbers[0]["number"]
            if len(numbers) == 0:
                break




def getPluginClass():
    return ADSLQieHuan

if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    clazz = getPluginClass()
    o = clazz()
    o.test()



