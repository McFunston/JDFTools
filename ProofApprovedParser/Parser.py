import sys
import xml.etree.ElementTree as ET
import CSVReader
import csv
from datetime import datetime
from datetime import timedelta
path = 'Approved.xml'

def datetime_parser(dt):
    return datetime.strptime(dt, '%a %b %d %H:%M:%S %Y')

def get_jobs_list(path):
    new_log = list()
    tree = ET.parse(path)
    root = tree.getroot()
    job_ids = list()
    
    SSValue = root.getchildren()[3]
    Rows = SSValue.getchildren()
    for Row in Rows:
        Columns = Row.getchildren()

        for column in Columns:
            # print (column.attrib['Name'])
            if column.attrib['Name'] == 'job_id':
                job_ids.append(column.text)     

    job_ids = set(job_ids)
    job_ids = list(job_ids)
    job_ids.sort()
    for id in job_ids:
        new_log.append([datetime.now().ctime(), id])
    return new_log

def approval_logger (xml_path, csv_path):
    try:
        file = open(csv_path, 'r')
    except IOError:
        file = open(csv_path, 'w')
        print("ruh roh")
    finally:
        file.close()
    current_log = CSVReader.read_log(csv_path)
    jobs = get_jobs_list(xml_path)
    log = list()
    log = [[l[0], l[1]] for l in current_log if datetime_parser(l[0]) > datetime.today() - timedelta(days=60)]
    # jobs_to_add = list()
    for job in jobs:
        if not_in_log(job, log):
            # print('Trying to add ' + file[1])
            log.append(job)
    with open(csv_path, 'w', newline='', encoding='latin-1') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for file_to_add in log:
            writer.writerow(file_to_add)

def not_in_log(job, log):
    not_in = True
    for entry in log:
        if entry[1] == job[1]:
            not_in = False
            return not_in
    return not_in


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Arguments 'xml path' and 'csv path' required")
    else:
        approval_logger(sys.argv[1], sys.argv[2])