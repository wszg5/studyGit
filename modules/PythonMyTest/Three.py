#coding:utf-8
import os

from multiprocessing import Process

'''
from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')


    def run_proc(name):
    print('Run child process %s(%s)...'%(name,os.getpid()))

if __name__=='__main__':
    print('parents process %s.'%os.getpid())
    p = Process(target=run_proc,args=('text',))
    print('child process will start.')
    p.start( )
    p.join( )
    print( 'Child process end.' )
'''



a = 1
m = a.__add__( 2 )
print( m )