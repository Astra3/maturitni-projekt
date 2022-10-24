# Maturitní projekt

Tohle repo funguje jako úložiště a archiv maturitního projektu.

## Build dokumentace

Základem spuštění projektu je nahlédnout do Sphinx dokumentace. Pro její build stačí nainstalovat requirements (ideálně
do virtual environment) a spustit:

```
pip -r requirements_dokumentace.txt
cd docs/
make html
```

Tato dokumentace obsahuje i API použití projektu a webového rozhraní.
