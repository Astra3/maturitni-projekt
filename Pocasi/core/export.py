"""
Export dat je nedokončená vlastnost programu z časových důvodů splnění deadline maturitní práce. V rámci splnění zadání
byl implementován jednoduchý export do csv
"""
from datetime import date

import pandas as pd

from Pocasi import pocasi_data


def to_csv(path="PathLike[str]", start: date | str = None, end: date | str = None):
    """
    Funkce, která uloží daný rozsah do specifikovaného .csv souboru.

    Args:
        path: cesta k uložení souboru
        start: začátek výběru
        end: konec výběru, pokud je ``None``, vybere vše od parametru ``start`` až po konec DataFrame

    Returns:

    """
    data: pd.DataFrame = pocasi_data.loc[start:end]
    data.to_csv(path)
