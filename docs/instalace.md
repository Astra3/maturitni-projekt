# Instalace modulu

Tahle stránka popisuje instalační proces celého programu.

## Virtual environment

### Funkce

Virtual environment (dále `venv`) slouží jako izolované Python prostředí. Jinými slovy, udělá nám větší pořádek v
nainstalovaných balíčcích, jelikož nemusíme používat balíčky, které máme nainstalované. Navíc umožní lepší vyváření
souboru s balíčky pro ostatní vývojáře.

### Instalace a aktivace

Prvním krokem je založit si venv (virtual environment). Jako u každého jiného Python projektu, založení venv není
nezbytným krokem, nicméně ulehčí organizaci balíčků nainstalovaných přes `pip`. Pokud si přejete přeskočit tuhle pasáž a
místo toho pracovat v systémovém prostředí, přeskočte na sekci {ref}`instalace:Instalace balíčků`.

`venv` založíme ve složce naší volby, preferovaně se ale používá složka "venv". Vytváří se následovně:

```
$ python3 -m venv venv
```

První `venv` značí název venv, druhé pak značí cestu. Po vytvoření je potřeba venv následovně aktivovat:

```
$ . venv/bin/activate
```

Před naší command prompt se poté objeví `(venv)`.

% @formatter:off
:::{admonition} Deaktivace `venv`
:class: important
% formatter:on

Pro deaktivaci se dá použít příkaz `deactivate`.
:::

## Instalace balíčků

Všechny vyžadované balíčky jak pro vyvíjení tak práci s modulem jsou definované v `requirements.txt` souboru. Instalační
manažer pro Python balíčky `pip` umí s těmito soubory pracovat a automaticky nainstalovat.

```
$ pip install -r requirements.txt
```

Takhle je vytvořen pořádek mezi nainstalovanými balíčky a je také nainstalováno vše, co je potřeba. Tento soubor se dá
také nainstalovat přes editor PyCharm. Zde stačí mít plugin na requirements.txt soubory, po jeho nainstalování a
otevření souboru v editoru se nabídne možnost automaticky nainstalovat všechny potřebné balíčky.

% TODO Doplnit informace, jak program spustit
