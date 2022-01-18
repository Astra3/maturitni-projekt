"""Tento soubor obsahuje tříd určené k importu dat počasí ve všech možných formátech."""
import datetime
import os.path
from io import StringIO

import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from Pocasi import data_path, rain_path, time_zone


def data_imp(inp="PathLike[str]", drop: bool = True) -> pd.DataFrame:
    """
    Funkce importuje data ze souboru nového formátu z nové meteostanice.

    Args:
        inp: cesta k souboru s daty
        drop: definuje zda zanechat pouze žádané položky nebo ne, tzn. že z původní databáze zanechá pouze out_temp,
            out_humidity, dew_point, wind_speed, wind_dir, gust bar a rain_data

    Returns:
        DataFrame všech hodnot

    Raises:
        FileNotFoundError: při špatném zadání hodnot
    """
    if not os.path.isfile(inp):
        raise FileNotFoundError("Vstupní soubor nebyl nalezen")

    with open(inp, "r") as file:
        data = file.readlines()
    # odstraní header a tabulátor u časových dat
    data = data[2:]
    data = [i.replace("\t", " ", 1) for i in data]

    # vloží vlastní hlavičku
    data.insert(0,
                "datetime\tout_temp\thi_out_temp\tlow_out_temp\tout_humidity\tdew_point\twind_speed\twind_dir\t"
                "wind_run\tgust\thi_wind_dir\twindchill\theat_index\tTHW_index\tbar\train_data\train_rate\t"
                "head_d-d\tcool_d-d\tin_temp\tin_humidity\tin_dew_point\tin_heat_index\tin_EMC\tin_air_density\t"
                "wind_samp\twind_Tx\tISS_reception\tarc_interval\n")

    # tohle spojí všechny listy do jednoho
    data = "".join(data)

    def data_parser(date):
        try:
            return datetime.datetime.strptime(date, "%d.%m.%y %H:%M")
        except ValueError:
            return None

    # StringIO vlastně převede string na file stream
    df = pd.read_csv(StringIO(data), sep="\t", parse_dates=[0], date_parser=data_parser, na_values=["---", "------"])

    df.set_index("datetime", inplace=True)
    df = df.tz_localize(time_zone, ambiguous="infer")
    if drop:
        df = df[["out_temp", "out_humidity", "dew_point", "wind_speed", "wind_dir", "gust", "bar", "rain_data"]]

    return df


def imp(rain: bool = False):
    """
    Funkce importující data z Feather databáze definovanou v __init__

    Args:
        rain: definuje, zda importovat z ``rain_path`` nebo z ``data_path``

    Returns:
        dataframe počasí z Feather formátu
    """
    df = pd.read_feather(rain_path) if rain else pd.read_feather(data_path)
    df.set_index("datetime", inplace=True)

    return df


