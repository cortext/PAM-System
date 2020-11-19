from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pam.pamsystem import PamSystem
import json
import pam.helpers as helper
import pandas as pd


router = APIRouter()


@router.get("/entities/_link", tags=["entities"])
def entityLinkage(name: str, country: Optional[str] = "", entityId: Optional[str] = None):
   
    cars = {'new_bvd_id': entityId,
            'company_name': name,
            'cnty_iso': country,
            'name_type': ['']
           }

    df_entities = pd.DataFrame(cars, columns = ['new_bvd_id', 'company_name', 'cnty_iso', 'name_type'])

    pam_system = PamSystem()
    pam_system.df_companies = df_entities
    pam_system.company_name_column = 'company_name'
    pam_system.country_column = 'cnty_iso'
    df_pam_accurate = helper.get_empty_df()
    df_pam_wrong = helper.get_empty_df()
    df_pam_checks = helper.get_empty_df()

    for query in PamSystem.QUERIES:
        pam_system.query = query
        pam_system._run()

        df_pam_wrong = df_pam_wrong.append(
                pam_system.df_wrong_matches)
        df_pam_checks = df_pam_checks.append(
            pam_system.df_to_check_matches)
        df_pam_accurate = df_pam_accurate.append(
            pam_system.df_accurate_matches)

    print('Grouping pam dataframe...')
    df_pam_accurate = helper.groupby_pam_dataframe(df_pam_accurate)
    df_pam_checks = helper.groupby_pam_dataframe(df_pam_checks)
    df_pam_wrong = helper.groupby_pam_dataframe(df_pam_wrong)

    df_pam_accurate = df_pam_accurate.append(df_pam_checks)
    result = df_pam_accurate.to_json() 
    response = parsed = json.loads(result)

    return response
