"""Tento soubor obsahuje třídu k importu .txt souboru s daty počasí."""
import os.path
from io import StringIO

import pandas as pd
import sqlalchemy


def imp(inp: str, drop: bool = True) -> pd.DataFrame:
    """
    Funkce přijímá cestu k exportovanému souboru z Davis Instruments software.

    :param drop: definuje zda zanechat pouze žádané položky nebo ne, tzn. že z původní databáze zanechá pouze out_temp, out_humidity, dew_point, wind_speed, wind_dir, gust a bar
    :param inp: cesta k souboru s daty
    :return: DataFrame všech hodnot
    :raises FileNotFoundError: při špatném zadání souboru
    """
    if not os.path.isfile(inp):
        raise FileNotFoundError("Vstupní soubor nebyl nalezen")

    with open(inp, "r") as file:
        data = file.readlines()
    data = data[2:]
    data = [i.replace("\t", " ", 1) for i in data]

    # vloží vlastní hlavičku
    data.insert(0,
                "datetime\tout_temp\thi_out_temp\tlow_out_temp\tout_humidity\tdew_point\twind_speed\twind_dir\t"
                "wind_run\tgust\thi_wind_dir\twindchill\theat_index\tTHW_index\tbar\train\train_rate\t"
                "head_d-d\tcool_d-d\tin_temp\tin_humidity\tin_dew_point\tin_heat_index\tin_EMC\tin_air_density\t"
                "wind_samp\twind_Tx\tISS_reception\tarc_interval\n")

    # tohle spojí všechny listy do jednoho
    data = "".join(data)

    # StringIO vlastně převede string na file stream
    df = pd.read_csv(StringIO(data), sep="\t", parse_dates=[0], na_values=["nan", "nannan"])

    df.set_index("datetime", inplace=True)
    df = df.tz_localize("Europe/Prague", ambiguous="infer")
    if drop:
        df = df[["out_temp", "out_humidity", "dew_point", "wind_speed", "wind_dir", "gust", "bar"]]

    return df


class Combine:
    """
    Třída ke jednoduchým úpravám DataFrame a importu.

    :param df1: DataFrame, se kterým se bude pracovat
    """
    def __init__(self, df1: pd.DataFrame):
        self.df = df1

    def combine_drop(self, df_append: pd.DataFrame, duplicate_index: str = "df_append"):
        """
        Metoda kombinující dohromady výchozí DataFrame a df_append s kontrolou a odstranění duplicitního indexu.
        Výsledný DataFrame bude vrácen, bude ale také uložen jako hlavní DataFrame třídy

        Příklad použití:

        >>> df
            0  1  2  3
        0   5  2  5  2
        1  10  2  8  2
        >>> df_append
           0   1  2  3
        0  5  10  3  5
        >>> comb = Combine(df)
        >>> comb.combine_drop(df_append, "df")
            0  1  2  3
        1  10  2  8  2

        Ve výše napsaném příkladu můžeme vidět kombinaci dvou DataFrames se stejnými indexy, ve výsledku pouze nultý
        index df2 přežije.

        :param df_append: druhý DataFrame v pořadí
        :param duplicate_index: přijímá "df2" pro odstranění dupes v df2 a "df" pro odstranění dupes ve výsledném DataFrame
        :return: zkombinovaný DataFrame
        :raises ValueError: při špatné hodnotě duplicate_index
        """
        pas = True
        # TODO: tohle může být switch statement od Python 3.10
        if duplicate_index == "df_append":
            Combine._drop_dupe_index(df_append)
            pas = False

        df = self.df.append(df_append)

        if duplicate_index == "df":
            Combine._drop_dupe_index(df)
        elif pas:
            raise ValueError("Zadána špatná hodnota pro duplicates")

        self.df = df
        return df

    def to_sql(self, conn: sqlalchemy.engine.base.Engine, table_name: str = "pocasi"):
        self.df.to_sql(table_name, conn, if_exists="replace")

    @staticmethod
    def _drop_dupe_index(data: pd.DataFrame):
        data.drop(index=data[data.index.duplicated()].index, inplace=True)


def old_import(file: str, drop: bool = True) -> pd.DataFrame:
    """
    Funkce přijme .csv soubor počasí a převede jej do DataFrame. První column je převedena na datetime objekt a je
    na ni nastaven Europe/Prague timezone. **Funkce je pouze pro starý formát a je zbytečná pro nový.**

    Příklad použití na databázi počasí:

    >>> old_import("2021.txt")

    :param drop: definuje zda zanechat pouze žádané položky nebo ne, tzn. že z původní databáze zanechá pouze out_temp, out_humidity, dew_point, wind_speed, wind_dir, gust a bar
    :param file: .csv soubor pro přijetí
    :return: pandas DataFrame přijatého souboru
    :raises FileNotFoundError: pokud input file neexistuje na disku
    :meta private:
    """
    if not os.path.exists(file):
        raise FileNotFoundError("Zadaný soubor neexistuje.")

    data: pd.DataFrame = pd.read_csv(file, parse_dates=[1])
    data.set_index("datetime", inplace=True)
    data = data.tz_localize("Europe/Prague", ambiguous="infer")
    if drop:
        data = data[["out_temp", "out_humidity", "dew_point", "wind_speed", "wind_dir", "gust", "bar"]]
    return data
