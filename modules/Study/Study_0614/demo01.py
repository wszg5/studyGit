# coding:utf-8


def h():
    print 'Wen Chuan',
    m = yield 5  # Fighting!
    print m
    d = yield 12
    print 'We are together!'
    yield 3

x = h()
# while True:
#     print "*" * 10
#     try:
#         a = x.next()
#         print 'a = %s' % a
#     except:
#         break

# for a in x:
#     print a
# m = x.next()  #m 获取了yield 5 的参数值 5
x.send(None)
d = x.send('Fighting!')  #d 获取了yield 12 的参数值12
x.next()
# print 'We will never forget the date', m, '.', d