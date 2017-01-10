import datetime

import random


########################################################################

class MyCache:
    """"""

    # ----------------------------------------------------------------------

    def __init__(self):

        """Constructor"""

        self.cache = {}

        self.max_cache_size = 10

        # ----------------------------------------------------------------------

    def __contains__(self, key):

        """

        根据该键是否存在于缓存当中返回True或者False

        """

        return key in self.cache

        # ----------------------------------------------------------------------

    def update(self, key, value):

        """

        更新该缓存字典，您可选择性删除最早条目

        """

        if key not in self.cache and len(self.cache) >= self.max_cache_size:
            self.remove_oldest()

        self.cache[key] = {'date_accessed': datetime.datetime.now(),

                           'value': value}

        # ----------------------------------------------------------------------

    def remove_oldest(self):

        """

        删除具备最早访问日期的输入数据

        """

        oldest_entry = None

        for key in self.cache:

            if oldest_entry == None:

                oldest_entry = key

            elif self.cache[key]['date_accessed'] < self.cache[oldest_entry][

                'date_accessed']:

                oldest_entry = key

        self.cache.pop(oldest_entry)

        # ----------------------------------------------------------------------

    @property
    def size(self):

        """

        返回缓存容量大小

        """

        return len(self.cache)
