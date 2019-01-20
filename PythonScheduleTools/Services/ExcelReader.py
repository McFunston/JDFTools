#!/usr/bin/env python3
"""MS Excel tools related to schedules saved as workbooks"""

from xlrd import open_workbook
from datetime import datetime
import time
import Cache


class ExcelReader():

    def __init__(self, data_source):
        self.path = data_source['Path']
        self.id_column = data_source['Id Column']
        self.date_column = data_source['Date Column']
        self.status_column = data_source['Status Column']
        self.status = data_source['Status']

    def _list_strip(self, list_to_strip):
        """Removes unecessary spaces from a list of cells
        Args:
        list_to_strip: A list of cells
        Returns: A list of strings"""
        stripped_list = [x.value.strip() for x in list_to_strip]
        return stripped_list

    def _get_data(self):
        cache = Cache.Cache()
        return cache.get_list(self.path, self._get_uncached_data)

    def _get_uncached_data(self):
        """Get the contents of the first worksheet of an Excel file
        Args:
        file_name: The name of the Excel file containing jobs
        Returns: Excel work sheet as xlrd.sheet.Sheet"""
        try:
            with open_workbook(self.path) as book:
                sheet = book.sheet_by_index(0)
            return sheet
        except FileNotFoundError:
            raise ValueError("That file doesn't exist at the given location")

    def _excel_to_dict(self):
        sheet = self._get_data()
        excel_dict = dict()
        for row_index in range(sheet.nrows - 1):
            for column_index in range(sheet.ncols - 1):
                cell_value = sheet.cell(row_index + 1, column_index + 1).value
                cell_value = cell_value.strip()
                cell_location = (row_index + 1, column_index + 1)
                excel_dict[cell_location] = cell_value
        return excel_dict

    def get_jobs_by_status(self, file_name, status_column, status):
        """Get all of the rows in an Excel file where the status column contains a certain status
        Args:
            file_name: Name of the Excel file
            status_column: Column that contains the statuses for the jobs
            status: Status to filter by
        Returns: A list of row contents
        """
        try:
            sheet = self._get_data()
        except ValueError as error:
            print(error.args)
            raise
        rows = sheet.get_rows()
        jobs = [self._list_strip(row)
                for row in rows if status in row[status_column].value]
        return jobs

    def get_just_ids(self, jobs, id_index):
        """Strip away everything except the job ids from a list of jobs and removes duplicates
        Args:
            jobs: A list of jobs
            id_index: Location in the list of the indices
        Returns: A list of job ids (string)
        """
        ids = [job[id_index] for job in jobs]
        ids = list(set(ids))
        return ids

    def get_list(self):
        ids_with_dates = list()
        jobs = self.get_jobs_by_status(
            self.path, self.status_column, self.status)
        for job in jobs:
            if self.status in job[self.status_column]:
                dte = job[self.date_column]
                dte = datetime.strptime(dte, '%m/%d/%Y %I:%M:%S %p')
                id_and_date = [dte.strftime('%c'), job[self.id_column]]
                ids_with_dates.append(id_and_date)
        return ids_with_dates

# fi = ExcelReader('TestData/Printflow-ToDo.xls', 3, 0, 2, 'Files In')
# po = ExcelReader('TestData/Printflow-ToDo.xls', 3, 0, 2, 'Proof Out')
# pi = ExcelReader('TestData/Printflow-ToDo.xls', 3, 0, 2, 'Proof In')

# k = fi.get_list()
# print(k)
# l = po.get_list()
# print(l)
# m = pi.get_list()
# print(m)
