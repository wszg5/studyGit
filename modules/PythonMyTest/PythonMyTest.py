# coding:utf-8



# def my_abs(x):
#     if not isinstance(x, (int, float)):
#         raise TypeError('bad operand type')
#     if x >= 0:
#         return x
#     else:
#         return -x
#
# print(my_abs('A'))

def add_end(L=[]):
    L.append('END')
    return L

print (add_end())
