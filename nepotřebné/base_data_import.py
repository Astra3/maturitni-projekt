"""
Tento skript je víceméně k ničemu pro finální projekt, jeho úkolem bylo naimportovat data ze zpracovaného .csv
souboru starého formátu
"""
import os.path

import pandas as pd
import sqlalchemy.engine.base
from sqlalchemy import create_engine


def base_import(file: str) -> pd.DataFrame:
    """
    Funkce přijme .csv soubor počasí a převede jej do DataFrame. První column je převedena na datetime objekt a je na ni
    nastaven Europe/Prague timezone.

    :param file: .csv soubor pro přijetí
    :return: pandas DataFrame přijatého souboru
    :raises FileNotFoundError: pokud input file neexistuje na disku
    """
    if not os.path.exists(file):
        raise FileNotFoundError("Zadaný soubor neexistuje.")

    data: pd.DataFrame = pd.read_csv(file, parse_dates=[1])
    data.set_index("datetime", inplace=True)
    data = data.tz_localize("Europe/Prague", ambiguous="infer")
    return data


def to_sql(data: pd.DataFrame, conn: sqlalchemy.engine.base.Engine, table_name: str = "pocasi"):
    """
    Funkce uloží DataFrame to sqlalchemy engine

    :param data: pandas DataFrame pro uložení
    :param conn: database engine
    :param table_name: jméno tabulky, default "pocasi"
    """
    data.to_sql(table_name, conn)


if __name__ == '__main__':
    df = base_import("Base data/total1.csv")
