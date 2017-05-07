from item_catalogue import DBSession
from item_catalogue.model.category import Category
from item_catalogue.model.menuitem import MenuItem

# Add sample data to database

categories = [
		{
			"name": "Soccer",
			"slug": "soccer"
		},

		{
			"name": "Basketball",
			"slug": "basketball"
		},

		{
			"name": "Baseball",
			"slug": "baseball"
		},

		{
			"name": "Hockey",
			"slug": "hockey"
		}
	]


items = [
		{
			"name": "Soccer Ball",
			"slug": "soccer_ball",
			"category_id": 1,
			"description": "hello world",
			"email": "guhyungm7@gmail.com"
		},

		{
			"name": "Soccer Pads",
			"slug": "soccer_pads",
			"category_id": 1,
			"description": "hello world",
			"email": "hmgu7@hotmail.com"
		},

		{
			"name": "Soccer Shoes",
			"slug": "soccer_shoes",
			"category_id": 1,
			"description": "hello world",
			"email": "guhyungm7@gmail.com"
		},

		{
			"name": "Soccer Pants",
			"slug": "soccer_pants",
			"category_id": 1,
			"description": "hello world",
			"email": "guhyungm7@gmail.com"
		},

		{
			"name": "Basketball",
			"slug": "basketball",
			"category_id": 2,
			"description": "hello world",
			"email": "guhyungm7@gmail.com"
		},

		{
			"name": "Basketball sneakers",
			"slug": "basketball_sneakers",
			"category_id": 2,
			"description": "hello world",
			"email": "guhyungm7@gmail.com"
		},

		{
			"name": "Baseball Bat",
			"slug": "baseball_bat",
			"category_id": 3,
			"description": "hello world",
			"email": "guhyungm7@gmail.com"
		},

		{
			"name": "Baseball",
			"slug": "baseball",
			"category_id": 3,
			"description": "hello world",
			"email": "bozenaLakto@gmail.com"
		},

		{
			"name": "Helmet",
			"slug": "helmet",
			"category_id": 4,
			"description": "hello world",
			"email": "coolperson@gmail.com"
		},

		{
			"name": "Hockey Stick",
			"slug": "hockey_stick",
			"category_id": 4,
			"description": "hello world",
			"email": "hockeystick@gmail.com"
		},
	]

session = DBSession()

# clear old entries
session.query(Category).delete()
session.commit()

session.query(MenuItem).delete()
session.commit()

for category in categories:
	new_category = Category(name = category["name"], slug = category["slug"])

	session.add(new_category)
	session.commit()


for item in items:
	new_item = MenuItem(name = item["name"], slug = item["slug"], category_id = item["category_id"], description = item["description"], author_email = item["email"])

	session.add(new_item)
	session.commit()


session.close()

