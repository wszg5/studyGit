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
      news_chars = []
      for id in chars:
          if id not in news_chars:
              news_chars.append(id)
      news_chars = news_chars[100:1100]
      return news_chars

const = _const()

const.WAIT_START_TIME=200

const.SERVER_IP = '192.168.1.11'


const.SERVER_IP = '192.168.1.11'

const.RETHINKDB_NAME = 'stf'
const.REPO_API_IP = '192.168.1.11'
const.REDIS_SERVER = '192.168.1.11'
const.MAX_SLOTS_TIM=5
const.MAX_SLOTS_WECHAT=3
const.MAX_SLOTS_MOBILEQQ=3
const.MAX_SLOTS_QQLITE=5
const.MAX_SLOTS_EIM=20
const.MAX_SLOTS_TOKEN=201
const.MAX_SLOTS_TOKEN=2
const.MAX_SLOTS_QQMAIL=30
const.MAX_SLOTS_163MAIL=3
const.MAX_SLOTS_NOW=2
const.MAX_SLOTS_YIXIN=80
const.MAX_SLOTS_QQINTERNATION=3
const.CHINESE_ARRAY = const.loadChinese()