"""Tento soubor obsahuje třídy určené k importu dat počasí ve všech možných formátech."""
import datetime
import os.path
from io import StringIO

import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from pocasi import data_path, rain_path, time_zone


def data_imp(inp="PathLike[str]", drop: bool = True) -> pd.DataFrame:
    """Funkce importuje data ze souboru nového formátu z nové meteostanice.

    Args:
        inp: Cesta k souboru s daty.
        drop: Definuje, zda zanechat pouze žádané položky nebo ne, tzn. že z původní databáze zanechá pouze out_temp,
            out_humidity, dew_point, wind_speed, wind_dir, gust bar a rain_data, rovněž odstraní i NaT index.

    Returns:
        DataFrame všech hodnot.

    Raises:
        FileNotFoundError: Pokud žádný soubor na zadané cestě neexistuje.
    """
    if not os.path.isfile(inp):
        raise FileNotFoundError("Vstupní soubor nebyl nalezen")

    with open(inp, "r") as file:
        data = file.readlines()
    # Odstraní header a tabulátor u časových dat
    data = data[2:]
    data = [i.replace("\t", " ", 1) for i in data]

    # Vloží vlastní hlavičku
    data.insert(0,
                "datetime\tout_temp\thi_out_temp\tlow_out_temp\tout_humidity\tdew_point\twind_speed\twind_dir\t"
                "wind_run\tgust\thi_wind_dir\twindchill\theat_index\tTHW_index\tbar\train_data\train_rate\t"
                "head_d-d\tcool_d-d\tin_temp\tin_humidity\tin_dew_point\tin_heat_index\tin_EMC\tin_air_density\t"
                "wind_samp\twind_Tx\tISS_reception\tarc_interval\n")

    # Tohle spojí všechny listy do jednoho
    data = "".join(data)

    def date_parser(date):
        try:
            return datetime.datetime.strptime(date, "%d.%m.%y %H:%M")
        except ValueError:
            return None

    # StringIO vlastně převede string na file stream
    # noinspection PyTypeChecker
    df = pd.read_csv(StringIO(data), sep="\t", parse_dates=[0], date_parser=date_parser, na_values=["---", "------"])

    df.set_index("datetime", inplace=True)
    df = df.tz_localize(time_zone, ambiguous=False)
    if drop:
        df = df[["out_temp", "out_humidity", "dew_point", "wind_speed", "wind_dir", "gust", "bar", "rain_data"]]
        df = df.loc[df.index.dropna()]

    return df


def imp(rain: bool = False) -> pd.DataFrame:
    """Funkce importující data z Feather databáze definovanou v __init__.

    Args:
        rain: Určuje, zda importovat z ``rain_path`` nebo z ``data_path``.

    Returns:
        DataFrame počasí z Feather formátu.
    """
    df = pd.read_feather(rain_path) if rain else pd.read_feather(data_path)
    df.set_index("datetime", inplace=True)

    return df


