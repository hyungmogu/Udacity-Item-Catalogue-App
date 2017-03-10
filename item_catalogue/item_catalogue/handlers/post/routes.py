from flask import render_template, request, url_for, redirect, flash, jsonify, make_response
from flask import Blueprint
from flask import session as login_session
from sqlalchemy import asc, desc, exc
from sqlalchemy.orm import exc as oexc

from item_catalogue import app, DBSession
from item_catalogue.model.category import Category
from item_catalogue.model.menuitem import MenuItem
from .. import helper

mod = Blueprint("post", __name__, template_folder="templates")

@mod.route("/items/new/", methods=["GET","POST"])
def createItem():
	if(request.method == "GET"):
		session = DBSession()

		categories = session.query(Category).all()

		if not helper.is_signed_in():
			flash("Not allowed. 'New Item' page requires login.", "error")
			return redirect(url_for("login.readLogin"))

		session.close()

		return render_template("newItem.html", categories = categories,
				logged_in=True)

	elif(request.method == "POST"):
		session = DBSession()

		title = request.form["title"]
		description = request.form["description"]
		category_id = int(request.form["category"])

		item_slug = helper.generate_slug(title)
		categories = session.query(Category).all()
		category_slug = session.query(Category).filter_by(id=category_id).one().slug
		num_of_identical_items = int(session.query(MenuItem).filter_by(category_id=category_id, slug=item_slug).count())

		if not helper.is_signed_in():
			session.close()

			flash("Not allowed. 'New Item' feature requires login.", "error")
			return redirect(url_for('login.readLogin'))
		if not (title and description):
			session.close()

			flash("Not allowed. Both title and description must exist.", "error")
			return render_template('newItem.html', categories=categories, logged_in=True, title=title, category_id=category_id, description=description)
		if not helper.is_unique(num_of_identical_items):
			session.close()

			flash("Not allowed. There already exists an item with the same "
				  "slug.", "error")
			return render_template("newItem.html",categories=categories, logged_in=True, title=title, category_id=category_id, description=description)

		item = MenuItem(name=title, slug=item_slug,
				description=description, category_id=category_id)
		session.add(item)
		session.commit()

		session.close()

		flash("'%s' has been successfully created."%title, "success")
		return redirect(url_for('post.readItem', category_slug=category_slug, item_slug=item_slug))

@mod.route("/items/<string:category_slug>/<string:item_slug>/edit/", 
	methods=["GET","POST"])
