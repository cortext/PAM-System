import sys
import click
import configparser
import pandas as pd
import elasticsearch
from cib.cleaner import normalizations
from elasticsearch import Elasticsearch

config = configparser.ConfigParser()
config.read('cib/config.ini')

ELASTIC_HOST = config['elasticsearch']['host']
ELASTIC_PORT = config['elasticsearch']['port']
ELASTIC_USER = config['elasticsearch']['user']
ELASTIC_PASS = config['elasticsearch']['password']


def _main(args=None):
    """
    The main routine.
    """
    global elastic
    not_found = 0

    if args is None:
        args = sys.argv[1:]

    print("Querying elasticsearch")

    elastic = Elasticsearch(
        ['localhost'],
        http_auth=(ELASTIC_USER, ELASTIC_PASS),
        scheme="http",
        port=ELASTIC_PORT,
    )

    df_names = pd.read_csv('data/load/sample_companies_name.csv')
    data = []

    for index, row in df_names.iterrows():
        print(row['companies'])
        match_result = match_by_fuzzy(row['companies'], row['cnty_iso'])
        if not match_result:
            not_found = not_found + 1
        data = data + match_result

    match_result = data

    df_export = pd.DataFrame(match_result,
                             columns=['doc_std_name', 'doc_std_name_id',
                                      'orbis_name', 'score'])
    df_export.to_csv('data/results/sample_patstat_matching.csv')
    print("total companies not found ", not_found)


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
                                  "min_score": 12,
                                  "query": {
                                          "match": {
                                            "doc_std_name": name + "~"
                                          }
                                        }
                                  })
    except elasticsearch.ElasticsearchException as es1:
        print("Error:", es1)
        match_data.append(["", "", name, ""])
        return match_data

    print("documents found", res['hits']['total'])

    for doc in res['hits']['hits']:
        match_data.append([doc['_source']['doc_std_name'],
                           doc['_source']['doc_std_name_id'], name,
                           doc['_score']])
        # print("%s) %s" % (doc['_id'], doc['_source']['doc_std_name']))

    return match_data


@click.command()
@click.option('--csv', default='input.csv',
              help='Csv file that contains the companies list.')
def normalize_names(csv):
    """
    prueba
    """
    df_names = pd.read_csv(csv)

    for index, row in df_names.iterrows():
        example = row['companies']
        normalizations.extract_stop_words(example)

    return 0


if __name__ == "__main__":
    # extract_stop_words()
    # _main()
    normalize_names()