class EditData:
    """Třída ke jednoduchým úpravám DataFrame a importu.

    Args:
        df1: Základní DataFrame, se kterým bude třída pracovat.
        sort: Určí, zda seřadit index při inicializaci, nebo ne.
    """

    def __init__(self, df1: pd.DataFrame | pd.Series, sort: bool = True):
        self.df = df1

        if sort:
            self.df.sort_index(inplace=True)

    def combine(self, df_append: pd.DataFrame | pd.Series) -> pd.DataFrame:
        """Metoda kombinující dohromady zadaný DataFrame, seřadí index a **odstraní duplicitní index**.

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
            df_append: DataFrame na kombinaci.

        Returns:
            Spojený DataFrame, rovněž také aktualizuje DataFrame uložený v objektu.
        """
        if isinstance(self.df, pd.Series):
            self.df = self.df.to_frame()
        if isinstance(df_append, pd.Series):
            df_append = df_append.to_frame()
        df = pd.concat([self.df, df_append])
        df.sort_index(inplace=True)

        self.df = df
        # Smaže duplicitní hodnoty v indexu
        self.df = self.df[~self.df.index.duplicated()]
        return df

    def rainfall(self, old: bool = False, drop_rain: bool = True, localize: bool = True) -> pd.Series:
        """Metoda vracející Series s daty o denních srážkách.

        Metoda bere data ze sloupce "rain_data" z DataFrame inicializovaném v objektu této třídy. Více o funkci v
        kapitole :ref:`import_dat/srážky:Srážky v počasí`.

        Args:
            localize: Odstranit data o časové zóně z výsledku?
            old: Rozlišuje mezi starým formátem srážek a novým (starý formát bere srážky na konci dne, nový sčítá srážky
             za celý den).
            drop_rain: Pokud True, tak odstraní "rain_data" column z DataFrame.

        Returns:
            Series, kde index jsou všechny dny a data tvoří informace o srážkách.
        """
        rain = self.df["rain_data"].resample("D")
        if old:
            rainfall: pd.Series = rain.last()
        else:
            rainfall = rain.sum()

        if localize:
            rainfall = rainfall.tz_localize(None)

        if drop_rain:
            self.df.drop(columns="rain_data", inplace=True)
        return rainfall

    def filter_unrealistic_data(self) -> None:
        """Odstraní velké výkyvy v datech.

        Obsahuje definici maximálních a minimálních parametrů. Rovněž filtruje všechny výkyvy v datech. **Vyžaduje, aby
        index neměl duplicitní data!**
        """

        # Dictionary sloupců, kde každý sloupec má tuple s (min, max) hodnotami pro daný sloupec
        min_max_values = {
            # (min, max)
            "out_temp": (-100, 100),
            "out_humidity": (1, 100),
            "dew_point": (-100, 100),
            "wind_speed": (0, 80),
            "bar": (800, 1200),
        }

        # Prochází sloupec za sloupcem a nahrazuje hodnoty zadané výše za NaN
        for name, values in min_max_values.items():
            self.df.loc[self.df[name] < values[0], name] = np.nan
            self.df.loc[self.df[name] > values[1], name] = np.nan

        # Hledá peaks v každém sloupci (výjimku tvoří směr větru)
        # Multiply zde slouží k pozdějšímu obrácení hodnot v DataFrame, změní se na -1 při druhém průchodu
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

    def to_feather(self, rain: bool = False) -> None:
        """Uloží data do feather formátu, který se používá v celém projektu.

        Args:
            rain (bool): Pokud True, bude ukládat do ``rain_path``, jinak do ``data_path``.
        """
        save = self.df.reset_index()
        path = rain_path if rain else data_path
        save.to_feather(path)


