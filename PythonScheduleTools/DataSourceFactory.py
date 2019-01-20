import json
import pprint
import unittest

import DataSources

DSFFILE = 'TestData/TestDataSources.json'


class DataSourceFactory:

    def __init__(self):
        self.sources = dict()

    def make_sources(self, id_list):
        all_sources = {}
        job_sources = {}
        with open(DSFFILE) as json_file:
            data_sources = json.load(json_file)

        for id_number in id_list:
            for key, value in data_sources.items():
                if 'Excel File' in value['Data Type']:
                    source = DataSources.ExcelStatus(value)
                if 'CSV Log File' in value['Data Type']:
                    source = DataSources.LogFileStatus(value)
                if 'Files' in value['Data Type']:
                    source = DataSources.FileStatus(value)
                if 'Folder' in value['Data Type']:
                    source = DataSources.FolderStatus(value)
                if 'File Name' in value['Data Type']:
                    source = DataSources.FileStatusByName(value)
                job_sources[key] = source
            # print(id_number)
            all_sources[id_number] = job_sources

        return all_sources


class DataSourceFactoryTests(unittest.TestCase):
    """DataSourceFactory unit tests"""

    def test_make_sources(self):
        """Check that DataSourceFactory can correctly instantiate a DataSource"""
        # Arrange
        DSF = DataSourceFactory()
        mock_id_list = ['687203', '689398', '690714', '684396']
        expected = True
        sources = DSF.make_sources(mock_id_list)

        # Act
        actual = sources['689398']['P drive Files - Huntclub'].check_status(
            'Files In', '689398')

        # Assert
        self.assertEqual(actual, expected)


unittest.main()
