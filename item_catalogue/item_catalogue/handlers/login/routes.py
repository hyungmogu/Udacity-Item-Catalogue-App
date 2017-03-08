import string
import random

import httplib2
import json
import requests
from flask import Blueprint
from flask import render_template, request, make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from item_catalogue import CLIENT_ID

mod = Blueprint("login",__name__,template_folder="templates")

#LOGIN
@mod.route("/login/")
def readLogin():
	# Create state token.
	# Note: It shields user from Cross Site Reference Forgery Attack.
	state = "".join(random.choice(string.ascii_uppercase + string.digits +
			string.ascii_lowercase) for x in xrange(32))
	login_session["state"] = state
	return render_template("login.html",session_state=login_session["state"])

@mod.route("/login/gconnect", methods=["POST"])
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

@mod.route("/login/fbconnect",methods=["POST"])
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
