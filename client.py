if __name__ == '__main__':
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



    #SERVER SH
    sock.connect(('106.15.188.206', 1443))



    #sock.connect(('47.88.62.3', 1443))


    #CLIENT
    #sock.connect(('47.90.97.203', 1443))

    print("connect send")
#
    sock.close()
    print("sock close")

    import time
    time.sleep(2)
    sock.send('1')
    print sock.recv(1024)