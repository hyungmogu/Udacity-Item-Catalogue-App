import os
import string
import random
from datetime import datetime

from sqlalchemy import create_engine, desc, asc, func, and_
from sqlalchemy.orm import sessionmaker, joinedload
from database_setup import Category, MenuItem

from flask import Flask, render_template, request, url_for, redirect, flash,jsonify
from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
engine = create_engine("sqlite:///itemcatalogue.db")
DBSession = sessionmaker(bind = engine)

CLIENT_ID = json.loads(open("client_secrets.json","r").read())["web"]["client_id"]


#EXTRA FUNCTIONS
def is_signed_in():
	if "username" not in login_session:
		return False
	return True

def is_data_changed(new_title, new_description, new_item_slug, new_category_id, old_item):
	if not (new_title == old_item.name):
		return True
	if not (new_item_slug == old_item.slug):
		return True
	if not (new_description == old_item.description):
		return True
	if not (new_category_id == old_item.category_id):
		return True
	return False

def has_unique_slug_in_cat(new_category_id,new_item_slug):
	count = int(session.query(MenuItem).filter_by(category_id=category_id,slug=item_slug).count())
	if count is not 0:
		return False
	else:
		return True

def is_unique(count):
	if count is not 0:
		return False
	else:
		return True

def generate_slug(title):
	lowercase_title = title.lower()
	slug = "_".join(lowercase_title.split())

	return slug

#LOGIN
@app.route("/login/")
def readLogin():
	# Create state token.
	# Note: It shields user from Cross Site Reference Forgery Attack.
	state = "".join(random.choice(string.ascii_uppercase + string.digits + 
			string.ascii_lowercase) for x in xrange(32))
	login_session["state"] = state
	return render_template("login.html",session_state=login_session["state"])

@app.route("/login/gconnect", methods=["POST"])
def gconnect():
	# Check the validity of session token.
	# Note: this is to shield user from Cross Reference Site Forgery Attack.
	if request.args.get("state") != login_session["state"]:
		response = make_response("Invalid state token", 401)
		response.headers["Content-Type"] = "application/json"
		return response
	# If all is well, harvest one time code.
	one_time_code = request.data
	# Swap one time code and client secret for credentials.
	try: 
		oauth_flow = flow_from_clientsecrets("client_secrets.json",
					scope="openid profile email")
		oauth_flow.redirect_uri = "postmessage"
		credentials = oauth_flow.step2_exchange(one_time_code)
	except FlowExchangeError:
		response = make_response(json.dumps("Failed to upgrade the " 
				"authorization code"),401)
		response.headers["Content-Type"] = "application/json"
		return response
	# Check for the validity of credentials.
	access_token = credentials.access_token
	url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"%
		access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url,"GET")[1])
	# If error, abort.
	if result.get("error"):
		response = make_response(json.dumps(result.get("error")),500)
		response.headers["Content-Type"] = "application/json"
		return response
	# If all is well, check if the token is for intended user.
	gplus_id = credentials.id_token["sub"]
	if result["user_id"] != gplus_id:
		response = make_response(json.dumps("Login invalid. Token's user ID "
				"doesn't match"),401)
		response.headers["Content-Type"] = "application/json"
		return response
	# If valid, verify that it is for this app.
	if (result["issued_to"] != CLIENT_ID):
		response = make_response(json.dumps("Login invalid. Token's client ID " 
				"does not match"),401)
		response.headers["Content-Type"] = "application/json"
		return response
	# If all is well, the credential is correct with high confidence.
	# Now, Check if user is logged in
	stored_credentials = login_session.get("access_token")
	stored_gplus_id = login_session.get("gplus_id")
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps("Current user is already connected."),200)
		response.headers["Content-Type"] = "application/json"
		return response
	# If all is well, continue the login process.
	# Retrieve and store the access token.
	login_session["access_token"] = access_token
	login_session["gplus_id"] = gplus_id
	# Get user info.
	userinfo_url = ("https://www.googleapis.com/oauth2/v3/userinfo")
	params= {"access_token": credentials.access_token,"alt": "json"}
	answer = requests.get(userinfo_url,params=params)
	data = answer.json()
	# Store user info in flask session.
	login_session["provider"] = "google"
	login_session["username"] = data["name"]
	login_session["picture"] = data["picture"]
	login_session["email"] = data["email"]
	response = make_response(json.dumps("success"),200)
	response.headers["Content-Type"] = "application/json"
	return response

