#!/usr/bin/env python3
"""Utilities to do with the the DataSources.json file"""
import json

def get_data_sources():
    """Returns the contents of the DataSources.json file"""
    with open('DataSources.json') as json_file:
        data_sources = json.load(json_file)
    return data_sources
