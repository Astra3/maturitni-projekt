"""Soubor obsahující funkce pro dotazy z databáze"""
import datetime
from datetime import date
from typing import Tuple, List

import pandas as pd
from bokeh.embed import file_html
from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.resources import CDN
from pandas.core.resample import DatetimeIndexResampler

from Pocasi import pocasi_data, rain_data


class DataRequest:
    """
    Třída sloužící k základnímu zpracování dat, dokáže poskytnout denní data počasí i čisté výsledky dat

    Args:
        start: počáteční čas
        end: konečný čas

    Raises:
        KeyError: start je větší než end a výsledný DataFrame je tudíž prázdný
    """

    def __init__(self, start: date | str | None, end: date | str = None):
        self.request: pd.DataFrame = pocasi_data.loc[start:end]
        if self.request.empty:
            raise KeyError(f"Špatně zadaný index, parametr start ({start}) je větší než end ({end})")

    def daily_summary(self, time_offset: int = -1) -> Tuple[pd.DataFrame, pd.Series, List[DatetimeIndexResampler]]:
        """
        Funkce vracející denní souhrny teplot. Vrací denní průměrnou teplotu počítanou v 7:00, 14:00 a 21:00 (dvakrát),
        dále vrátí maximální vítr a teplotu a minimální teplotu i s ostatními hodnotami v té době.

        Args:
            time_offset: časový offset pro hodnoty měřené v daném čase, závisí na časové zóně

        Returns:
            Vrací tuple se třemi parametry. První je DataFrame všech hodnot v měřících časech teploty
            (7, 14 a 21 hodin). Druhý je denní průměr hodnot. Třetí položka je list obsahující
            ``DatetimeIndexResampler`` pandas objekty, kde první položka v listu je resampler maximální teploty, druhá
            obsahuje minimální teplotu, třetí maximální rychlost větru a čtvrtá nárazy větru.

            Rekapitulace:

            #. DataFrame hodnot v měřících časech
            #. denní průměr hodnot
            #. několik DatetimeIndexResampler objektů
                #. maximální teplota
                #. minimální teplota
                #. maximální rychlost větru
                #. maximální nárazy větru
        """

        request: pd.DataFrame = self.request
        request = request.loc[:, ["out_temp", "out_humidity", "dew_point", "bar", "wind_speed", "wind_dir", "gust"]]

        # odstraní nepotřebné sloupce
        resampled = request.loc[:, ["out_temp", "out_humidity", "wind_speed", "gust"]]
        resampled = resampled.resample("D")
        # tohle zapíše do všech hodnot původního DataFrame hodnotu maximální...divné vysvětlit mimo debugger
        max_min = [resampled.transform(max), resampled.transform(min)]

        # hodnoty jdou následovně v řadě: maximální teplota, minimální teplota a max vítr a nárazy
        max_min_values = [
            request[request.out_temp == max_min[0].out_temp],
            request[request.out_temp == max_min[1].out_temp],
            request[request.wind_speed == max_min[0].wind_speed],
            request[request.gust == max_min[0].gust]
        ]

        # odstraní informace o časovém pásmu a převede na DatetimeInderResampler
        max_min_values = [i.tz_convert(None) for i in max_min_values]
        max_min_values = [i.resample("D") for i in max_min_values]

        # udělá resample na dny pro všechny hodnoty
        request = request.resample("H").nearest()

        # hodnoty se vybírají jen podle GMT+1, čili se vše převede do UTC a z časů se pak odečítá jedna hodina
        request = request.tz_convert("UTC")

        # přidá do dataframe data hodnoty v sedm hodin GMT+1
        data: pd.DataFrame = request.at_time(datetime.time(7 + time_offset))
        # přidá následující časy do data a seřadí index
        times = [14, 21]
        for i in times:
            data = data.append(request.at_time(datetime.time(i + time_offset)))
        data.sort_index(inplace=True)

        # přidá poslední hodnotu z times k teplotě a spočítá denní průměry teplot
        temp_means: pd.Series = data.loc[:, "out_temp"]
        temp_means = temp_means.append(request.out_temp.at_time(datetime.time(times[-1] + time_offset)))
        temp_means = temp_means.resample("D").mean()
        temp_means.rename("temp_means", inplace=True)
        temp_means = temp_means.tz_convert(None)

        return data, temp_means, max_min_values

    def raw_data(self):
        """
        Statická metoda vracející slice z dat celého DataFrame. Nic extra speciálního, move on.

        Returns:
            Slice z ``pocasi_data``

        Raises:
            KeyError: pokud se nějaký z parametrů pro slice nelíbí pandas
        """

        return self.request


