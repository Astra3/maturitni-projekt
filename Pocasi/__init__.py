"""
Balíček Počasí slouží k analýze dat z meteostanice. Je rozdělený na tři části:
* ``core`` se stará o import dat, jejich export, výpis dat a tvorbu grafů
* ``cli`` je pro terminálový front-end k balíčku ``core`` a jedná se vlastně o uživatelské rozhraní v CLI
* ``web`` je webový front-end pro balíček ``core``, jedná se o uživatelské rozhraní ve webovém prohlížeči

Soubor ``__init__`` ukládá do proměnné ``data_path`` cestu k tabulce databáze. Jedná se o feather databázi,
takže její přípona je zpravidla ``.feather``. To stejné platí pro rain_path, akorát jde o data o počasí. """

data_path = "database.feather"
rain_path = "rainfall.feather"