def editItem(category_slug,item_slug):
	if request.method == "GET":
		session = DBSession()

		categories = session.query(Category).all()
		try:
			category = session.query(Category).filter_by(slug=category_slug).one()
			item = session.query(MenuItem).filter_by(slug=item_slug,category_id=category.id).one()
		except exc.SQLAlchemyError:
			session.close()

			flash("Not allowed. The item doesn't exist.", "error")
			return redirect(url_for("home.readMain"))

		if not helper.is_signed_in():
			session.close()

			flash("Not allowed. 'Update' feature requires login", "error")
			return redirect(url_for("login.readLogin"))

		session.close()

		return render_template("editItem.html", categories=categories, category_slug=category_slug, item=item, item_slug=item_slug, logged_in=True)

	elif request.method == "POST":	
		# TODO: Add a feature that allows users to choose their own slug
		# TODO: Add a function that checks for special symbols other than '_' in slugs
		session = DBSession()

		new_title = request.form["title"]
		new_description = request.form["description"]
		new_category_id = int(request.form["category"])
		new_item_slug = helper.generate_slug(new_title)

		categories = session.query(Category).all()
		num_of_identical_items = int(session.query(MenuItem).filter_by(category_id=new_category_id,slug=new_item_slug).count())

		try:
			new_category_slug = session.query(Category).filter_by(id=new_category_id).one().slug
			old_item = (session.query(MenuItem, Category.slug)
				   .join(MenuItem.category)
				   .filter(Category.slug==category_slug, MenuItem.slug==item_slug)
				   .one()).MenuItem
		except oexc.NoResultFound:
			session.close()

			flash("Not allowed. The item doesn't exist.", "error")
			return redirect(url_for("home.readMain"))

		# Check if user is updating post without changing slug and category
		if (category_slug==new_category_slug) and (item_slug==new_item_slug):
			old_item.title = new_title
			old_item.description = new_description
			session.add(old_item)
			session.commit()

			session.close()

			flash("'%s' successfully edited."%new_title, "success")
			return redirect(url_for('post.readItem',category_slug=category_slug,item_slug=item_slug))

		# Check if all conditions are met to edit blog post.
		if not helper.is_signed_in():
			session.close()

			flash("Not allowed. 'Update' feature requires login", "error")
			return redirect(url_for("login.readLogin"))
		if not helper.is_data_changed(new_title, new_description, new_item_slug, new_category_id, old_item):
			session.close()

			flash("No data has been changed.","warning")
			return redirect(url_for('post.readItem', category_slug=category_slug, item_slug=item_slug))	
		if not (new_title and new_description):
			session.close()

			flash("Not allowed. Both title and description must not be empty.", "error")
			return render_template("editItem.html", new_title=new_title, new_description=new_description, new_category_id=new_category_id, categories=categories, category_slug=category_slug, item_slug=item_slug, logged_in=True)
		if not helper.is_unique(num_of_identical_items):
			session.close()

			flash("Not allowed. There already exists an item with the same slug.", "error")
			return render_template("editItem.html", new_title=new_title, new_description=new_description, new_category_id=new_category_id, categories=categories, category_slug=category_slug, item_slug=item_slug, logged_in=True)

		old_item.name = new_title
		old_item.slug = new_item_slug
		old_item.description = new_description
		old_item.category_id = new_category_id
		session.add(old_item)
		session.commit()

		session.close()

		flash("'%s' successfully edited."%new_title, "success")
		return redirect(url_for('post.readItem',category_slug=new_category_slug,item_slug=new_item_slug))

@mod.route("/items/<string:category_slug>/<string:item_slug>/delete/", 
	methods=["GET","POST"])
def deleteItem(category_slug, item_slug):
	if(request.method == "GET"):
		session = DBSession()

		try:
			item = (session.query(MenuItem).join(MenuItem.category).
				filter(Category.slug==category_slug, MenuItem.slug==item_slug).
				one())
		except exc.SQLAlchemyError:
			session.close()

			flash("Not allowed. The item doesn't exist.", "error")
			return redirect(url_for("home.readMain"))

		if not helper.is_signed_in():
			flash("Not allowed. 'Delete' feature requires login.", "error")
			return redirect(url_for("login.readLogin"))

		session.close()

		return render_template("deleteItem.html", category_slug=category_slug,
			item_slug=item_slug, logged_in=True)

	elif (request.method == "POST"):
		session = DBSession()

		try:
			item = (session.query(MenuItem).join(MenuItem.category).
				filter(Category.slug==category_slug, MenuItem.slug==item_slug).
				one())
		except exc.SQLAlchemyError:
			session.close()

			flash("Not allowed. The item doesn't exist.", "error")
			return redirect(url_for("home.readMain"))

		if not helper.is_signed_in():
			flash("Not allowed. 'Delete' feature requires login.", "error")
			return redirect(url_for("login.readLogin"))

		session.delete(item)
		session.commit()

		session.close()
		
		flash("'%s' successfully deleted." % item.name, "success")
		return redirect(url_for("home.readMain"))

@mod.route("/items/<string:category_slug>/<string:item_slug>/")
def readItem(category_slug,item_slug):
	session = DBSession()

	try:
		item = (session.query(MenuItem,Category.slug).join(MenuItem.category).
			filter(Category.slug==category_slug,MenuItem.slug==item_slug).one())
	except oexc.NoResultFound:
		flash("Not allowed. The item doesn't exist.", "error")
		return redirect(url_for("home.readMain"))

	session.close()

	# Determine which button to put. Login or logout?
	# If logged in, insert logout buttion.
	# If not, insert login button
	if not helper.is_signed_in():
		return render_template("item.html", item=item)
	return render_template("item.html", item=item, logged_in=True)
