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
session.add(quoteItem2)
session.commit()

#Add sample quotes
quoteItem3 = QuoteItem(user_id=1, name="Love quote", content="I look at you and see the rest of my life in front of my eyes.", author="Unknown",  category=category2)
session.add(quoteItem3)
session.commit()

#Add sample quotes
quoteItem4 = QuoteItem(user_id=1, name="Another Love quote", content="The greatest happiness of life is the conviction that we are loved; loved for ourselves, or rather, loved in spite of ourselves.", author="Victor Hugo",  category=category2)
session.add(quoteItem4)
session.commit()

#Add sample quotes
quoteItem5 = QuoteItem(user_id=1, name="Life quote", content="Don't cry because it's over, smile because it happened.", author="Dr. Seuss",  category=category3)
session.add(quoteItem5)
session.commit()

#Add sample quotes
quoteItem6 = QuoteItem(user_id=1, name="Life quote", content="You've gotta dance like there's nobody watching, Love like you'll never be hurt, Sing like there's nobody listening, And live like it's heaven on earth.", author="William W. Purkey",  category=category3)
session.add(quoteItem6)
session.commit()

print "Sample quotes added."
