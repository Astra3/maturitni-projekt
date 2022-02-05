from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from pocasi.web_app.main.forms import LoginForm
from pocasi.web_app.models import User

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    """Domovská stránka aplikace."""
    return render_template("home.html", title="Domovská stránka")


@main.route("/login", methods=["GET", "POST"])
def login():
    """Stránka s přihlášením."""
    form = LoginForm()
    if form.validate_on_submit():
        login_user(User(), remember=form.remember.data)
        flash("Úspěšně přihlášen!", "success")

        return redirect(url_for("main.home"))

    return render_template("login.html", form=form, title="Přihlášení")


@main.route("/logout")
@login_required
def logout():
    """Odhlásí uživatele a přesměruje na domovskou stránku."""
    logout_user()
    flash("Úspěšně odhlášen!", "success")
    return redirect(url_for("main.home"))
