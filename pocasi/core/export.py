"""
Export dat je nedokončená vlastnost programu z časových důvodů splnění deadline práce. V rámci splnění zadání
byl implementován jednoduchý export do csv.
"""
from datetime import date

import pandas as pd

from pocasi import pocasi_data


def to_csv(path="PathLike[str]", start: date | str = None, end: date | str = None) -> None:
    """Funkce, která uloží daný rozsah dat do specifikovaného .csv souboru.

    Args:
        path: Cesta k uložení souboru.
        start: Začátek výběru.
        end: Konec výběru, pokud je ``None``, vybere vše od parametru ``start`` až po konec DataFrame.
    """
    data: pd.DataFrame = pocasi_data.loc[start:end]
    data.to_csv(path)
