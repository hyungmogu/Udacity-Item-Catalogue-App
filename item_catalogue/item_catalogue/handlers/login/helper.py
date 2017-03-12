import requests
import json
import httplib2

from flask import session as login_session
from flask import request, make_response
from oauth2client.client import flow_from_clientsecrets

def send_response(status_code,message=""):
    response = make_response(json.dumps(message),status_code)
    response.headers["Content-Type"] = "application/json"

    return response

def g_is_user_already_logged_in(gplus_id):
    stored_credentials = login_session.get("access_token")
    stored_gplus_id = login_session.get("gplus_id")

    if stored_credentials is None:
        return False
    if gplus_id != stored_gplus_id:
        return False
        
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
    oauth_flow = flow_from_clientsecrets(
        "client_secrets.json",scope="openid profile email")
    oauth_flow.redirect_uri = "postmessage"
    return oauth_flow.step2_exchange(one_time_code)

def g_check_access_token(access_token):
    url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"
           % access_token)
    h = httplib2.Http()
    return json.loads(h.request(url,"GET")[1])

def fb_get_access_token(one_time_token):
    REDIRECT_URI = "http://localhost:5000/welcome"
    FB_APP_ID = (
        json.loads(open("fb_client_secrets.json","r").read())["web"]["app_id"])
    FB_APP_SECRET = (
        json.loads(open("fb_client_secrets.json","r").read())["web"]["app_secret"])

    url = ("https://graph.facebook.com/oauth/access_token?"
        "grant_type=fb_exchange_token&"
        "client_id=%s&"
        "client_secret=%s&"
        "redirect_uri=%s&"
        "fb_exchange_token=%s"%(
            FB_APP_ID, FB_APP_SECRET, 
            REDIRECT_URI, one_time_token))
    h = httplib2.Http()
    result = h.request(url,"GET")[1]
    return result.split("&")[0]

def fb_get_user_data(access_token):
    url = ("https://graph.facebook.com/v2.4/me?%s&fields=name,id,email,picture" 
           % access_token)
    h = httplib2.Http()
    result = h.request(url,"GET")[1]
    print(result)
    return json.loads(result)