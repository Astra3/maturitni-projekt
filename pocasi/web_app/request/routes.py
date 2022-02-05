from tempfile import gettempdir

from bokeh.resources import CDN
from flask import Blueprint, render_template, flash
from flask_login import login_required

from pocasi.core.imp import ImportSave, FileInvalidError
from pocasi.web_app.request.forms import ImportForm

request_blueprint = Blueprint("request_blueprint", __name__)


@request_blueprint.route("/summary")
def summary():
    """Stránka s formulářem pro denní souhrn."""
    js_file = "js/js_request.html"
    # Ukazuje počet dní, po kolika zobrazit varování o zobrazení moc dat, pro odstranění stačí nastavit na 0
    day_limit = 400
    return render_template("request/data_request_form.html", title="Denní souhrn", js_file=js_file,
                           day_limit=day_limit)


@request_blueprint.route("/table")
def table():
    """Stránka s formulářem pro tabulku na vypsání čistých dat."""
    # Změna pořadí v dropdown vyžaduje změnu v render_table cestě!
    dropdown = ["Veškeré zaznamenané data", "Srážky"]
    day_limit = 40
    return render_template("request/dropdown_request_form.html", title="Výpis dat", dropdown=dropdown,
                           day_limit=day_limit, is_table=True)


@request_blueprint.route("/graf")
def graf():
    """Stránka s formulářem pro grafy."""
    dropdown = ["Denní teploty", "Tlak", "Srážky"]
    day_limit = 0
    # cdn parametr zde slouží pro inicializaci BokehJS
    return render_template("request/dropdown_request_form.html", title="Graf", dropdown=dropdown, day_limit=day_limit,
                           is_graph=True, cdn=CDN.render())


@request_blueprint.route("/import_data", methods=["GET", "POST"])
@login_required
def import_data():
    """Stránka vyžadující login s formulářem pro import dat."""
    form = ImportForm()
    if form.validate_on_submit():
        file_name = "pocasi_projekt.csv"
        file_data: str = form.file.data.read().decode()
        temp_file_path = f"{gettempdir()}/{file_name}"
        with open(temp_file_path, "w") as f:  # Soubor se ukládá to temp directory
            f.write(file_data)
        try:
            with ImportSave() as imp:
                imp.import_append(temp_file_path)
            flash("Soubor úspěšně nahrán!", "success")
            flash("Je vyžadován restart aplikace pro provedení změn!", "warning")
        except FileInvalidError:
            flash("Nahraný soubor byl neplatný!", "danger")
    return render_template("request/import_form.html", form=form, title="Import dat")
