from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import Blueprint, jsonify
from sqlalchemy import asc

from item_catalogue import app, DBSession
from item_catalogue.model.category import Category
from item_catalogue.model.menuitem import MenuItem

mod = Blueprint("api", __name__, template_folder="templates")


@mod.route("/catalog.json/")
def get_all_items():

    session = DBSession()

    try:
        categories = session.query(Category).order_by(asc(Category.id)).all()

        if len(categories) is 0:
            raise NoResultFound
        output = [x.serialize for x in categories]

    except NoResultFound:
        output = {"error": {"type": "not_found", "title": "Empty Search Result", "description": "Category table has no entries"}}
        return jsonify(output)

    for category in output:
        print(category)
        items = session.query(MenuItem).filter_by(category_id = int(category["id"])).all()

        if len(items) is not 0:
            category["items"] = [x.serialize for x in items]

    session.close()

    return jsonify(output)


@mod.route("/catalog.json/<string:category_slug>/")
def get_a_category(category_slug):

    session = DBSession()

    try:
        category = session.query(Category).filter_by(slug = category_slug).one()
        output = category.serialize
    except NoResultFound:
        output = {"error": {"type": "not_found", "title": "Empty Search Result", "description": "'{0}' is not found in database".format(category_slug)}}
        return jsonify(output)
    except MultipleResultsFound:
        output = {"error": {"type": "multiple_results", "title": "Multiple Results Found", "description": "'{0}' returned multiple results".format(category_slug)}}
        return jsonify(output)

    items = session.query(MenuItem).filter_by(category_id = category.id).all()
    serialized_items = [x.serialize for x in items]

    if len(items) is not 0:
        output["items"] = serialized_items

    return jsonify(output)


@mod.route("/catalog.json/<string:category_slug>/<string:item_slug>/")
def get_a_item(category_slug, item_slug):

    session = DBSession()

    try:
        category = session.query(Category).filter_by(slug = category_slug).one()
    except NoResultFound:
        output = {"error": {"type": "not_found", "title": "Empty Search Result", "description": "Category '{0}' is not found in database".format(category_slug)}}
        return jsonify(output)
    except MultipleResultsFound:
        output = {"error": {"type": "multiple_results", "title": "Multiple Results Found", "description": "Category '{0}' returned multiple results".format(category_slug)}}
        return jsonify(output)

    try:
        item = session.query(MenuItem).filter_by(category_id = category.id, slug = item_slug).one()
        output = item.serialize
    except NoResultFound:
        output = {"error": {"type": "not_found", "title": "Empty Search Result", "description": "Item '{0}' under category '{1}' is not found in database".format(item_slug, category_slug)}}
        return jsonify(output)
    except MultipleResultsFound:
        output = {"error": {"type": "multiple_results", "title": "Multiple Results Found", "description": "Item '{0}' under category '{1}' returned multiple results".format(item_slug, category_slug)}}
        return jsonify(output)

    session.close()

    return jsonify(output)