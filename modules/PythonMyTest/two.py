#coding=utf-8
import datetime
import re
from zcache import cache


'''
时间判断方法
'''

import logging
#logging.basicConfig(level=logging.INFO)

def timeinterval(self, z, args):
    now = datetime.datetime.now( )
    nowtime = now.strftime( '%Y-%m-%d %H:%M:%S' )  # 将日期转化为字符串 datetime => string
    logging.info( '现在的时间%s' % nowtime )
    gettime = cache.get( 'WXSaveId_time' )
    logging.info( '以前的时间%s' % gettime )
    d1 = datetime.datetime.strptime( nowtime, '%Y-%m-%d %H:%M:%S' )
    if gettime != None:
        d2 = datetime.datetime.strptime( gettime, '%Y-%m-%d %H:%M:%S' )
        delta1 = (d1 - d2)
        # print( delta1 )
        delta = re.findall( r"\d+\.?\d*", str( delta1 ) )  # 将天小时等数字拆开
        day1 = int( delta[0] )
        hours1 = int( delta[1] )
        minutes1 = 0
        if 'days' in str( delta1 ):
            minutes1 = int( delta[2] )
            allminutes = day1 * 24 * 60 + hours1 * 60 + minutes1
        else:
            allminutes = day1 * 60 + hours1  # 当时间不超过天时此时天数变量成为小时变量
        logging.info( "day=%s,hours=%s,minutes=%s" % (day1, hours1, minutes1) )

        logging.info( '两个时间的时间差%s' % allminutes )
        set_time = int( args['set_time'] )  # 得到设定的时间
        if allminutes < set_time:  # 由外界设定
            z.toast( '该模块未满足指定时间间隔,程序结束' )
            return 'end'
        else:
            cache.set( 'WXSaveId_time', nowtime )

    else:
        cache.set( 'WXSaveId_time', nowtime )
