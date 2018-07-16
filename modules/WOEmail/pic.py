#-*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFont
ttfont = ImageFont.truetype("/home/zunyun/text/font/Wesley__.ttf",20)  #这里我之前使用Arial.ttf时不能打出中文，用华文细黑就可以
im = Image.open("/home/zunyun/text/img/test.png")
import os
import StringIO
import pygame

pygame.init( )

text = u"这是一段测试文本，test 123。"

im = Image.new( "RGB", (300, 50), (255, 255, 255) )
# dr = ImageDraw.Draw(im)
# font = ImageFont.truetype(os.path.join("fonts", "simsun.ttc"), 18)
font = pygame.font.Font( os.path.join( "fonts", "/home/zunyun/text/font/田相岳圆楷体.ttf" ), 18 )

# dr.text((10, 5), text, font=font, fill="#000000")
rtext = font.render( text, True, (0, 70, 90), (255, 123, 66) )

# pygame.image.save(rtext, "t.gif")
sio = StringIO.StringIO( )
pygame.image.save( rtext, sio )
sio.seek( 0 )

line = Image.open( sio )
im.paste( line, (10, 5) )

# im.show( )
im.save( "t.png" )