from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from item_catalogue.model import Base


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