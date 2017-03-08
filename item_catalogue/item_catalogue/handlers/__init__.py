import os
import string
import random

import httplib2
import json
import requests
from flask import render_template, request, url_for, redirect, flash, jsonify, make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy import asc, desc, exc

from item_catalogue import app, DBSession, CLIENT_ID
from item_catalogue.model.category import Category
from item_catalogue.model.menuitem import MenuItem
from item_catalogue.handlers.login.routes import mod
from item_catalogue.handlers.logout.routes import mod
import item_catalogue.handlers.helper as helper

app.register_blueprint(login.routes.mod)
app.register_blueprint(logout.routes.mod)

#ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(error):
	flash("Not allowed. The page or item you've requested doesn't exist.", "error")
	return redirect(url_for("readMain"))

#API
@app.route("/catalog.json/")
def readAPI():
	session = DBSession()
	categories = session.query(Category).all()
	# Convert query result into a list of JSON objects.
	serialized_categories = [x.serialize for x in categories]
	# Converty query result of menu_items into a list of JSON objects.
	# Then, fit them inside corresponding categories under "items" attribute.
	for category in serialized_categories:
		items = session.query(MenuItem).filter_by(category_id = 
			  category["id"]).all()
		if items:
			category["items"] = [x.serialize for x in items]
	session.close()
	return jsonify(category=serialized_categories)

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

@app.route("/items/new/", methods=["GET","POST"])
def createItem():
	if(request.method == "GET"):
		session = DBSession()

		categories = session.query(Category).all()

		if not helper.is_signed_in():
			flash("Not allowed. 'New Item' page requires login.", "error")
			return redirect(url_for("readLogin"))

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
			return redirect(url_for('readLogin'))
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
		return redirect(url_for('readItem', category_slug=category_slug, item_slug=item_slug))

@app.route("/items/<string:category_slug>/<string:item_slug>/edit/", 
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
			return redirect(url_for("readMain"))

		# Check if user is authorized to edit the post.
		if not helper.is_signed_in():
			session.close()

			flash("Not allowed. 'Update' feature requires login", "error")
			return redirect(url_for("readLogin"))

		session.close()

		return render_template("editItem.html",categories=categories,category_slug=category_slug,item=item,item_slug=item_slug)

	elif request.method == "POST":	
		# TODO: Add a feature that allows users to choose their own slug
		# TODO: Add a function that checks for special symbols other than '_' in slugs
		# TODO: Add a function that returns true if user is modifying the same post.
		#		If so, update title, description, and then redirect user to readItem page.
		# TODO: Fix the problem of user not being allowed to modify their own post.
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
				   .one())[0]
		except exc.SQLAlchemyError:
			session.close()

			flash("Not allowed. The item doesn't exist.", "error")
			return redirect(url_for("readMain"))

		# Check if user is updating post without changing slug and category
		if (category_slug==new_category_slug) and (item_slug==new_item_slug):
			old_item.title = new_title
			old_item.description = new_description
			session.add(old_item)
			session.commit()

			session.close()

			flash("'%s' successfully edited."%new_title, "success")
			return redirect(url_for('readItem',category_slug=category_slug,item_slug=item_slug))

		# Otherwise, proceed.
		# Check if all conditions are met to edit blog post.
		if not helper.is_signed_in():
			session.close()

			flash("Not allowed. 'Update' feature requires login", "error")
			return redirect(url_for("readLogin"))
		if not helper.is_data_changed(new_title, new_description, new_item_slug, new_category_id, old_item):
			session.close()

			flash("No data has been changed.","warning")
			return redirect(url_for('readItem', category_slug=category_slug, item_slug=item_slug))	
		if not (new_title and new_description):
			session.close()

			flash("Not allowed. Both title and description must not be empty.", "error")
			return render_template("editItem.html", new_title=new_title,new_description=new_description,new_category_id=new_category_id,categories=categories,category_slug=category_slug,item_slug=item_slug)
		if not helper.is_unique(num_of_identical_items):
			session.close()

			flash("Not allowed. There already exists an item with the same slug.", "error")
			return render_template("editItem.html",new_title=new_title,new_description=new_description,new_category_id=new_category_id,categories=categories,category_slug=category_slug,item_slug=item_slug)

		old_item.title = new_title
		old_item.description = new_description
		old_item.category_id = new_category_id
		session.add(old_item)
		session.commit()

		session.close()

		flash("'%s' successfully edited."%new_title, "success")
		return redirect(url_for('readItem',category_slug=new_category_slug,item_slug=new_item_slug))

@app.route("/items/<string:category_slug>/<string:item_slug>/delete/", 
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
			return redirect(url_for("readMain"))

		if not helper.is_signed_in():
			flash("Not allowed. 'Delete' feature requires login.", "error")
			return redirect(url_for("readLogin"))

		session.close()

		return render_template("deleteItem.html", category_slug=category_slug,
			item_slug=item_slug)

	elif (request.method == "POST"):
		session = DBSession()

		try:
			item = (session.query(MenuItem).join(MenuItem.category).
				filter(Category.slug==category_slug, MenuItem.slug==item_slug).
				one())
		except exc.SQLAlchemyError:
			session.close()

			flash("Not allowed. The item doesn't exist.", "error")
			return redirect(url_for("readMain"))

		if not helper.is_signed_in():
			flash("Not allowed. 'Delete' feature requires login.", "error")
			return redirect(url_for("readLogin"))

		session.delete(item)
		session.commit()

		session.close()
		
		flash("'%s' successfully deleted." % item.name, "success")
		return redirect(url_for("readMain"))

@app.route("/items/<string:category_slug>/<string:item_slug>/")
def readItem(category_slug,item_slug):
	session = DBSession()

	try:
		item = (session.query(Category.slug,MenuItem).join(MenuItem.category).
			filter(Category.slug==category_slug,MenuItem.slug==item_slug).one())
	except exc.SQLAlchemyError:

		flash("Not allowed. The item doesn't exist.", "error")
		return redirect(url_for("readMain"))

	session.close()

	# Determine which button to put. Login or logout?
	# If logged in, insert logout buttion.
	# If not, insert login button
	if not helper.is_signed_in():
		return render_template("item.html", item=item)
	return render_template("item.html", item=item, logged_in=True)
	

@app.route("/welcome/")
def readWelcome():
	if not helper.is_signed_in():
		flash("Not allowed. 'Welcome' page requires login.", "error")
		redirect(url_for("readLogin"))

	return render_template("welcome.html",username=login_session["username"])

