#!/usr/bin/env python3
# sample regex (^|\D)\d{6}($|\D)
"""Folder and file utilities"""
import re
import os
import os.path
from os import listdir
from os.path import isfile, isdir, join
import time
import unittest


def get_file_list(path):
    """Given a path returns a list of all files contained,
    Args: path: Path that you want to get the file list from
    Returns: list of string (file names)"""
    try:
        file_list = [f for f in listdir(path) if isfile(join(path, f))]
        return file_list
    except FileNotFoundError:
        print("Failure in get_file_list")
        return ["Bad folder structure"]


def get_full_file_list(path):
    """Given a path returns a list of all files contained,
    with full path,
    Args: path: Path that you want to get the file list from
    Returns: list of string (file names)"""
    file_list = list()
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.lower().endswith(".pdf") or f.lower().endswith(".tif")]:
        #for filename in filenames:
            if filename[0] != ".":
                file_list.append(os.path.join(dirpath, filename))
            #print(os.path.join(dirpath, filename))
    return file_list

def get_full_file_list_no_subpath(path):
    """Given a path returns a list of all files contained,
    with full path, does not include subdirectories
    Args: path: Path that you want to get the file list from
    Returns: list of string (file names)"""
    file_list = list()
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.lower().endswith(".pdf") or f.lower().endswith(".tif")]:
        #for filename in filenames:
            if filename[0] != ".":
                file_list.append(os.path.join(dirpath, filename))
            #print(os.path.join(dirpath, filename))
        break
    return file_list

def get_file_list_with_date_no_subs(path):
    """Given a path, returns a list of dates and file paths
    Args: path: Path that you want to get the file list from
    Returns: list of [date, path]
    """
    #print(path)
    file_list = get_full_file_list_no_subpath(path)
    file_list_with_date = list()
    for file in file_list:
        #print(file)
        if file[0] != ".":
            #file = os.path.normpath(file)
            try:
                file_with_date = [time.ctime(
                    os.path.getmtime(file)), os.path.basename(file)]
                file_list_with_date.append(file_with_date)
            except FileNotFoundError:
                print(file + " is not a real file")
    return file_list_with_date

def get_file_list_with_date(path):
    """Given a path, returns a list of dates and file paths
    Args: path: Path that you want to get the file list from
    Returns: list of [date, path]
    """
    #print(path)
    file_list = get_full_file_list(path)
    file_list_with_date = list()
    for file in file_list:
        #print(file)
        if file[0] != ".":
            #file = os.path.normpath(file)
            try:
                file_with_date = [time.ctime(
                    os.path.getmtime(file)), os.path.basename(file)]
                file_list_with_date.append(file_with_date)
            except FileNotFoundError:
                print(file + " is not a real file")
    return file_list_with_date


def get_folder_list(path):
    """Given a path returns a list of all folders contained,
    path -- Path that you want to get the file list from
    Returns list of string (folder names)"""
    try:
        folder_list = [f for f in listdir(path) if isdir(join(path, f))]
        return folder_list
    except FileNotFoundError:
        print("Failure in get_folder_list" + path)
        return

def get_folder_list_with_date(path):
    """Given a path, returns a list of dates and folders
    Args: path: Path that you want to get the file list from
    Returns: list of [date, foldernames]
    """
    folder_list_with_date = list()
    folder_list = [f for f in listdir(path) if isdir(join(path, f))]
    for folder in folder_list:
        folder_with_date = [time.ctime(os.path.getmtime(path+'/'+folder)), folder]
        folder_list_with_date.append(folder_with_date)
    return folder_list_with_date

def find_folders(path, names):
    """Returns a list of the complete paths of folders if they exists within the given path.
    path -- List of paths to search
    names -- List of partial or complete names to search for
    Returns a list of paths as strings.
    """
    found_folders = list()
    folder_candidates = get_folder_list(path)
    if folder_candidates:
        for name in names:
            for folder in folder_candidates:
                if name in folder:
                    fullpath = path + '/' + folder
                    found_folders.append(fullpath)
        return found_folders
    else:
        return


def folder_append(folders, sub_folder):
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


