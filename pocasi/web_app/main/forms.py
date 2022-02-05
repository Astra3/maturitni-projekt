from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

from pocasi.web_app import bcrypt


# noinspection PyMethodMayBeStatic
class LoginForm(FlaskForm):
    """Přihlašovací formulář."""

    password = PasswordField("Heslo", validators=[DataRequired()], render_kw={'autofocus': True})
    remember = BooleanField("Zapamatovat přihlášení?", default=True)
    submit = SubmitField("Přihlásit")

    def validate_password(self, entered_password):
        try:
            with open("heslo.txt", "r") as f:
                hashed_password = f.readline()
            if not bcrypt.check_password_hash(hashed_password, entered_password.data):
                raise ValidationError("Heslo není platné!")
        except FileNotFoundError:
            raise ValidationError("Soubor s heslem neexistuje!")
