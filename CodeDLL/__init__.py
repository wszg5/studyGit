# coding:utf-8
import os
from ctypes import *


class codeDLL:

    def __init__(self):
        base_dir = os.path.abspath( os.path.join( os.path.dirname( __file__ ), os.path.pardir, "CodeDLL" ) )
        self.TYDLLPath = base_dir + '/TYDLL/OCR.dll'
        self.QQDLLPath = base_dir + '/QQDLL/OCR.dll'

    def QQPlayCode(self, image):  # 0代表天涯，1代表ＱＱ

        data = image.read()
        path = self.QQDLLPath
        dll = windll.LoadLibrary(path)
        ret = dll.OCR_PY(data, len(data))
        ocrVal= c_char_p(ret)
        ocrCode = str(ocrVal.value)
        print(ocrVal)
        return ocrCode

    def TYPlayCode(self):  # 0代表天涯，1代表ＱＱ

        with open('04pX1Cno.png', 'rb') as f:
            data = f.read()

        path = self.TYDLLPath
        dll = windll.LoadLibrary(path)
        ret = dll.OCR_PY(data, len(data))
        ocrVal= c_char_p(ret)
        ocrCode = str(ocrVal.value, encoding="utf-8")
        print(ocrVal)






if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