class EditData:
    """
    Třída ke jednoduchým úpravám DataFrame a importu.

    Args:
        df1: základní DataFrame, se kterým se bude pracovat
        sort: určí, zda seřadit index nebo ne
    """

    def __init__(self, df1: pd.DataFrame | pd.Series, sort: bool = True):
        self.df = df1

        if sort:
            self.df.sort_index(inplace=True)

    def combine(self, *df_append: pd.DataFrame | pd.Series):
        """
        Metoda kombinující dohromady všechny zadané DataFrames, seřadí index a odstraní duplicitní index.

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
        >>> comb = EditData(dataframe)
        >>> comb.combine(dataframe_append)
            0   1  2  3
        0   5   2  5  2
        0   5  10  3  5
        1  10   2  8  2

        Ve výše napsaném příkladu můžeme vidět kombinaci dvou DataFrames se stejnými indexy a jejich kombinaci do
        jednoho.

        Args:
            df_append: několik DataFrames následujících za sebou

        Returns:
            spojený DataFrame, rovněž také uloží daný DataFrame do objektu
        """
        df = self.df.append(list(df_append))
        df.sort_index(inplace=True)

        self.df = df
        return df

    def rainfall(self, old=False, drop_rain: bool = True, localize: str | None = None) -> pd.Series:
        """
        Funkce vracející Series s daty o denních srážkách. Metoda bere data ze sloupce "rain_data" z DataFrame
        inicializovaném v objektu této třídy. Více o funkci v kapitole :ref:`Srážky v počasí`.

        Args:
            localize: lokalizuje rainfall do zadané časové zóny, pokud je None, odstraní lokalizaci časové zóny
            old: rozlišuje mezi starým formátem srážek a novým (starý formát bere srážky na konci dne, nový sčítá srážky
             za celý den)
            drop_rain: pokud True, tak odstraní "rain_data" column z DataFrame

        Returns:
            index tvoří data dnů a data je počet srážek za daný den
        """
        rain = self.df["rain_data"].resample("D")
        if old:
            rainfall: pd.Series = rain.last()
        else:
            rainfall = rain.sum()

        if localize is None or type(localize) == str:
            rainfall = rainfall.tz_localize(localize)

        if drop_rain:
            self.df.drop("rain_data", axis=1, inplace=True)
        return rainfall

    def filter_unrealistic_data(self):
        """
        Obsahuje definici maximálních a minimálních parametrů. Rovněž filtruje všechny výkyvy v datech. *Rovněž smaže
        duplicitní data v indexu!*

        """

        self.df.drop(index=self.df[self.df.index.duplicated()].index, inplace=True)

        # dictionary sloupců, kde každý sloupec má tuple s (min, max) hodnotami pro daný sloupec
        min_max_values = {
            "out_temp": (-100, 100),
            "out_humidity": (1, 100),
            "dew_point": (-100, 100),
            "wind_speed": (0, 80),
            "bar": (800, 1200)
        }

        # prochází sloupec za sloupcem a maže hodnoty zapsané výše
        for name, values in min_max_values.items():
            self.df.loc[self.df[name] < values[0], name] = np.nan
            self.df.loc[self.df[name] > values[1], name] = np.nan

        # hledá peaks v každém sloupci (výjimku tvoří směr větru)
        # multiply zde slouží k pozdějšímu obrácení hodnot v DataFrame, změní se na -1
        multiply = 1
        for _ in range(2):
            for i in self.df.drop(columns="wind_dir").keys():
                data = self.df[i].dropna().copy()
                p, _ = find_peaks(data.values * multiply, threshold=3)  # find_peaks vrací pouze indexy
                while p.size > 0:  # kontroluje zda find_peaks vůbec něco vrací
                    data.loc[data.iloc[p].index] = np.nan  # nahradí data získané z find_peaks za nan
                    self.df.loc[data.index, i] = data  # uloží do hlavního df celé třídy
                    data = self.df[i].dropna().copy()  # a cyklus se opakuje
                    p, _ = find_peaks(data.values * multiply, threshold=3)
            multiply = -1

    def to_feather(self, rain: bool = False):
        """
        Uloží data do feather formátu, který se používá v celém projektu.

        Args:
            rain (bool): pokud True, bude ukládat do ``rain_path``, jinak do ``data_path``

        """
        save = self.df.reset_index()
        path = rain_path if rain else data_path
        save.to_feather(path)


