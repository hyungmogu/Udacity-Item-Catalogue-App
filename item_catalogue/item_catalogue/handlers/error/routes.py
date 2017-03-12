from flask import Blueprint, redirect, url_for, flash

mod = Blueprint("error", __name__)

#ERROR HANDLERS
@mod.app_errorhandler(404)
def page_not_found(error):
    flash("Not allowed. The page or item you've requested doesn't exist.", "error")
    return redirect(url_for("home.readMain"))
