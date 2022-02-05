"""
Balíček Počasí slouží k analýze dat z meteostanice. Je rozdělený na tři části:
* ``core`` se stará o import dat, jejich export, výpis dat a tvorbu grafů
* ``web_app`` je webový front-end pro balíček ``core``, jedná se o uživatelské rozhraní ve webovém prohlížeči

Soubor ``__init__`` ukládá do proměnné ``data_path`` cestu k tabulce databáze. Jedná se o feather databázi,
takže její přípona je zpravidla ``.feather``. To stejné platí pro rain_path, akorát jde o data o počasí. Soubory
sloužící jako zálohy mají příponu ``.bak``.

Dále inicializuje proměnné ``rain_data`` a ``pocasi_data`` s příslušnými daty, za předpokladu, že soubory uvedené v
``path`` proměnných existují. Pokud ne, jsou obě hodnoty nastaveny na ``None``. """
from os import path

data_path = "database.feather"
rain_path = "rainfall.feather"
time_zone = "Europe/Prague"
# Při změně timezone věnujte pozornost i time_offset parametru u metody Pocasi.core.request.DataRequest.daily_summary

from pocasi.core.imp import imp

pocasi_data = imp() if path.isfile(data_path) else None
rain_data = imp(True) if path.isfile(rain_path) else None
