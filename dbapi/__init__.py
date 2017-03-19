# coding:utf-8
import rethinkdb as r
#https://github.com/lucidfrontier45/RethinkPool
from rethinkpool import RethinkPool
from const import const
import time, random


class dbapi:

    def __init__(self):
        self.s = ""

    def finddevices(self):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            devices = r.table('devices').filter({'present': True, 'ready': True}).order_by('statusChangedAt').run(res.conn)
            return devices


    def log_error(self,serial, summary, message):
        self.log_warn(serial ,summary, message, "error")

    def log_warn(self, serial,summary, message, level="warn"):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            uid = time.time() + random.randint(10000, 20000)
            log = {"id": uid,"serial":serial, "summary":summary, "message": message, "level": level, "UpdatedAt": r.now().run(res.conn, time_format="raw")}
            r.table("warn_msg").insert(log).run(res.conn)

    def GetDeviceTask(self, serial):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
                device = r.table('devices').get(serial).run(res.conn)
                if device and device.get("task_id"):
                    return device["task_id"]
        return None


    def GetBusyVirtualDevices(self):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            steps = r.table('v_devices').order_by('serial').run(res.conn)
            return steps


    def GetTask(self, taskid):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            task = r.table('tasks').get(taskid).run(res.conn)
            return task

    def GetTaskSteps(self, taskid):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            steps = r.table('taskSteps').get_all(taskid, index='task_id').order_by('sort').run(res.conn)
            return steps

    def GetSlotInfo(self, serial, appType, slotNum):
        id = '%s_%s_%s' % (serial, appType, slotNum)
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            info = r.table("slots").get(id).run(res.conn)
            return info


    def SaveSlotInfo(self, serial, type, name,empty, current, info):
        id = '%s_%s_%s'%(serial,type,name)
        slot = {"id":id, "serial": serial, "type": type, "name":name,"empty": empty, "current":current, "info":info}
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            stats = r.table("slots").get(id).update(slot).run(res.conn)
            if stats["skipped"]:
                slot["createdAt"] = r.now().run(res.conn, time_format="raw")
                slot["last_pick"] = r.now().run(res.conn, time_format="raw")
                r.table("slots").insert(slot).run(res.conn)

    def PickSlot(self, serial, type, name):
        id = '%s_%s_%s'%(serial,type,name)
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            now = r.now().run(res.conn, time_format="raw")
            r.table("slots").get(id).update({"last_pick": now}).run(res.conn)



    def ListSlots(self, serial, type):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            list = r.table("slots").get_all(serial, index='serial').filter({'type': type}).order_by('name').run(res.conn)
            return list;


    def ListSlotsInterval(self, serial, type, interval):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            list = r.table("slots").get_all(serial, index='serial').filter((r.row["type"] == type) & (r.row["empty"] == 'false') & ( r.row["last_pick"] + int(interval) < r.now()  ) ).order_by('name').run(res.conn)
            return list;

    def GetSetting(self, key):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            setting = r.table('setting').get(key).run(res.conn)
            if setting:
                return setting["value"]


    def GetCache(self, key, interval):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)

        with pool.get_resource() as res:
            list = r.table("setting").get_all(key).filter(r.row["UpdatedAt"] + int(interval) < r.now()).order_by('name').run(res.conn)
            if (len(list) > 0):
                return list[0]

        return None

    def SetCache(self, key, value):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            cache = {"key": key, "value": value, "UpdatedAt": r.now().run(res.conn, time_format="raw")}

            stats = r.table("setting").get(key).update(cache).run(res.conn)
            if stats["skipped"]:
                r.table("setting").insert(cache).run(res.conn)

    def DelCache(self,key):
        pool = RethinkPool(max_conns=120, initial_conns=10, host=const.SERVER_IP,
                           port=28015,
                           db=const.RETHINKDB_NAME)
        with pool.get_resource() as res:
            r.table("setting").get(key).delete().run(res.conn)

dbapi = dbapi()
