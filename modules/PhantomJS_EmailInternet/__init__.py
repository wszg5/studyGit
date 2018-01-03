# coding: utf-8

asdlFile = open("/home/zunyun/视频/未命名文件夹/bin/asdl.txt","r")
asdl = asdlFile.readlines()
account = asdl[0][:-1]
password = asdl[1][:-1]
print account,password