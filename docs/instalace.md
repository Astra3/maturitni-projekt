# Instalace modulu

Tahle stránka popisuje instalační proces celého programu.

## Předpoklady pro instalaci

Následující návod předpokládá, že na systému je nainstalovaný Python 3.10 a že pod příkazem `python` v terminálu je
tahle verze. Verze se dá vyčíst spuštěním tohoto příkazu v terminálu.

Na operačním systému Windows je doporučena verze programu Python z Microsoft Store (kvůli její jednoduché přístupnosti z
PowerShell a jednoduché instalaci), na Linuxu z repozitářů distributora používané distribuce.

## Virtual environment

Virtual environment (dále `venv`) slouží jako izolované Python prostředí. Jinými slovy, udělá nám větší pořádek v
nainstalovaných balíčcích, jelikož nemusíme používat balíčky, které máme nainstalované pro celý systém. Navíc umožní
lepší vyváření souboru s balíčky pro ostatní vývojáře.

### Instalace a spouštění

Prvním krokem je založit si venv (virtual environment). Jako u každého jiného Python projektu, založení venv není
nezbytným krokem, nicméně ulehčí organizaci balíčků nainstalovaných přes `pip`. Pokud si přejete přeskočit tuhle pasáž a
místo toho pracovat v systémovém prostředí, přeskočte na sekci {ref}`instalace:Instalace balíčků`.

`venv` založíme ve složce naší volby, preferovaně se ale používá složka "venv". Vytváří se následovně:

```
$ python -m venv venv
```

První `venv` značí název venv, druhé pak značí cestu. Po vytvoření je potřeba venv následovně aktivovat:

```
$ . venv/bin/activate
```

Před naší command prompt se poté objeví `(venv)`. Tento dá stylizovat pouze pokud uživatel
používá [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh) a nainstaluje si na
úpravu [plugin](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/virtualenv).

% @formatter:off
:::{admonition} Deaktivace `venv`
:class: important
% formatter:on

Pro deaktivaci se dá použít příkaz `deactivate`.
:::

## Instalace balíčků

Všechny vyžadované balíčky jak pro vyvíjení tak práci s modulem (mimo dokumentaci, viz {ref}`build_dokumentace:Instalace potřebných modulů`) jsou definované v `requirements.txt` souboru. Instalační
manažer pro Python balíčky `pip` umí s těmito soubory pracovat a automaticky nainstalovat.

```
$ pip install -r requirements.txt
```

Takhle je vytvořen pořádek mezi nainstalovanými balíčky a je také nainstalováno vše, co je potřeba. Tento soubor se dá
také nainstalovat přes editor PyCharm. Zde stačí mít plugin na requirements.txt soubory, po jeho nainstalování a
otevření souboru v editoru se nabídne možnost automaticky nainstalovat všechny potřebné balíčky.

