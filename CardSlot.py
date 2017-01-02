# coding:utf-8
import httplib, json
from uiautomator import Device
class CardSlot:

    def backup(self, d, name):        #备份当前卡槽
        d.server.adb.cmd("shell", "su -c 'chmod -R 777 /data/data/com.tencent.tim/'").wait()
        d.server.adb.cmd("shell", "su -c 'mkdir /data/data/com.zy.bak/'").wait()
        d.server.adb.cmd("shell", "su -c 'chmod -R 777 /data/data/com.zy.bak/'").wait()
        d.server.adb.cmd("shell", "mkdir /data/data/com.zy.bak/tim").wait()
        d.server.adb.cmd("shell", "rm -r -f /data/data/com.zy.bak/tim/%s/" % name).wait()
        d.server.adb.cmd("shell", "rm -r -f  /data/data/com.zy.bak/tim/zy_name_*").wait()

        d.server.adb.cmd("shell", "mkdir /data/data/com.zy.bak/tim/%s" % name).wait()
        d.server.adb.cmd("shell",
                         "cp -r -f -p /data/data/com.tencent.tim/databases/  /data/data/com.zy.bak/tim/%s/" % name).wait()
        d.server.adb.cmd("shell",
                         "cp -r -f -p /data/data/com.tencent.tim/shared_prefs/  /data/data/com.zy.bak/tim/%s/" % name).wait()
        d.server.adb.cmd("shell",
                         "cp -r -f -p /data/data/com.tencent.tim/txlib/  /data/data/com.zy.bak/tim/%s/" % name).wait()
        # d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/jpeglib/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        # d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/mailsdklib/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        d.server.adb.cmd("shell",
                         "cp -r -f -p /data/data/com.tencent.tim/files/  /data/data/com.zy.bak/tim/%s/" % name).wait()
        # d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/app_webview/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        # d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/app_systemface/  /data/data/com.zy.bak/tim/%s/"%name).wait()
        # d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.tencent.tim/app_profilecard/  /data/data/com.zy.bak/tim/%s/"%name).wait()

        d.server.adb.cmd("shell", "mkdir /data/data/com.zy.bak/tim/zy_name_%s_name/" % name).wait()


    def restore(self, d, name):     #导出卡槽
        # d.server.adb.cmd("shell", "am force-stop com.tencent.tim").wait()
        d.server.adb.cmd("shell", "pm clear com.tencent.tim").wait()
        d.server.adb.cmd("shell", "rm -r -f  /data/data/com.zy.bak/tim/zy_name_*").wait()

        d.server.adb.cmd("shell",
                         "cp -r -f -p /data/data/com.zy.bak/tim/%s/databases/ /data/data/com.tencent.tim/" % name).wait()
        d.server.adb.cmd("shell",
                         "cp -r -f -p /data/data/com.zy.bak/tim/%s/shared_prefs/ /data/data/com.tencent.tim/" % name).wait()
        d.server.adb.cmd("shell",
                         "cp -r -f -p /data/data/com.zy.bak/tim/%s/txlib/ /data/data/com.tencent.tim/" % name).wait()
        # d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/jpeglib/ /data/data/com.tencent.tim/"%name).wait()
        # d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/mailsdklib/ /data/data/com.tencent.tim/"%name).wait()
        d.server.adb.cmd("shell",
                         "cp -r -f -p /data/data/com.zy.bak/tim/%s/files/ /data/data/com.tencent.tim/" % name).wait()
        # d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/app_webview/ /data/data/com.tencent.tim/"%name).wait()
        # d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/app_systemface/ /data/data/com.tencent.tim/"%name).wait()
        # d.server.adb.cmd("shell", "cp -r -f -p /data/data/com.zy.bak/tim/%s/app_profilecard/ /data/data/com.tencent.tim/"%name).wait()

        d.server.adb.cmd("shell", "mkdir /data/data/com.zy.bak/tim/zy_name_%s_name/" % name).wait()


if __name__ == '__main__':
    cardsolt = CardSlot()
    d = Device("HT4A3SK00853")
    # cardsolt.backup(d,2)
    cardsolt.restore(d,2)