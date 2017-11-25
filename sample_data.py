#Import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Import from database_setup.py
from database_setup import Base, User, Category, CatalogItem

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Add dummy user
User1 = User(name="Baba lala", email="baba@lala.com",
             picture='http://via.placeholder.com/400x400')
session.add(User1)
session.commit()
print "Added user!"

def addCategory(category_name):
    category = Category(user_id=1, name=category_name)
    session.add(category)
    session.commit()
    print "Added " + category_name + " category"

def addItem(item_name,item_description,category_id):
    item = CatalogItem(name=item_name, description=item_description, category_id=category_id)
    session.add(item)
    session.commit()
    print "Added " + item_name + " item"


addCategory("Soccer")

addItem("Soccer Ball","Start off any pickup game with your mates by kicking around the Soccer Ball. Crafted of a nylon-wound/TPC carcass, this ball holds strong for extended match play and offers soft touch for precision passing. The butyl bladder provides optimal air retention, making for consistent performance and shape through regulation.",1)

addItem("Soccer Goalkeeper Gloves", "Outfitted with an EVA backhand and latex palm to maximize your movements in between the posts, the Soccer Goalie Gloves provide a lightweight feel to execute well-timed parries and catching saves to keep your squad in the match and your scoring record clean.",1)

addCategory("Basket")

addItem("Basketball Shoes", "A stretchy, foam-backed mesh upper helps keep your feet cool and comfortable when the game heats up, while soft foam molded around the ankle improves comfort.",2)

addCategory("Baseball")

addItem("USA Youth Bat", "Designed with a durable aluminum barrel, the 2018 USA Bat also includes an extended barrel design to enlarge the sweet spot.",3)

addItem("Baseball Practice Shirt", "Lightweight, durable and comfortable, the Baseball Shirt is perfect for practice or for wearing under your uniform on game day.",3)

addCategory("Frisbee")

addItem("Sport Disc", "Ultimate is a fast paced, non-contact field game that combines the non-stop movement and athletic endurance of soccer with the aerial passing skills of football", 4)

addItem("Frisbee Cleats", "Comfortability is great, and durability will last you at least 2 competitive seasons. Overall a fantastic cleat if you are receiver/cutter. ", 4)

addCategory("Snowboarding")

addItem("Snowboard Boots", "Snowboard Boots for a comfortable, supportive fit on the mountain. With a mid-range flex rating, these boots allow give while still offering support. ", 5)

addCategory("Rock Climbing")

addItem("Tube Chalk Bag", "A classic chalk bag with a deep pile lining, toothbrush holder, and a chalk proof closure.", 6)

addItem("Climbing Helmets", "A durable multi-purpose climbing helmet for women that adapts easily to your head shape and size.", 6)

addCategory("Football")

addItem("All-Field 3.0 Football", "All-Field Football is a durable ball built for the toughest play, with a synthetic leather cover that helps improve control for an enhanced grip in all conditions.", 7)

addCategory("Skating")

addItem("Cruiser Skateboard", "9-ply maple deck features a slight concave shape with single kicktail, which offers optimum gripping power. You'll look stylish with the bottom graphics and painted edges.", 8)

addCategory("Hockey")

addItem("Ice Hockey Goalie Stick", "Ice Hockey Goalie Stick is built to withstand the countless force of pucks at high velocity to ensure consistent performance and feel.", 9)

print "Sample data added."
