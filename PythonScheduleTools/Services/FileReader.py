#!/usr/bin/env python3
# sample regex (^|\D)\d{6}($|\D)
"""Class for checking files and modification dates"""

import os
import os.path
from os import listdir
from os.path import isfile, isdir, join
import time
import Cache


class FileReader():

    def __init__(self, data_source):
        self.path = data_source['Path']

    def _get_full_file_list(self):
        """Given a path returns a list of all files contained,
        with full path,
        Args: path: Path that you want to get the file list from
        Returns: list of string (file names)"""
        file_list = [join(self.path, f) for f in listdir(
            self.path) if isfile(join(self.path, f)) and f[0] != "."]
        return file_list

    def _get_uncached_data(self):
        """Given a path, returns a list of dates and file paths
        Args: path: Path that you want to get the file list from
        Returns: list of [date, path]
        """
        file_list = self._get_full_file_list()
        file_list_with_date = list()
        for file in file_list:
            if file[0] != ".":
                try:
                    file_with_date = [time.ctime(
                        os.path.getmtime(file)), os.path.basename(file)]
                    file_list_with_date.append(file_with_date)
                except FileNotFoundError:
                    print(file + " is not a real file")
        return file_list_with_date

    def _get_data(self):
        cache = Cache.Cache()
        return cache.get_list(self.path, self._get_uncached_data)

    def get_list(self):
        return self._get_data()


