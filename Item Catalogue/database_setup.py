import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# create database equivalent of tables
class Category(Base):
	__tablename__ = 'category'
	name = Column(String(80), primary_key=True)

class MenuItem(Base):
	__tablename__ = 'menu_item'
	name = Column(String(80), primary_key=True)
	description = Column(String(300))
	date_created = Column(DateTime,nullable=False)
	category_name = Column(String(80),ForeignKey('category.name'))
	category = relationship(Category)

# put everything together in a file called itemcatalogue.db
engine = create_engine('sqlite:///itemcatalogue.db')
Base.metadata.create_all(engine)