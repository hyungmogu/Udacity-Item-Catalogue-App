import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Sequence, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# create database equivalent of tables
class Category(Base):
	__tablename__ = 'category'
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable= False)
	slug = Column(String(80),nullable=False)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'slug': self.slug
		}

class MenuItem(Base):
	__tablename__ = 'menu_item'
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable=False)
	slug = Column(String(80), nullable=False)
	description = Column(String(300))
	category_id = Column(Integer,ForeignKey('category.id'))
	category = relationship(Category)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'slug': self.slug,
			'description': self.description,
			'category_id': self.category_id,	
		} 

# put everything together in a file called itemcatalogue.db
engine = create_engine('sqlite:///itemcatalogue.db')
Base.metadata.create_all(engine)