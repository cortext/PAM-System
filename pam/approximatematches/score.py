import sys

elastic_score_scale = {
'low' : {'top': 13, 'value': 0},
'medium-low' : {'top': 15, 'value': 30},
'medium': {'top': 20, 'value': 60},
'high': {'top': 100, 'value': 100}
}

score_distribution = {
'elasticsearch' : 0.2,
'levensthein_score'   : 0.7,
'jaro_winkler': 0.3,
'distance_score': 0.6
}

def pam_score(filter, elastic_score, distance_score):
    """
    pam_score
    """
    if elastic_score < elastic_score_scale['low']['top']:
        new_elastic_score = elastic_score_scale['low']['value']
    elif elastic_score < elastic_score_scale['medium-low']['top']:
        new_elastic_score = elastic_score_scale['medium-low']['value']
    elif elastic_score < elastic_score_scale['medium']['top']:
        new_elastic_score = elastic_score_scale['medium']['value']
    elif elastic_score < elastic_score_scale['high']['top']:
        new_elastic_score = elastic_score_scale['high']['value']

    new_elastic_score = new_elastic_score * score_distribution['elasticsearch']
    pam_score = new_elastic_score + (distance_score
                                     * score_distribution['distance_score']) + filter

    return pam_score

def calculate_distance_score(levensthein_score, jaro_winkler_score,
                             name_length):
    """
    calculate_distance_score
    """
    if name_length > 5 and levensthein_score < 80 : levensthein_score -= 20
    if name_length > 5 and jaro_winkler_score < 0.8 : jaro_winkler_score -= 0.2

    distance_score = (levensthein_score * 0.7) + ((jaro_winkler_score * 100) * 0.3)
    return distance_score
