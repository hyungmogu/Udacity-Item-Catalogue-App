from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, MenuItem

from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind = engine)

app.debug = False
app.run(host='0.0.0.0', port=5000)
