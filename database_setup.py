#Import needed lib from SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


#Setup 'User' table
class User(Base):
    __tablename__ = 'user'


    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    email = Column(String(80), nullable = False)
    picture = Column(String(250))


    #property decoration for serialize (JSON)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name'          : self.name,
            'id'            : self.id,
            'email'         : self.email,
            'picture'       : self.picture,
        }


#Setup 'Category' table
class Category(Base):
    __tablename__ = 'category'


    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    catalogitem = relationship('CatalogItem', cascade='all, delete-orphan')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    #property decoration for serialize (JSON)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name'          : self.name,
            'id'            : self.id,
        }



#Setup 'QuoteItem' table
class CatalogItem(Base):
    __tablename__ = 'catalogitem'


    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)



    #property decoration for serialize (JSON)
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'           : self.name,
           'description'    : self.description,
           'id'             : self.id,
           'category'       : self.category.name,
       }



engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
