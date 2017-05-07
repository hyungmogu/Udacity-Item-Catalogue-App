__version__ = "0.4.0"
__author__ = "Hyungmo Gu"


import os

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, url_for

from item_catalogue.model import Base

app = Flask(__name__)
engine = create_engine("sqlite:///model/itemcatalogue.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

import item_catalogue.handlers
import item_catalogue.add_sample_data

# url_for cash busting.
# Note: This solves the trouble of css not refreshing the old file.
# More info can be found here: http://flask.pocoo.org/snippets/40/.
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

