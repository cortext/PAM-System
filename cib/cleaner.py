from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def extract_stop_words():
    """
    extract_stop_word
    """
    stop_words = set(stopwords.words('english'))
    df_names = pd.read_csv('cib/data/guo_magerman.csv')

    for index, row in df_names.iterrows():
        word_tokens = word_tokenize(row['magerman'].lower())
        # filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []

        for w in word_tokens:
            if w in stop_words:
                filtered_sentence.append(w)

        if filtered_sentence and (
            len(word_tokens) > 3) and "&" not in word_tokens:
            print(row['magerman'])
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
