import sys
import click
import configparser
import textdistance
import pandas as pd
import elasticsearch
from cib.cleaner import normalizations
from elasticsearch import Elasticsearch
from fuzzywuzzy import fuzz


config = configparser.ConfigParser()
config.read('cib/config.ini')

ELASTIC_HOST = config['elasticsearch']['host']
ELASTIC_PORT = config['elasticsearch']['port']
ELASTIC_USER = config['elasticsearch']['user']
ELASTIC_PASS = config['elasticsearch']['password']


def match_by_elastic(df_names, column):
    """
    The main routine.
    """
    global elastic
    not_found = 0
    total_found = 0

    print("Querying elasticsearch")

    elastic = Elasticsearch(
        ['localhost'],
        http_auth=(ELASTIC_USER, ELASTIC_PASS),
        scheme="http",
        port=ELASTIC_PORT,
    )

    data = []

    for index, row in df_names.iterrows():
        print(row[column])
        match_result = elastic_query(row[column], row['cnty_iso'])
        if not match_result:
            not_found = not_found + 1
        else:
            total_found = total_found + len(match_result)
        data = data + match_result

    match_result = data

    del df_names
    df_elastic = pd.DataFrame(match_result,
                             columns=['doc_std_name', 'doc_std_name_id',
                                      'orbis_name', 'number_patents',
                                      'elastic_score'])

    print("Total companies not found ", not_found)
    print("Total candidates for matching ", total_found)

    return df_elastic


def elastic_query(name, iso_country):
    """
    match_by_fuzzy
    """
    name = str(name)
    match_data = []

    try:
        res = elastic.search(index="cib_patstat_applicants2",
                             body={
                                  "size": 300,
                                  "min_score": 10,
                                  "query": {
                                    "bool": {
                                      "must":
                                        {
                                          "match": {
                                            "doc_std_name": name
                                          }
                                        },
                                        "filter": {
                                        "term": {
                                          "iso_ctry.keyword": iso_country
                                           }
                                        }
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
                           doc['_source']['n_patents'],
                           doc['_score']])
        # print("%s) %s" % (doc['_id'], doc['_source']['doc_std_name']))

    return match_data


def normalize_names(csv, column):
    """
    normalize_names
    """
    df_names = pd.read_csv(csv)
    company_name = ""

    for index, row in df_names.iterrows():
        example = str(row[column])
        company_name = normalizations.extract_stop_words(example)
        df_names.set_value(index, column, company_name)

    return df_names


def distance_matching_proccesor(df_pam):

    for index, row in df_pam.iterrows():
        ratio = fuzz.token_sort_ratio(row['orbis_name'].lower(),
                                         row['doc_std_name'].lower())
        jaro_winkler_score = textdistance.jaro_winkler(
                                         row['orbis_name'].lower(),
                                         row['doc_std_name'].lower())
        elastic_score = row['elastic_score']
        name_length = len(row['orbis_name'].split())
        if name_length > 5 : elastic_score -= 10
        distance_score = calculate_distance_score(ratio, jaro_winkler_score,
                                                  name_length)
        final_score = pam_score(20, elastic_score, distance_score)
        df_pam.set_value(index, 'levensthein_score', ratio)
        df_pam.set_value(index, 'jaro_winkler_score', jaro_winkler_score)
        df_pam.set_value(index, 'pam_score', final_score)

    return df_pam

def pam_score(filter, elastic_score, distance_score):
    if elastic_score < 13:
        new_elastic_score = 0
    elif elastic_score < 15:
        new_elastic_score = 30 * 0.2
    elif elastic_score < 20:
        new_elastic_score = 60 * 0.2
    else:
        new_elastic_score = 100 * 0.2

    pam_score = new_elastic_score + (distance_score * 0.6) + filter

    return pam_score

def calculate_distance_score(levensthein_score, jaro_winkler_score,
                             name_length):
    if name_length > 5 and levensthein_score < 80 : levensthein_score -= 20
    if name_length > 5 and jaro_winkler_score < 0.8 : jaro_winkler_score -= 0.2

    return (levensthein_score * 0.7) + ((jaro_winkler_score * 100) * 0.3)


@click.command()
@click.option('--csv', default='/data/loads/companies.csv',
              help='Csv file that contains the companies list.')
@click.option('--column', default='company_name',
              help='Define the name of the column which contains '
              'the companies names.')
@click.option('--output', default='data/results/pam_results.csv',
              help='The output file where results are stored.')
def cli(csv, column, output):
    """
    cli
    """
    df_companies = normalize_names(csv, column)
    df_elastic = match_by_elastic(df_companies, column)
    df_pam = distance_matching_proccesor(df_elastic)
    df_pam.to_csv(output)


if __name__ == "__main__":
    cli()
