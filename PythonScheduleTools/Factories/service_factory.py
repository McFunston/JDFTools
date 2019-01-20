#!/usr/bin/env python3
"""A factory for creating a checker/reader object for a data source"""
import Services.FileReader
import Services.CSVReader
import Services.ExcelReader
import Services.FolderReader

def create_service(data_source_dict):
    """Create the correct service based on a data_source_dict"""
    source = data_source_dict['Data Type']
    if source == 'Files' or source == 'File Name':
        service = Services.FileReader.FileReader(data_source_dict)
    if source == 'Excel File':
        service = Services.ExcelReader.ExcelReader(data_source_dict)
    if source == 'CSV Log File':
        service = Services.CSVReader.CSVReader(data_source_dict)
    if source == 'Folder':
        service = Services.FolderReader.FolderReader(data_source_dict)
    return service
