# def odd():
#     print('step 1')
#     yield "a"
#     print('step 2')
#     yield "b"
#     print('step 3')
#     yield("5")
#
# o = odd()
# num = 10
# LL = [[1]]
# for i in range(1,num):
#     LL.append([(0 if j== 0 else LL[i-1][j-1])+ (0 if j ==len(LL[i-1]) else LL[i-1][j]) for j in range(i+1)])
#
# # for l in LL:
# #     print l
#
#
# def test():
#     L = [1]
#     # while True:
#         # yield L
#         # L.append( 0 )
#         # L = [L[i - 1] + L[i] for i in range( len( L ) )]
#     L = [1]
#     while True:
#         yield L
#         L = [1] + [x + y for x, y in zip( L[:-1], L[1:] )] + [1]

# t = test()
# for i in range(10):
#     print next(t)
# from collections import Iterator,Iterable
# print isinstance([], Iterable)
# print isinstance([], Iterator)

def test(x):
    if x >2 and x < 4:
        x = x + 3
    elif x>4 and x < 8:
        x = x * x
    else:
        x = 0