class ImportSave:
    """
    Tato třída umí jednoduše naimportovat data ze souboru, převést je databáze, přidat je a uložit. Měla by být výhradně
    použita v rámci context manageru.

    Raises:
        ValueError: pokud se nenaleznou buď data srážek, nebo počasí - pokud neexistuje ani jedno, tak jsou automaticky
            vytvořeny
    """

    def __init__(self):
        from Pocasi import pocasi_data, rain_data

        if (pocasi_data is None) != (rain_data is None):
            raise ValueError("Chybí data počasí nebo srážek!")

        if (pocasi_data is None) and (rain_data is None):
            # tahle situace by se reálně neměla stát, a tudíž nebude testovaná
            self.pocasi = EditData(pd.DataFrame())
            self.rain = EditData(pd.DataFrame())
        else:
            self.pocasi = EditData(pocasi_data)
            self.rain = EditData(rain_data)

    def import_append(self, file="PathLike[str]"):
        """
        Rychlý import a přidání do DataFrames

        Args:
            file: soubor nového formátu, ze kterého importovat
        """
        df = data_imp(file)
        edit = EditData(df)
        self.rain.combine(edit.rainfall())
        self.pocasi.combine(edit.df)

    def close(self):
        self.rain.to_feather(True)
        self.pocasi.to_feather()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class LegacyImport:
    """
    Třída obsahující funkce a metody sloužící k importu starých formátů souborů. Nepoužité front-endem a označené jako
    private třída pro Sphinx.

    :meta private:
    """

    @staticmethod
    def old_import(file="PathLike[str]", ambiguous_localize: str = "infer", drop: bool = True, is_iso8601: bool = True,
                   dropna_index: bool = True, remove_duplicit_index: bool = True) -> pd.DataFrame:
        """
        Funkce přijme .csv soubor počasí a převede jej do DataFrame. První column je převedena na datetime objekt a je
        na ni nastaven Europe/Prague timezone. **Funkce je pouze pro starý formát a je zbytečná pro nový.**

        Args:
            is_iso8601: určuje, zda je datum v ISO8601 formátu, nebo v místním, českém
            file: .csv soubor pro přijetí
            ambiguous_localize: ambiguous parametr k funkci
                :doc:`tz_localize <pandas:reference/api/pandas.DataFrame.tz_localize>`
            drop: definuje zda zanechat pouze žádané položky nebo ne, tzn. že z původní databáze zanechá pouze 
                out_temp, out_humidity, dew_point, wind_speed, wind_dir, gust, bar a day_rain
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

        data: pd.DataFrame = pd.read_csv(file, parse_dates=[1], na_values=na_values, low_memory=False,
                                         date_parser=None if is_iso8601 else LegacyImport._data_parser)

        data.set_index("datetime", inplace=True)
        if remove_duplicit_index:  # index se odstraní až když je "datetime" indexem
            LegacyImport._drop_dupe_index(data)

        # lokalizace time zone
        data = data.tz_localize(time_zone, ambiguous=ambiguous_localize, nonexistent="shift_forward")
        if dropna_index:
            data = data[data.index.notna()]

        if drop:
            data = data[["out_temp", "out_humidity", "dew_point", "wind_speed", "wind_dir", "gust", "bar", "day_rain"]]

        data.rename({"day_rain": "rain_data"}, axis=1, inplace=True)
        return data

    @staticmethod
    def conv2012(inp="2012.csv", is2012: bool = True) -> pd.DataFrame:
        """
        Tato funkce dokáže vzít formát data *nejen* z roku 2012 a převést jej na
        `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_.

        Args:
            is2012: formát data roku 2012 je trochu jiný než oproti roku 2018, tento parametr existuje v rámci zachování
                kompatibility mezi oběma soubory
            inp: jméno souboru k úpravě

        Returns:
            DataFrame se správným formátem datu
        """

        def data_parser_additional(date):
            if date is np.nan:
                return None
            else:
                return datetime.datetime.strptime(date, "%d.%m.%Y %H:%M")

        df = pd.read_csv(inp, parse_dates=["datetime"],
                         date_parser=LegacyImport._data_parser if is2012 else data_parser_additional)
        return df

    @staticmethod
    def _drop_dupe_index(data: pd.DataFrame):
        """
        Funkce odstraní jakýkoliv duplicitní index z DataFrame.

        Args:
            data: odstranit data z tohoto DataFrame
        """
        data.drop(index=data[data.index.duplicated()].index, inplace=True)

    @staticmethod
    def _data_parser(date):
        if date is np.nan:
            return None
        else:
            return datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
