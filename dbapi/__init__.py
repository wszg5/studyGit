# coding:utf-8
import rethinkdb as r
#https://github.com/lucidfrontier45/RethinkPool
from rethinkpool import RethinkPool
from const import const
import time, random


class dbapi:

    def __init__(self):
        '''
        self.pool = RethinkPool(max_conns=5, initial_conns=1, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        '''

    def finddevices(self):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        devices = r.table('devices').filter({'present': True, 'ready': True}).order_by('statusChangedAt').run(conn)
        conn.close(noreply_wait=False)
        return devices


    def log_error(self,serial, summary, message):
        self.log_warn(serial ,summary, message, "error")

    def log_warn(self, serial,summary, message, level="warn"):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        uid = time.time() + random.randint(10000, 20000)
        log = {"id": uid, "serial": serial, "summary": summary, "message": message, "level": level,
               "UpdatedAt": r.now().run(conn, time_format="raw")}
        r.table("warn_msg").insert(log).run(conn)

        conn.close(noreply_wait=False)

    def GetDeviceTask(self, serial):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        device = r.table('devices').get(serial).run(conn)
        conn.close(noreply_wait=False)

        if device and device.get("task_id"):
            return device["task_id"]
        return None

    def GetDevicesByTask(self, taskId):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        devices = r.table('devices').filter({"task_id", taskId}).run(conn)
        conn.close(noreply_wait=False)

        return devices




    def GetTask(self, taskid):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        task = r.table('tasks').get(taskid).run(conn)
        conn.close(noreply_wait=False)
        return task

    def GetTaskSteps(self, taskid):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        steps = r.table('taskSteps').get_all(taskid, index='task_id').order_by('sort').run(conn)
        conn.close(noreply_wait=False)
        return steps

    def GetSlotInfo(self, serial, appType, slotNum):
        id = '%s_%s_%s' % (serial, appType, slotNum)

        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        info = r.table("slots").get(id).run(conn)
        conn.close(noreply_wait=False)

        return info


    def SaveSlotInfo(self, serial, type, name,empty, current, info):
        id = '%s_%s_%s'%(serial,type,name)
        slot = {"id":id, "serial": serial, "type": type, "name":name,"empty": empty, "current":current, "info":info}
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        stats = r.table("slots").get(id).update(slot).run(conn)
        if stats["skipped"]:
            slot["createdAt"] = r.now().run(conn, time_format="raw")
            slot["last_pick"] = r.now().run(conn, time_format="raw")
            r.table("slots").insert(slot).run(conn)
        conn.close(noreply_wait=False)


    def PickSlot(self, serial, type, name):
        id = '%s_%s_%s'%(serial,type,name)
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        now = r.now().run(conn, time_format="raw")
        r.table("slots").get(id).update({"last_pick": now}).run(conn)
        conn.close(noreply_wait=False)



    def ListSlots(self, serial, type):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        list = r.table("slots").get_all(serial, index='serial').filter({'type': type}).order_by('name').run(conn)
        conn.close(noreply_wait=False)

        return list;


    def ListSlotsInterval(self, serial, type, interval):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        list = r.table("slots").get_all(serial, index='serial').filter(
            (r.row["type"] == type) & (r.row["empty"] == 'false') & (
            r.row["last_pick"] + int(interval) < r.now())).order_by('name').run(conn)
        conn.close(noreply_wait=False)
        return list;

    def GetSetting(self, key):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        setting = r.table('setting').get(key).run(conn)
        conn.close(noreply_wait=False)
        if setting:
            return setting["value"]


    def GetCache(self, key, interval):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        list = r.table("setting").get_all(key).filter(r.row["UpdatedAt"] + int(interval) < r.now()).order_by('name').run(conn)
        conn.close(noreply_wait=False)

        if (len(list) > 0):
            return list[0]

        return None

    def SetCache(self, key, value):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        cache = {"key": key, "value": value, "UpdatedAt": r.now().run(conn, time_format="raw")}
        stats = r.table("setting").get(key).update(cache).run(conn)
        if stats["skipped"]:
            r.table("setting").insert(cache).run(conn)
        conn.close(noreply_wait=False)



    def DelCache(self,key):
        conn = r.connect(host=const.SERVER_IP,
                         port=28015,
                         db=const.RETHINKDB_NAME)
        r.table("setting").get(key).delete().run(conn)
        conn.close(noreply_wait=False)


dbapi = dbapi()
