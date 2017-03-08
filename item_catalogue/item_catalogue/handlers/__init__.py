from flask import render_template, url_for, redirect, flash
from flask import session as login_session
from sqlalchemy import asc, desc, exc

from item_catalogue import app, DBSession
from item_catalogue.model.category import Category
from item_catalogue.model.menuitem import MenuItem
from item_catalogue.handlers.login.routes import mod
from item_catalogue.handlers.logout.routes import mod
from item_catalogue.handlers.post.routes import mod
from item_catalogue.handlers.api.routes import mod
from item_catalogue.handlers.home.routes import mod
from item_catalogue.handlers.category.routes import mod
from . import helper

app.register_blueprint(login.routes.mod)
app.register_blueprint(logout.routes.mod)
app.register_blueprint(post.routes.mod)
app.register_blueprint(api.routes.mod)
app.register_blueprint(home.routes.mod)
app.register_blueprint(category.routes.mod)

#ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(error):
	flash("Not allowed. The page or item you've requested doesn't exist.", "error")
	return redirect(url_for("home.readMain"))

#ROUTES
@app.route("/welcome/")
def readWelcome():
	if not helper.is_signed_in():
		flash("Not allowed. 'Welcome' page requires login.", "error")
		redirect(url_for("login.readLogin"))

	return render_template("welcome.html",username=login_session["username"])

