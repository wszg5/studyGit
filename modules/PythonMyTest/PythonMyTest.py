# import urllib
# def callbackfunc(blocknum, blocksize, totalsize):
#     '''回调函数
#     @blocknum: 已经下载的数据块
#     @blocksize: 数据块的大小
#     @totalsize: 远程文件的大小
#     '''
#     percent = 100.0 * blocknum * blocksize / totalsize
#     if percent > 100:
#         percent = 100
#     print ("%.2f%%"% percent)
#
# url = 'http://www.sina.com.cn'
# local = '/home/geeklee/1.html'
# urllib.urlretrieve(url, local, callbackfunc)

# coding=utf-8
import requests
import urllib2
import os

from lxml import etree
html = requests.get("http://cl.d5j.biz/htm_mob/7/1612/2172569.html")
html.encoding = 'utf-8'
selector = etree.HTML(html.text)
content = selector.xpath('//table//img/@src')
for imgurl in content:
    name = imgurl[-9:];
    os.chdir(r"D:")
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
        'Cookie': 'AspxAutoDetectCookieSupport=1',
    }
    request = urllib2.Request(imgurl, None, header)  #刻意增加头部header，否则本行与下一行可以写为：response = urllib2.urlopen(imgurl)
    response = urllib2.urlopen(request)
    f = open(name , 'wb')
    f.write(response.read())
    f.close()
    print(imgurl)