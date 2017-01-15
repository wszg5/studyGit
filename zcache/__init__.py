#!/usr/bin/env python
# -*- coding: utf-8 -*-

#sudo pip install redis

import redis
from const import const


class _cache:
    def __init__(self):
        self.pool = redis.ConnectionPool(host=const.REDIS_SERVER, port=6379, db=0)


    def set(self, key, value, timeout=300):
        r = redis.Redis(connection_pool=self.pool)
        r.set(key,value, ex=timeout)

    def get(self, key):
        r = redis.Redis(connection_pool=self.pool)
        return r.get(key)

    def delete(self, key):
        r = redis.Redis(connection_pool=self.pool)
        return r.delete(key)

    def clear(self):
        r = redis.Redis(connection_pool=self.pool)
        r.flushdb()

    def addSet(self, key, value):
        r = redis.Redis(connection_pool=self.pool)
        r.sadd(key, value)

    def popSet(self, key):
        r = redis.Redis(connection_pool=self.pool)
        return r.spop(key)


cache = _cache()

cache.clear()