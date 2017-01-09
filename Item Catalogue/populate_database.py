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
category_names = ['Soccer','Basketball','Frisbee','Snowboarding']

for category_name in category_names:
	newCategory = Category(name = category_name)
	session.add(newCategory)
	session.commit()


#adding menu items for soccer category
soccer = session.query(Category).filter_by(name="Soccer").first()
shingGuards = MenuItem(name="Two Shinguards", category_id=soccer.id)
session.add(shingGuards)
session.commit()

#adding menu items for snowboarding category
sbItemNames = ["Goggles","Snowboard"]
snowboarding = session.query(Category).filter_by(name="Snowboarding").first()


for sbItemName in sbItemNames:
	newSbItem = MenuItem(name = sbItemName, category_id=snowboarding.id)
	session.add(newSbItem)
	session.commit()





