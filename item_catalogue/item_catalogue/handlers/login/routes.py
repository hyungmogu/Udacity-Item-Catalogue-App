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

mod = Blueprint("login",__name__,template_folder="templates")

def send_response(status_code,message=""):
	response = make_response(json.dumps(message),status_code)
	response.headers["Content-Type"] = "application/json"

	return response

def g_is_user_already_logged_in(gplus_id):
	stored_credentials = login_session.get("access_token")
	stored_gplus_id = login_session.get("gplus_id")

	if stored_credentials is not None and gplus_id == stored_gplus_id:
		return True

def g_get_user_data(access_token):
	userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
	params= {"access_token": access_token, "alt": "json"}
	answer = requests.get(userinfo_url, params=params)

	return answer.json()

def is_session_token_valid():
	# Note: this shields user from Cross Reference Site Forgery Attack.
	if request.args.get("state") != login_session["state"]:
		return False
	return True	

def g_get_credentials(one_time_code):
	oauth_flow = flow_from_clientsecrets("client_secrets.json",
				scope="openid profile email")
	oauth_flow.redirect_uri = "postmessage"
	return oauth_flow.step2_exchange(one_time_code)

def g_check_access_token(access_token):
	url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"%
		access_token)
	h = httplib2.Http()
	return json.loads(h.request(url,"GET")[1])

def fb_get_access_token(one_time_token):
	REDIRECT_URI = "http://localhost:5000/welcome"
	FB_APP_ID = json.loads(open("fb_client_secrets.json","r").read())["web"]["app_id"]
	FB_APP_SECRET = json.loads(open("fb_client_secrets.json","r").read())["web"]["app_secret"]

	url = ("https://graph.facebook.com/oauth/access_token?"
		"grant_type=fb_exchange_token&"
		"G_CLIENT_ID=%s&"
		"client_secret=%s&"
		"redirect_uri=%s&"
		"fb_exchange_token=%s"%(FB_APP_ID, FB_APP_SECRET, REDIRECT_URI, one_time_token))
	h = httplib2.Http()
	result = h.request(url,"GET")[1]
	return result.split("&")[0]

def fb_get_user_data(access_token):
	url = "https://graph.facebook.com/v2.4/me?%s&fields=name,id,email,picture"%access_token
	h = httplib2.Http()
	result = h.request(url,"GET")[1]
	return json.loads(result)

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
	G_CLIENT_ID = json.loads(open("client_secrets.json","r").read())["web"]["client_id"]
	one_time_code = request.data

	# Harvest access token and gplus_id
	try:
		credentials = g_get_credentials(one_time_code)
		access_token = credentials.access_token
		gplus_id = credentials.id_token["sub"]
	except FlowExchangeError:
		return send_response(401, "Failed to upgrade the authorization code.")

	result = g_check_access_token(access_token)

	# First, check if somebody is attempting CSRF attack
	if not is_session_token_valid():
		return send_response(401,"Invalid state token")
	# Check for errors in transmission.
	if result.get("error"):
		return send_response(500,result.get("error"))
	# If all is well, check if the token is for intended user.
	if result["user_id"] != gplus_id:
		return send_response(500,result.get("error"))
	# If valid, verify that it is for this app.
	if (result["issued_to"] != G_CLIENT_ID):
		return send_response(401,result.get("Login invalid. Token's client ID "
				"does not match"))
	# If all is well, the credential is correct with high confidence.
	if g_is_user_already_logged_in(gplus_id):
		return send_response(200, "Current User is already logged in.")

	data = g_get_user_data(access_token)
	
	login_session["access_token"] = access_token
	login_session["gplus_id"] = gplus_id
	login_session["provider"] = "google"
	login_session["username"] = data["name"]
	login_session["picture"] = data["picture"]
	login_session["email"] = data["email"]

	return send_response(200, "success")

@mod.route("/login/fbconnect",methods=["POST"])
def fbconnect():
	one_time_token = request.data

	if not is_session_token_valid():
		return send_response(401,"Invalid state token")

	access_token = fb_get_access_token(one_time_token)

	data = fb_get_user_data(access_token)

	login_session["provider"] = "facebook"
	login_session["username"] = data["name"]
	login_session["email"] = data["email"]
	login_session["facebook_id"] = data["id"]
	login_session["picture"] = data["picture"]["data"]["url"]

	return send_response(200, "success")
