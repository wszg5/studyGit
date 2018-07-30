# coding:utf-8
import os

from selenium import webdriver

options = webdriver.ChromeOptions( )
options.add_argument( 'disable-infobars' )
options.add_argument( 'lang=zh_CN.UTF-8' )
fl = False
# options.add_argument( 'headless' )
# 更换头部
# options.add_argument(user_agent)
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
options.add_argument( 'user-agent="%s' % user_agent )
try:
    driver = webdriver.Chrome( chrome_options=options, executable_path="/opt/google/chrome/chromedriver" )
except:
    if not os.path.exists( "C:\Users\Administrator\AppData\Local\Temp" ):
        os.mkdir( "C:\Users\Administrator\AppData\Local\Temp" )

print "dfs"