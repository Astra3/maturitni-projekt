# Denní souhrny a výpisy dat

Program umí hledat a zpracovat databázi počasí a vracet lehce zpracovatelné údaje.

## Základy o třídě DataRequest

Třída {class}`pocasi.core.request.DataRequest` se inicializuje s datem. Zde je příklad inicializace této třídy pro rok
2020 a 2021:

```pycon
>>> from pocasi.core.request import DataRequest
>>> data = DataRequest("2020", "2021")
```

## Denní souhrny

Denní souhrny jsou způsob, kterém lze získat informace o dnech v zadaném rozmezí dat. Metoda
{meth}`pocasi.core.request.DataRequest.daily_summary` vrací data v listu v následujícím rozložení:

1. DataFrame hodnot v měřících časech

   To jest DataFrame, který obsahuje hodnoty pro každý den zadaný v rozmezí při inicializaci třídy
   {class}`pocasi.core.request.DataRequest` v měřících časech (tedy v 7:00, 15:00 a 21:00). Tyto časy jsou o hodinu
   posunuté během průběhu letního času.
2. Denní průměry hodnot

   DataFrame, který obsahuje index dní a jejich průměrné hodnoty teplot.
3. Několik `DateTimeIndexResampler` objektů s minimálními a maximálními teplotami
    1. Maximální teplota
    2. Minimální teplota
    3. Maximální rychlost větru
    4. Maximální nárazy větru

   Tyto objekty obsahují maximální denní hodnoty včetně ostatních hodnot v době, kdy byly změřeny.

   :::{admonition} Použití `DateTimeIndexResampler` objektu
   :class: tip

   Následující kód ukazuje použití těchto objektů u maximální teploty za den 2020-01-05:
   ```pycon
   >>> from pocasi.core.request import DataRequest
   >>> data = DataRequest("2020-01-05", "2020-01-05")
   >>> summary = data.daily_summary()
   >>> 
   >>> for _, i in summary[2][0]:
   ...     print(i)
   ... 
                              out_temp  out_humidity  ...  wind_dir  gust
   datetime                                           ...                
   2020-01-05 13:41:30+01:00       1.3          63.0  ...        NW   5.4
   2020-01-05 13:51:30+01:00       1.3          63.0  ...        NW   5.8
   2020-01-05 14:01:30+01:00       1.3          62.0  ...        NW   4.8
   2020-01-05 14:11:30+01:00       1.3          63.0  ...        NW   2.7
   ```
   :::
4. Denní déšť

   DataFrame obsahující dny jako index a jako data hodnoty o srážkách.

## Výpis čistých dat

K tomu slouží metoda {meth}`pocasi.core.request.DataRequest.raw_data`.

Použití metody:

```pycon
>>> from pocasi.core.request import DataRequest
>>> data = DataRequest("2020-01-05", "2020-01-05")
>>> data.raw_data()
                           out_temp  out_humidity  ...  gust     bar
datetime                                           ...              
2020-01-05 00:01:30+01:00       0.9          92.0  ...   0.0  1012.9
2020-01-05 00:11:30+01:00       0.8          92.0  ...   0.0  1012.9
2020-01-05 00:21:30+01:00       0.7          92.0  ...   0.0  1013.1
2020-01-05 00:31:30+01:00       0.6          92.0  ...   0.0  1012.9
2020-01-05 00:41:30+01:00       0.6          92.0  ...   0.0  1012.9
                             ...           ...  ...   ...     ...
2020-01-05 16:41:30+01:00      -1.0          66.0  ...   1.0  1024.6
2020-01-05 16:51:30+01:00      -1.4          67.0  ...   0.0  1024.4
2020-01-05 17:01:30+01:00      -1.8          68.0  ...   1.4  1024.6
2020-01-05 17:11:30+01:00      -1.9          69.0  ...   0.0  1024.7
2020-01-05 17:14:24+01:00      -2.2          70.0  ...   0.0  1024.8
[105 rows x 7 columns]
```

## Obsah třídy `DataRequest`

```{eval-rst}
..  autoclass:: pocasi.core.request.DataRequest
    :noindex:
    :members:
```
