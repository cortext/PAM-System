# mapping dictionary that contains the settings and
# _mapping schema for a new Elasticsearch index:

entities = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1,
        "provided_name": "entities",
        "analysis": {
            "filter": {
                "stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "stopwords": {
                    "type": "stop",
                    "stopwords": [
                        "_english_"
                    ]
                }
            },
            "analyzer": {
                "pamAnalyzer": {
                    "filter": [
                        "stopwords",
                        "lowercase",
                        "stemmer"
                    ],
                    "tokenizer": "pamTokenizer"
                }
            },
            "tokenizer": {
                "pamTokenizer": {
                    "type": "ngram",
                    "min_gram": 3,
                    "max_gram": 3,
                    "token_chars": [
                        "letter",
                        "digit"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "entity_id": {
                "type": "text"  # formerly "string"
            },
            "entity_name": {
                "type": "text",
                "analyzer": "pamAnalyzer"
            },
            "country": {
                "type": "text",
                "index": "not_analyzed",
                "search_analyzer": "keyword",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 2
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
}
