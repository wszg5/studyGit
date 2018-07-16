# coding:utf-8
import httplib
import json


def GetNumber(cateId, interval, limit, status='normal', statusLock='YES', number=None, name=None):
    path = "/repo_api/number/pick?status=%s&cate_id=%s&interval=%s&limit=%s&statusLock=%s&number=%s&name=%s" % (
        status, cateId, interval, limit, statusLock, number, name)
    conn = httplib.HTTPConnection( "192.168.1.51", 8686, timeout=30 )
    conn.request( "GET", path )
    response = conn.getresponse( )
    if response.status == 200:
        data = response.read( )
        numbers = json.loads( data )
        return numbers
    else:
        return []

while True:
    try:
        x = GetNumber("46",0,"1")
        print "woshihanma%s"%x[0]["number"]
    except Exception,e:
        print e