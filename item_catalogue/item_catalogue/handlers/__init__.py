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
from . import helper

app.register_blueprint(login.routes.mod)
app.register_blueprint(logout.routes.mod)
app.register_blueprint(post.routes.mod)
app.register_blueprint(api.routes.mod)

#ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(error):
	flash("Not allowed. The page or item you've requested doesn't exist.", "error")
	return redirect(url_for("readMain"))

#ROUTES
@app.route("/")
def readMain():
	session = DBSession()

	categories_for_menu = session.query(Category).order_by(asc(Category.name)).all()
	items = (session.query(Category.slug,MenuItem.name,MenuItem.slug).
			join(MenuItem.category).order_by(desc(MenuItem.id)).limit(20).all())

	# Determine which button to put. Login or logout?
	# If logged in, insert logout buttion.
	# If not, insert login button
	if not helper.is_signed_in():
		session.close()

		return render_template("main.html", menuItems=items, categories=categories_for_menu)

	session.close()

	return render_template("main.html", menuItems=items, categories=categories_for_menu,
						   logged_in=True)

@app.route("/items/<string:category_slug>/")
def readCategory(category_slug):
	# TODO: Fix items not showing on page.

	session = DBSession()

	try:
		current_category = session.query(Category).filter_by(slug=category_slug).one()
	except exc.SQLAlchemyError:
			session.close()

			flash("Not allowed. The page doesn't exist.", "error")
			return redirect(url_for("readMain"))

	categories_for_menu = session.query(Category).order_by(asc(Category.name)).all()
	items = session.query(MenuItem).filter_by(category_id=current_category.id).all()
	items_count = (session.query(MenuItem)
						  .filter_by(category_id=current_category.id).count())

	# Determine which button to put. Login or logout?
	# If logged in, insert logout buttion.
	# If not, insert login button
	if not helper.is_signed_in():
		session.close()

		return render_template("category.html", currentCategory=current_category,
				categories=categories_for_menu, menuItems=items,
				count=items_count)

	session.close()

	return render_template("category.html", currentCategory=current_category,
			categories=categories_for_menu, menuItems=items,
			count=items_count, logged_in=True)

@app.route("/welcome/")
def readWelcome():
	if not helper.is_signed_in():
		flash("Not allowed. 'Welcome' page requires login.", "error")
		redirect(url_for("readLogin"))

	return render_template("welcome.html",username=login_session["username"])

