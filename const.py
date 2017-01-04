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
const.SERVER_IP = '192.168.1.33'
const.RETHINKDB_NAME = 'stf'
const.REPO_API_IP = '192.168.1.33'
const.MAX_SLOTS=60