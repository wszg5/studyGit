#!flask/bin/python
from flask import Flask, request, render_template, url_for, request,redirect,make_response,session

import os
app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return render_template('regist.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5555)
