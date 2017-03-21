# coding:utf-8
import json
import mimetypes
import os, stat
import urllib
import urllib2

import requests


class client_lianzong(object):
    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.soft_id = '72358'
        self.soft_key = 'a6b010fff6d247669c4b4bde98673709'
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }
        self.im_type_list = {
            '4_number_char': 1001
        }

    def getCode(self, im, im_type, timeout=60):
        opener = urllib2.build_opener(MultipartPostHandler)
        #temp = tempfile.mkstemp(suffix=".png")
        #os.write(temp[0],im)
        params = { "user_name"      : '%s' % self.username,
                   "user_pw"        : "%s" % self.password ,
                   "yzmtype_mark"   : "%s" % self.im_type_list[im_type] ,
                   "upload"          : im
                 }

        result = opener.open("http://v1-http-api.jsdama.com/api.php?mod=php&act=upload", params).read()
        result = json.loads(result)
        return {"Result": result["data"]["val"], "Id": result["data"]["id"]}


    def reportError(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'user_name': self.username,
            'user_pw': self.password,
            'yzm_id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://v1-http-api.jsdama.com/api.php?mod=php&act=error', data=params, headers=self.headers)
        return r.json()


class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

doseq = 1


class MultipartPostHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order - 10 # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for(key, value) in data.items():
                     if type(value) == file:
                         v_files.append((key, value))
                     else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", traceback

            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if(request.has_header('Content-Type')
                   and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print "Replacing %s with %s" % (request.get_header('content-type'), 'multipart/form-data')
                request.add_unredirected_header('Content-Type', contenttype)

            request.add_data(data)
        return request

    def multipart_encode(vars, files, boundary = None, buffer = None):
        if boundary is None:
            boundary = "--1234567890"
        if buffer is None:
            buffer = ''
        for(key, value) in vars:
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"' % key
            buffer += '\r\n\r\n' + value + '\r\n'
        for(key, fd) in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = fd.name.split('/')[-1]
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename)
            buffer += 'Content-Type: %s\r\n' % contenttype
            fd.seek(0)
            buffer += '\r\n' + fd.read() + '\r\n'
        buffer += '--%s--\r\n\r\n' % boundary
        return boundary, buffer
    multipart_encode = Callable(multipart_encode)
    https_request = http_request

if __name__ == "__main__":
    lz = client_lianzong("power001", "13141314")
    im = open("/home/zunyun/yzm.jpg", 'rb')
    print lz.getCode(im, "4_number_char")
    print lz.reportError("5104838994")