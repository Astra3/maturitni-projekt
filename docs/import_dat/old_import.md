# Import dat starého formátu

Tato část dokumentace je víceméně deprecated, nicméně je stále nezbytné popsat, jak proběhl proces importu dat formátu
ze staré meteostanice. Celý tento proces byl relativně trial and error.

---

% tohle je potřeba odkazovat zvlášť kvůli tomu nadpisu protože v něm je code...prostě lmao
(txt-format)=

## `.txt` formát

Původně byly všechny původní data v `.txt` formátu. Tento formát je velmi nevhodný pro zobrazení dat a víceméně fungoval
jako `.csv` oddělené tabulátory. V dropdown oknu pod odstavcem se nachází ukázka.

:::{dropdown} Ukázka dat ze souboru 1-2015.txt

```none
804	2015-01-01 00:07	10	43	19.1	74	-5.0	986.5	0.0	0.0	NNE	1028.9	-8.9	-5.0	0.0	0.0	0.0	0.0	0.0	0	0
805	2015-01-01 00:17	10	43	19.1	74	-5.0	986.5	0.0	0.0	NNE	1028.9	-8.9	-5.0	0.0	0.0	0.0	0.0	0.0	0	0
806	2015-01-01 00:27	10	43	19.1	75	-5.0	986.6	0.0	0.0	NNE	1029.0	-8.8	-5.0	0.0	0.0	0.0	0.0	0.0	0	0
807	2015-01-01 00:37	10	43	19.1	75	-5.0	986.5	0.0	0.0	NNE	1028.9	-8.8	-5.0	0.0	0.0	0.0	0.0	0.0	0	0
```

:::

% @formatter:off
:::{admonition} `.txt` soubory s počasím
:class: note
% @formatter:on

Skoro každý soubor mezi roky 2011 a 2018 je uložen v `.txt` formátu ve stejném, jako je zmíněný výše. Výjimku tvoří rok
2012 (viz {ref}`Rok 2012`) a prosinec 2018 (viz {ref}`Hlavičky textu`).
:::

Jak lze vidět, daným datům chybí i hlavička. Nicméně díky tomu, že jsou data konzistentní (kromě roku 2018, o něm
později), tak je můžeme velmi lehce před provedením dalších operací zkombinovat:

```none
cat *.txt > 2015.csv
```

