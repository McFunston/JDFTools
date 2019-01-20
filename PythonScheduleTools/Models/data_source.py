#!/usr/bin/env python3
"""A single source of data by which to determine the status of a job"""


class DataSource():
    """A single source of data by which to determine the status of a job"""

    def __init__(self, job_id, service, data_source_args):
        self.path = data_source_args['Path']
        self.source_name = data_source_args['Source Name']
        self.status = data_source_args['Status']
        self.service = service
        self.job_id = job_id
        
