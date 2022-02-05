import json

from bokeh.embed import json_item
from flask import Blueprint, abort, render_template, request

from pocasi.core.request import DataRequest, Graph

render = Blueprint("render", __name__)
table_index = ["Teplota (°C)", "Vlhkost (%)", "Rosný bod", "Tlak (hPa)", "Rychlost větru (m/s)", "Směr větru",
               "Nárazy větru"]


@render.route("/render_table")
def render_table():
    """Vrátí jQuery DataTable s daty o počasí.

    Přijímá následující GET parametry:
        * ``type`` - definuje typ grafu
            * ``1`` - vrátí data pouze o srážkách
            * cokoliv jiného - vrátí všechny data
        * ``start`` - definuje počáteční datum grafu
        * ``end`` - definuje konec grafu
    """
    values = _get_values(True)
    try:
        lol = DataRequest(values["start"], values["end"])
        if values["type"] != "1":
            # Pořadí položek v tabulce, v souladu s table_index
            order = ["out_temp", "out_humidity", "dew_point", "bar", "wind_speed", "wind_dir", "gust"]
            data = lol.raw_data().reindex(columns=order)
            index = table_index
            is_rain = False
        else:
            data = lol.raw_data(True)
            index = ["Srážky"]
            is_rain = True
        return render_template("render/raw_render.html", table=data, table_index=index, is_rain=is_rain)
    except (TypeError, KeyError) as ex:
        print(f"V aplikaci se stala chyba: {ex}")
        abort(400)


@render.route("/render_graf")
def render_graf():
    """Stránka co vrací JSON Bokeh grafu na základě možných GET parametrů:

    * ``type`` - definuje typ grafu
        * ``denní_souhrn`` - denní souhrny maximální, minimální a průměrné teploty
        * ``tlak`` - hodnoty tlaku
        * ``srážky`` - sloupcový graf srážek
    * ``start`` - definuje počáteční datum grafu
    * ``end`` - definuje konec grafu
    """
    values = _get_values(True)
    if values["type"] is not None:
        try:
            grafy = Graph(values["start"], values["end"])
            # Validní typy: "denní_souhrn", "tlak" a "srážky"
            match values["type"]:
                case "Denní teploty":
                    grafy.daily_temp()
                case "Tlak":
                    grafy.bar()
                case "Srážky":
                    grafy.rain()
                case _:
                    abort(404)
            val = json.dumps(json_item(grafy.p))
            return val
        # Zachytí všechny typy výjimek při neplatném datu, nemělo by se nikdy stát mimo přímý přístup na stránku
        except (TypeError, KeyError) as ex:
            print(f"V aplikaci se stala chyba: {ex}")
            abort(400)
    else:
        print('Přístup na stránku s grafy bez GET parametru "type"')
        return abort(400)


@render.route("/render_summary")
def render_summary():
    """Vytvoří denní souhrny dat. Přijímá ``start`` a ``end`` parametry přes GET."""
    values = _get_values()
    try:
        req = DataRequest(values["start"], values["end"])
        data = req.daily_summary()
        all_data = data[0].tz_convert("Europe/Prague").resample("D")
        return render_template("render/summary_render.html", data=data, all_data=all_data, index=table_index,
                               title="Prohlížeč dat")
    # Zachytí všechny typy výjimek při neplatném datu, nemělo by se nikdy stát mimo přímý přístup na stránku
    except (TypeError, KeyError) as ex:
        print(f"V aplikaci se stala chyba: {ex}")
        abort(400)


def _get_values(get_type: bool = False) -> dict:
    """Získá několik hodnot přes GET.

    Získá přes GET parametry ``start`` a ``end``. Případně může získat i parametr ``type``. Z těchto parametrů jsou
    odstraněny uvozovky a pokud jsou prázdné, jsou nastaveny na None.

    Args:
        get_type: Má získat i parametr ``type``?

    Returns:
        dictionary všech hodnot vypsaných výše.
    """
    values = {
        "type": request.args.get("type") if get_type else None,
        "start": request.args.get("start"),
        "end": request.args.get("end")
    }
    for key, item in values.items():
        if type(item) == str:
            values[key] = item.strip('"')

    for name, item in values.items():
        if item == "":
            values[name] = None

    return values
