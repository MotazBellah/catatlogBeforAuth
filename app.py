from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from database_setup import Catalog, Base, Item

from tmdb3 import set_key
from tmdb3 import searchMovie

from urlparse import urlparse

set_key('b42f313de752b4082729b83599e87b3f')

engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

def getMovieInf(movieName):
    movie = searchMovie(movieName)
    if len(movie):
        trailer = movie[0].youtube_trailers[0].geturl()
        overview = movie[0].overview
        rating = movie[0].userrating
        return trailer, overview, rating
    return False

@app.route('/')
@app.route('/catalogs')
def showCatalog():
    '''This page will sho all my catalogs'''
    catalogs = session.query(Catalog).all()
    return render_template('catalogs.html', catalogs = catalogs)

# @app.route('/catalogs/<item_name>', methods = ['GET', 'POST'])
# def searchItem(item_name):
#     if request.method == 'POST':
#         name = request.form['name']
#         items = session.query(Item).all()
#         if item in items:
#             if name == item.name:
#                 catalog_name = name.catalog
#                 return redirect(url_for('showItemInfo', catalog_name=catalog_name, name=name))
#         else:
#             print 'c'


@app.route('/catalog/<catalog_name>')
@app.route('/catalog/<catalog_name>/items')
def showItem(catalog_name):
    '''show catalog's items %s''' % catalog_name
    poster = []
    catalogs = session.query(Catalog).all()
    catalog_id = session.query(Catalog).filter_by(name = catalog_name).first().id
    catalog = session.query(Catalog).filter_by(name = catalog_name).one()
    items = session.query(Item).filter_by(catalog_id = catalog.id).all()
    for item in items:
        movie = searchMovie(item.name)
        poster.append(movie[0].poster.geturl())
    print poster
    return render_template('items.html', items = items, catalog = catalog, catalogs=catalogs, catalog_name=catalog_name, x = len(items), poster=poster)
    # return render_template('items.html', items = (items, poster), catalog = catalog, catalogs=catalogs, catalog_name=catalog_name)

@app.route('/catalog/<catalog_name>/<item_name>')
def showItemInfo(catalog_name, item_name):
    '''edit catalog's items %s''' % item_name
    movie = getMovieInf(item_name)
    catalogs = session.query(Catalog).all()
    items = session.query(Item).filter_by(name = item_name).first()
    catalog = session.query(Catalog).filter_by(id = items.catalog_id).first()
    if movie:
        m = urlparse(movie[0]).query[2:]
        overview = movie[1]
        rating = movie[2]
        # Need to render new html file in case no trailer found
    return render_template('itemInfo.html', items = items, rating = rating, overview=overview, m = m, catalogs=catalogs)

@app.route('/catalog/<catalog_name>/items/new', methods = ['GET', 'POST'])
def newItem(catalog_name):
    '''create new catalog's items %s''' % catalog_name
    catalog_id = session.query(Catalog).filter_by(name = catalog_name).first().id
    if request.method == 'POST':
        newItem = Item(name = request.form['name'], catalog_id = catalog_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showItem', catalog_name=catalog_name))
    else:
        return render_template('newItem.html', catalog_name=catalog_name)

@app.route('/catalog/<catalog_name>/<item_name>/edit', methods = ['GET', 'POST'])
def editItem(catalog_name, item_name):
    '''edit catalog's items %s''' % item_name
    catalogs = session.query(Catalog).all()
    editedItem = session.query(Item).filter_by(name = item_name).first()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        if request.form.get('genre') != 'Choose...':
            editedCatalog = str(request.form.get('genre'))
            editedItem.type = editedCatalog
            catalog_id = session.query(Catalog).filter_by(name = editedCatalog).first().id
            editedItem.catalog_id = catalog_id

        return redirect(url_for('showItem', catalog_name=catalog_name))
    else:
        return render_template('editItem.html', item_name = item_name, catalogs = catalogs, catalog_name=catalog_name, item = editedItem)

@app.route('/catalog/<catalog_name>/<item_name>/delete', methods = ['GET', 'POST'])
def deleteItem(catalog_name, item_name):
    '''delete catalog's items %s''' % item_name
    item = session.query(Item).filter_by(name = item_name).first()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showItem', catalog_name=catalog_name))
    else:
        return render_template('deleteItem.html', item_name = item_name, catalog_name=catalog_name, item = item)




if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
