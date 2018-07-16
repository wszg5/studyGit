# coding: utf-8
# import win32ras
import time, os

class IPChange:
    def __init__(self):
        pass

    def Connect(self,dialname, account, passwd):
        dial_params = (dialname, '', '', account, passwd, '')
        return win32ras.Dial(None, None, dial_params, None)

    def DialBroadband(self):
        dialname = '宽带连接'  # just a name
        asdlFile = open( r"c:\asdl.txt", "r" )
        asdl = asdlFile.readlines( )
        account = asdl[0][:-1]
        passwd = asdl[1][:-1]

        try:
            # handle is a pid, for disconnect or showipadrress, if connect success return 0.
            # account is the username that your ISP supposed, passwd is the password.
            handle, result =self.Connect(dialname, account, passwd)
            if result == 0:
                print "Connection success!"
                return handle, result
            else:
                print "Connection failed, wait for 5 seconds and try again..."
                time.sleep(5)
                self.DialBroadband()
        except:
            print "Can't finish this connection, please check out."
            return

    def Disconnect(self,handle):
        if handle != None:
            try:
                win32ras.HangUp(handle)
                print "Disconnection success!"
                return "success"
            except:
                print "Disconnection failed, wait for 5 seconds and try again..."
                time.sleep(5)
                self.Disconnect(handle)
        else:
            print "Can't find the process!"
            return

    def Check_for_Broadband(self):
        connections = []
        connections = win32ras.EnumConnections()
        if (len(connections) == 0):
            print "The system is not running any broadband connection."
            return
        else:
            print "The system is running %d broadband connection." % len(connections)
            return connections

    def ShowIpAddress(self,handle):
        print win32ras.GetConnectStatus(handle)
        data = os.popen("ipconfig", "r").readlines()
        have_ppp = 0
        ip_str = None
        for line in data:
            if line.find("宽带连接") >= 0:
                have_ppp = 1
            # if your system language is English, you should write like this:
            # if have_ppp and line.strip().startswith("IP Address"):
            # in othewords, replace the "IPv4 地址" to "IP Address"
            if have_ppp and line.strip().startswith("IPv4 地址"):
                ip_str = line.split(":")[1].strip()
                have_ppp = 0
                print ip_str

    # get my ipaddress anf disconnect broadband connection.
    def ooo(self):
        data = self.Check_for_Broadband()
        # if exist running broadband connection, disconnected it.
        if data != None:
            for p in data:
                self.ShowIpAddress(p[0])
                if (self.Disconnect(p[0]) == "success"):
                    print "%s has been disconnected." % p[1]
                time.sleep(3)
        else:
            pid, res = self.DialBroadband()
            self.ShowIpAddress(pid)
            time.sleep(3)
            self.Disconnect(pid)
        return "finsh test"


def getPluginClass():
    return IPChange

if __name__ == "__main__":
    # global args

    import sys

    reload(sys)
    sys.setdefaultencoding( 'utf-8' )

    clazz = getPluginClass()
    o = clazz()
    o.ooo()

