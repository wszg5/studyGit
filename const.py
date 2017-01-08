#coding:utf-8

class _const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass

  def __setattr__(self, name, value):
      if name in self.__dict__:
          raise self.ConstError("can't change const %s" % name)
      if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value

const = _const()
const.WAIT_START_TIME=12
const.SERVER_IP = '127.0.0.1'
const.RETHINKDB_NAME = 'stf'

const.REPO_API_IP = '127.0.0.1'

const.MAX_SLOTS_TIM=10

const.MAX_SLOTS_WECHAT=20
const.MAX_SLOTS_MOBILEQQ=10
const.MAX_SLOTS_QQLITE=10
const.MAX_SLOTS_EIM=10
