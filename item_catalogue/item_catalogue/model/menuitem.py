from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String

from item_catalogue.model import Base
from item_catalogue.model.category import Category

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