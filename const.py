#coding:utf-8
class _const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass
  def __setattr__(self, name, value):
      if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value
const = _const()

const.WAIT_START_TIME=200
const.SERVER_IP = '127.0.0.1'
const.RETHINKDB_NAME = 'stf'
const.REPO_API_IP = '127.0.0.1'
const.REDIS_SERVER = '127.0.0.1'
const.MAX_SLOTS_TIM=50
const.MAX_SLOTS_WECHAT=20
const.MAX_SLOTS_MOBILEQQ=50
const.MAX_SLOTS_QQLITE=50
const.MAX_SLOTS_EIM=50
