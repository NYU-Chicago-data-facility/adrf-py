from . import remote_models
import requests
import json


class Table(remote_models.RemoteModel):
    remote_host = "http://localhost:8000"
    remote_endpoint = remote_host + "/api/v1/datatables"
    remote_id_field = 'name'
    model = 'Table'


class Dataset(remote_models.RemoteModel):
    remote_host = "http://localhost:8000"
    remote_endpoint = remote_host + "/api/v1/datasets"
    remote_id_field = 'dataset_id'
    model = 'Dataset'

    @property
    def table_names(self):
        return [t.name for t in self.__tables()]

    def __tables(self):
        response = requests.get(url=Table.remote_endpoint + '?dataset=' + self.id)
        if response.status_code == 200:
            tables = []
            for table in response.json():
                tables += [Table(dfrn=table['name'], remote_url=table['url'])]
            return tables
        else:
            raise remote_models.RemoteObjectNotFound('Error getting tables for {0} identified by {1}.'.format(self.model, self.dfrn))

    def table(self, table_name):
        for t in self.__tables():
            if t.name == table_name:
                return t
        return None




