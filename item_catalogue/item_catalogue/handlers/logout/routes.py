import json
import httplib2
from flask import Blueprint
from flask import flash, redirect, url_for
from flask import session as login_session

from .. import helper

mod = Blueprint("logout", __name__, template_folder="templates")


@mod.route("/logout")
def logout():
    """

    NOTE: Revoke login requests are disabled. Both Google 
          and Facebook recommends that login be revoked
          when user wishes to delete account / application.

          Source:

          - Google: https://developers.google.com/identity/protocols/
                    OAuth2InstalledApp#tokenrevoke
          - Facebook: https://developers.facebook.com/docs/
                      facebook-login/permissions/
                      requesting-and-revoking#revokelogin 

    """
    if not helper.is_signed_in():
        flash("You've already logged out.", "warning")
        return redirect(url_for("home.read_main"))

    if login_session["provider"] == "google":
        # access_token = login_session["access_token"]

        # url = ("https://accounts.google.com/o/oauth2/revoke?token=%s" 
        #        % access_token)
        #
        # print(url)
        # internet = httplib2.Http()
        # result = internet.request(url, "GET")[0]

        # print(json.dumps(result))

        # if not int(result["status"]) == 200:
        #   flash("Error occured while logging out.", "error")
        #   return redirect(url_for("home.read_main"))

        del login_session["access_token"]
        del login_session["gplus_id"]
        del login_session["username"]
        del login_session["email"]
        del login_session["picture"]
        del login_session["provider"]

    elif login_session["provider"]=="facebook":
        # facebook_id = login_session["facebook_id"]

        # url = ("https://graph.facebook.com/%s/permissions?access_token=" 
        #        % facebook_id)
        # h = httplib2.Http()
        # result = h.request(url, 'DELETE')[1]

        del login_session["facebook_id"]
        del login_session["username"]
        del login_session["email"]
        del login_session["picture"]
        del login_session["provider"]

    flash("Logout Successful.", "success")
    return redirect(url_for("home.read_main"))