from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileSize
from wtforms import SubmitField
from wtforms.validators import DataRequired


class ImportForm(FlaskForm):
    """Formulář přijímající soubor s daty pro import."""

    file = FileField("Importovaná data",
                     validators=[FileAllowed(["csv", "txt"]), FileSize(max_size=1.0486 * 10 ** 7), DataRequired()])
    submit = SubmitField("Nahrát")
