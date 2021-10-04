Instalace modulu
==================

Tahle stránka popisuje instalační proces celého programu.

Virtual environment
--------------------

Funkce
^^^^^^
Virtual environment (dále ``venv``) slouží jako izolované Python prostředí. Jinými slovy, udělá nám větší pořádek v
nainstalovaných balíčcích, jelikož nemusíme používat balíčky, které máme nainstalované. Navíc umožní lepší vyvoření
souboru s balíčky pro ostatní vývojáře.

Instalace a aktivace
^^^^^^^^^^^^^^^^^^^^^
Prvním krokem je založit si venv (virtual environment). Jako u každého jiného Python projektu, založení venv
není nezbytným krokem, nicméně ulehčí organizaci balíčků nainstalovaných přes ``pip``. Pokud si přejete přeskočit
tuhle pasáž a místo toho pracovat v systémovém prostředí, přeskočte na sekci :ref:`Instalace balíčků<Instalace balíčků>`.

``venv`` založíme ve složce naší volby, preferovaně se ale používá složka "venv". Vytváří se následovně:

..  code-block:: bash

    $ python3 -m venv venv

První ``venv`` značí název venv, druhé pak značí cestu. Po vytvoření je potřeba venv následovně aktivovat:

..  code-block:: bash

    $ . venv/bin/activate

Před naší command prompt se poté objeví ``(venv)``.

..  note::
    Pro deaktivaci se dá použít příkaz ``deactivate``.


Instalace balíčků
------------------
Všechny vyžadované balíčky jak pro vyvíjení tak práci s modulem jsou definované v ``requirements.txt`` souboru.
Instalační manažer pro Python balíčky ``pip`` umí s těmito soubory pracovat a automaticky nainstalovat.

..  code-block::

    $ pip install -r requirements.txt

Takhle je vytvořen pořádek mezi nainstalovanými balíčky a je také nainstalováno vše, co je potřeba.

..  TODO Doplnit informace, jak program spustit
