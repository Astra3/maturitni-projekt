# Zpracování dokumentace

Tato kapitola se zabývá zpracováním HTML dokumentace a převod ze Sphinx formy do HTML.

## Instalace potřebných modulů

Moduly a knihovny potřebné ke zpracování a převodu souborů dokumentace se nachází v `requirements_dokumentace.txt`. Pro
jejich instalaci stačí do terminálu zadat:

```none
pip install -r requirements_dokumentace.txt
```

Tím se nainstaluje Sphinx a všechny potřebné doplňky.

## Psaní do dokumentace

Dokumentace se nachází ve složce `docs/`, kde ve složce `_templates` jsou předlohy a ve složce `_build` výsledné formáty
z build procesu. Samotné soubory dokumentace mají buď příponu `.md` nebo `.rst`. `.md` je pro Markdown soubory a veškerý
text v těchto souborech je napsaný v Markdown formátu. `.rst` je pro reStructuredText soubory, které jsou jen ve složce
`API/`. Jak se píše Markdown syntax pro Sphinx je definováno
v [manuálu pro myST](https://myst-parser.readthedocs.io/en/latest/sphinx/index.html). Obsažena je i dokumentace API,
vygenerována přes [`sphinx.ext.autodoc`](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html).

## Build dokumentace

Zde se budeme zabývat, jak vygenerovat API dokumentaci a jak převést dokumentaci do HTML a epub formátů. Sphinx je
nástroj určený ke tvorbě technických dokumentací k (zejména) Python projektům, nabízející neskutečně obrovské nástroje
ulehčující a automatizující celou práci.

### Build API dokumentace

K tomu se používá `sphinx-apidoc` příkaz, který je nainstalovaný společně se Sphinx. Provádí se následovně, předpokládá
se že working directory je v `docs`:

```none
sphinx-apidoc -PMfo API/ -t _templates/ ../pocasi
```

Tím se vytvoří ve složce `API/` soubory k API dokumentaci, ke kterým je automaticky vytvořen i jejich obsah.

### Build do HTML a epub formátů

Následující příkaz vytvoří HTML a epub dokumentaci, opět se předpokládá že working directory je `docs`:

```none
sphinx-build -b html . _build/html
sphinx-build -b epub . _build/epub
```

:::{admonition} Lze použít i `make`
:class: hint

Za předpokladu, že máte nainstalovaný příkaz `make`, je možno jej použít pro zpracování dokumentace:

```none
make html
make epub
```

:::

:::{attention}

Pro kompletní build dokumentace je smazat obsah ve složkách `_build` a `API`. Nestane se-li tak, změní se pouze soubory,
ve kterých byly provedeny úpravy (nežádoucí pro HTML dokumentaci)!
:::

:::{seealso}

[`rinohtype`](https://github.com/brechtm/rinohtype) -- dá se použít ke tvorbě pdf souborů z dokumentace
:::
