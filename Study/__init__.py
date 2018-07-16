# coding:utf-8
# l_mem = []
#
# l = l_mem           # the first call
# for i in range(2):
#     l.append(i*i)
#
# print l             # [0, 1]
#
# l_mem2 = [3,2,1]
# l = l_mem2      # the second call
# for i in range(3):
#     l.append(i*i)
#
# print l             # [3, 2, 1, 0, 1, 4]
#
# l = l_mem           # the third call
# for i in range(3):
#     l.append(i*i)
#
# print l             # [0, 1, 0, 1, 4]

# l_mem = 0
#
# l = l_mem           # the first call
# for i in range(3):
#     l = l + i * i
# print  l,l_mem

# def f1(a, b, c=0, *args, **kw):
#     print 'a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw
#
# args = (1, 2, 3, 4,5)
# kw = {'d': 99, 'x': '#'}
# f1(*args, **kw)
#
# it = iter([1, 2, 3, 4, 5])
# while True:
#     try:
#         x = next(it)
#     except StopIteration:
#         break
# def f(x,y,z):
#     return x * y * z
#
# a = reduce(f,[1,2,3,5])
# print a


# def normalize(name):
#     return name[0].upper() + name[1:].lower()
#
# l = ['adam', 'LISA', 'barT']
# a = map(normalize,l)
# print a
#
# def strToFloat(num):
#     numArr = num.split(".")

# def _odd_iter():
#     n = 1
#     while True:
#         n = n + 2
#         yield n
# def _not_divisible(n):
#     y =  lambda x: x % n > 0
#     return y
# def primes():
#     yield 2
#     it = _odd_iter() # 初始序列
#     while True:
#         n = next(it) # 返回序列的第一个数
#         yield n
#         it = filter(_not_divisible(n), it) # 构造新序列
#         print "it:-->",it
# for n in primes():
#     if n < 1000:
#         print(n)
#     else:
#         break


# def primes(n):
#     for i in range(2,n):
#         if n % i ==0:
#             print n, "-->是和数"
#             break
#     else:
#         print n,"-->是质数"
#
#
# primes(93)

# def count():
#     fs = []
#     for i in range(1, 4):
#         def f():
#              return i*i
#         fs.append(f)
#     return fs
#
# f1, f2, f3 = count()
# print f1()

# import tensorflow as tf
#
# a = tf.constant( [1.0, 2.0, 3.0], shape=[3], name='a' )
#
# b = tf.constant( [1.0, 2.0, 3.0], shape=[3], name='b' )
#
# c = a + b
#
# sess = tf.Session( config=tf.ConfigProto( log_device_placement=True ) )
#
# print sess.run( c )

# a  = map(lambda x:x*x,[1,2,3,4])
# print a
# def is_odd(n):
#     return n % 2 == 1
#
# L = list(filter(is_odd, range(1, 20)))
#
#
# a = filter(lambda n:n%2==1,range(1, 20))
# print a
#
# def log(func):
#     def wrapper(*args, **kw):
#         print('call %s():' % func.__name__)
#         return func(*args, **kw)
#     return wrapper
#

# import functools
#
# def log(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kw):
#         print('call %s():' % func.__name__)
#         return func(*args, **kw)
#     return wrapper
# @log
# def now():
#     print('2015-3-25')
# now()


# def foo(x):
#      print locals()
# foo(1)

# def outer(some_func):
#      def inner():
#          print "before some_func"
#          ret = some_func() # 1
#          return ret + 1
#      return inner
# def foo():
#      return 1
# decorated = outer(foo) # 2
# decorated()


# class Coordinate( object ):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def __repr__(self):
#         return "Coord: " + str( self.__dict__ )
#
#
# def add(a, b):
#     return Coordinate( a.x + b.x, a.y + b.y )
#
#
# def sub(a, b):
#     return Coordinate( a.x - b.x, a.y - b.y )
#
#
# one = Coordinate( 100, 200 )
# two = Coordinate( 300, 200 )
# print add( one, two )

# class Student(object):
#
#     @property
#     def scorea(self):
#         return self._score
#
#     @scorea.setter
#     def scorea(self, value):
#         if not isinstance(value, int):
#             raise ValueError('score must be an integer!')
#         if value < 0 or value > 100:
#             raise ValueError('score must between 0 ~ 100!')
#         self._score = value
#
# s = Student()
# s.scoreq = 88
# print s.scoreq
# s.scorea = 455545
# print s.scorea
# from enum import Enum, unique
#
# @unique
# class Weekday(Enum):
#     Sun = 0 # Sun的value被设定为0
#     Mon = 1
#     Tue = 2
#     Wed = 3
#     Thu = 4
#     Fri = 5
#     Sat = 6
#     S = "s"
# day1 = Weekday.Mon
# print day1

class Hello(object):
    def hello(self, name='world'):
        print('Hello, %s.' % name)

