import textdistance
from fuzzywuzzy import fuzz
from pam.approximatematches import score


def run_distance_matching(company_name, patstat_name,
                          elastic_score, query):
    """
    run_distance_matching
    """
    company_name = company_name.lower()
    patstat_name = patstat_name.lower()

    levensthein_score = fuzz.token_sort_ratio(company_name, patstat_name)
    jaro_winkler_score = textdistance.jaro_winkler(company_name, patstat_name)
    ratcliff_score = textdistance.ratcliff_obershelp(company_name,
                                                     patstat_name)

    name_length = len(company_name.split())
    if name_length > 5:
        elastic_score -= 10

    distance_score = score.calculate_distance_score(levensthein_score,
                                                    jaro_winkler_score,
                                                    ratcliff_score,
                                                    name_length)

    pam_score = score.pam_score(query, elastic_score, distance_score,
                                name_length)

    return {
        'levensthein_score': levensthein_score,
        'jaro_winkler_score': jaro_winkler_score,
        'ratcliff_obershelp_score': ratcliff_score,
        'pam_score': pam_score
    }
