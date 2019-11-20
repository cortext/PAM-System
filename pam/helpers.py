import pandas as pd


def free_up_dataframes():
    return True


def number_of_guos_detected():

    df_accurate_country = pd.read_csv('data/results/accurate_matches.csv')
    df_accurate_wordwide = pd.read_csv('data/results/accurate_matches2.csv')

    df_accurate_wordwide = groupby_pam_dataframe(df_accurate_wordwide)
    df_accurate_wordwide.to_csv('data/results/accurate_wordwide.csv')

    df_accurate_final = df_accurate_country.append(df_accurate_wordwide)
    df_accurate_final = groupby_pam_dataframe(df_accurate_final)

    df_accurate_final.to_csv('data/results/accurate_final.csv')


def groupby_pam_dataframe(df):

    df_groupby = df.sort_values(
            'pam_score', ascending=False).drop_duplicates([
                'doc_std_name_id', 'orbis_id'])

    return df_groupby


def count_the_total_matches():
    df_accurate_final = pd.read_csv('data/results/accurate_final.csv')
    print(df_accurate_final['orbis_name'].nunique())


def get_empty_df():
    return pd.DataFrame()
