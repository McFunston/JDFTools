#!/usr/bin/env python3
"""Classes related to data collection for job statuses
All classes must share the folowing interface:
self.source_name (property)
self.check_status(self, status, job_id) (method)"""
import unittest

import CSVReader
import ExcelReader
import FolderChecker
import ListShaper

#from abc import ABC, abstractmethod


class ExcelStatus:
    """Data source in which the status is derived from an Excel file."""
    # def __init__(self, source_name, path, id_column, status_column):

    def __init__(self, data_source_dictionary):
        self.source_name = data_source_dictionary.get('Source Name')
        self.path = data_source_dictionary['Path']
        self.id_column = data_source_dictionary['Id Column']
        self.status_column = data_source_dictionary['Status Column']
        self.status = data_source_dictionary['Status']

    def check_status(self, status, job_id):
        """Check whether a given status is True. Required as part of interface"""
        return_status = ExcelReader.check_job_status(
            status,
            self.path,
            job_id,
            self.id_column,
            self.status_column)
        return return_status

    def get_job_ids(self):
        """Return a list of job ids from the Excel file. Required as part of interface"""
        job_ids = ExcelReader.get_all_ids(self.path, self.id_column)
        return list(set(job_ids))


class LogFileStatus:
    """Data source in which the status is derived from a comma delimited log file"""
    # def __init__(self, source_name, path, status):

    def __init__(self, data_source_dictionary):
        self.source_name = data_source_dictionary['Source Name']
        self.path = data_source_dictionary['Path']
        self.status = data_source_dictionary['Status']

    def check_status(self, status, job_id):
        """Check whether a given status is true. Required as part of interface"""
        candidates = CSVReader.find_in_csv(self.path, [job_id])
        # if candidates: return True
        return bool(candidates)

    def get_job_ids(self):
        """Return a list of job ids from the csv file. Required as part of interface"""
        job_ids = CSVReader.list_jobs(self.path)
        return job_ids


class FileStatusByName:
    """Data source in which the status is derived from the existence of
    files in a given folder which contain the job id in their name
    (ie does a certain folder contain files containing 687254)"""
    # def __init__(self, source_name, path, status):

    def __init__(self, data_source_dictionary):
        self.source_name = data_source_dictionary['Source Name']
        self.path = data_source_dictionary['Path']
        self.status = data_source_dictionary['Status']

    def check_status(self, status, job_id):
        """Check whether a given status is true. Required as part of interface"""
        findings = FolderChecker.get_files_containing(self.path, job_id)
        if len(findings) > 0:
            return True

    def get_job_ids(self):
        """Return a list of job ids from the files at self.path. Required as part of interface"""
        file_list = FolderChecker.get_file_list_with_date(self.path)
        job_ids = ListShaper.job_lister(file_list)
        return job_ids


class FileSystemStatus:
    """Abstract class for file or folder based statuses in which the path is
    /static_path/path_containing_job_id/static_subpath (the job folders are
    always contained in a given folder (/dockets for example) and always
    contain a given subfolder (/Production/Print for ex))"""
    # def __init__(self, source_name, path, sub_path, status):

    def __init__(self, data_source_dictionary):
        self.source_name = data_source_dictionary.get('Source Name')
        self.path = data_source_dictionary.get('Path')
        self.sub_path = data_source_dictionary.get('Sub Path')
        self.status = data_source_dictionary.get('Status')

    def get_job_ids(self):
        """Return a list of job ids from the folders at self.path. Required as part of interface"""
        folder_list = FolderChecker.get_folder_list_with_date(self.path)
        job_ids = ListShaper.job_lister(folder_list)
        return job_ids


class FileStatus(FileSystemStatus):
    """Data source in which the status is derived from the existence of files within a
    given root path, variable path containg a string, and a given sub path.
    (ie /Dockets/*variable*/files contains files so the status should be "Files In")"""

    def __init__(self, data_source_dictionary):
        super().__init__(data_source_dictionary)

    def check_status(self, status, job_id):
        """Check whether a given status is true. Required as part of interface"""
        folders_to_check = FolderChecker.find_folders(self.path, [job_id])
        folders_to_check = FolderChecker.folder_append(
            folders_to_check, self.sub_path)
        print_files = FolderChecker.count_files(folders_to_check)
        return bool(print_files)

    def get_job_ids(self):
        super().get_job_ids()