@app.route("/login/fbconnect",methods=["POST"])
def fbconnect():
	# Check the validity of session token.
	# Note: this is to shield user from Cross Reference Site Forgery Attack.
	if request.args.get("state") != login_session["state"]:
		response = make_response("Invalid state token", 401)
		response.headers["Content-Type"] = "application/json"
		return response	

	# If all is well, harvest one time code.
	access_token = request.data
	redirect_uri = "http://localhost:5000/welcome"

	app_id = json.loads(open("fb_client_secrets.json","r").read())["web"]["app_id"]
	app_secret = json.loads(open("fb_client_secrets.json","r").read())["web"]["app_secret"]

	url = ("https://graph.facebook.com/oauth/access_token?"
		"grant_type=fb_exchange_token&"
		"client_id=%s&"
		"client_secret=%s&"
		"redirect_uri=%s&"
		"fb_exchange_token=%s"%(app_id,app_secret,redirect_uri,access_token))
	h = httplib2.Http()
	result = h.request(url,"GET")[1]
	token = result.split("&")[0]

	url = "https://graph.facebook.com/v2.4/me?%s&fields=name,id,email,picture"%token
	h = httplib2.Http()
	result = h.request(url,"GET")[1]
	data = json.loads(result)

	login_session["provider"] = "facebook"
	login_session["username"] = data["name"]
	login_session["email"] = data["email"]
	login_session["facebook_id"] = data["id"]
	login_session["picture"] = data["picture"]["data"]["url"]

	response = make_response(json.dumps("success"),200)
	response.headers["Content-Type"] = "application/json"
	return response


@app.route("/logout")
def logout():
	# Checks if user is logged in.
	# If not, redirect user to main page.
	# If logged in, log the user out by revoking access code.
	if('username' not in login_session):
		flash("You've already logged out.","error")
		return redirect(url_for("readMain"))
	if(login_session["provider"] == "google"):
		access_token = login_session["access_token"]
		# Note: the url returns 200 if successful, and 400 otherwise.
		url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % access_token
		internet = httplib2.Http()
		result = internet.request(url,"GET")[0]
		# Finally, dump session data, and free-up resources.
		del login_session["access_token"]
		del login_session["gplus_id"]
		del login_session["username"]
		del login_session["email"]
		del login_session["picture"]
		del login_session["provider"]
	elif(login_session["provider"]=="facebook"):
		facebook_id = login_session["facebook_id"]
		url = "https://graph.facebook.com/%s/permissions" %facebook_id
		h = httplib2.Http()
		result = h.request(url,'DELETE')[1]
		# Finally, dump session data, and free-up resources.
		del login_session["facebook_id"]
		del login_session["username"]
		del login_session["email"]
		del login_session["picture"]
		del login_session["provider"]
	flash("Logout Successful.","success")
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
	# Querying all categories for category menu.
	categories = session.query(Category).order_by(asc(Category.name)).all()
	# Query 20 most recent entries in descending order.
	items = (session.query(Category.slug,MenuItem.name,MenuItem.slug).
			join(MenuItem.category).order_by(desc(MenuItem.id)).limit(20).all())
	session.close()
	# Checks if user is logged in.
	# If so, insert logout buttion.
	# If not, insert login button.
	if "username" in login_session:
		return render_template("main.html",menuItems=items,categories=categories,
				logged_in=True)
	else:
		return render_template("main.html",menuItems=items,categories=categories)

@app.route("/items/<string:category_slug>/")
def readCategory(category_slug):
	session = DBSession()
	# Query all categories for category menu.
	categories = session.query(Category).order_by(asc(Category.name)).all()
	# Query all items in the current category for current category menu.
	currentCategory = session.query(Category).filter_by(slug = category_slug).one()
	currentCategoryItems = (session.query(Category.slug,MenuItem.name,
								MenuItem.slug).
							join(MenuItem.category).
							filter(Category.slug == category_slug).all())
	# Find number of items. 
	# Note: This is to be displayed beside the title of current category menu.
	itemsCount = (session.query(MenuItem).
				filter_by(category_id = currentCategory.id).count())
	session.close()
	# Checks if user is logged in.
	# If so, insert logout buttion.
	# If not, insert login button
	if "username" in login_session:
		return render_template("category.html",currentCategory=currentCategory,
				categories=categories,menuItems=currentCategoryItems,
				count=itemsCount,logged_in=True)
	else:
		return render_template("category.html",currentCategory=currentCategory,
				categories=categories,menuItems=currentCategoryItems,
				count=itemsCount)

