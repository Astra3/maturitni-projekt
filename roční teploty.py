from datetime import datetime
from pocasi import pocasi_data

year = datetime.now().year - 1

data = pocasi_data.loc["2012":str(year), "out_temp"]
ah = data.resample("Y")
avg = ah.mean()

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
