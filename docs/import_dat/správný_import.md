# Pravidla pro správný import dat

Při zkoumání dat lze zjistit, že data nejsou poněkud správně zpracované, nicméně je možné je ještě zpracovat v programu.
Proto existuje několik pravidel pro správný import dat:

1. Číselné hodnoty nesmí být v uvozovkách.
2. Pro desetinné hodnoty se používá desetinná tečka.
3. Veškeré {abbr}`NaN (Not a Number)` hodnoty jsou v textu zapsané jako "nan", "---", "--.-", "------" nebo "--" (bez
   uvozovek).
4. Sloupec s časem a datem musí být jednotný (problém nového formátu).
5. Sloupec s časem by měl ideálně používat [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) nebo konzistentní datový
   formát.
6. Sloupec s časem a datem musí být nastaven jako index.
7. Veškerý formát data musí být v UTC.
8. Duplicitní data musí vyfiltrovány být odstraněny.
9. Zbytečné sloupce obsahující data jako "index" nebo "save interval" jsou přebytečné a musí také pryč.
10. Odstranit veškeré řádky s indexem {abbr}`NaT (Not a Time)`
11. Odstranit řádky plné {abbr}`NaN (Not a Number)` hodnot

Ve výchozím stavu program nesplňuje kompletně bod 5, jelikož filtruje více sloupců než je nezbytně třeba, například
vnitřní teplotu. Je to z toho důvodu, že tyhle data jsou irelevantní pro sledování venkovního vývinu počasí. Více
informací nabízí funkce {func}`Pocasi.core.imp.data_imp` a metoda {meth}`Pocasi.core.imp.LegacyImport.old_import`.