class ImportSave:
    """Jednoduchý import a uložení.

    Tato třída umí jednoduše naimportovat data ze souboru, převést je databáze, přidat je a uložit. Rovněž vytvoří
    zálohy starých dat. Měla by být výhradně použita v rámci context manageru.

    Raises:
        ValueError: Pokud se nenaleznou buď data srážek, nebo počasí - pokud neexistuje ani jedno, tak jsou automaticky
            vytvořeny.
    """

    def __init__(self):
        from pocasi import pocasi_data, rain_data

        if (pocasi_data is None) != (rain_data is None):
            raise ValueError("Chybí data počasí nebo srážek!")

        if (pocasi_data is None) and (rain_data is None):
            # Tahle situace by se reálně neměla stát, a tudíž nebude testovaná
            self.pocasi = EditData(pd.DataFrame())
            self.rain = EditData(pd.DataFrame())
        else:
            self.pocasi = EditData(pocasi_data)
            self.rain = EditData(rain_data)

    def import_append(self, file="PathLike[str]") -> None:
        """Rychlý import a přidání do DataFrames

        Args:
            file: Soubor **nového formátu**, ze kterého importovat.

        Raises:
            FileInvalidError: Výjimka je vyvolána, pokud je vstupní soubor neplatný nebo prázdný.
        """
        df = data_imp(file)
        if df.empty:
            raise FileInvalidError("Soubor se nezdá být platný!")
        edit = EditData(df)
        edit.filter_unrealistic_data()
        self.rain.combine(edit.rainfall())
        self.pocasi.combine(edit.df)

    def close(self) -> None:
        """Uloží data do jejich příslušných formátů, pokud spuštěno přes ``with`` keyword, spustí se automaticky.
        Taky vytvoří zálohu předešlých dat.
        """
        files = [data_path, rain_path]
        temp_files = [f"{data_path}.bak", f"{rain_path}.bak"]
        # Odstraní současné zálohy
        for temp_path in temp_files:
            if os.path.isfile(temp_path):
                os.remove(temp_path)

        # Přidá k současným souborům .bak příponu
        for path, temp_path in zip(files, temp_files):
            os.rename(path, temp_path)

        # Uloží nové .feather soubory
        self.rain.to_feather(True)
        self.pocasi.to_feather()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class FileInvalidError(Exception):
    """Chyba definující neplatný soubor, použitá v :class:`pocasi.core.imp.ImportSave`."""
    pass


class LegacyImport:
    """Import starého formátu.

    Třída obsahuje funkce a metody sloužící k importu starých formátů souborů. Nepoužité front-endem a označené jako
    private třída pro Sphinx.

    :meta private:
    """

    @staticmethod
    def old_import(file="PathLike[str]", ambiguous_localize: str = "infer", drop: bool = True, is_iso8601: bool = True,
                   dropna_index: bool = True) -> pd.DataFrame:
        """Metoda importující ``.csv`` soubor starého formátu.

        Metoda přijme ``.csv`` soubor počasí a převede jej do DataFrame. První column je převedena na datetime objekt
        a je na ni nastaven výchozí timezone. **Funkce je pouze pro starý formát a je zbytečná pro nový.**

        Args:
            is_iso8601: Určuje, zda je datum v ISO8601 formátu, nebo v místním, českém formátu.
            file: .csv soubor pro přijetí.
            ambiguous_localize: Ambiguous parametr k funkci
                :doc:`tz_localize <pandas:reference/api/pandas.DataFrame.tz_localize>`.
            drop: Definuje zda zanechat pouze žádané položky nebo ne, tzn. že z původní databáze zanechá pouze
                out_temp, out_humidity, dew_point, wind_speed, wind_dir, gust, bar a day_rain.
            dropna_index: Pokud True, tak odstraní všechny NaT hodnoty z indexu.

        Returns:
            pandas DataFrame přijatého souboru.
            
        Raises:
            FileNotFoundError: Pokud input file neexistuje na disku.
        """
        if not os.path.exists(file):
            raise FileNotFoundError("Zadaný soubor neexistuje.")

        na_values = ["nan", "---", "--.-", "--"]

        data: pd.DataFrame = pd.read_csv(file, parse_dates=[1], na_values=na_values, low_memory=False,
                                         date_parser=None if is_iso8601 else LegacyImport._date_parser)

        data.set_index("datetime", inplace=True)

        # Lokalizace time zone
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
            is2012: Formát data roku 2012 je trochu jiný než oproti roku 2018, tento parametr existuje v rámci zachování
                kompatibility mezi oběma soubory.
            inp: Jméno souboru k úpravě.

        Returns:
            DataFrame se správným formátem data.
        """

        def data_parser_additional(date):
            if date is np.nan:
                return None
            else:
                return datetime.datetime.strptime(date, "%d.%m.%Y %H:%M")

        df = pd.read_csv(inp, parse_dates=["datetime"],
                         date_parser=LegacyImport._date_parser if is2012 else data_parser_additional)
        return df

    @staticmethod
    def _date_parser(date):
        if date is np.nan:
            return None
        else:
            return datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
