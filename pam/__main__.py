import click
import pam.helpers as helper
from pam.pamsystem import PamSystem


@click.command()
@click.option('--csv', default='/data/loads/companies.csv',
              help='Csv file that contains the companies list.')
@click.option('--column', default='company_name',
              help='Define the name of the column which contains '
              'the companies names.')
@click.option('--country', default='cnty_iso',
              help='Define the name of the column which contains '
              'the company country.')
@click.option('--output', default='data/results/',
              help='The output file where results are stored.')
def cli(csv, column, country, output):
    """
    cli
    """

    pam_system = PamSystem()
    pam_system.set_df_companies(csv)
    pam_system.company_name_column = column
    pam_system.country_column = country
    df_pam_accurate = helper.get_empty_df()
    df_pam_wrong = helper.get_empty_df()
    df_pam_checks = helper.get_empty_df()

    for query in PamSystem.QUERIES:
        pam_system.query = query
        pam_system._run()
        pam_system.df_accurate_matches.to_csv('data/results/pam_results_'
                                              + query + '.csv')
        pam_system.df_wrong_matches.to_csv('data/results/pam_wrong_'
                                           + query + '.csv')
        pam_system.df_to_check_matches.to_csv('data/results/pam_to_check_'
                                              + query + '.csv')

        df_pam_wrong = df_pam_wrong.append(
                pam_system.df_wrong_matches)
        df_pam_checks = df_pam_checks.append(
            pam_system.df_to_check_matches)
        df_pam_accurate = df_pam_accurate.append(
            pam_system.df_accurate_matches)

    print('grouping pam dataframe...')
    df_pam_accurate.to_csv(output + 'accurate_matching2.csv')

    df_pam_accurate = helper.groupby_pam_dataframe(df_pam_accurate)
    df_pam_checks = helper.groupby_pam_dataframe(df_pam_checks)
    df_pam_wrong = helper.groupby_pam_dataframe(df_pam_wrong)

    df_pam_accurate.to_csv(output + 'accurate_matching.csv')
    df_pam_checks.to_csv(output + 'to_checks_matching.csv')
    df_pam_wrong.to_csv(output + 'wrong_matching.csv')


if __name__ == "__main__":
    cli()
