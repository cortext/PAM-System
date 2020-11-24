# mapping dictionary that contains the settings and
# _mapping schema for a new Elasticsearch index:

entities = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1,
        "provided_name": "entities"
    },
    "mappings": {
        "properties": {
            "entity_id": {
                "type": "text"  # formerly "string"
            },
            "entity_name": {
                "type": "text",
                "analyzer": "test"
            },
            "country": {
                "type": "text",
                "analyzer": "keyword",
                "search_analyzer": "keyword",
                "fields":{
                    "keyword":{
                        "type":"keyword",
                        "ignore_above":2
                    }
                }
            },
            "dataset_id": {
                "type": "integer"
            },
            "dataset": {
                "type": "text"
            }
        }
    }
