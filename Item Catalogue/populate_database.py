from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, MenuItem

engine = create_engine('sqlite:///itemcatalogue.db')
DBSession = sessionmaker(bind = engine)

session = DBSession()


#adding categories
category_names = ['Soccer','Basketball','Frisbee','Snowboarding']

for category_name in category_names:
	newCategory = Category(name = category_name)
	session.add(newCategory)
	session.commit()


#adding menu items for soccer category
shingGuards = MenuItem(name="Two Shinguards",category_name="Soccer",date_created= datetime.now())
session.add(shingGuards)
session.commit()

#adding menu items for snowboarding category
sbItemNames = ["Goggles","Snowboard"]

for sbItemName in sbItemNames:
	newSbItem = MenuItem(name = sbItemName, category_name = "Snowboarding", date_created= datetime.now())
	session.add(newSbItem)
	session.commit()





