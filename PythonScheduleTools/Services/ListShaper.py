import unittest
import re
from datetime import datetime


def find_earlier(item1, item2):
    """Given two jobs [date, string] returns the earlier one"""
    item1_date_time = datetime.strptime(item1[0], '%a %b %d %H:%M:%S %Y')
    item2_date_time = datetime.strptime(item2[0], '%a %b %d %H:%M:%S %Y')
    if item1_date_time < item2_date_time:
        return item1
    else:
        return item2

def space_strip(list_to_strip):
    """Removes unecessary spaces from a list of [date, string]
    Args:
    list_to_strip: A list of cells
    Returns: A list of strings"""
    stripped_list = list()
    for item_to_strip in list_to_strip:
        item_to_strip[1] = item_to_strip[1].strip()
        stripped_list.append(item_to_strip)
    #stripped_list = [x.strip() for x in list_to_strip]
    return stripped_list

def job_lister(results):
    shaped_results = list()
    jobs = list()
    found_jobs = list()
    for result in results:
        #r = (re.search("(?<!\d)\d{6}(?!\d)", result[1]))
        r = (re.search(r'(?<!\d)\d{6}(?!\d)', result[1]))
        if r != None:
            jobs.append(r.group(0))
    for job in jobs:
        found_jobs.append(job)
        found_jobs = list(set(found_jobs))
        found_jobs.sort()
    return found_jobs

def find_job(jobs_list, search_string):
    """Searches for search_string within a jobs list [Date, String]. Returns a list of [Date, String]"""
    found_jobs = list()
    for job in jobs_list:
        if search_string in job[1]:
            found_jobs.append(job)
    return found_jobs

def job_counter(jobs_list, job_number):
    """Returns the number of times that job_number occurs in a list of [date, string]"""
    count = 0
    for job in jobs_list:
        if job_number in job[1]:
            count += 1            
    return count


class MyTest(unittest.TestCase):
    item1 = ['Tue May 30 09:15:42 2017', "item1r684500"]
    item2 = ['Wed May 24 15:44:57 2017', "700000item2"]
    item3 = ['Wed May 24 15:44:57 2017', "item3r684500item2"]
    item4 = ['Tue May 30 09:15:42 2017', "item1r685300 "]
    items = list()
    items.append(item1)
    items.append(item2)
    items.append(item3)
    items.append(item4)

    def test_find_earlier(self):
        # Arrange

        expected = self.item2
        # Act
        actual = find_earlier(self.item1, self.item2)
        # Assert
        self.assertEqual(actual, expected)

    def test_job_lister(self):
        # Arrange
        expected = ["684500", '685300', "700000"]
        # Act
        actual = job_lister(self.items)
        # Assert
        self.assertEqual(actual, expected)

    def test_job_counter(self):
        # Arrange
        expected = 2
        # Act
        actual = job_counter(self.items, "684500")
        # Assert
        self.assertEqual(actual, expected)

    def test_space_strip(self):
        # Arrange
        expected = ['Tue May 30 09:15:42 2017', "item1r685300"]
        # Act
        actual = space_strip(self.items)
        actual = actual[3]
        # Assert
        self.assertEqual(actual, expected)
    
    def test_find_job(self):
        # Arrange
        expected = [['Tue May 30 09:15:42 2017', "item1r685300 "]]
        # Act
        actual = find_job(self.items, '685300')
        # Assert
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
