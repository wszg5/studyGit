# coding:utf-8

# from io import StringIO
#
# f = StringIO()
# f.write(u"hello")
# f.write(u" ")
# f.write(u"zhouge!")
#
# print (f.getvalue())
# f.close()
import json
import os
import pickle
# print(os.name)
#
# # print(os.environ)
#
# print(os.path.abspath('.'))
#
# import shutil
# shutil.copyfile("/home/zunyun/text/img/test.png","/home/zunyun/text/img/test01.png")
#
#
# print(os.listdir("."))

# def printDir(path,name=None):
#     if os.path.exists(path):
#         # print( "",os.listdir( path ) )
#         for i in os.listdir( path ):
#             print("文件完整的路径为%s"%os.path.join(path,i))
#             if name:
#                 if name in i.split(".")[0]:
#                     print("包含%s的文件为%s"%(name,i))
#
#     else:
#         print("%s路径不存在"%path)
#
# printDir("/home/zunyun/text/img","test02")
# obj = d = dict(name='Bob', age=20, score=88)
# # with open("/home/zunyun/text/img/test.txt","rb") as f:
# #     # pickle.dump(obj,f)
# #     print(pickle.load(f))
# s = json.dumps(obj, ensure_ascii=False)
# # print(obj)
# print(s)

# print(os.getpid())
# print(os.fork())
import random

from multiprocessing import Process,Pool

import time, threading

# 新线程执行的代码:
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)
