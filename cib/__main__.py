import sys
import configparser
import pandas as pd
import elasticsearch
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from elasticsearch import Elasticsearch

config = configparser.ConfigParser()
config.read('cib/config.ini')

elastic_host = config['elasticsearch']['host']
elastic_port = config['elasticsearch']['port']
elastic_user = config['elasticsearch']['user']
elastic_pass = config['elasticsearch']['password']


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
        http_auth=(elastic_user, elastic_pass),
        scheme="http",
        port=elastic_port,
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


def extract_stop_words():
    """
    extract_stop_word
    """
    stop_words = set(stopwords.words('english'))
    df_names = pd.read_csv('cib/data/guo_magerman.csv')

    for index, row in df_names.iterrows():
        word_tokens = word_tokenize(row['magerman'].lower())
        # filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []

        for w in word_tokens:
            if w in stop_words:
                filtered_sentence.append(w)

        if filtered_sentence and (
            len(word_tokens) > 3) and "&" not in word_tokens:
            print(row['magerman'])
            print(filtered_sentence)


if __name__ == "__main__":
    # extract_stop_words()
    _main()
