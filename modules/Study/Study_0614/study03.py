# coding:utf-8

import re

string = "sasafds12493-aFSLdfd_!#5"

#目标：匹配出  12493-aFSLdfd

result = re.match(r"([a-z]{7}\d{5})(\-)([0-9a-zA-Z\_]*)",string)

# print re.match(r'^(\d+?)(0*)$', '102300').groups()
# print(result.group(2))

# print 'a b   c'.split(' ')
#
# print re.split("[\+\s\,]+",'a+,+ b  + ,c')

# a = re.compile("([a-z]{7}\d{5})(\-)([0-9a-zA-Z\_]*)")
# print a.match(string).groups()

def is_valid_email(address):
    if re.match(r'^[0-9a-zA-Z_.]+@[a-z]+.com$', address):
        return "匹配成功"
    else:
        return "匹配失败"

print(is_valid_email("someone@gmail.com"))
print(is_valid_email('bill.gates@microsoft.com'))
print(is_valid_email('bob#example.com'))
print(is_valid_email('mr-bob@example.com'))

