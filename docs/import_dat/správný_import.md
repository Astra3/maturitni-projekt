# Pravidla pro správný import dat

Při zkoumání dat lze zjistit, že data nejsou poněkud správně zpracované, nicméně je možné je ještě zpracovat v programu.
Proto bylo ustanoveno několik pravidel pro správný import dat z textových souborů:

1. Číselné hodnoty nesmí být v uvozovkách.
2. Pro desetinné hodnoty se používá desetinná tečka.
3. Veškeré {abbr}`NaN (Not a Number)` hodnoty jsou v textu zapsané jako "nan", "---", "--.-", "------" nebo "--" (bez
   uvozovek).
4. Sloupec s časem a datem musí být jednotný (problém nového formátu).
5. Sloupec s časem by měl používat [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) nebo konzistentní datový formát.
6. Sloupec s časem a datem musí být nastaven jako index.
7. Veškerý formát zpracovaných dat musí být v UTC.
8. Duplicitní indexy musí vyfiltrovány být odstraněny.
9. Zbytečné sloupce obsahující data jako "index" nebo "save interval" jsou přebytečné a musí také pryč.
10. Odstranit veškeré řádky s indexem {abbr}`NaT (Not a Time)`.
11. Vyfiltrovat data s nereálnými hodnotami a nahradit je {abbr}`NaN (Not a Number)` hodnotami.

Ve výchozím stavu program filtruje při importu několik sloupců, které jsou irelevantní pro tento projekt, například
vnitřní teplotu. Je to z toho důvodu, že tyhle data jsou irelevantní pro sledování venkovního vývinu počasí. Více
informací nabízí funkce {func}`pocasi.core.imp.data_imp` a metoda {meth}`pocasi.core.imp.LegacyImport.old_import`.
