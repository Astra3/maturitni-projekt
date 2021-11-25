# Import dat nového formátu

Tato kapitola popisuje programátorský postup importu dat ze současné meteostanice. Cílem je mít celý import proveden
automaticky přes skript.

## Jak to funguje

Nový formát nesplňuje několik bodů pro {ref}`správný import dat <Pravidla pro správný import dat>`, jmenovitě datum,
časovou zónu a hlavičku ve dvou řádcích. Celý skript funguje tak, že hlavičku nejprve odstraní a poté přidá vlastní
hlavičku přizpůsobenou ostatním, starším formátům. Poté se odstraní druhý tabulátor z každého řádku, to zapříčiní
spojení data a času dohromady. Pak se samozřejmě ještě převede formát časového údaje do time-zone aware. **Celý formát
používá tabulátory!**

Formát hlavičky *(`\t` funguje jako tabulátor)*:

```none
datetime\tout_temp\thi_out_temp\tlow_out_temp\tout_humidity\tdew_point\twind_speed\twind_dir\twind_run\tgust\thi_wind_dir\twindchill\theat_index\tTHW_index\tbar\train\train_rate\thead_d-d\tcool_d-d\tin_temp\tin_humidity\tin_dew_point\tin_heat_index\tin_EMC\tin_air_density\twind_samp\twind_Tx\tISS_reception\tarc_interval\n
```

## Postup programu při importu dat z nových souborů

Tohle je podstatně jednodušší oproti starému formátu. Opět zde je kontrola, zda daný soubor vůbec existuje. Nakonec se
tento soubor otevře, do proměnné se načtou všechny jeho řádky a první dva se odstraní. Jsou nahrzeny indexem pro data
zmíněným v části {ref}`Jak to funguje`.

Dále se použije parser dat pro lokální časový formát a celá proměnná se dá, za pomocí StringIO do `pandas` přes
{doc}`pandas:reference/api/pandas.read_csv` metodu.

Jako finální krok nastavíme datum jako index a převedeme jej to timezone aware formátu, kterým je fixně "Europe/Prague".
Nakonec odstraníme hodnoty přebytečné pro tento projekt, například síla signálu venkovního senzoru ke stanici.

## Obsah skriptu `Core.imp`

```{eval-rst}
..  automodule:: Pocasi.core.imp
    :noindex:
    :members:
```