class Graph(DataRequest):
    """
    Třída sloužící ke následujících grafů:

    * tlak
    * denní souhrn průměrné, maximální a minimální teploty
    * sloupcový graf srážek

    Data se vybírají z rozsahu v parametrech ``start`` a ``end``. **Třída může mít neočekávané chování při tvorbě více
    než jednoho grafu!**

    Args:
        start: počáteční čas
        end: konečný čas

    Raises:
        KeyError: start je větší než end a výsledný DataFrame je tudíž prázdný
    """

    def __init__(self, start: date | str | None, end: date | str = None):
        super().__init__(start, end)
        self.rain_data: pd.DataFrame = rain_data.loc[start:end]

        # x-axis je ve všech případech datum
        self.p = figure(output_backend="webgl", x_axis_type="datetime",
                        tools="pan,wheel_zoom,reset,box_zoom,save,crosshair")
        self.p.xaxis.axis_label = "Datum"

        # metoda `bar` tuhle hodnotu přepisuje
        self._date_tooltip = ("Datum", "@datetime{%F}")
        self.p.sizing_mode = "stretch_both"
        self.p.xaxis.major_label_orientation = 1.2

        # odstraní bokeh logo
        self.p.toolbar.logo = None

    def bar(self) -> str:
        """
        Vytvoří spojnicový graf tlaku

        Returns:
            string s HTML tagy generující graf
        """
        name = "Tlak"
        self.p.line("datetime", "bar", source=self.request.tz_localize(None), line_join="round", legend_label=name)
        self.p.yaxis.axis_label = "Tlak (hPa)"

        self._date_tooltip = ("Datum", "@datetime{%x %X}")

        self.p.xaxis.major_label_orientation = 1.2

        hover = HoverTool(
            tooltips=[
                self._date_tooltip,
                (name, "@{bar}{0 0.0} hPa")
            ],
            formatters={
                "@datetime": "datetime"
            },
            mode="vline"
        )
        self.p.add_tools(hover)
        return file_html(self.p, CDN, name)

    def daily_temp(self) -> str:
        """
        Vytvoří spojnicový graf se třemi čárami, zelená s maximální teplotou, červená s průměrnou a modrá s minimální.
        Barvy se dají upravit v metodě, v proměnné pojmenované ``colors``.

        Returns:
            string s HTML tagy generující graf
        """
        self.p.yaxis.axis_label = "Teplota (°C)"

        name = {
            "temp_means": "t_avg",
            "max": "t_max",
            "min": "t_min"
        }
        # více barev zde https://docs.bokeh.org/en/latest/docs/reference/colors.html#bokeh-colors-named
        colors = {
            "temp_means": "red",
            "max": "green",
            "min": "dodgerblue"
        }
        daily = self.daily_summary()
        df = daily[1]
        df = df.to_frame()
        temp_max: pd.Series = daily[2][0].out_temp.max()
        temp_min: pd.Series = daily[2][1].out_temp.max()
        df = df.assign(max=temp_max, min=temp_min)
        df = df.tz_localize(None)

        self.p.line("datetime", "max", source=df, color=colors["max"], legend_label=name["max"])
        means = self.p.line("datetime", "temp_means", source=df, color=colors["temp_means"],
                            legend_label=name["temp_means"], line_width=1.5)
        self.p.line("datetime", "min", source=df, color=colors["min"], legend_label=name["min"])
        hover = HoverTool(
            renderers=[means],  # tooltip se vygeneruje pouze pro jednu čáru, ne pro všechny tři
            tooltips=[
                self._date_tooltip,
                (name["temp_means"], "@{temp_means}{0.00}°C"),
                (name["max"], "@{max}{0.00}°C"),
                (name["min"], "@{min}{0.00}°C")
            ],
            formatters={
                "@datetime": "datetime"
            },
            mode="vline"
        )
        self.p.add_tools(hover)
        # přidá možnost klikat na legendu a ztlumovat spojnice dle libosti
        self.p.legend.click_policy = "mute"

        return file_html(self.p, CDN, "Denní souhrny")

    def rain(self) -> str:
        """
        Vygeneruje sloupcový graf se srážkami.

        Returns:
            string s HTML tagy generující graf
        """
        self.p.yaxis.axis_label = "Srážky (mm/d)"
        name = "Srážky"

        self.p.vbar(x="datetime", top="rain_data", source=self.rain_data, legend_label=name, width=.5)

        hover = HoverTool(
            tooltips=[
                self._date_tooltip,
                (name, "@{rain_data} mm/d")
            ],
            formatters={
                "@datetime": "datetime"
            },
            mode="vline"
        )

        # FIXME hover tool nefunguje, nevím kde je chyba a hledat to nebudu
        self.p.add_tools(hover)
        return file_html(self.p, CDN, name)
