#!/usr/bin/env python3
# sample regex (^|\D)\d{6}($|\D)
"""Folder and file utilities"""

import os
import os.path
from os import listdir
from os.path import isfile, isdir, join
import time
import Cache


class FolderReader():

    def __init__(self, data_source):
        self.path = data_source['Path']

    def _get_uncached_data(self):
        """Given a path, returns a list of dates and folders
        Args: path: Path that you want to get the file list from
        Returns: list of [date, foldernames]
        """
        folder_list_with_date = list()
        folder_list = [f for f in listdir(
            self.path) if isdir(join(self.path, f))]
        for folder in folder_list:
            folder_with_date = [time.ctime(
                os.path.getmtime(self.path + '/' + folder)), folder]
            folder_list_with_date.append(folder_with_date)
        return folder_list_with_date

    def _get_data(self):
        cache = Cache.Cache()
        return cache.get_list(self.path, self._get_uncached_data)

    def _folder_append(self, folders, sub_folder):
        """Appends subfolder paths onto a list of folders
            Args:
                folders: list of folders to append to
                sub_folder: path to append (string)
            Returns: list of folder paths
        """
        full_folder = list()
        if folders:
            for folder in folders:
                folder += sub_folder
                full_folder.append(folder)
            return full_folder
        else:
            return

    def _folder_exists(self, folder):
        """Check it a folder exists at a given path
        Args:
            folder: Path of folder to check
        Returns: True if folder exists, False if it doesn't
    """
        if os.path.exists(folder):
            return True
        else:
            return False

    def get_list(self):
        return self._get_data()

