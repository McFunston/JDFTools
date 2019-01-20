#!/usr/bin/env python3
"""Basic job class. Contains all possible status sources for a single job"""

class Job(object):
    """Basic job class. Contains all possible status sources for a single job"""
    def __init__(self, name):
        self.name = name
        self.data_sources = {}

    def add_source(self, source):
        """Add a new data source to the data_sources dictionary,
        overwriting any that already have that name
        Arg:
            source: new data source"""
        self.data_sources = {**self.data_sources, **source}
