from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, MenuItem

from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalogue.db')
DBSession = sessionmaker(bind = engine)

@app.route('/')
def readMainPage():
"""
readMainPage()

Returns category and 20 most recent menu items
"""
	session = DBSession()

	#query all entries in category. Store result in a variable called categories
	categories = session.query(Category).all()

	#query 20 most recent entries in menu item. store result in a variable called menuItems.
	menuItems = session.query(MenuItem).order_by(desc(MenuItem.date_created)).limit(20).all()

	session.close()
	#return template filled with query result
	return render_template('main.html',menuItems = menuItems, categories = categories)

# @app.route('/<string:category_name>/')
# def readCategory(category_name):
# """
# readCategory()

# Returns all categories and menu items of whatever clicked category in alphabetical order

# """	

# 	session = DBSession()

# 	#query all entries in category.
# 	categories = session.query(Category).all()

# 	#query all menu items in the category
# 	menuItems = session.query(MenuItem).filter_by(category_name= category_name).order_by(desc(MenuItem.name))
# 	session.close()

# 	return render_template('category.html')


# @app.route('/<string:category_name>/new', methods=['GET','POST'])
# def createMenuItems(category_name):
# """
# createMenuItem(category_name,item_name)

# Returns templates and processes information required to create menu items

# """
# 	if(request.method == 'GET'):

# 		return render_template('newMenuItem.html')
	
# 	elif(request.method == 'POST'):

# 		return redirect(url_for('readMenuItems',category_name = category_name))

# @app.route('/<string:category_name>/<string:item_name>/edit', methods=['GET','POST'])
# def editMenuItem(category_name,item_name):
# """
# editMenuItem(category_name,item_name)

# Returns templates and processes information required to edit a menu item
# """

# 	if(request.method == 'GET'):
# 		return render_template('editMenuItem.html')

# 	elif (request.method == 'POST'):

# 		return redirect(url_for('readMenuItem',category_name=category_name,item_name=item_name))

# @app.route('/<string:category_name>/<string:item_name>/delete', methods=['GET','POST'])
# def deleteMenuItem(category_name,item_name):


# 	if(request.method == 'GET'):

# 		return render_template('deleteMenuItem.html')

# 	elif (request.method == 'POST'):

# 		return redirect(url_for('readCategory',category_name=category_name))

# @app.route('/<string:category_name>/<string:item_name>')
# def readMenuItem(category_name,item_name):

# 	return render_template('menuItem.html')

app.debug = False
app.run(host='0.0.0.0', port=5000)
