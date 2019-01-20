#!/usr/bin/env python3
"""Tools for extracting job info from CSV files"""
import csv
import unittest

import ListShaper

def read_log(file_name):

    #csvfile = open(file_name, newline='', encoding='latin-1', mode='r')
    with open(file_name, newline='', encoding='latin-1', mode='r') as csvfile:
        reader = csv.reader(x.replace('\0', '') for x in csvfile)    
        log = [log_items for log_items in reader]
    return log


def find_in_csv(file_name, search_strings):
    """Find a string within a CSV file
    Args:
        file_name: Name of csv file to search
        search_string: String to be searched for
    Returns: A list of dates and print jobs
    """
    with open(file_name, newline='', encoding='latin-1') as csvfile:
        reader = csv.reader(x.replace('\0', '') for x in csvfile)
        findings = list()
        read = [r for r in reader]
        for search_string in search_strings:
            for r in read:
                if len(r) > 1 and str(search_string) in str(r[1]):
                    findings.append([r[0], r[1]])

    return findings

def list_jobs(file_name):
    log = read_log(file_name)
    
    jobs = ListShaper.job_lister(log)
    return jobs

class CSVReader(unittest.TestCase):
    def test_read_log(self):
        #Arrange
        log = read_log('TestData/ProofLog.csv')
        expected = 'Tue May 16 12:09:08 2017'
        #Act
        actual = log[0][0]
        #Assert
        self.assertEqual(actual, expected)

#jobs = list_jobs('TestData/ProofLog.csv')
#print(jobs)

#if __name__ == '__main__':
#    unittest.main()
