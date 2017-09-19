#coding:utf-8
import os


class _const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass
  def __setattr__(self, name, value):
      if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value

  def loadChinese(self):
      base_dir = os.path.dirname(__file__)
      filename = os.path.join(base_dir, 'libs/chinese.txt')
      allText = open(filename).read()
      chars = list(allText.decode('utf8'))
      print(chars[5])
      news_chars = []
      for id in chars:
          if id not in news_chars:
              news_chars.append(id)
      news_chars = news_chars[100:1100]
      return news_chars

const = _const()

const.WAIT_START_TIME=200
const.SERVER_IP = '192.168.1.11'
const.RETHINKDB_NAME = 'stf'
const.REPO_API_IP = '192.168.1.51'
const.REDIS_SERVER = '192.168.1.11'
const.MAX_SLOTS_TIM=10
const.MAX_SLOTS_WECHAT=20
const.MAX_SLOTS_MOBILEQQ=10
const.MAX_SLOTS_QQLITE=6
const.MAX_SLOTS_EIM=20
const.MAX_SLOTS_TOKEN=201
const.CHINESE_ARRAY = const.loadChinese()