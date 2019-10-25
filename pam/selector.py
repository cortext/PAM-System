import pandas as pd

accurate_matches_query = {
'min_score' : 79,
'score_patent_condition'   : 66,
'number_patents': 11
}

wrong_matches_query = {
'max_score' : 58,
'score_patent_condition'   : 66,
'number_patents': 10
}

matches_to_check_query = {
'min_score' : 58,
'score_patent_condition'   : 66,
'number_patents': 10
}


def run_selector_processor(df_pam):
    """
    distance_matching_proccesor
    """
    accurate_matches = df_pam[(df_pam['pam_score'] >
                               accurate_matches_query['min_score'])]

    accurate_matches = accurate_matches.append(df_pam[
        (df_pam['pam_score'] > accurate_matches_query['score_patent_condition'])
        & (df_pam['pam_score'] < accurate_matches_query['min_score'])
        & (df_pam['number_patents'] < accurate_matches_query['number_patents'])
        ])

    wrong_matches = df_pam[(df_pam['pam_score'] <
                            wrong_matches_query['max_score'])]
    wrong_matches = wrong_matches.append(df_pam[
        (df_pam['pam_score'] > wrong_matches_query['max_score']) &
        (df_pam['pam_score'] < wrong_matches_query['score_patent_condition']) &
        (df_pam['number_patents'] < wrong_matches_query['number_patents'])
        ])

    matches_to_check = df_pam[
        (df_pam['pam_score'] > matches_to_check_query['min_score']) &
        (df_pam['pam_score'] < matches_to_check_query['score_patent_condition'])
        & (df_pam['number_patents'] > matches_to_check_query['number_patents'])
        ]

    accurate_matches.to_csv('data/results/accurate_matches.csv')
    wrong_matches.to_csv('data/results/wrong_matches.csv')
    matches_to_check.to_csv('data/results/matches_to_check.csv')

    del accurate_matches
    del wrong_matches
    del matches_to_check


def selector_accurate_matches(df_pam):
    """
    selector_accurate_matches
    """
    accurate_matches = df_pam[(df_pam['pam_score'] >
                               accurate_matches_query['min_score'])]

    accurate_matches = accurate_matches.append(df_pam[
        (df_pam['pam_score'] > accurate_matches_query['score_patent_condition'])
        & (df_pam['pam_score'] < accurate_matches_query['min_score'])
        & (df_pam['number_patents'] < accurate_matches_query['number_patents'])
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
        (df_pam['pam_score'] > matches_to_check_query['min_score']) &
        (df_pam['pam_score'] < matches_to_check_query['score_patent_condition'])
        & (df_pam['number_patents'] > matches_to_check_query['number_patents'])
        ]

    return matches_to_check
