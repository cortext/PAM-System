import configparser
import elasticsearch
from elasticsearch import Elasticsearch


class SearchEngine():
    """
    Application-level class, builds the application
    """

    def __init__(self, **kwargs):
        """
        Initialize a new Elasticsearch connection.
        """

        # init the connection variables
        self.build_parameters()
        # create an elastic search connection
        self.connection = self.init_connection()

    def build_parameters(self, config_file='pam/config.ini'):
        """
        Configure the application.
        """

        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        self.ELASTIC_HOST = self.config['elasticsearch']['host']
        self.ELASTIC_PORT = self.config['elasticsearch']['port']
        self.ELASTIC_USER = self.config['elasticsearch']['user']
        self.ELASTIC_PASS = self.config['elasticsearch']['password']

        self.company_name = None
        self.country_filter = None
        self.company_id = None
        self.name_type = None
        self.query = 'worldwide'

    def init_connection(self):
        """
        Set connection
        """

        connection = Elasticsearch(
            ['localhost'],
            http_auth=(self.ELASTIC_USER, self.ELASTIC_PASS),
            scheme="http",
            port=self.ELASTIC_PORT,
        )

        return connection

    def query_by_company(self):
        """
        query_by_company
        """

        match_data = []
        self.company_name = str(self.company_name)
        query = self.query_builder()

        try:
            res = self.connection.search(index="cib_patstat_applicants2",
                                         body=query)
        except elasticsearch.ElasticsearchException as es1:
            print("Company name: ", self.company_name) 
            print("Error:", es1)
            match_data.append(["", "", self.company_id,
                               self.company_name, self.name_type, 0, 0])
            return match_data

        for doc in res['hits']['hits']:
            match_data.append([doc['_source']['doc_std_name'],
                               doc['_source']['doc_std_name_id'],
                               self.company_id, self.company_name,
                               self.name_type, doc['_source']['n_patents'],
                               doc['_score']])

        return match_data

    def query_builder(self):
        """
        query_builder
        """

        if self.query == 'restricted_to_jurisdiction':
            query = {
                "size": 3,
                "min_score": 10,
                "query": {
                    "bool": {
                        "must":
                        {
                            "match": {
                                "doc_std_name": {
                                    "query": self.company_name
                                }
                            }
                        },
                        "filter": {
                            "term": {
                                "iso_ctry.keyword": self.country_filter
                            }
                        }
                    }
                }
            }
        elif self.query == 'out_jurisdiction':
            query = {
                "size": 3,
                "min_score": 10,
                "query": {
                    "bool": {
                        "must":
                        { 
                            "match": {
                                "doc_std_name": {
                                    "query": self.company_name 
                                }
                            }
                        },
                        "must_not": {
                            "match": {
                                "iso_ctry.keyword": self.country_filter
                            }
                        }
                    }
                }
            }

        return query