## CSRF token
Tento token brání proti [CSRF](https://cs.wikipedia.org/wiki/Cross-site_request_forgery) útokům na stránku přes cookies.
Odkaz výše odkazuje na Wikipedii, kde je napsaný příklad útoku. Tato aplikace používá autorizační token proti CSRF.

:::{admonition} CSRF token není nutný pro **testování** aplikace
:class: tip
Modul si umí vygenerovat vlastní CSRF token pro zlehčení testování a pro umožnění vygenerování API dokumentace. Pokud je
tento token takto vygenerován, skript vypíše varování do konzole.
:::

### Vygenerování CSRF tokenu

V mnoha případech by si člověk mohl říct, že pseudonáhodný token by byl dostačující, nicméně webové aplikace musí mít 
vysoké zabezpečení, a čím méně předvídatelné náhody, tím lépe.

Python obsahuje modul {doc}`secrets <python:library/secrets>`, který slouží ke generování, ačkoliv stále 
pseudonáhodných, silných a těžko předvídatelných tokenů. Příklad vygenerování tokenu do této aplikace

:::{code-block} pycon
:emphasize-lines: 2, 3
:linenos:
>>> import secrets
>>> secrets.token_hex(16)
'38c753c0b645505a7e04431eb4f776bd'
>>>
:::

Takhle vygenerovaný token (řádek 3) potom můžeme zkopírovat do environment variable. Na řádku 2 můžeme změnit v 
parametru funkce `token_hex`, který změní délku výsledného klíče.

### Nastavení environment variable

Environment variable (dále "env var"), česky proměnná prostředí, je typ proměnné, která je zachována a přístupná pro 
všechny programy operačního systému, pro které byla inicializována. Tento projekt ji používá pro uschování CSRF tokenu. 

Kvůli vysokému zabezpečení tohoto tokenu je nejlepší ho mít v env var. Env var se vytvářejí jinak na každém operačním
systému, nicméně zde jsou příkazy pro její vytvoření v na Windows a Linux rámci tohoto programu:

::::::{tab-set}
:::::{tab-item} Windows

::::{tab-set}
:::{tab-item} PowerShell
```powershell
$Env:<POCASI_APLIKACE_WEB> = "secret_key"
python web_app.py
```
:::

:::{tab-item} CMD
```bat
setx POCASI_APLIKACE_WEB "secret_key"
python web_app.py
```
:::
::::

:::::

:::::{tab-item} Linux
Pro Linux existují dvě možnosti:
1. Proměnnou exportovat přes `export` a pak spustit program:
    ```bash
    $ export POCASI_APLIKACE_WEB="secret_key"
    $ python web_app.py
    ```
2. Vytvořit proměnnou přímo před programem:
    ```bash
    $ POCASI_APLIKACE_WEB="secret_key" python web_app.py
    ```
:::::
::::::

## Nastavení hesla

Program používá heslo zabezpečené pomocí bcrypt algoritmu. Vzhledem k tomu, že program bude používat jen jeden uživatel,
heslo se nachází v souboru `heslo.txt`. Výchozí heslo je `123456`, ale dá se změnit například následovně:

:::{code-block} pycon
:emphasize-lines: 2
>>> from pocasi.web_app import bcrypt
>>> bcrypt.generate_password_hash("heslo").decode()
'$2b$12$OlJIcEe1xRJH8AaKbXLZnO9nADZNitS/Fj7r9EhiNpj6vEDtLnznW'
:::

Na zvýrazněném řádku změníme string `"heslo"` na vlastní heslo, které nám vyhovuje. Výsledný string z funkce můžeme poté 
zkopírovat a vložit do souboru `heslo.txt`.

## Spouštění programu

Stačí se jen navigovat do složky, kde se nachází skript `run_web.py` (domovská složka projektu). Ten stačí spustit pro 
webové rozhraní.

:::{warning}
Před spuštěním programu je potřeba se ujistit, že se terminál nachází ve stejné složce, jako `run_web.py`!
:::

## Pokročilá konfigurace

Program nabízí možnost si nakonfigurovat cesty k souborům a časovou zónu dle libosti.

### Konfigurace cestám k souborům databáze

Program ukládá dvě databáze, jednu pro déšť a druhou pro všechny ostatní data. Při importu nových dat přes webové rozhraní se tyhle databáze
zkopírují (zůstávají ve stejných složkách) a stará verze dostane příponu `.bak`. Funguje tedy jako záloha.

Pro změnu cest stačí změnit hodnoty proměnných ve složce `pocasi`, soubor `__init__.py`. Konkrétně se jedná o proměnné:

* `rain_path` - cesta k dešti
* `data_path` - cesta k ostatním datům

Cesty mohou být jak absolutní (třeba `C:\Users\foo\database.feather`), tak i relativní (například `foo/database.feather`).
Pokud jsou relativní, tak jejich počáteční bod je ve složce, kde byl program spuštěn (anglicky working directory).

### Konfigurace časové zóny

Jméno současně používané časové zóny, se nachází ve složce složce 
`pocasi`, v souboru `__init__.py`, v proměnné `time_zone`. Program vezme jakoukoliv časovou zónu, kterou vezme modul 
{doc}`datetime <python:library/datetime>`.

% @formatter:off
:::{admonition} Nebezpečí změny časové zóny
:class: danger
% formatter:on

Změna časové zóny je **velmi** nebezpečná operace vyžadující spousty testování, pokud je provedena. Nyní totiž testována
není!
:::

Pro úspěšnou **teoretickou** změnu časového pásma, je potřeba provést následující kroky:

1. Změna proměnné `time_zone` v `__init__.py`
2. Změna výchozí hodnoty parametru `time_offset` v metodě 
{meth}`daily_summary() <pocasi.core.request.DataRequest.daily_summary>`
3. Import databáze, změna časové zóny v ní a následné uložení

Jednoduchá změna časového pásma v datech počasí by vypadala nějak takhle:

```{code-block} py
:emphasize-lines: 4
from pocasi.core.imp import imp, EditData

data = imp()
data = data.tz_convert("UTC")

edit = EditData(data)
# edit.to_feather()
```

Zvýrazněný řádek provádí tyhle časové změny, hodnota v uvozovkách je název časového pásma.

:::{caution}
Soubor se daty o srážkách **ne**obsahuje informace o časovém pásmu, jinými slovy, je tz-naive. Je přizpůsobený pouze na 
časové pásmo "Europe/Prague," a jeho změna by vyžadovala náročné a velké úpravy. 
:::
