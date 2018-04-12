from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///item-catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Category 1
category1 = Category(name="Soccer")
session.add(category1)
session.commit()

item1 = Item(user_id=1, title="Ball", description="A soccer ball",
             category=category1)
session.add(item1)
session.commit()

item2 = Item(user_id=1, title="Gloves", description="Gloves for a Keeper",
             category=category1)
session.add(item2)
session.commit()

item3 = Item(user_id=1, title="Goal", description="A soccer goal",
             category=category1)
session.add(item3)
session.commit()

# Category 2
category2 = Category(name="Basketball")
session.add(category2)
session.commit()

item4 = Item(user_id=1, title="Ball", description="A basket ball",
             category=category2)
session.add(item4)
session.commit()

item5 = Item(user_id=1, title="Hoop", description="NBA Basketball hoop",
             category=category2)
session.add(item5)
session.commit()

# Category 3
category3 = Category(name="Baseball")
session.add(category3)
session.commit()

item6 = Item(user_id=1, title="Red Bat", description="A red bat",
             category=category3)
session.add(item6)
session.commit()


item7 = Item(user_id=1, title="Green Bat", description="A green bat",
             category=category3)
session.add(item7)
session.commit()


item8 = Item(user_id=1, title="Blue Bat", description="A blue bat",
             category=category3)
session.add(item8)
session.commit()


item9 = Item(user_id=1, title="Yellow Bat", description="A yellow bat",
             category=category3)
session.add(item9)
session.commit()

# Category 4
category4 = Category(name="Frisbee")
session.add(category4)
session.commit()

item10 = Item(user_id=1, title="Red Frisbee", description="A red frisbee",
              category=category4)
session.add(item10)
session.commit()

item11 = Item(user_id=1, title="Pruple Frisbee",
              description="A purple frisbee",
              category=category4)
session.add(item11)
session.commit()

item12 = Item(user_id=1, title="Black Frisbee", description="A black frisbee",
              category=category4)
session.add(item12)
session.commit()

item13 = Item(user_id=1, title="White Frisbee", description="A white frisbee",
              category=category4)
session.add(item13)
session.commit()


# Category 5
category5 = Category(name="Snowboarding")
session.add(category5)
session.commit()

item14 = Item(user_id=1, title="Snowboard", description="A fancy snowboard",
              category=category5)
session.add(item14)
session.commit()

# Category 6
category6 = Category(name="Rock Climbing")
session.add(category6)
session.commit()

item15 = Item(user_id=1, title="10m Rope",
              description="A rope with a length of 10 meters",
              category=category6)
session.add(item15)
session.commit()

item16 = Item(user_id=1, title="15m Rope",
              description="A rope with a length of 15 meters",
              category=category6)
session.add(item16)
session.commit()

item17 = Item(user_id=1, title="20m Rope",
              description="A rope with a length of 20 meters",
              category=category6)
session.add(item17)
session.commit()

item18 = Item(user_id=1, title="30m Rope",
              description="A rope with a length of 30 meters",
              category=category6)
session.add(item18)
session.commit()

item19 = Item(user_id=1, title="50m Rope",
              description="A rope with a length of 50 meters",
              category=category6)
session.add(item19)
session.commit()

item20 = Item(user_id=1, title="100m Rope",
              description="A rope with a length of 100 meters",
              category=category6)
session.add(item20)
session.commit()

item21 = Item(user_id=1, title="150m Rope",
              description="A rope with a length of 150 meters",
              category=category6)
session.add(item21)
session.commit()

# Category 7
category7 = Category(name="Football")
session.add(category7)
session.commit()

item22 = Item(user_id=1, title="Flags",
              description="Flags for referees", category=category7)
session.add(item22)
session.commit()

item23 = Item(user_id=1, title="Pads",
              description="Protectors for the players", category=category7)
session.add(item23)
session.commit()

item24 = Item(user_id=1, title="Helmet",
              description="Helmet for the players", category=category7)
session.add(item24)
session.commit()

# Category 8
category8 = Category(name="Skating")
session.add(category8)
session.commit()

# Category 9
category9 = Category(name="Hockey")
session.add(category9)
session.commit()

item25 = Item(user_id=1, title="Goal",
              description="A goal", category=category9)
session.add(item25)
session.commit()

item26 = Item(user_id=1, title="Goal+",
              description="A better goal", category=category9)
session.add(item26)
session.commit()

item27 = Item(user_id=1, title="Goal++",
              description="A perfect goal", category=category9)
session.add(item27)
session.commit()

item27 = Item(user_id=1, title="Stick",
              description="A hockey stick", category=category9)
session.add(item27)
session.commit()

print "added items!"
