#Import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Import from database_setup.py
from database_setup import Base, User, Category, QuoteItem

engine = create_engine('sqlite:///quotes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Add dummy user
User1 = User(name="Baba lala", email="baba@lala.com",
             picture='http://via.placeholder.com/400x400')
session.add(User1)
session.commit()
print "Added user!"

#Add work category
category1 = Category(user_id=1, name="Work")
session.add(category1)
session.commit()
print "Added 'Work' category"

#Add love category
category2 = Category(user_id=1, name="Love")
session.add(category2)
session.commit()
print "Added 'Love' category"

#Add life category
category3 = Category(user_id=1, name="Life")
session.add(category3)
session.commit()
print "Added 'Life' category"


#Add sample quotes
quoteItem1 = QuoteItem(user_id=1, name="Quote for bad working day", content="Success is no accident. It is hard work, perseverance, learning, studying, sacrifice and most of all, love of what you are doing or learning to do", author="Pele",  category=category1)
session.add(quoteItem1)
session.commit()

#Add sample quotes
quoteItem2 = QuoteItem(user_id=1, name="Work quote", content="Stay positive and happy. Work hard and don't give up hope. Be open to criticism and keep learning. Surround yourself with happy, warm and genuine people.", author="Tena Desae",  category=category1)
session.add(quoteItem1)
session.commit()
