import sys
import click
import pandas as pd
import pam.helpers as helper
import pam.selector as selector
from pam.cleaner import normalizations
from pam.searchengine import SearchEngine
from pam.approximatematches import fuzzy


def run_pam_system(df_companies, company_name_column, query):
    """
    run_pam_system
    """

    df_companies = cleaner_processor(df_companies, company_name_column)
    df_elastic = search_engine_proccesor(df_companies,
                                                     company_name_column, query)
    df_pam = distance_matching_proccesor(df_elastic, query)

    return df_pam


def cleaner_processor(df_companies, company_name_column):
    """
    normalize_names
    """

    company_name = ""

    for index, row in df_companies.iterrows():
        example = str(row[company_name_column])
        company_name = normalizations.extract_stop_words(example)
        df_companies.loc[index, company_name_column] = company_name

    return df_companies


def search_engine_proccesor(df_companies, company_name_column, query):
    """
    The main routine.
    """

    not_found = 0
    total_found = 0

    print("Querying elasticsearch.....")

    search_engine = SearchEngine()
    search_engine.query = query
    data = []

    for index, row in df_companies.iterrows():
        print(row[company_name_column])
        search_engine.company_name = row[company_name_column]
        search_engine.country_filter = row['cnty_iso']
        match_result = search_engine.query_by_company()
        if not match_result:
            not_found = not_found + 1
        else:
            total_found = total_found + len(match_result)
        data = data + match_result

    match_result = data

    df_elastic = pd.DataFrame(match_result,
                              columns=['doc_std_name', 'doc_std_name_id',
                                       'orbis_name', 'number_patents',
                                       'elastic_score'])

    print("Total companies not found ", not_found)
    print("Total candidates for matching ", total_found)
    print("Total number of patents ", df_elastic['number_patents'].sum())

    return df_elastic


def distance_matching_proccesor(df_pam, query):
    """
    distance_matching_proccesor
    """

    for index, row in df_pam.iterrows():
        company_name = row['orbis_name']
        patstat_name = row['doc_std_name']
        elastic_score = row['elastic_score']
        score_list = fuzzy.run_distance_matching(company_name, patstat_name,
                                                 elastic_score, query)

        df_pam.loc[index,
                   'levensthein_score'] = score_list['levensthein_score']

        df_pam.loc[index,
                   'jaro_winkler_score'] = score_list['jaro_winkler_score']

        df_pam.loc[index, 'pam_score'] = score_list['pam_score']

    return df_pam


def selector_proccesor(df_pam):
    """
    distance_matching_proccesor
    """

    df_accurated_matches = selector.selector_accurate_matches(df_pam)

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
    # I need to have present that will be needed to implement an
    # exception handling for the variable query when doesn't exist

    df_companies = pd.read_csv(csv)
    company_name_column = column

    query = 'restricted_to_jurisdiction'
    df_pam_in_jurisdiction = run_pam_system(df_companies, company_name_column,
                                            query)
    selector.run_selector_processor(df_pam_in_jurisdiction)
    df_pam_in_jurisdiction.to_csv(output)

    # query = 'out_jurisdiction'
    # df_pam_out_juridiction = run_pam_system(df_companies, company_name_column,
    #                                         query)

    # helper.number_of_guos_detected()
    # helper.count_the_total_matches()
    #
    # df_companies = cleaner_processor(csv, company_name_column)
    # df_elastic_with_filter = search_engine_proccesor(df_companies,
    #                                                  company_name_column, True)
    # df_elastic_non_filter = search_engine_proccesor(df_companies,
    #                                                 company_name_column, False)
    # df_pam_with_filter = distance_matching_proccesor(df_elastic_with_filter)
    # df_pam_non_filter = distance_matching_proccesor(df_elastic_with_filter,
    #                                                 False)
    #
    # selector.run_selector_processor(df_pam)
    # df_pam.to_csv(output)
    #
    # del df_elastic
    # del df_pam
    #
    # df_elastic = search_engine_proccesor2(df_companies, column)
    # df_pam = distance_matching_proccesor(df_elastic)
    # selector.run_selector_processor2(df_pam)
    # df_pam.to_csv(output)
