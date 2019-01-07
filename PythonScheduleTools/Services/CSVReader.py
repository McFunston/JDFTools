#!/usr/bin/env python3
"""Tools for extracting job info from CSV files"""
import csv
import os
import datetime
import time
import ListShaper
import Cache

class CSVReader():

    def __init__(self, data_source):
        self.path = data_source['Path']

    def get_data(self):
        cache = Cache.Cache()
        return cache.get_list(self.path, self._get_uncached_data)

    def _get_uncached_data(self):

        with open(self.path, newline='', encoding='latin-1', mode='r') as csvfile:
            reader = csv.reader(x.replace('\0', '') for x in csvfile)
            log = [log_items for log_items in reader]
        return log

    def get_list(self):
        return self.get_data()


# test_csv = CSVReader('ProofLog.csv')
# test1 = test_csv.get_list()

# test2 = test_csv.get_list()