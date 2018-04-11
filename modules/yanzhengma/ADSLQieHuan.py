# coding:utf-8

from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter  
import sys
import os  
import pytesseract
from pyocr import tesseract
import time

def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        if "jpg" in child:
            jpgList.append(child)

def OutCode(code):
    file=open(SettingFile+"data.txt",'w')
    file.write(code)
    file.close()
    print (code)

# 黑白反色，白色替换  
# 此处N直接为255  
# 小于N的 被替换成黑色  
# 大于等于N的 被替换成白色，255代表白色，0代表黑色
if __name__=='__main__':
    while 1:
        SettingFile="/home/zunyun/dumps/Dump20171103/"
        jpgList=[]
        eachFile(SettingFile)
        for i in jpgList:
            try:
                print "我是ｉ：" + i
                im = Image.open(i)
                im=im.convert('L')#图片转换为灰色图像
                im=im.convert('RGBA')#图片转换成RGBA模式
                pixdata = im.load()
                print im

                for y in range(im.size[1]):
                    for x in range(im.size[0]):
                    #循环图像里的每一个像素。每个像素为一个长度为4的列表。因为图片转换成RGBA模式，所以列表长度为4，A就是透明度
                            if pixdata[x,y][0]>170 and pixdata[x,y][1]>170 and pixdata[x,y][2]>170 and pixdata[x,y][3]>170:
                                pixdata[x,y]=(255, 255, 255, 0)
                            else:  
                                pixdata[x,y]=(0, 0, 0, 0)

                im.save("asa.png")
                #下面code与注释的code实现的功能一样
                code=pytesseract.image_to_string(im)
                # code=tesseract.image_to_string(im)
                OutCode(code)
                os.remove(i)
            except Exception as e:
                code="Unrecognized"
                print e
                OutCode(code)
                os.remove(i)
        time.sleep(5)