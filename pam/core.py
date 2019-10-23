import sys
import click
import pandas as pd
import pam.selector as selector
from pam.cleaner import normalizations
from pam.searchengine import SearchEngine
from pam.approximatematches import fuzzy


def cleaner_processor(csv, column):
    """
    normalize_names
    """
    df_names = pd.read_csv(csv)
    company_name = ""

    for index, row in df_names.iterrows():
        example = str(row[column])
        company_name = normalizations.extract_stop_words(example)
        df_names.loc[index, column] = company_name

    return df_names


def search_engine_proccesor(df_names, column):
    """
    The main routine.
    """
    not_found = 0
    total_found = 0

    print("Querying elasticsearch.....")

    search_engine = SearchEngine()
    data = []

    for index, row in df_names.iterrows():
        print(row[column])
        search_engine.company_name = row[column]
        search_engine.country_filter = row['cnty_iso']
        match_result = search_engine.query_by_company()
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
    print("Total number of patents ", df_elastic['number_patents'].sum())

    return df_elastic


def distance_matching_proccesor(df_pam):
    """
    distance_matching_proccesor
    """
    for index, row in df_pam.iterrows():
        company_name = row['orbis_name']
        patstat_name = row['doc_std_name']
        elastic_score = row['elastic_score']
        score_list = fuzzy.run_distance_matching(company_name, patstat_name,
                                                 elastic_score)

        df_pam.loc[index,
                   'levensthein_score'] = score_list['levensthein_score']

        df_pam.loc[index,
                   'jaro_winkler_score'] = score_list['jaro_winkler_score']

        df_pam.loc[index, 'pam_score'] = score_list['pam_score']

    return df_pam


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
    df_companies = cleaner_processor(csv, column)
    df_elastic = search_engine_proccesor(df_companies, column)
    df_pam = distance_matching_proccesor(df_elastic)
    selector.run_selector_processor(df_pam)
    df_pam.to_csv(output)
