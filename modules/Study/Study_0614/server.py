# coding:utf-8

from hello import application

from wsgiref.simple_server import make_server

httpd = make_server("",8000,application)

print('Serving HTTP on port 8000...')

httpd.serve_forever()