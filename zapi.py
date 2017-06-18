#!flask/bin/python
# coding:utf-8

import re

from flask import Flask, jsonify
from flask import request
from slot.adb_slot import adb_slot
from uiautomator import Adb


app = Flask(__name__)


@app.route('/zapi/read_file', methods=['POST'])
def readFile():
    serial = request.form['serial']
    path = request.form['path']
    if not serial:
        return jsonify({'success': False, 'msg': u'paramter serial is missed'})
    if not path:
        return jsonify({'success': False, 'msg': u'paramter path is missed'})

    adb = Adb(serial=serial)
    out = adb.run_cmd("shell", "\"su -c 'cat %s'\"" % path).output
    return out;


@app.route('/zapi/slot', methods=['POST'])
def slot():
    print(request.args)
    print(request.values)
    action = request.form['action']
    if 'id' in request.form:
        id = request.form['id']

    serial = request.form['serial']
    type = request.form['type']

    if 'remark' in request.form:
        remark = request.form['remark']
    else:
        remark = "Backed";

    if not action:
        return jsonify({'success': False, 'msg': u'paramter action is missed'})



    if not serial:
        return jsonify({'success': False, 'msg': u'paramter serial is missed'})

    slot = adb_slot(serial, type)
    if action == "save":
        slot.backup(id, remark)
        return jsonify({'success': True, 'msg': u'Save slot success'})

    if action == "restore":
        slot.restore(id)
        return jsonify({'success': True, 'msg': u'Restore slot success'})

    if action == "clear":
        slot.clear(id)
        return jsonify({'success': True, 'msg': u'Clear slot success'})

    if action == "list":
        result = []
        slots = slot.getSlots()
        if not slots:
            slots = {};
        for index in range(1, 21):
            if slots.has_key(str(index)) :
                obj = slots[str(index)]
                obj['empty'] = False;
                obj['id'] = index
            else:
                obj = {'id':index, 'empty': True}
            result.append(obj)

        return jsonify(result)

    return "-"



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3344, threaded=True)
