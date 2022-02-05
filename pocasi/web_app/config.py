class Config:
    # Tohle by samozřejmě mělo být ideálně v environment variable, pro účely lehčího testování není.
    # Tento token je důležitý z důvodu bezpečnosti, jeho únik by mohl vytvořit bezpečnostní díry za pomocí cookies v
    # login systému a formulářích. Jinými slovy zabraňuje CSRF.
    SECRET_KEY = "6cd39e51fe54aa7d47da9b7f6c82d1a0"
