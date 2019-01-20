#!/usr/bin/env python3
"""A utility to add any new folders in a given folder to a comma separated text file"""
import sys
import csv
import CSVReader
import FolderChecker
from datetime import datetime
from datetime import timedelta

def datetime_parser(dt):
    return datetime.strptime(dt, '%a %b %d %H:%M:%S %Y')

def jdf_logger(folder, logfile):
    files = FolderChecker.get_folder_list_with_date(folder)
    csv_path = '/Users/MicaFunston/Downloads/' + logfile
    try:
        file = open(csv_path, 'r')
    except IOError:
        file = open(csv_path, 'w')
        print("ruh roh")
    finally:
        file.close()
    current_log = CSVReader.read_log(csv_path)
    log = list()
    log = [[l[0], l[1]] for l in current_log if datetime_parser(l[0]) > datetime.today() - timedelta(days=60)]
    #log = [[l[0], l[1]] for l in current_log]
    files_to_add = list()
    for file in files:
        if file not in log:
            # print('Trying to add ' + file[1])
            log.append(file)
    # log.append(files_to_add)
    with open(csv_path, 'w', newline='', encoding='latin-1') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for file_to_add in log:
            writer.writerow(file_to_add)
# quotechar='|'

#jdf_logger('/Volumes/Dockets/Impositions', 'jdfs.csv')

#folder_watcher("//192.168.113.50/share/", "ProofLog2.csv")
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Arguments 'folder' and 'logfile' required")
    else:
        jdf_logger(sys.argv[1], sys.argv[2])
