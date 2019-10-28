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
@click.option('--output', default='data/results/pam_results.csv',
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

    for query in PamSystem.QUERIES:
        pam_system.query = query
        pam_system._run()
        df_pam_accurate = df_pam_accurate.append(pam_system.df_accurate_matches)

    df_pam_accurate = helper.groupby_pam_dataframe(df_pam_accurate)
    df_pam_accurate.to_csv(output)


if __name__ == "__main__":
    cli()