Valná většina těchto `.txt` souborů používá desetinné čárky místo teček. Nicméně
používají [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
formát na data.

% @formatter:off
:::{admonition} Pozor na roky **2018** a **2012** a **červen 2015**!
:class: attention
% @formatter:on

Rok 2018 je v datech zapsaný jinak, veškeré data až do půlky prosince jsou v `.txt` souborech. Nicméně druhá půlka
prosince je v Excel souboru. Tento problém se řeší stejně, jako {ref}`Excel formát`. Tato část prosince má rovněž jinou
hlavičku (viz kapitola {ref}`Hlavičky textu`). {ref}`Červen roku 2015` je kombinace mezinárodního formátu data a
místního.

Rovněž také pozor na rok 2012 (viz {ref}`Rok 2012`) a červen roku 2015.
:::

### Červen roku 2015

Červen roku 2015 je z půlky napsaný v ISO 8601 a z menší, druhé půlky v místním časovém formátu. Při nezpracování může v
datech nastat následující situace:

```none
2015-01-07 00:06:00    13.9
2015-01-07 00:07:00   -14.5
2015-01-07 00:16:00    13.6
2015-01-07 00:17:00   -14.4
2015-01-07 00:26:00    13.4
```

Data zde se ukazují, jako že jsou v lednu, v reálu hodnoty s pozitivní teplotou jsou v červnu. Formát dat vypadá
následovně `2015-01-07` pro leden a `1.7.2015` pro červen. Stejně jako u zapeklité situace s
{ref}`rokem 2012 <Rok 2012>`, rovněž i zde můžeme použít metodu {meth}`Pocasi.core.imp.LegacyImport.conv2012`.

## Excel formát

Tímto elegantním řešením máme **skoro** (viz poznámka výše) hotové roky 2011-2018 a můžeme se pohnout dále. Tyto Excel
soubory mají jeden list na každý měsíc. Tohle je samozřejmě nežádoucí a je potřeba tyto listy vyexportovat do lépe
zpracovatelných souborů a zkombinovat. Elegantním řešením je použít tento skript[^1] pro LibreOffice Calc:

% @formatter:off
:::{dropdown} Převedení všech sheets do `.csv` v LibreOffice Calc
% @formatter:on

```{code-block} vbscript
:linenos:
:emphasize-lines: 16
REM  *****  BASIC  *****

Sub convertSheetsToCSVs
Dim fileProps(0) as new com.sun.star.beans.PropertyValue
sheets = ThisComponent.Sheets

fileProps(0).Name = "FilterName"
fileProps(0).Value = "Text - txt - csv (StarCalc)"

i = 0

Do While sheets.Count > i
  sheet = sheets.getByIndex(i)
  cntrllr = ThisComponent.CurrentController
  cntrllr.setActiveSheet(sheet)
  sURL = "filePath/" & sheets.ElementNames(i) & ".csv"
  ThisComponent.storeToURL(sURL, fileProps())
  i = i + 1
Loop
End Sub
```

Věnujte zvláštní pozornost zvýrazněnému řádku 16. Text `filePath` nahraďte absolutní cestou k souboru. Soubor se pak
uloží jako `jméno_listu.csv` do zadané cesty.
:::

Po zkombinování všech `.csv` souborů se setkáme s následující tabulkou (po otevření v tabulkovém editoru):

|     |                    |     |      |     |     |     |        |       |     |     |     |     |     |      |      |      |      |      |
|-----|--------------------|-----|------|-----|-----|-----|--------|-------|-----|-----|-----|-----|-----|------|------|------|------|------|
| 57  | 01.10.2019 0:02:50 | 10  | 19.1 | 69  | 8.4 | 89  | 1007.4 | 960.6 | 0.0 | 0.0 | E   | 6.7 | 8.4 | 0.00 | 0.00 | 1.80 | 0.00 | 1.80 |
| 58  | 01.10.2019 0:12:50 | 10  | 19.1 | 69  | 8.2 | 89  | 1007.4 | 960.6 | 0.0 | 0.0 | S   | 6.5 | 8.2 | 0.00 | 0.00 | 1.80 | 0.00 | 1.80 |
| 59  | 01.10.2019 0:22:50 | 10  | 19.1 | 69  | 8.2 | 90  | 1007.5 | 960.7 | 0.0 | 0.0 | S   | 6.7 | 8.2 | 0.00 | 0.00 | 1.80 | 0.00 | 1.80 |
| 60  | 01.10.2019 0:32:50 | 10  | 19.1 | 69  | 8.1 | 90  | 1007.6 | 960.8 | 0.0 | 0.0 | S   | 6.6 | 8.1 | 0.00 | 0.00 | 1.80 | 0.00 | 1.80 |

% @formatter:off
:::{admonition} Místní datový formát
% @formatter:on

Všimněte si, že Excel formát používá místní formát datu, na rozdíl od {ref}``.txt formátu <txt-format>``
:::

% @formatter:off
:::{admonition} Excel soubory s počasím
:class: note
% @formatter:on

Veškeré období mezi prosincem 2018 a březnem 2021 tvoří Excel tabulky s konzistentním formátováním. Jedinou výjimku
tvoří rok 2012.
:::

### Rok 2012

Celý rok 2012 je uložen jako Excel tabulka. To samo o sobě by nebyl problém, problém je, že tento rok používá místní
datový formát, stejně jako všechny ostatní Excel dokumenty. Nicméně jelikož se tento soubor nachází mezi spousty `.txt`
a sdílí s nimi i formát hlavičky, je zde porušena konzistence data (porušení bodu 5 v
{ref}`Pravidlech pro správný import <Pravidla pro správný import dat>`). Nejprve je třeba tyhle data odděleně
naimportovat a exportovat s jiným formátem data. Víceméně udělat něco na zkombinovaný dataset následujícího:

**Před provedením následující operace je třeba přidat do importovaného souboru hlavičku, více info v kapitole
{ref}`Hlavičky textu`!**

```pycon
>>> import pandas as pd
>>> df = pd.read_csv("Base data/total 2011-2018/2012.csv")
>>> df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1])
>>>
```

Případně lze ještě použít `df.to_csv(soubor.csv)`. Zde je tato možnost vynechána z důvodů pro funkční doctest.

## Hlavičky textu

Různé formáty dat mají různé hlavičky, tzn. že Excel formát má jiné hlavičky a `.txt` formát má taky jiné hlavičky.
Tohle pravidlo platí víceméně pro celou dokumentaci, až na slavný rok 2012 - ten sdílí hlavičku s ostatními `.txt`
soubory. Hlavičky všech souborů vypadají tedy následovně:

| Formát        | Hlavička                                                                                                                                                                                                |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `.txt` a 2012 | `no,datetime,interval,in_humidity,in_temp,out_humidity,out_temp,abs_pressure,wind_speed,gust,wind_dir,bar,dew_point,windchill,hour_rain,day_rain,week_rain,month_rain,total_rain,wind_level,gust_level` |
| Excel         | `no,datetime,interval,in_temp,in_humidity,out_temp,out_humidity,bar,abs_pressure,wind_speed,gust,wind_dir,dew_point,windchill,hour_rain,day_rain,week_rain,month_rain,total_rain`                       |

% @formatter:off
:::{note}
% @formatter:on

Pro zkopírování klikněte třikrát na danou hlavičku a pak použijte Ctrl+V.
:::

## Třída `LegacyImport`

```{eval-rst}
..  autoclass:: Pocasi.core.imp.LegacyImport
    :members:
    :noindex:
```

## Postup programu při importu dat ze souborů

Jak lze vidět, metoda {meth}`old_import <Pocasi.core.imp.LegacyImport.old_import>` má spoustu parametrů pro použití, a s
každým z nich se nakládá jinak. Nejprve funkce testuje, zda soubor zadaný do `file` vůbec existuje. Poté si funkce
vytvoří proměnnou `na_values` s NaN definicemi, které jsem objevil při analýze dat.

Dále se inicializuje parser na data a pak se za pomocí {doc}`pandas:reference/api/pandas.read_csv` přečte `.csv` soubor
s daty. Jako sloupec s daty se automaticky bere druhý sloupec, do parametru `na_values` se dává stejnojmenná
proměnná, `low_memory` se dává na False kvůli lepšímu a příjemnějšímu určení datových typů. Nakonec, do `date_parser` se
buď dává stejnojmenná funkce inicializovaná dříve, nebo None, na základě parametru `is_iso8601`. Nakonec se datum
nastaví jako index.

Nyní je na řade převedení dat do timezone aware formátu, jako timezone se automaticky bere Europe/Prague. Poté se na
základě parametru `remove_duplicit_index` odstraní duplicitní index dat za pomocí skryté metody
{meth}`drop_dupe_index <Pocasi.core.imp.LegacyImport._drop_dupe_index>`.

Úplně na závěr se odstraní přebytečné, a pro tento projekt nezajímavé, data, sloupec "day_rain" se přejmenuje na "rain",
jen kvůli konzistenci.

% @formatter:off
:::{warning}
% @formatter:on

Některé hodnoty se dávají na zpracování přímo modulu `pandas`. Na základě uživatelské chyby může program vyhodit
výjimku.
:::

[^1]: Odpověď se skriptem
na [ask.libreoffice.org](https://ask.libreoffice.org/t/how-do-i-export-all-sheets-from-a-spreadsheet/12024/4)