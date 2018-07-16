# coding:utf-8

import hashlib


md5 = hashlib.md5()

md5.update("how to study python".encode("utf-8"))

print md5.hexdigest()