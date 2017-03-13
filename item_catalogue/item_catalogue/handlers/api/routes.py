from flask import Blueprint, jsonify 

from item_catalogue import app, DBSession
from item_catalogue.model.category import Category
from item_catalogue.model.menuitem import MenuItem

mod = Blueprint("api", __name__, template_folder="templates")


@mod.route("/catalog.json/")
def read_api():
    session = DBSession()
    categories = session.query(Category).all()

    serialized_categories = [x.serialize for x in categories]

    for category in serialized_categories:
        items = session.query(MenuItem).filter_by(category_id = 
              category["id"]).all()
        if items:
            category["items"] = [x.serialize for x in items]

    session.close()

    return jsonify(category=serialized_categories)