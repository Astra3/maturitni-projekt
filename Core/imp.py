"""Tento soubor obsahuje třídu k importu .txt souboru s daty počasí."""
import os.path
from io import StringIO
from os import PathLike

import pandas as pd
import sqlalchemy

from Core import conn


def data_imp(inp: PathLike[str], drop: bool = True) -> pd.DataFrame:
    """

    Args:
        inp: cesta k souboru s daty
        drop: definuje zda zanechat pouze žádané položky nebo ne, tzn. že z původní databáze zanechá pouze out_temp,
            out_humidity, dew_point, wind_speed, wind_dir, gust a bar

    Returns:
        DataFrame všech hodnot

    Raises:
        FileNotFoundError: při špatném zadání hodnot
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
    df = pd.read_csv(StringIO(data), sep="\t", parse_dates=[0], na_values=["---"])

    df.set_index("datetime", inplace=True)
    df = df.tz_localize("Europe/Prague", ambiguous="infer")
    if drop:
        df = df[["out_temp", "out_humidity", "dew_point", "wind_speed", "wind_dir", "gust", "bar"]]

    return df


def imp(conn: sqlalchemy.engine.base.Engine, table_name: str = "pocasi"):
    """
    Funkce importující data z SQL databáze

    Args:
        conn: SQLAlchemy connection
        table_name: jméno tabulky

    Returns:
        dataframe počasí z SQL
    """
    df = pd.read_sql(table_name, conn, index_col=["datetime"])

    return df


class Combine:
    """
    Třída ke jednoduchým úpravám DataFrame a importu.

    Args:
        df1: DataFrame, se kterým se bude pracovat
    """

    def __init__(self, df1: pd.DataFrame):
        self.df = df1

    def combine(self, *df_append: pd.DataFrame):
        """
        Metoda kombinující dohromady všechny zadané DataFrames

        Příklad použití:

        >>> dataframe = pd.DataFrame([[5, 2, 5, 2], [10, 2, 8, 2]])
        >>> dataframe
            0  1  2  3
        0   5  2  5  2
        1  10  2  8  2
        >>> dataframe_append = pd.DataFrame([[5, 10, 3, 5]])
        >>> dataframe_append
           0   1  2  3
        0  5  10  3  5
        >>> comb = Combine(dataframe)
        >>> comb.combine(dataframe_append)
            0   1  2  3
        0   5   2  5  2
        1  10   2  8  2
        0   5  10  3  5

        Ve výše napsaném příkladu můžeme vidět kombinaci dvou DataFrames se stejnými indexy a jejich kombinaci do
        jednoho.

        Args:
            df_append: několik DataFrames následujících za sebou

        Returns:
            spojený DataFrame, rovněž také uloží daný DataFrame do objektu
        """
        df = self.df.append(list(df_append))

        self.df = df
        return df

    def to_sql(self, table_name: str = "pocasi"):
        self.df.to_sql(table_name, conn, if_exists="replace")


class LegacyImport:
    """
    Třída obsahující funkce a metody sloužící k importu starých formátů souborů. Nepoužité front-endem a označené jako
    private třída pro Sphinx.

    :meta private:
    """

    @staticmethod
    def old_import(file: PathLike[str], ambiguous_localize: str = "infer", drop: bool = True, dropna_index: bool = True,
                   remove_duplicit_index: bool = True) -> pd.DataFrame:
        """
        Funkce přijme .csv soubor počasí a převede jej do DataFrame. První column je převedena na datetime objekt a je
        na ni nastaven Europe/Prague timezone. **Funkce je pouze pro starý formát a je zbytečná pro nový.**

        Args:
            file: .csv soubor pro přijetí
            ambiguous_localize: ambiguous parametr k funkci :doc:`tz_localize <pandas:reference/api/pandas.DataFrame.tz_localize>`
            drop: definuje zda zanechat pouze žádané položky nebo ne, tzn. že z původní databáze zanechá pouze 
                out_temp, out_humidity, dew_point, wind_speed, wind_dir, gust a bar
            dropna_index: pokud True, tak odstraní všechny NaT hodnoty z indexu
            remove_duplicit_index: umožňuje odstranit duplicitní index z importovaných dat

        Returns:
            pandas DataFrame přijatého souboru
            
        Raises:
            FileNotFoundError: pokud input file neexistuje na disku
        """
        if not os.path.exists(file):
            raise FileNotFoundError("Zadaný soubor neexistuje.")

        na_values = ["nan", "---", "--.-", "--"]
        data: pd.DataFrame = pd.read_csv(file, parse_dates=[1], na_values=na_values, low_memory=False)

        data.set_index("datetime", inplace=True)
        if remove_duplicit_index:  # index se odstraní až když je "datetime" indexem
            LegacyImport._drop_dupe_index(data)

        # lokalizace time zone
        data = data.tz_localize("Europe/Prague", ambiguous=ambiguous_localize, nonexistent="shift_forward")
        if dropna_index:
            data = data[data.index.notna()]

        if drop:
            data = data[["out_temp", "out_humidity", "dew_point", "wind_speed", "wind_dir", "gust", "bar"]]
        return data

    @staticmethod
    def conv2012(inp: PathLike[str] = "2012.csv") -> pd.DataFrame:
        """
        Tato funkce dokáže vzít formát data z roku 2012 a převést jej na
        `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_.

        Args:
            inp: jméno souboru k úpravě

        Returns:
            DataFrame se správným formátem datu
        """
        df = pd.read_csv(inp, parse_dates=["datetime"])
        return df

    @staticmethod
    def _drop_dupe_index(data: pd.DataFrame):
        """
        Funkce odstraní jakýkoliv duplicitní index z DataFrame.

        Args:
            data: odstranit data z tohoto DataFrame
        """
        data.drop(index=data[data.index.duplicated()].index, inplace=True)
