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


#Setup 'Category' table
class Category(Base):
    __tablename__ = 'category'


    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
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
class QuoteItem(Base):
    __tablename__ = 'quoteitem'


    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    content = Column(String(250))
    author = Column(String(80), nullable = False)
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
           'content'        : self.content,
           'id'             : self.id,
           'category'       : self.category_name,
       }



engine = create_engine('sqlite:///quotes.db')


Base.metadata.create_all(engine)
