import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

from item_catalogue.model import category
from item_catalogue.model import menuitem

# put everything together in a file called itemcatalogue.db
engine = create_engine('sqlite:///model/itemcatalogue.db')
Base.metadata.create_all(engine)