#!/usr/bin/env python3
"""A simple caching system to very briefly cache the results from CSVReader and ExcelReader"""
import datetime
import random
import time

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Cache(metaclass=Singleton):
    def __init__(self):
        
        self.cache = {}

    def _check_cache(self, source_name):        
        if source_name in self.cache:
            cache_cutoff = self.cache[source_name]["Creation Date"] + datetime.timedelta(minutes=3)
            print('In the cache, checking date')
            print(cache_cutoff - datetime.datetime.now())
            if datetime.datetime.now() < cache_cutoff:
                return True

    def get_list(self, source_name, fallback):
        if self._check_cache(source_name):
            print('In Cache')            
            ids_with_dates = self.cache[source_name]['List']
        else:
            print('Not in cache')
            ids_with_dates = fallback()
            self.cache[source_name] = {}
            self.cache[source_name]['List'] = ids_with_dates
            self.cache[source_name]['Creation Date'] = datetime.datetime.now()
            
        return ids_with_dates
# def get_rand():
#     rnd = random.randint(1,1000)
#     return rnd
# cache = Cache()

# for i in range(1,9):
#     test = cache.get_list("Test", get_rand)    
#     print(test)
#     time.sleep(10)

