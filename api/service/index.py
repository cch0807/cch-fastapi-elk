from elasticsearch import Elasticsearch


class IndexService:
    def __init__(self):
        self.es: Elasticsearch = Elasticsearch("elastic:9200")

    def get_es(self):
        return self.es

    def get_index(self, index_name):
        res = self.es.indices.get(index=index_name)

        return res

    def create_index(self, index_name):
        if self.es.indices.exists(index=index_name):
            return False
        res = self.es.indices.create(index=index_name)

        return res

    def create_index_data(self, index_name, data):
        self.es.index(index=index_name, body=data)

        return True

    def delete_index(self, index_name):
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)

    def delete_index_data(self, index_name):
        pass
