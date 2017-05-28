from PIL import Image
'''
class Student(object):

    def get_score(self):
         return self._score

    def set_score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value

    对属性进行封装

    Python内置的@property装饰器就是负责把一个方法变成属性调用的

    MixIn
    在设计类的继承关系时，通常，主线都是单一继承下来的，例如，Ostrich(鸵鸟)继承自Bird。但是，如果需要“混入”额外的功能，通过多重继承就可以实现，比如，让Ostrich除了继承自Bird外，再同时继承Runnable。这种设计通常称之为MixIn。

    于Python允许使用多重继承，因此，MixIn就是一种常见的设计。
    只允许单一继承的语言（如Java）不能使用MixIn的设计。



























'''
class Sreen:
    @property
    def width(self):
        return self.width
    @width.setter
    def width(self,width):
        self.width=width
    @property
    def height(self):
        return self.height
    @height.setter
    def height(self,h):
        self.height=h
    def resolution(self):
        return self.width*self.height



s = Sreen()
s.height = 4
s.width = 5
print s.resolution()











