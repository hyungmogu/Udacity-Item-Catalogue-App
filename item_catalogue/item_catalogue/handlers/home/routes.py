from flask import Blueprint, render_template, url_for
from sqlalchemy import asc, desc

from item_catalogue import DBSession
from item_catalogue.model.category import Category
from item_catalogue.model.menuitem import MenuItem
from .. import helper

mod = Blueprint("home", __name__, template_folder="templates")


@mod.route("/")
def readMain():
    session = DBSession()

    categories_for_menu = (
        session.query(Category).order_by(asc(Category.name)).all())
    items = (
        session.query(Category.slug, MenuItem.name, MenuItem.slug)
        .join(MenuItem.category).order_by(desc(MenuItem.id)).limit(20).all())

    # Determine which button to put. Login or logout?
    # If logged in, insert logout buttion.
    # If not, insert login button
    if not helper.is_signed_in():
        session.close()

        return render_template(
            "main.html", menuItems=items, categories=categories_for_menu)

    session.close()

    return render_template(
        "main.html", menuItems=items, categories=categories_for_menu,
        logged_in=True)