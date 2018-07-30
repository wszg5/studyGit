# coding:utf-8
import httplib
import json
import urllib
import requests
data = {"QQNumber": "2354646","cardslot": "jksdc"}
path = "/test"
# conn = httplib.HTTPConnection( "127.0.0.1", "5000", timeout=30 )
# params = urllib.urlencode( data )
# conn.request( method="POST", url=path, body=params )
# response = conn.getresponse( )
# if response.status == 200:
#     data = response.read( )
#     numbers = json.loads( data )
# else:
#     print "fdsfcs"
with open("/home/zunyun/wz/pic/test.jpg","rb") as f:
    content = f.read()
files = {"img":content}
r = requests.post("http://127.0.0.1:5000/test",files=files)
print r.status_code
print r.text
