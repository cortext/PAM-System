import textdistance
from fuzzywuzzy import fuzz
from pam.approximatematches import score

def run_distance_matching(company_name, patstat_name,
                          elastic_score, query):
    """
    run_distance_matching
    """
    ratio = fuzz.token_sort_ratio(company_name.lower(),
    patstat_name.lower())
    jaro_winkler_score = textdistance.jaro_winkler(
    company_name.lower(),
    patstat_name.lower())
    name_length = len(company_name.split())
    if name_length > 5 : elastic_score -= 10
    distance_score = score.calculate_distance_score(ratio,
    jaro_winkler_score,
    name_length)
    pam_score = score.pam_score(query, elastic_score, distance_score)

    return {
    'levensthein_score' : pam_score,
    'jaro_winkler_score'   : jaro_winkler_score,
    'pam_score': pam_score
    }
