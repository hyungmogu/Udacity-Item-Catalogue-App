import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask

app = Flask(__name__)
engine = create_engine("sqlite:///itemcatalogue.db")
DBSession = sessionmaker(bind = engine)

CLIENT_ID = json.loads(open("client_secrets.json","r").read())["web"]["client_id"]

import item_catalogue.views