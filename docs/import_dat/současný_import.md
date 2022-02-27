# Import dat nového formátu

Tato kapitola popisuje programátorský postup importu dat ze současné meteostanice. Cílem je mít celý import proveden
automaticky přes skript.

## Jak to funguje

Nový formát nesplňuje několik bodů pro
{ref}`správný import dat <import_dat/správný_import:Pravidla pro správný import dat>`, jmenovitě datum, časovou zónu a
hlavičku ve dvou řádcích. Celý skript funguje tak, že hlavičku nejprve odstraní a poté přidá vlastní hlavičku
přizpůsobenou ostatním, starším formátům. Poté se odstraní druhý tabulátor z každého řádku, to zapříčiní spojení data a
času dohromady. Pak se samozřejmě ještě převede formát časového údaje do time-zone aware. **Celý formát používá
tabulátory!**

Formát hlavičky *(`\t` funguje jako tabulátor)*:

```none
datetime\tout_temp\thi_out_temp\tlow_out_temp\tout_humidity\tdew_point\twind_speed\twind_dir\twind_run\tgust\thi_wind_dir\twindchill\theat_index\tTHW_index\tbar\train\train_rate\thead_d-d\tcool_d-d\tin_temp\tin_humidity\tin_dew_point\tin_heat_index\tin_EMC\tin_air_density\twind_samp\twind_Tx\tISS_reception\tarc_interval\n
```

## Třída {class}`ImportSave <pocasi.core.imp.ImportSave>`

Pro usnadnění celého procesu existuje i třída {class}`ImportSave <pocasi.core.imp.ImportSave>`, která si automaticky
vezme DataFrame, se kterým se pracuje, přidá k němu data a uloží jej do výchozí cesty, společně se srážkami. Také
vytvoří zálohy předchozí databáze.

Příklad:

```{code-block} py
:linenos:
from pocasi.core.imp import ImportSave

with ImportSave() as imp:
    imp.import_append("2021.txt")
```

## Postup programu při importu dat z nových souborů

Tohle je podstatně jednodušší oproti starému formátu. Opět zde je kontrola, zda daný soubor vůbec existuje. Nakonec se
tento soubor otevře, do proměnné se načtou všechny jeho řádky a první dva se odstraní. Jsou nahrazeny indexem pro data
zmíněným v části {ref}`import_dat/současný_import:Jak to funguje`.

Dále se použije parser dat pro lokální časový formát a celá proměnná se dá, za pomocí StringIO do `pandas` přes
{doc}`pandas:reference/api/pandas.read_csv` metodu.

Jako finální krok nastavíme datum jako index a převedeme jej to timezone aware formátu, kterým je fixně "Europe/Prague".
Nakonec odstraníme hodnoty přebytečné pro tento projekt, například síla signálu venkovního senzoru ke stanici.

# Import dat z Feather formátu

Skript `pocasi.core.imp` obsahuje funkci {func}`pocasi.core.imp.imp`, která umožňuje jednoduchý import dat o dešti a
počasí.

```pycon
>>> from pocasi.core.imp import imp
>>> pocasi = imp()
>>> rain = imp(True)
```

## Obsah skriptu `pocasi.core.imp`

```{eval-rst}
..  automodule:: pocasi.core.imp
    :noindex:
    :members:
```
