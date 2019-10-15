import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def extract_stop_words(string=""):
    """
    extract_stop_word
    """
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(string.lower())

    # filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []

    for w in word_tokens:
        if w in stop_words:
            filtered_sentence.append(w)

    if filtered_sentence and (
        len(word_tokens) > 3) and "&" not in word_tokens:
        print(string)
        print(filtered_sentence)


def magerman_normalization():
    """
    extract_stop_word
    """
    return 0


def patstat_normalization():
    """
    extract_stop_word
    """
    return 0


def stripping_org_names():
    """
    stripping_org_names
    """
    return 0


def cleaning_country_names():
    """
    cleaning_country_names
    """
    return 0


def extract_noise_names():
    """
    extract_noise_names
    """
    return 0
