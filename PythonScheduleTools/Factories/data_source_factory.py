#!/usr/bin/env python3
"""A factory for creating data sources"""
import Models.data_source as ds
import service_factory


class DataSourceFactory():
    """A factory for creating data sources"""

    def _merge_path(self, job_id, data_source_dict):
        """Merges the path, job id, and subpath. Returns it as a string"""
        if 'Sub Path' in data_source_dict:
            merged_path = data_source_dict['Path'] + \
                job_id + data_source_dict['Subpath']
            del data_source_dict['Subpath']
        else:
            merged_path = data_source_dict['Path']
        return merged_path

    def create_data_source(self, job_id, data_source_dict):
        """Creates one data source given a job id, and a data_source_dict (from DataSources.json)"""
        data_source_args = {}
        service = service_factory.create_service(data_source_dict)
        path = self._merge_path(job_id, data_source_dict)
        data_source_args['Path'] = path
        data_source_args['Source Name'] = data_source_dict['Source Name']
        data_source_args['Status'] = data_source_dict['Status']
        data_source = ds.DataSource(job_id, service, data_source_args)
        return data_source

    def create_data_source_list(self, job_id_list, data_source_dict):
        """Creates a list of data sources given a list of ids and a data_source_dict"""
        data_sources = list()
        for job_id in job_id_list:
            data_source = self.create_data_source(job_id, data_source_dict)
            data_sources.append(data_source)
        return data_sources
