# Srážky v počasí

Pro správné zpracování dat počasí je velmi nezbytné zpracovávat srážky. V základních datech se srážky nacházely ve dvou
formách:

1. déšť zaznamenaný každých 24 hodin
2. počet srážek za každý jeden záznam

## Starý formát srážek

Starý formát zaznamenával srážky do záznamů ve 24 hodinovém intervalu. Jinými slovy, pokud v nějakém záznamu přibyde
nějaký počet srážek, tento počet srážek se zde zachová po dobu uplynutí 24 hodin.

% @formatter:off
:::{admonition} Příklad
:class: note
% @formatter:on

Například, pokud v záznamu 24. 11. 2018 8:50 přibude 0.2 mm srážek, tak tato hodnota se smaže v čase 25. 11. 2018 8:50.
Každá hodnota, která přijde mezi tímto čase se přičte a odečte po uplynutí jednoho dne od jejího přičtení.
:::

Meteorologie pracuje s tímto údajem běžně a zapisuje jeho stav na konci dne. Program tedy bere poslední záznam z daného
dne a zapíše do databáze denní déšť, na základě tohoto záznamu.

## Nový formát srážek

Nový formát srážek zapisuje počet srážek pro daný záznam. Program tedy pak pro získání celkového počtu srážek musí
všechny záznamy za daný den sečíst.

## Postup programu při zpracování srážek

Nejprve se na DataFrame inicializovaný ve třídě EditData aplikuje `groupby` metoda na sloupec "rain":

```python
rain = self.df["rain"].groupby(self.df.index.date)
```

Poté můžeme pokračovat s dalšími úpravami.

### Starý formát

Tohle seskupí data mezi dny, a za pomocí metody `tail(1)` získáme poslední záznam za den. Nakonec provedeme následující
na index dat:

```python
pd.to_datetime(rainfall.index.date)
```

Poté v případě zájmu uživatele převedeme časový index do časové zóny (vzhledem k tomu, že neukládáme čas, se ve výchozím
stavu tohle neprovádí).

### Nový formát

Převod nového formátu je podstatně jednodušší, víceméně spočívá jen v použití metody `sum()` na DataFrame a opět převod
data do Pandas datetime formátu.

## Metoda `rainfall`

```{eval-rst}
..  automethod:: pocasi.core.imp.EditData.rainfall
    :noindex:
```