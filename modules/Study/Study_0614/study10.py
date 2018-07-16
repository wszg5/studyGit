# coding:utf-8

import mysql.connector
import MySQLdb
conn = mysql.connector.connect(user="root",password="",host="localhost",database="test",use_unicode=True,port=3306,charset = 'utf8')

cursor = conn.cursor()
cursor.execute('drop table userp')
cursor.execute('create table userp (id varchar(20) primary key, name varchar(20)) ENGINE=InnoDB DEFAULT CHARSET=utf8')
#
cursor.execute('insert into userp (id, name) values (%s, %s)', ['4', 'fdsfs'])

cursor.execute("select * from userp")
result = cursor.fetchall()
print result[0][1].encode("utf-8")

print cursor.rowcount

conn.commit()

cursor.close()


