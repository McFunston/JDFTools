#!/usr/bin/env python3
"""MS Excel tools related to schedules save as workbooks"""
import sys
import pprint
from xlrd import open_workbook


def list_strip(list_to_strip):
    """Removes unecessary spaces from a list of cells
    Args:
       list_to_strip: A list of cells
    Returns: A list of strings"""
    stripped_list = [x.value.strip() for x in list_to_strip]
    return stripped_list


def get_all_jobs(file_name):
    """Get the contents of the first worksheet of an Excel file
    Args:
       file_name: The name of the Excel file containing jobs
    Returns: Excel work sheet as xlrd.sheet.Sheet"""
    try:
        with open_workbook(file_name) as book:
            sheet = book.sheet_by_index(0)
        return sheet
    except FileNotFoundError:
        raise ValueError("That file doesn't exist at the given location")


def excel_to_dict(file_name):
    sheet = get_all_jobs(file_name)
    excel_dict = dict()
    for row_index in range(sheet.nrows - 1):
        for column_index in range(sheet.ncols - 1):
            cell_value = sheet.cell(row_index + 1, column_index + 1).value
            cell_value = cell_value.strip()
            cell_location = (row_index + 1, column_index + 1)
            excel_dict[cell_location] = cell_value
    return excel_dict


def get_jobs(file_name, columns):
    """Print a list of jobs columns from an Excel File.

    Args:
        file_name: The name of the Excel file containing jobs
        columns: A list of the column indices to get

    Returns: list(list(str))  """
    with open_workbook(file_name) as book:
        sheet = book.sheet_by_index(0)
    jobs_info = list()
    for row_index in range(sheet.nrows - 1):
        job_info = list()
        for column_index in columns:
            cell_value = sheet.cell(row_index + 1, column_index).value
            cell_value = cell_value.strip()
            job_info.append(cell_value)
        jobs_info.append(job_info)
        # print(jobs_info[row_index])
    return jobs_info


def get_jobs_by_id(file_name, id_column, job_id):
    """Gets the rows in a workbook that relate to a given job

    Args:
        file_name: The name of the Excel file containing jobs
        id_column: Column containg job identifier (job#, invoice#, etc)
        job_id: A string to search for that is unique to the job being searched for

    Returns: A list containg the rows that match the job_id"""
    try:
        sheet = get_all_jobs(file_name)
    except ValueError as error:
        print(error.args)
        raise
    rows = sheet.get_rows()
    jobs = [list_strip(row)
            for row in rows if row[id_column].value == str(job_id)]
    return jobs


def get_jobs_by_status(file_name, status_column, status):
    """Get all of the rows in an Excel file where the status column contains a certain status
    Args:
        file_name: Name of the Excel file
        status_column: Column that contains the statuses for the jobs
        status: Status to filter by
    Returns: A list of row contents
    """
    try:
        sheet = get_all_jobs(file_name)
    except ValueError as error:
        print(error.args)
        raise
    rows = sheet.get_rows()
    jobs = [list_strip(row)
            for row in rows if status in row[status_column].value]
    return jobs


def get_just_ids(jobs, id_index):
    """Strip away everything except the job ids from a list of jobs and removes duplicates
    Args:
        jobs: A list of jobs
        id_index: Location in the list of the indices
    Returns: A list of job ids (string)
    """
    ids = [job[id_index] for job in jobs]
    ids = list(set(ids))
    return ids


def get_all_ids(path, id_column):
    """Get all job ids from a given Excel File
    Args:
        path: Path to Excel file to get ids from
        id__column: 0 based column that has ids
    Returns: A list of job ids (string)
    """
    all_jobs = get_all_jobs(path)
    all_ids = get_just_ids(all_jobs, id_column)
    return all_ids


def check_job_status(status, path, job_id, id_column, status_column):
    jobs = get_jobs_by_id(path, id_column, job_id)
    return_status = False
    for job in jobs:
        if job[status_column] == status:
            return_status = True
    return return_status

#test = check_job_status('Dollco Printing-Proof In', 'Printflow-ToDo1.xls', "687556", 3, 2)
# print(test)