class FolderStatus(FileSystemStatus):
    """Data source in which the status is derived from the existence of a folder within a
    given root path, variable path containg a string, and a given sub path.
    (ie /Prinect Jobs/*variable*/Sequences contains a plating folder so the
    status should be "Proof In")"""

    # def __init__(self, source_name, path, sub_path, folder, status):
    def __init__(self, data_source_dictionary):
        super().__init__(data_source_dictionary)
        self.folder = data_source_dictionary.get('Folder')

    def check_status(self, status, job_id):
        """Check whether a given status is true. Required as part of interface"""
        folders_to_check = FolderChecker.find_folders(self.path, [job_id])
        folders_to_check = FolderChecker.folder_append(
            folders_to_check, self.sub_path)
        for folder_to_check in folders_to_check:
            if FolderChecker.folder_exists(folder_to_check + self.folder):
                return True
            else:
                return False

    def get_job_ids(self):
        super().get_job_ids()


class DataSourceTests(unittest.TestCase):
    """DataSource unit tests"""

    def test_excel_check_status(self):
        """Check that class implements check_status properly"""
        # Arrange
        test_dictionary = {'Source Name': 'Test',
                           'Path': 'Printflow-ToDo1.xls',
                           'Id Column': 3,
                           'Status Column': 2,
                           'Status': 'Dollco Printing-Proof In'}
        excel_test = ExcelStatus(test_dictionary)
        expected = True
        # Act
        actual = excel_test.check_status('Dollco Printing-Proof In', '685597')
        # Assert
        self.assertEqual(actual, expected)

    def test_log_file_status(self):
        """Check that class implements check_status properly"""
        # Arange
        test_dictionary = {'Source Name': 'Test',
                           'Path': 'ProofLog.csv',
                           'Status': 'Hunt Club-Proof Out'}
        expected = False
        log_file_test = LogFileStatus(test_dictionary)
        # Act
        actual = log_file_test.check_status('Hunt Club-Proof Out', '690331')
        # Assert
        self.assertEqual(actual, expected)

    def test_file_status(self):
        """Check that class implements check_status properly"""
        # Arrange
        test_dictionary = {'Source Name': 'Test',
                           'Path': 'TestData/Dockets',
                           'Sub Path': '/Production/Print',
                           'Status': 'Files In'}
        print(len(test_dictionary))
        expected = True
        test_object = FileStatus(test_dictionary)
        # Act
        actual = test_object.check_status('Files In', '685543')
        # Assert
        self.assertEqual(actual, expected)

    def test_folder_status(self):
        """Check that class implements check_status properly"""
        # Arrange
        test_dictionary = {'Source Name': 'Test',
                           'Path': 'TestData/Dockets',
                           'Sub Path': '/Production',
                           'Folder': '/Print',
                           'Status': 'Files In'}
        expected = True
        test_object = FolderStatus(test_dictionary)
        # Act
        actual = test_object.check_status('Proof In', '685543')
        # Assert
        self.assertEqual(actual, expected)

    def test_file_status_by_name(self):
        """Check that class implements check_status properly"""
        # Arrange
        test_dictionary = {'Source Name': 'Test',
                           'Path': 'TestData/Dockets/684421/Production/Print',
                           'Status': 'Proof In'}
        expected = True
        test_object = FileStatusByName(test_dictionary)
        # Act
        actual = test_object.check_status('Files In', 'Test2')
        # Assert
        self.assertEqual(actual, expected)

#test_object = FolderStatus('P Drive', 'TestData/Dockets', '/Production', '/Print', 'Proof In')
#print(test_object.check_status('Files In', '685543'))


if __name__ == '__main__':
    unittest.main()