@app.route("/items/new/", methods=["GET","POST"])
def createItem():
	if(request.method == "GET"):
		session = DBSession()

		categories = session.query(Category).all()

		if is_signed_in():
			flash("Not allowed. 'New Item' page requires login.","error")
			return redirect(url_for("readLogin"))

		session.close()

		return render_template("newItem.html", categories = categories,
				logged_in=True)

	elif(request.method == "POST"):
		session = DBSession()

		title = request.form["title"]
		description = request.form["description"]
		category_id = int(request.form["category"])

		item_slug = generate_slug(title)
		categories = session.query(Category).all()
		category_slug = session.query(Category).filter_by(id=category_id).one().slug
		num_of_identical_items = int(session.query(MenuItem).filter_by(category_id=category_id, slug=item_slug).count())

		if not is_signed_in():
			session.close()

			flash("Not allowed. 'New Item' feature requires login.","error")
			return redirect(url_for('readLogin'))
		if not (title and description):
			session.close()

			flash("Not allowed. Both title and description must exist.")
			return render_template('newItem.html', categories=categories, logged_in=True, title=title, category_id=category_id, description=description)
		if not is_unique(num_of_identical_items):
			session.close()

			flash("Not allowed. There already exists an item with the same "
				  "slug.","error")
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
		except NoResultFound:
			flash("Not allowed. The page doesn't exist.")
			redirect(url_for("readMain"))
		session.close()
		# Check if user is authorized to edit the post.
		if not is_signed_in():
			flash("Not allowed. 'Update' feature requires login","error")
			return redirect(url_for("readLogin"))

		return render_template("editItem.html",categories=categories,category_slug=category_slug,item=item,item_slug=item_slug)

	elif request.method == "POST":	
		# TODO: Add a feature that allows users to choose their own slug
		# TODO: Add a function that checks for special symbols other than '_' in slugs
		# TODO: Add a function that returns true if user is modifying the same post.
		#		If so, update title, description, and then redirect user to readItem page.
		# TODO: Fix the problem of user not being allowed to modify their own post.

		new_title = request.form["title"]
		new_description = request.form["description"]
		new_category_id = int(request.form["category"])
		new_item_slug = generate_slug(new_title)

		session = DBSession()
		categories = session.query(Category).all()
		try:
			new_category_slug = session.query(Category).filter_by(id=new_category_id).one().slug
			old_item = (session.query(MenuItem, Category.slug)
				   .join(MenuItem.category)
				   .filter(Category.slug==category_slug, MenuItem.slug==item_slug)
				   .one())[0]
		except NoResultFound:
			flash("Not allowed. The page doesn't exist.")
			redirect(url_for("readMain"))
		session.close()

		# Check if all conditions are met to edit blog post.
		if not is_signed_in():
			flash("Not allowed. 'Update' feature requires login","error")
			return redirect(url_for("readLogin"))
		if not is_data_changed(new_title, new_description, new_item_slug, new_category_id, old_item):
			flash("No data has been changed.","warning")
			return redirect(url_for('readItem', category_slug=category_slug, item_slug=item_slug))	
		if not (new_title and new_description):
			flash("Not allowed. Both title and description must not be empty.", "error")
			return render_template("editItem.html", new_title=new_title,new_description=new_description,new_category_id=new_category_id,categories=categories,category_slug=category_slug,item_slug=item_slug)
		if not has_unique_slug_in_cat(new_category_id,new_item_slug):
			flash("Not allowed. There already exists an item with the same slug.","error")
			return render_template("editItem.html",new_title=new_title,new_description=new_description,new_category_id=new_category_id,categories=categories,category_slug=category_slug,item_slug=item_slug)

		session = DBSession()
		old_item.title = new_title
		old_item.description = new_description
		old_item.category_id = new_category_id
		session.add(old_item)
		session.commit()
		session.close()

		flash("'%s' successfully edited."%new_title,"success")
		return redirect(url_for('readItem',category_slug=new_category_slug,item_slug=new_item_slug))

@app.route("/items/<string:category_slug>/<string:item_slug>/delete/", 
	methods=["GET","POST"])
def deleteItem(category_slug,item_slug):
	if(request.method == "GET"):
		# Checks if user is logged in.
		if "username" not in login_session:
			flash("Not allowed. 'Delete' feature requires login.","error")
			return redirect(url_for("readLogin"))
		return render_template("deleteItem.html",category_slug=category_slug,
			item_slug=item_slug)
	elif (request.method == "POST"):
		# Checks if user is logged in.
		if "username" not in login_session:
			flash("Not allowed. 'Delete' feature requires login.","error")
			return redirect(url_for("readLogin"))
		session = DBSession()
		# Find item by slug and then delete it
		# NOTE: need error message here. what if item is already deleted?
		item = (session.query(MenuItem).join(MenuItem.category).
			filter(Category.slug == category_slug, MenuItem.slug == item_slug).
			one())
		session.delete(item)
		session.commit()
		session.close()
		flash("'%s' successfully deleted."%item.name,"success")
		return redirect(url_for("readMain"))

@app.route("/items/<string:category_slug>/<string:item_slug>/")
def readItem(category_slug,item_slug):
	session = DBSession()
	# Query item by slug
	item = (session.query(Category.slug,MenuItem).join(MenuItem.category).
		filter(Category.slug == category_slug,MenuItem.slug == item_slug).one())
	session.close()
	# Checks if user is logged in.
	# If so, insert logout buttion.
	# If not, insert login button.
	if "username" in login_session:
		return render_template("item.html",item=item,logged_in=True)
	else:
		return render_template("item.html",item=item)			

@app.route("/welcome/")
def readWelcome():
	# Checks if user is logged in..
	if "username" not in login_session:
		flash("Not allowed. 'Welcome' page requires login.","error")
		redirect(url_for("readLogin"))
	# If all is well, retrieve username, and render template
	return render_template("welcome.html",username=login_session["username"])

# url_for cash busting. 
# Note: This solves the trouble of css not refreshing the old file. 
# More info can be found here: http://flask.pocoo.org/snippets/40/ .
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get("filename", None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

app.debug = False
app.secret_key = 'A9012ASD09812@)(J*AS(&FJHASHVUaiuw1bSA&Dy712bhc'
app.run(host='0.0.0.0', port=5000)
