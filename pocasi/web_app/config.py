from os import getenv

import click

token = getenv("POCASI_APLIKACE_WEB")
if token is None:
    click.secho("VAROVÁNÍ!", fg="red", bold=True)
    click.secho("Environment variable 'POCASI_APLIKACE_WEB' nebyla nastavena, nastavuji výchozí hodnotu!\n"
                "Pokud neplánujete použít během tohoto spuštění webové rozhraní, můžete tuto zprávu ignorovat.",
                fg="red")
    # noinspection SpellCheckingInspection
    token = "99dffb7a12f77ede47a83175bc0c430b0d35939a4d705eadfe5039ca0ab5cd9e"


class Config:
    # Tento token je důležitý z důvodu bezpečnosti, jeho únik by mohl vytvořit bezpečnostní díry za pomocí cookies v
    # login systému a formulářích. Jinými slovy zabraňuje CSRF.
    SECRET_KEY = token
