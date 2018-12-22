import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Catalog(Base):
    __tablename__ = "catalog"

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            }


class Item(Base):
    __tablename__ = "item"

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    type = Column(String(250))
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog)

    # To use JSON
    @property
    def serialize(self):
        #Returns object data in easily format
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'type': self.type,
        }

engine = create_engine('sqlite:///catalogitem.db')

Base.metadata.create_all(engine)
