#!flask/bin/python
# coding:utf-8

import re

from flask import Flask, jsonify
from flask import request
import os
import subprocess

app = Flask(__name__)

@app.route('/dsfkjwe/console')
def console():
    import subprocess
    subprocess.call(["systemctl restart ztask.service"], shell=True)
    return "-"

@app.route('/dsfaawe/provider')
def provider():
    import subprocess
    subprocess.call(["systemctl restart stf-provider@floor4.service"], shell=True)
    return "-"

@app.route('/dsfkjw323e/sys')
def sysd():
    import subprocess
    subprocess.call(["sudo reboot -f"], shell=True)
    return "-"



@app.route('/asf23d3h/s3ss')
def shut():
    import subprocess
    subprocess.call(["shutdown -fh now"], shell=True)
    return "-"

@app.route('/w3i778/8888s')
def s543hut():
    import subprocess
    subprocess.call(["tail -10000 /var/log/messages > /data/zy/zylog/message"], shell=True)
    return "-"


@app.route('/w3321p78/8k888s')
def s599hut():
    import subprocess
    if os.path.exists('/data/zy/framework/ztask.info'):
        subprocess.call(["7za x /data/zy/framework/ztask.abc -pUFE*GHU=IK#7suw6o54w3e9987we2 -aoa -o/home/ztask/"], shell=True)
        subprocess.call(["systemctl restart ztask.service"], shell=True)

    if os.path.exists('/data/zy/framework/zconsole.info'):
        subprocess.call(["7za x /data/zy/framework/zconsole.abc -pUFE*GHU=IK#7s3322OPOndeaudfwe2 -aoa -o/home/zconsole/"], shell=True)
        subprocess.call(["systemctl restart zconsole.service"], shell=True)

    subprocess.call(["rm -rf /data/zy/framework/*"], shell=True)

    return "-"


@app.route('/a2342d3h/s21s', methods=['POST'])
def reset():
    info_filename = '/data/zy/s.info'
    ip = request.form['ip']
    gateway = request.form['gateway']
    domain = request.form['domain']
    repo = request.form['repo']
    if  ip and gateway and domain and repo :
        if os.path.exists(info_filename):
            os.remove(info_filename)
        f = open(info_filename, "w")
        f.writelines("REPO_DATABASE_IP=%s\n"%repo)
        f.writelines("SERVER_IP=%s\n"%ip)
        f.writelines("SERVER_GATEWAY=%s\n"%gateway)
        f.writelines("SERVER_DOMAIN=%s\n"%domain)
        f.close()
        subprocess.call(["sh /etc/reset_ip.d"], shell=True)
        return "-"
    else:
        return "F"



@app.route('/w338878/k888s')
def s528hut():
    if NetCheck("www.baidu.com"):
        return jsonify({'success': True, 'msg': u'Baidu可以正常访问'})

    return jsonify({'success': False, 'msg': u'服务器网络可能存在故障，Baidu无法正常访问'})




def NetCheck(ip):
   try:
    p = subprocess.Popen(["ping -c 1 "+ ip],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out=p.stdout.read()
    if 'icmp_seq' and 'bytes from' and 'time' in out:
        return True
    else:
        return False
   except:
    print 'NetCheck work error!'
    return False

if __name__ == '__main__':
    print NetCheck('www.baidu.com')
    app.run(debug=False)
