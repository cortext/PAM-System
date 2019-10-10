import sys
import pandas as pd
import elasticsearch
from elasticsearch import Elasticsearch


def _main(args=None):
    """
    The main routine.
    """
    global elastic

    if args is None:
        args = sys.argv[1:]

    print("Querying elasticsearch")

    elastic = Elasticsearch(
        ['localhost'],
        http_auth=('elastic_user', 'elastic_pass'),
        scheme="http",
        port=9200,
    )

    df_names = pd.read_csv('path/to/file')
    data = []

    for index, row in df_names.iterrows():
        print(row['original'])
        match_result = match_by_fuzzy(row['original'], row['cnty_iso'])
        data = data + match_result

    match_result = data

    df_export = pd.DataFrame(match_result,
                             columns=['doc_std_name', 'doc_std_name_id',
                                      'orbis_name', 'score'])
    df_export.to_csv('patstat_match.csv')


def match_by_fuzzy(name, iso_country):
    """
    match_by_fuzzy
    """
    name = str(name)
    match_data = []

    try:
        res = elastic.search(index="cib_patstat_applicants2",
                             body={
                                  "size": 100,
                                  "min_score": 16,
                                  "query": {
                                    "bool": {
                                      "must": [
                                        {
                                          "match": {
                                            "doc_std_name": name + "?"
                                          }
                                        },
                                        {
                                          "match": {
                                            "iso_ctry": iso_country
                                          }
                                        }
                                      ]
                                    }
                                  }
                                })
    except elasticsearch.ElasticsearchException as es1:
        print("Error:", es1)
        match_data.append(["", "", name, ""])
        return match_data

    print(" documents found", res['hits']['total'])

    for doc in res['hits']['hits']:
        match_data.append([doc['_source']['doc_std_name'],
                           doc['_source']['doc_std_name_id'], name,
                           doc['_score']])
        # print("%s) %s" % (doc['_id'], doc['_source']['doc_std_name']))

    return match_data


def read_data():
    """
    prueba
    """

    return 0


if __name__ == "__main__":
    _main()
