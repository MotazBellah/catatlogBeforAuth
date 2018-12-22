from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Catalog, Base, Item

engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

b = Catalog(name = "Drama")
session.add(b)
session.commit()
b1 = Item(name = " The Godfather", catalog = b)
session.add(b1)
session.commit()

c = Catalog(name = "Sci-Fi")
session.add(c)
session.commit()
c1 = Item(name = "Intersteller", catalog = c)
session.add(c1)
session.commit()

d = Catalog(name = "Crime")
session.add(d)
session.commit()
d1 = Item(name = "The Departed", catalog = d)
session.add(d1)
session.commit()

e = Catalog(name = "Comedy")
session.add(e)
session.commit()
ee1 = Item(name = " The Hangover", catalog = e)
session.add(ee1)
session.commit()

f = Catalog(name = "Musical")
session.add(f)
session.commit()
f1 = Item(name = "Into The Woods", catalog = f)
session.add(f1)
session.commit()

h = Catalog(name = "Animation")
session.add(h)
session.commit()
h1 = Item(name = "The Lion king", catalog = h)
session.add(h1)
session.commit()

v = Catalog(name = "Romace")
session.add(v)
session.commit()
v1 = Item(name = "Titanic", catalog = v)
session.add(v1)
session.commit()

y = Catalog(name = "History")
session.add(y)
session.commit()
y1 = Item(name = "Downfall", catalog = y)
session.add(y1)
session.commit()
