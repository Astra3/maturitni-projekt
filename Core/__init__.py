"""
Hlavní funkcí Core balíčku je poskytnout funkční základní model programu pro počasí.

Soubor ukládá do proměnné ``database`` tabulku, kterou používá pro ukládání SQL. Je nezbytné ji upravit pro změnu
databáze.
"""
from sqlalchemy import create_engine

database = "sqlite:///database.db"

conn = create_engine(database)
