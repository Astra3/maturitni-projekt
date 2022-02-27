# Tento soubor slouží ke spuštění webu v produkčním prostředí za pomocí gunicorn. Pro úspěšné spuštění je tedy potřeba
# mít nainstalovaný gunicorn
gunicorn "run_web:create_app()" -w 4 -b 0.0.0.0:5000
