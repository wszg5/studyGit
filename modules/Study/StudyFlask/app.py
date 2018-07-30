# coding:utf-8
from ctypes import windll,c_char_p

import time
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username=='admin' and password=='password':
        return render_template('signin-ok.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)

@app.route('/test', methods=['POST'])
def test():
    data = request.files['img']
    path2 = ""
    # with open( path2, 'rb' ) as f:
    #     data = f.read( )
    try:
        dll = windll.LoadLibrary( r'/home/zunyun/wz/OCR.dll' )
    except Exception as e:
        print e
    time.sleep( 3 )
    ret = dll.OCR( data, len( data ) )
    time.sleep( 3 )
    ocrVal = c_char_p( ret )
    time.sleep( 2 )
    ocrCode = str( ocrVal.value )
    print(ocrCode)
    if ocrCode == "-10":
        print "验证码没识别出来"
        return "验证码没识别出来"
    else:
        return ocrCode

if __name__ == '__main__':
    app.run()


if __name__ == '__main__':
    app.run()