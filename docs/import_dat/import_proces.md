# Proces importu a exportu dat počasí

Tento dokument popisuje, jak proběhl import všech dat všech formátů do jednotné databáze.

## Kód k importu dat ze stanice

Následující kód ukazuje, jak je možno zkombinovat všechny data z textových souborů do DataFrame a následně s ním
pracovat přes funkce v modulu pandas.

{{ data_import }}

% data_import je code block obsahující soubor se stejnojmenným jménem

:::{attention}

Kód není funkční v současné verzi programu kvůli rozhodnutí pro smazání výchozích dat!
:::

## Import z dat programu

K tomuhle slouží funkce {func}`imp <pocasi.core.imp.imp>`. Je detailněji popsaná v
{ref}`import_dat/současný_import:Import dat z Feather formátu`

## Export do formátu programu

Objekt třídy {class}`EditData <pocasi.core.imp.EditData>` má metodu pro uložení do feather formátu,
{meth}`to_feather <pocasi.core.imp.EditData.to_feather>`. V příkladě uvedeném v kapitole
{ref}`import_dat/import_proces:Kód k importu dat ze stanice` lze v posledních dvou zakomentovaných řádcích vidět, jak je
použít v kontextu daného procesu importu.

### Popis funkce exportu a importu

Pro projekt bylo rozhodnuto pro formát datového souboru [`feather`](https://arrow.apache.org/docs/python/feather.html).
Tento formát je binární a vznikl pouze za účelem pro knihovny jako `pandas`. Prvně před exportem se index zresetuje,
čili datum se nahradí číselnými hodnotami a datum se vrací do "datetime" sloupce. Tohle se pak napravuje při importu
dat.
