from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, MenuItem

engine = create_engine('sqlite:///itemcatalogue.db')
DBSession = sessionmaker(bind = engine)

session = DBSession()

#cleaning tables before populating
session.query(Category).delete()
session.query(MenuItem).delete()
session.commit()

#adding categories
categories = [{'name':'Soccer','slug':'soccer'},{'name':'Basketball','slug':'basketball'},{'name':'Frisbee','slug':'frisbee'},{'name':'Snowboarding','slug':'snowboarding'}]

for category in categories:
	newCategory = Category(name = category['name'], slug= category['slug'])
	session.add(newCategory)
	session.commit()


#adding menu items for soccer category
soccer = session.query(Category).filter_by(name="Soccer").first()
shingGuards = MenuItem(name="Two Shinguards", slug="two_singuards", category_id=soccer.id)
session.add(shingGuards)
session.commit()

#adding menu items for snowboarding category
sbItems = [{'name':"Goggles",'slug':'goggles'},{'name':"Snowboard",'slug':'snowboard'}]
snowboarding = session.query(Category).filter_by(name="Snowboarding").first()


for sbItem in sbItems:
	newSbItem = MenuItem(name = sbItem['name'], slug=sbItem['slug'], category_id=snowboarding.id)
	session.add(newSbItem)
	session.commit()





