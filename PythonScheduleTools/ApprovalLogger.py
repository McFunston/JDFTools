#!/usr/bin/env python3
import FolderChecker
import sys
import csv
import CSVReader
import PDFFormChecker

from datetime import datetime
from datetime import timedelta

def datetime_parser(dt):
    return datetime.strptime(dt, '%a %b %d %H:%M:%S %Y')

def get_jobs_list(path):
    job_list = FolderChecker.get_folder_list(path)
    return job_list

def get_full_path(path, job, sub_path):
    full_path = path + '/' + job + sub_path
    return full_path

def logger(path, csv_path, sub_path):
    try:
        file = open(csv_path, 'r')
    except IOError:
        file = open(csv_path, 'w')
    finally:
        file.close()
    job_list = get_jobs_list(path)
    current_log = CSVReader.read_log(csv_path)
    log = list()
    log = [[l[0], l[1]] for l in current_log if datetime_parser(l[0]) > datetime.today() - timedelta(days=60)]
    logged_jobs = [l[1] for l in log]
    for job in job_list:
        if str(job) not in logged_jobs:
            full_path = get_full_path(path, job, sub_path)
            forms = FolderChecker.get_file_list_with_date_no_subs(full_path)
            
            for form in forms:
                log_entry = list()
                log_entry.append(form[0])
                log_entry.append(job)
                potential_log_addition = list()
                potential_log_addition.append(log_entry)
                if datetime_parser(form[0]) > datetime.today() - timedelta(days=14): 
                        if PDFFormChecker.PDFFormChecker(full_path + "/" + form[1], 'PROOF OK AS SUBMITTED', 'Yes'):
                            log.append(log_entry)
    with open(csv_path, 'w', newline='', encoding='latin-1') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for file_to_add in log:
            writer.writerow(file_to_add)
logger('/Volumes/Dockets', '/Users/MicaFunston/Downloads/ApprovedJobs.csv', '/PREPRESS/PROOFSLIP')