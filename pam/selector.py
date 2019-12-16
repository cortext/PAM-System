import pandas as pd
import math


class PamSelector():

    base_matches_query = {
            'min_score': 66,
            }

    accurate_matches_query = {
            'min_score': 76,
            'score_patent_condition': 66,
            'number_patents': 11
            }

    def __init__(self, pam_results):
        """
        Initialize a new selector instance.
        """

        # init the PAM Selector attributes
        self.df_base_matches = pd.DataFrame()
        self.df_pam = pam_results
        self.df_accurate_matches = pd.DataFrame()
        self.df_wrong_matches = pd.DataFrame()
        self.df_to_check_matches = pd.DataFrame()

    def _run(self):
        """
        _run
        """

        self.selector_base_matches()
        self.selector_accurate_matches()
        self.selector_matches_to_check()
        self.selector_wrong_matches()
        # self.selector_enrich_not_found()
        # self.selectro_enrich_low_patents()

    def selector_base_matches(self):
        """
        selector_base_matches
        """
        df_pam = self.df_pam
        base_matches_query = self.base_matches_query

        base_matches = df_pam[(df_pam['pam_score'] >=
                              base_matches_query['min_score'])]

        base_matches = base_matches.append(
                base_matches[(base_matches['pam_score'] >= 73) |
                             (base_matches['number_patents'] >= 10) |
                             (base_matches['elastic_score'] >= 13) |
                             (base_matches['jaro_winkler_score'] >= 0.92) |
                             (base_matches['orbis_name'].str.split(
                             ).str.len().lt(2))
                             ])

        self.df_base_matches = base_matches

    def selector_accurate_matches(self):
        """
        selector_accurate_matches
        """

        base_matches = self.df_base_matches
        accurate_matches_query = self.accurate_matches_query
        df_pam = self.df_pam

        accurate_matches = base_matches[(base_matches['pam_score'] >=
                                        accurate_matches_query['min_score'])]

        accurate_matches = accurate_matches.append(
                base_matches[(base_matches['pam_score'] >
                             accurate_matches_query['score_patent_condition'])
                             & (base_matches['pam_score'] <
                                 accurate_matches_query['min_score'])
                             & (base_matches['number_patents'] <
                                 accurate_matches_query['number_patents'])
                             ])

        accurate_matches = accurate_matches.append(df_pam[
            (df_pam['levensthein_score'] >= 65) &
            (df_pam['jaro_winkler_score'] >= 0.89)
            ])

        accurate_matches = self.query_by_parameterization(
                accurate_matches, levensthein_score=70,
                jaro_w_score=0.7, ratcliff_score=0.7)

        accurate_matches = self.query_by_parameterization(
                accurate_matches, elastic_score=11,
                jaro_w_score=0.89, pam_score=68)

        accurate_matches = self.query_by_parameterization(
                accurate_matches, jaro_w_score=0.85,
                pam_score=71)

        accurate_matches = self.query_by_parameterization(
                accurate_matches, elastic_score=19,
                jaro_w_score=0.85, ratcliff_score=0.78,
                pam_score=78)

        accurate_matches = self.query_by_parameterization(
                accurate_matches, elastic_score=14.3, levensthein_score=71,
                ratcliff_score=0.85, n_patents=100)

        accurate_matches = accurate_matches[
                (accurate_matches['pam_score'] >= 72) |
                (accurate_matches['elastic_score'] >= 13) |
                (accurate_matches['jaro_winkler_score'] >= 0.93) |
                (accurate_matches['levensthein_score'] >= 77) |
                (accurate_matches['orbis_name'].str.split().str.len().lt(2)) |
                (len(accurate_matches['orbis_name']) < 13)
                ]

        self.df_accurate_matches = accurate_matches

    def selector_wrong_matches(self):
        """
        selector_wrong_matches
        """
        df_base_matches = self.df_base_matches
        df_pam = self.df_pam

        df_wrong = df_pam.merge(df_base_matches[['orbis_id',
                                                'doc_std_name_id']],
                                indicator=True, how='outer',
                                on=['orbis_id', 'doc_std_name_id'])

        df_wrong = df_wrong[df_wrong['_merge'] == 'left_only']

        self.df_wrong_matches = df_wrong

    def selector_matches_to_check(self):
        """
        selector_matches_to_check
        """

        df_base_matches = self.df_base_matches
        df_accurate_matches = self.df_accurate_matches

        matches_to_check = df_base_matches.merge(
                df_accurate_matches[['orbis_id', 'doc_std_name_id']],
                indicator=True, how='outer',
                on=['orbis_id', 'doc_std_name_id']
                )

        matches_to_check = matches_to_check[
                matches_to_check['_merge'] == 'left_only'
                ]

        self.df_to_check_matches = matches_to_check

    def selector_enrich_not_found(self):
        """
        selector_enriching_not_found
        """

        df_wrong = self.df_wrong_matches
        df_accurate = self.df_accurate_matches
        df_to_check = self.df_to_check_matches

        companies_not_found = df_wrong[
            (~df_wrong.orbis_id.isin(df_accurate.orbis_id))
            & (~df_wrong.orbis_id.isin(df_to_check.orbis_id))
            ]

        not_found_many_patents = companies_not_found[
                companies_not_found['number_patents'] > 10]

        companies_not_found = not_found_many_patents.append(
            companies_not_found[~companies_not_found.orbis_id.isin(
                not_found_many_patents.orbis_id)]
            )

        self.df_to_check_matches = df_to_check.append(companies_not_found)

    def selector_enrich_low_patents():
        return True

    def query_by_parameterization(
            self, pam_type_df, elastic_score=math.inf,
            levensthein_score=math.inf, jaro_w_score=math.inf,
            ratcliff_score=math.inf, pam_score=math.inf, n_patents=math.inf,
            company_max_name_len=0):
        """
        selector_matches_to_check
        """

        # Pam type Dataframe for querying
        df = pam_type_df

        results = df[
                (df['elastic_score'] >= elastic_score) |
                (df['levensthein_score'] >= levensthein_score) |
                (df['jaro_winkler_score'] >= jaro_w_score) |
                (df['ratcliff_obershelp_score'] >= ratcliff_score) |
                (df['pam_score'] >= pam_score) |
                (df['number_patents'] >= n_patents) |
                (df['orbis_name'].str.split().str.len().lt(
                    company_max_name_len)
                 )
                ]

        return results
