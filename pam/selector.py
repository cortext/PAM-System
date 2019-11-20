
accurate_matches_query = {
    'min_score': 76,
    'score_patent_condition': 66,
    'number_patents': 11
}

wrong_matches_query = {
    'max_score': 66,
    'score_patent_condition': 66,
    'number_patents': 10
}

matches_to_check_query = {
    'min_score': 66,
    'score_patent_condition': 76,
    'number_patents': 10
}


def selector_accurate_matches(df_pam):
    """
    selector_accurate_matches
    """

    accurate_matches = df_pam[(df_pam['pam_score'] >=
                               accurate_matches_query['min_score'])]

    accurate_matches = accurate_matches.append(df_pam[
        (df_pam['pam_score']
         > accurate_matches_query['score_patent_condition'])
        & (df_pam['pam_score'] < accurate_matches_query['min_score'])
        & (df_pam['number_patents'] < accurate_matches_query['number_patents'])
    ])

    accurate_matches = accurate_matches[
            (accurate_matches['levensthein_score'] >= 70)
            | (accurate_matches['jaro_winkler_score'] >= 0.7)
            | (accurate_matches['ratcliff_obershelp_score'] >= 0.7)
            ]

    accurate_matches = accurate_matches[
            (accurate_matches['pam_score'] >= 68)
            | (accurate_matches['elastic_score'] >= 11)
            | (accurate_matches['jaro_winkler_score'] >= 0.9)
            ]

    accurate_matches = accurate_matches[
            (accurate_matches['pam_score'] > 71)
            | (accurate_matches['jaro_winkler_score'] >= 0.85)
            ]

    accurate_matches = accurate_matches[(accurate_matches['elastic_score']
                                         > 19) |
                                        (accurate_matches['jaro_winkler_score']
                                         > 0.75) |
                                        (accurate_matches['ratcliff_'
                                                          'obershelp_score']
                                         > 0.77)
                                        ]

    accurate_matches = accurate_matches[(accurate_matches['elastic_score']
                                         > 14.2) |
                                        (accurate_matches['levensthein_score']
                                         >= 70) |
                                        (accurate_matches['ratcliff_'
                                                          'obershelp_score']
                                         >= 0.70) |
                                        (accurate_matches['number_patents']
                                         > 100)
                                        ]

    accurate_matches = accurate_matches[(accurate_matches['elastic_score']
                                         > 14.2) |
                                        (accurate_matches['levensthein_score']
                                         >= 70) |
                                        (accurate_matches['ratcliff_'
                                                          'obershelp_score']
                                         >= 0.70) |
                                        (accurate_matches['number_patents']
                                         > 100)
                                        ]

    accurate_matches = accurate_matches.append(df_pam[
                                        (df_pam['levensthein_score']
                                         >= 65) &
                                        (df_pam['jaro_winkler_score']
                                         >= 0.89)
                                        ])

    return accurate_matches


def selector_wrong_matches(df_pam):
    """
    selector_wrong_matches
    """

    wrong_matches = df_pam[(df_pam['pam_score'] <
                            wrong_matches_query['max_score'])]
    wrong_matches = wrong_matches.append(df_pam[
        (df_pam['pam_score'] > wrong_matches_query['max_score']) &
        (df_pam['pam_score'] < wrong_matches_query['score_patent_condition']) &
        (df_pam['number_patents'] < wrong_matches_query['number_patents'])
    ])

    return wrong_matches


def selector_matches_to_check(df_pam):
    """
    selector_matches_to_check
    """

    matches_to_check = df_pam[
        (df_pam['pam_score'] >= matches_to_check_query['min_score']) &
        (df_pam['pam_score'] <
         matches_to_check_query['score_patent_condition'])
        & (df_pam['number_patents'] > matches_to_check_query['number_patents'])
    ]

    return matches_to_check