def count_files(folders):
    """Count the files contained in a folder
    Args:
        folder: Path to check
    Returns: [Folder Path, Count of files contained (int), List of files]
    """
    folder_size = list()
    if folders:
        for folder in folders:
            #file_list = get_file_list(folder)
            file_list = get_file_list_with_date(folder)
            if file_list:
                folder_size.append([folder, len(file_list), file_list])
        return folder_size
    else:
        return


def get_files_containing(path, search_string):
    """Gets a list of files in a path that contain a string
    Args:
        path: Path to check
        search_string: string to search for
    Returns: [data, file including full path]
    """
    files = get_file_list_with_date(path)
    file_list = list()
    for file in files:
        if search_string in file[1]:
            file_list.append(file)
    return file_list


def folder_exists(folder):
    """Check it a folder exists at a given path
    Args:
        folder: Path of folder to check
    Returns: True if folder exists, False if it doesn't
"""
    if os.path.exists(folder):
        return True
    else:
        return False


class MyTest(unittest.TestCase):
    """FolderChecker.py Unit Tests"""

    def test_get_file_list(self):
        """get_file_list unit test"""
        # Arrange
        expected = ['test.pdf']
        # Act
        actual = get_file_list('TestData/Dockets/685543/Production/print')
        # Assert
        self.assertEqual(actual, expected)

    def test_get_full_file_list(self):
        """get_full_file_list unit test"""
        # Arrange
        expected = ['TestData/Dockets/685543/Production/print\\test.pdf']
        # Act
        actual = get_full_file_list('TestData/Dockets/685543/Production/print')
        # Assert
        self.assertEqual(actual, expected)

    def test_get_file_list_with_date(self):
        """get_file_list_with_date unit test"""
        # Arrange
        expected = [['Sun May  7 10:06:02 2017', 'test.pdf']]
        # Act
        actual = get_file_list_with_date(
            'TestData/Dockets/685543/Production/print')
        # Assert
        self.assertEqual(actual, expected)

    def test_get_folder_list(self):
        """get_folder_list unit test"""
        # Arrange
        expected = ['672143', '684421', '685543', '687203', '689398']
        # Act
        actual = get_folder_list('TestData/Dockets')
        # Assert
        self.assertEqual(actual, expected)

    def test_find_folders(self):
        """find_folders unit test"""
        # Arrange
        expected = ['TestData/Dockets/672143', 'TestData/Dockets/684421']
        # Act
        actual = find_folders('TestData/Dockets', ['672143', '684421'])
        # Assert
        self.assertEqual(actual, expected)

    def test_folder_append(self):
        """folder_append unit test"""
        # Arrange
        expected = ['TestData/Dockets/672143']
        # Act
        actual = folder_append(['TestData/Dockets/'], '672143')
        # Assert
        self.assertEqual(actual, expected)

    def test_count_files(self):
        """count_files unit test"""
        # Arrange
        expected = [[
            'TestData/Dockets/685543/Production/print',
            1,
            [['Sun May  7 10:06:02 2017', 'test.pdf']]]]
        # Act
        actual = count_files(['TestData/Dockets/685543/Production/print'])
        # Assert
        self.assertEqual(actual, expected)

    def test_folder_exists(self):
        """folder_exists unit test"""
        # Arrange
        expected = True
        # Act
        actual = folder_exists('TestData/Dockets/685543/Production/print')
        # Assert
        self.assertEqual(actual, expected)

    def test_get_files_containing(self):
        """get_files_containing unit test"""
        # Arrange
        expected = [['Sun May  7 10:06:45 2017', 'Test2.pdf']]
        # Act
        actual = get_files_containing(
            'TestData/Dockets/684421/Production/Print', "Test2")
        # Assert
        self.assertEqual(actual, expected)
    def test_get_folder_list_with_date(self):
        """get_folder_list_with_date"""
        # Arrange
        expected = [['Sun May  7 09:48:35 2017', 'Print']]
        # Act
        actual = get_folder_list_with_date("TestData/Dockets/672143/Production")
        # Assert
        self.assertEqual(actual, expected)

#TEST = get_folder_list_with_date("TestData/Dockets/672143/Production")
#print(TEST)

if __name__ == '__main__':
    unittest.main()
