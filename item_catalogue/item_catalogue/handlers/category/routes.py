from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy import asc, exc

from item_catalogue import DBSession
from item_catalogue.model.category import Category
from item_catalogue.model.menuitem import MenuItem
from .. import helper

mod = Blueprint("category", __name__, template_folder="templates")

@mod.route("/items/<string:category_slug>/")
def readCategory(category_slug):
	# TODO: Fix items not showing on page.

	session = DBSession()

	try:
		current_category = session.query(Category).filter_by(slug=category_slug).one()
	except exc.SQLAlchemyError:
			session.close()

			flash("Not allowed. The page doesn't exist.", "error")
			return redirect(url_for("home.readMain"))

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
