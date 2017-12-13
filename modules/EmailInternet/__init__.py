import re



pattern = re.compile(ur'\bid="ZC.*?" \b')
str = '<div id="ZC4412-X8uJ0acJOdzz1FUPVCPRN7c" un="mail" list="item,<div id=m,<div id="ZC4412-X8uJ0acJOdzz1FUPVCPRN8c" un="mail" list="item,<div id=m,<div id="ZC4412-X8uJ0acJOdzz1FUPVCPRN9c" un="mail" list="item'
print(pattern.search(str).group())

line = '<div id="ZC4412-X8uJ0acJOdzz1FUPVCPRN7c" un="mail" list="item,<div id=m,'

searchObj = re.search( r'\bid="ZC.*?" \b', str, re.M | re.I )


if searchObj:
   print "searchObj.group() : ", searchObj.group()
   print "searchObj.group(1) : ", searchObj.group(1)
   print "searchObj.group(2) : ", searchObj.group(2)
else:
   print "Nothing found!!"


