from flask import Blueprint, render_template, redirect, url_for, flash
from flask import session as login_session

from item_catalogue import DBSession
from .. import helper

mod = Blueprint("welcome", __name__, template_folder="templates")

@mod.route("/welcome/")
def readWelcome():
    if not helper.is_signed_in():
        flash("Not allowed. 'Welcome' page requires login.", "error")
        redirect(url_for("login.readLogin"))

    return render_template("welcome.html", username=login_session["username"],
                           logged_in=True)

