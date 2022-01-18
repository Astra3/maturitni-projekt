from bokeh.resources import CDN
from flask import render_template

from Pocasi.core.request import DataRequest, Graph
from Pocasi.web_app import app


@app.route("/")
@app.route("/home")
def home():
    data = DataRequest.raw_data("2020-09-27")
    return render_template("table.html", data=data, zip=zip)


@app.route("/graphRend")
def graph_rend():
    graph = Graph()
    return graph.add_temp()


@app.route("/graf")
def graf():
    return render_template("graf.html", cdn=CDN.render())
