import string
import random

import json
from flask import Blueprint
from flask import render_template, request
from flask import session as login_session
from oauth2client.client import FlowExchangeError

from . import helper

mod = Blueprint("login",__name__,template_folder="templates")

#LOGIN
@mod.route("/login/")
def readLogin():
	# Create state token.
	# Note: This shields user from Cross Site Reference Forgery Attack.
	state = "".join(random.choice(string.ascii_uppercase + string.digits +
			string.ascii_lowercase) for x in xrange(32))
	login_session["state"] = state

	return render_template("login.html",session_state=login_session["state"])

@mod.route("/login/gconnect", methods=["POST"])
def gconnect():
	G_CLIENT_ID = json.loads(open("client_secrets.json","r").read())["web"]["client_id"]
	one_time_code = request.data

	# Harvest access token and gplus_id
	try:
		credentials = helper.g_get_credentials(one_time_code)
		access_token = credentials.access_token
		gplus_id = credentials.id_token["sub"]
	except FlowExchangeError:
		return send_response(401, "Failed to upgrade the authorization code.")

	result = helper.g_check_access_token(access_token)

	# First, check if somebody is attempting CSRF attack
	if not helper.is_session_token_valid():
		return send_response(401,"Invalid state token")
	# Check for errors in transmission.
	if result.get("error"):
		return helper.send_response(500,result.get("error"))
	# If all is well, check if the token is for intended user.
	if result["user_id"] != gplus_id:
		return helper.send_response(500,result.get("error"))
	# If valid, verify that it is for this app.
	if (result["issued_to"] != G_CLIENT_ID):
		return helper.send_response(401,result.get("Login invalid. Token's client ID "
				"does not match"))
	# If all is well, the credential is correct with high confidence.
	if helper.g_is_user_already_logged_in(gplus_id):
		return helper.send_response(200, "Current User is already logged in.")

	data = helper.g_get_user_data(access_token)
	
	login_session["access_token"] = access_token
	login_session["gplus_id"] = gplus_id
	login_session["provider"] = "google"
	login_session["username"] = data["name"]
	login_session["picture"] = data["picture"]
	login_session["email"] = data["email"]

	return helper.send_response(200, "success")

@mod.route("/login/fbconnect",methods=["POST"])
def fbconnect():
	one_time_token = request.data

	if not helper.is_session_token_valid():
		return helper.send_response(401,"Invalid state token")

	access_token = helper.fb_get_access_token(one_time_token)

	data = helper.fb_get_user_data(access_token)

	login_session["provider"] = "facebook"
	login_session["username"] = data["name"]
	login_session["email"] = data["email"]
	login_session["facebook_id"] = data["id"]
	login_session["picture"] = data["picture"]["data"]["url"]

	return helper.send_response(200, "success")
