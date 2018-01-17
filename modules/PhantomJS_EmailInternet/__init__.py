# coding:utf-8
import random
import time
from selenium import webdriver


while True:
    user_agent = "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.resourceTimeout"] = 1000
    cap["phantomjs.page.settings.loadImages"] = True
    cap["phantomjs.page.settings.disk-cache"] = True
    cap["phantomjs.page.settings.userAgent"] = user_agent

    cap["phantomjs.page.customHeaders.User-Agent"] = user_agent
    driver = webdriver.PhantomJS( desired_capabilities=cap,executable_path="/usr/local/phantomjs/bin/phantomjs")
    # driver.close()
    # driver.quit( )
    # 检查是否连接网络
    # driver.get( "https://www.baidu.com/" )
    # if "百度一下" in driver.page_source.encode( "utf-8" ):
    #     print "Internet OK"
    # else:
    #     print "Internet NO"
    #     driver.quit( )
    #     return

        # driver.save_screenshot( "5.png" )
    # QQNumber = "2179298964"
    # QQPassword = "sbkl2225"
    # para = {"x_key": "x_01", "x_value": QQNumber}
    # totalList = Repo( ).GetTIMInfomation( repo_cookies_id, para )
    # if len(totalList)==0:
    #     driver.get( "https://w.mail.qq.com/" )
    # else:
    #     total = None
    #     for i in totalList:
    #         if i["x_01"]==QQNumber:
    #             total = i
    #             break
    #     if not total is None:
    #         geturl = totalList["x02"]
    #         getcookie = totalList["phonenumber"]
    #         driver.get( geturl )
    #         time.sleep(2)
    #         driver.add_cookie(getcookie)
    #         driver.get( geturl )
    #     else:
    #         driver.get( "https://w.mail.qq.com/" )
    # 打开QQ邮箱登陆界面
    driver.get( "http://data.zunyun.net//repo_api/account/statusInfo?cate_id=%s&status=%s&Number=%s&IMEI=%s&cardslot=%s" % ("306","exception","2318461074","","") )
    driver.save_screenshot("ceshi.png")
    try:
        driver.get( url )
        driver.save_screenshot( "ceshi2.png" )
    except:
        pass

    try:
        obj = driver.find_element_by_xpath( "//td[@class='enter_mail_button_td']/a" )
        obj.click( )

    except:
        print "error"

    # driver.save_screenshot( "xxx.png" )
    # # driver.close()
    # # driver.quit()
    #
    # cookie ={'domain': '.mail.qq.com', 'name': 'mpwd', 'expires': '\u5468\u4e09, 10 1\u6708 2018 09:23:39 GMT', 'value': '76B5754E4B5F180625366E729727C115A4084636BACFF7C8264C3BE4A5326BEF@2564855064@4',
    #          'expiry': 1515576219, 'path': '/', 'httponly': False, 'secure': False}
    # driver.add_cookie(cookie)
    # driver.get('https://w.mail.qq.com/cgi-bin/today?sid=BR2GhBFf2joUw1sB0F7TgfMX,4,qYUdGY3g5RWRVQTUtZEV6THQ2cjVxTEdBTnRBVnIwMzVBNmhmR0o0dk1ma18.&first=1&mcookie=disabled' )


    # print  driver.page_source
    # print driver.get_cookies()
    # print driver.current_url
    # print driver.title
    # cap_dict = driver.desired_capabilities
    # for key in cap_dict:
    #     print '%s: %s' % (key, cap_dict[key])

    # obj = driver.find_element_by_id('del_u')

    driver.save_screenshot( "111.png" )
    try:
        driver.find_element_by_id( "u" ).clear( )
    except:
        pass
    try:
        # ///
        driver.find_element_by_id( "u" ).send_keys( "2321398887" )
        driver.find_element_by_id( "p" ).send_keys( "dgus8541" )
        driver.save_screenshot( "222.png" )
        time.sleep( 1 )
        driver.find_element_by_id( "go" ).click( )
        time.sleep(3)
    except:
        pass

    # while True:
    #     try:
    #         driver.find_element_by_id( "go" ).click( )
    #     except:
    #         break

    driver.save_screenshot( "333.png" )

    try:
        obj = driver.find_element_by_class_name( "qm_btnIcon" )
        print "登陆成功"
        url = driver.current_url
    except:
        print "登陆失败"
    print driver.get_cookies()
    driver.delete_all_cookies( )
    print "2:",driver.get_cookies( )
    driver.close()
    driver.quit()

    # http://data.zunyun.net/repo_api/account/statusInfo?cate_id=306&status=exception&Number=2312524255&IMEI=&cardslot=%22