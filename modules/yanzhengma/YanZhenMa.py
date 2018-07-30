# coding:utf-8
import ImageEnhance
from PIL import Image
import PIL.ImageOps
from pytesseract import pytesseract


def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


if __name__ == "__main__":
    im = Image.open('qwq.png')

    # # 图片的处理过程
    # im = im.convert('L')
    # binaryImage = im.point(initTable(), '1')
    # im1 = binaryImage.convert('L')
    # im2 = PIL.ImageOps.invert(im1)
    #
    # # 图像二值化
    # im3 = im2.convert('1')
    # im4 = im3.convert('L')
    #
    # enhancer = ImageEnhance.Contrast( im4 )
    # im4 = enhancer.enhance( 4 )
    #
    #
    # # 将图片中字符裁剪保留
    # box = (5, 5, 105, 42)
    # region = im4.crop(box)
    #
    # # 将图片字符放大
    # out = region.resize((120, 38))
    # asd = pytesseract.image_to_string(out)
    # print asd
    # print (out.show())




    enhancer = ImageEnhance.Contrast( im )
    im = enhancer.enhance( 2 )
    im = im.convert( '1' )
    data = im.getdata( )
    w, h = im.size

    black_point = 0
    for x in xrange( 1, w - 1 ):
        for y in xrange( 1, h - 1 ):
            mid_pixel = data[w * y + x]  # 中央像素点像素值
            if mid_pixel == 0:  # 找出上下左右四个方向像素点像素值
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]

                # 判断上下左右的黑色像素点总个数
                if top_pixel == 0:
                    black_point += 1
                if left_pixel == 0:
                    black_point += 1
                if down_pixel == 0:
                    black_point += 1
                if right_pixel == 0:
                    black_point += 1
                if black_point >= 3:
                    im.putpixel( (x, y), 0 )

                black_point = 0
    im.show( )
    im.save( 'show49.png' )




