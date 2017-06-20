#!flask/bin/python
# coding:utf-8


from flask import Flask, jsonify
from flask import request
from adb import Adb
from slot import Slot

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
def slotService():
    reqs = request.json

    action = request.json['action']
    if 'id' in request.json:
        id = request.json['id']

    serial = request.json['serial']
    type = request.json['type']

    if 'remark' in request.json:
        remark = request.json['remark']
    else:
        remark = "Backed";

    if 'page' in reqs:
        page = reqs['page']
    else:
        page = 1;

    if not action:
        return jsonify({'success': False, 'msg': u'paramter action is missed'})

    if not serial:
        return jsonify({'success': False, 'msg': u'paramter serial is missed'})

    slot = Slot(serial, type)
    if action == "save":
        if remark == "":
            remark = "BackUp"
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
        idFrom = (page - 1)*20 + 1
        idTo = (page-1) * 20 + 20
        for index in range(idFrom, idTo + 1):
            if slots.has_key(str(index)) :
                obj = slots[str(index)]
                obj['empty'] = False;
                obj['id'] = index
            else:
                obj = {'id':index, 'empty': True}
            result.append(obj)

        return jsonify({'slots': result })

    return "-"



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3344, threaded=True)
