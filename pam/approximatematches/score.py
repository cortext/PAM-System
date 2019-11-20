import sys

# In order to redefine the elasticsearch score it has been needed to
# create a list of parameters where depending on the range of the score
# is set a new value
elastic_score_scale = {
    'low': {'range': 13, 'value': 0},
    'medium-low': {'range': 15, 'value': 30},
    'medium': {'range': 20, 'value': 60},
    'high': {'range': 100, 'value': 100}
}

# Percentage used for every score parameter for calculating the pam score.
# In total the values should sum 1 (100% of pam score)
score_distribution = {
    'elasticsearch': 0.2,
    'levensthein': 0.4,
    'jaro_winkler': 0.3,
    'ratcliff_obershelp_score': 0.3,
    'query_used': 0.2,
    'distance_score': 0.6
}

score_for_query = {
    'restricted_to_jurisdiction': 100,
    'out_jurisdiction': 0
}


def pam_score(query, elastic_score, distance_score, name_length):
    """
    pam_score
    """
    if elastic_score < elastic_score_scale['low']['range']:
        new_elastic_score = elastic_score_scale['low']['value']
    elif elastic_score < elastic_score_scale['medium-low']['range']:
        new_elastic_score = elastic_score_scale['medium-low']['value']
    elif elastic_score < elastic_score_scale['medium']['range']:
        new_elastic_score = elastic_score_scale['medium']['value']
    elif elastic_score < elastic_score_scale['high']['range']:
        new_elastic_score = elastic_score_scale['high']['value']

    filter_score = score_for_query[query] * score_distribution['query_used']
    new_elastic_score = new_elastic_score * score_distribution['elasticsearch']

    pam_score = new_elastic_score + (
        distance_score * score_distribution['distance_score']
    ) + filter_score

    if name_length > 4:
        pam_score -= 10

    return pam_score


def calculate_distance_score(levensthein_score, jaro_winkler_score,
                             ratcliff_obershelp_score, name_length):
    """
    calculate_distance_score
    """
    if name_length > 5 and levensthein_score < 80:
        levensthein_score -= 20
    if name_length > 5 and jaro_winkler_score < 0.8:
        jaro_winkler_score -= 0.2

    distance_score = (levensthein_score *
                      score_distribution['levensthein']) + ((
                          jaro_winkler_score * 100) *
                          score_distribution['jaro_winkler']) + ((
                              ratcliff_obershelp_score * 100) *
                          score_distribution['ratcliff_obershelp_score'])

    return distance_score
