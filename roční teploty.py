from datetime import datetime
from pocasi import pocasi_data
from pocasi.core.request import DataRequest
import click

year = datetime.now().year - 1
click.echo("Zadejte jedničku pro výpočet průměru ze všech hodnot, nulu pro výpočet přes daily_summary.")
c = click.getchar()

if c == "1":
    click.secho("Všechny hodnoty", bold=True, fg="yellow")
    data = pocasi_data.loc["2012":str(year), "out_temp"]
else:
    click.secho("daily_summary", bold=True, fg="yellow")
    req = DataRequest("2012", str(year))
    data = req.daily_summary()[1]

res = data.resample("Y")
avg = res.mean()

print(avg)

# from bokeh.io import show
# from bokeh.plotting import figure
#
# p = figure(x_axis_type="datetime")
# p.xaxis.axis_label = "Datum"
# p.yaxis.axis_label = "Teplota"
# p.sizing_mode = "stretch_both"
# p.xaxis.major_label_orientation = 1.2
# p.toolbar.logo = None
# jj = ah.mean()
# jj = jj.to_frame()
# p.line("datetime", "out_temp", source=jj, line_join="round", legend_label="Průměrná roční teplota")
# show(p)
