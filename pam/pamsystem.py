import pandas as pd
# import pam.helpers as helper
import pam.selector as selector
from pam.cleaner import normalizations
from pam.searchengine import SearchEngine
from pam.approximatematches import fuzzy


class PamSystem():
    """
    Application-level class, builds the application
    """

    QUERIES = ['restricted_to_jurisdiction', 'out_jurisdiction']

    def __init__(self, **kwargs):
        """
        Initialize a new Elasticsearch connection.
        """

        # init the PAM System attributes
        self.df_companies = ''
        self.company_name_column = ''
        self.country_column = ''
        self.query = ''
        self.df_elastic = pd.DataFrame()
        self.df_pam = pd.DataFrame()
        self.df_accurate_matches = pd.DataFrame()
        self.df_wrong_matches = pd.DataFrame()
        self.df_to_check_matches = pd.DataFrame()

    def _run(self):
        """
        _run
        """

        self.cleaner_processor()
        self.search_engine_proccesor()
        self.distance_matching_proccesor()
        # self.df_pam = helper.groupby_pam_dataframe(self.df_pam)
        self.selector_processor()

    def cleaner_processor(self):
        """
        cleaner_processor
        """

        print("Running processor.....")
        company_name = ""

        for index, row in self.df_companies.iterrows():
            example = str(row[self.company_name_column])
            company_name = normalizations.extract_stop_words(example)
            self.df_companies.loc[index,
                                  self.company_name_column] = company_name

    def search_engine_proccesor(self):
        """
        search_engine_proccesor.
        """

        not_found = 0
        total_found = 0

        print("Querying elasticsearch.....")

        search_engine = SearchEngine()
        search_engine.query = self.query
        data = []

        for index, row in self.df_companies.iterrows():
            # print(row[self.company_name_column])
            search_engine.company_name = row[self.company_name_column]
            search_engine.country_filter = row['cnty_iso']
            search_engine.company_id = row['new_bvd_id']
            search_engine.name_type = row['name_type']
            match_result = search_engine.query_by_company()
            if not match_result:
                not_found = not_found + 1
            else:
                total_found = total_found + len(match_result)
            data = data + match_result

        match_result = data

        self.df_elastic = pd.DataFrame(match_result,
                                       columns=['doc_std_name',
                                                'doc_std_name_id',
                                                'orbis_id', 'orbis_name',
                                                'name_type', 'number_patents',
                                                'elastic_score'])

        print("Total companies not found ", not_found)
        print("Total candidates for matching ", total_found)
        print("Total number of patents ",
              self.df_elastic['number_patents'].sum())

    def distance_matching_proccesor(self):
        """
        distance_matching_proccesor
        """

        print("Running distance matching processor.....")

        self.df_pam = self.df_elastic

        for index, row in self.df_pam.iterrows():
            company_name = row['orbis_name']
            patstat_name = row['doc_std_name']
            elastic_score = row['elastic_score']

            score_list = fuzzy.run_distance_matching(company_name,
                                                     patstat_name,
                                                     elastic_score, self.query)

            self.df_pam.loc[index,
                            'levensthein_score'] = score_list[
                                    'levensthein_score']

            self.df_pam.loc[index,
                            'jaro_winkler_score'] = score_list[
                                    'jaro_winkler_score']

            self.df_pam.loc[index,
                            'ratcliff_obershelp_score'] = score_list[
                                    'ratcliff_obershelp_score']

            self.df_pam.loc[index, 'pam_score'] = score_list['pam_score']

            self.df_pam.loc[index, 'query'] = self.query
            self.df_pam.loc[index, 'orbis_id'] = str(row['orbis_id'])
            self.df_pam.loc[index, 'name_type'] = row['name_type']

    def selector_processor(self):
        """
        selector_proccesor
        """

        print("Running selector processor.....")

        self.df_accurate_matches = selector.selector_accurate_matches(
            self.df_pam)
        self.df_wrong_matches = selector.selector_wrong_matches(self.df_pam)
        self.df_to_check_matches = selector.selector_matches_to_check(
            self.df_pam)

    def set_df_companies(self, csv):
        self.df_companies = pd.read_csv(csv)
        # self.df_companies = pd.read_csv(csv, encoding='ISO-8859-1')
