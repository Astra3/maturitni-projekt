# Třída {class}`EditData <pocasi.core.imp.EditData>`

Tato třída slouží ke zpracování a importu dat. Součástí její inicializace je DataFrame, se kterým třída bude pracovat.
Také seřadí index.

## Spojení dvou DataFrame dohromady

Metoda {meth}`pocasi.core.imp.EditData.combine` spojí DataFrame ve třídě a DataFrame/Series dohromady. Při tomto spojení
se odstraní duplicitní data vzniklé spojením a také se seřadí index.

## Generování dat o srážkách

Metoda {meth}`pocasi.core.imp.EditData.rainfall` generující srážky z dat. Ve výchozím stavu očekává nový formát dat, ale
umí i starý formát dat.

## Filtr divných dat

Metoda {meth}`pocasi.core.imp.EditData.filter_unrealistic_data` umí filtrovat z databáze hodnoty, které nedávají smysl.
Například odstraní všechny teploty nad 100°C a výkyvy teplot. Na tohle se používá funkce
{doc}`scipy:reference/generated/scipy.signal.find_peaks`. Program běží přes databázi v cyklu, dokud tahle funkce nevrátí
ani jedinou hodnotu. Poté se hodnoty v DataFrame obrátí a provádí se filtrace pro záporné a velmi nízké hodnoty.

Parametry funkce {doc}`scipy:reference/generated/scipy.signal.find_peaks` jsou nastaveny tak, aby se vyfiltrovalo vše,
co nedává smysl. Tyto hodnoty byly silně testovány a jsou funkční pro tyto účely. Jinými slovy, pokud mezi dvěma záznamy
dat vedle sebe je větší rozdíl než 3, je takhle vysoká hodnota přepsána na NaN.

## Uložení dat

Metoda {meth}`pocasi.core.imp.EditData.to_feather` umí uložit data do `pocasi_path` (výchozí stav) nebo `rain_path`.

## Obsah třídy `EditData`

```{eval-rst}
..  autoclass:: pocasi.core.imp.EditData
    :members:
    :noindex:
```

