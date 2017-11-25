#Import flask and sqlalchemy library
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#Import asc desc
from sqlalchemy import asc, desc
#Import for anti forgery state token
from flask import session as login_session
import random, string

#Import from database_setup.py
from database_setup import Base, User, Category, CatalogItem

app = Flask(__name__)

#Create database connection
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Making anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


#Making API Endpoint for '/items/JSON'
@app.route('/items/JSON')
def itemsJSON():
    items = session.query(CatalogItem).all()
    return jsonify(items=[i.serialize for i in items])


#Making API Endpoint for '/item/<int:item_id>/JSON'
@app.route('/item/<int:item_id>/JSON')
def itemJSON(item_id):
    item = session.query(CatalogItem).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)


#Making API Endpoint for '/categories/JSON'
@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


#Making API Endpoint for '/category/<int:category_id>/JSON'
@app.route('/category/<int:category_id>/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return jsonify(category=category.serialize)


#Routing for '/' and '/quotes'
@app.route('/')
@app.route('/items')
def showItems():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(CatalogItem).order_by(desc(CatalogItem.id))
    return render_template('main.html', categories=categories, items=items)


#Routing for '/category/<int:category_id>'
@app.route('/category/<int:category_id>')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(category_id=category_id)
    return render_template('category.html', category_id=category_id, items=items, category=category)

#Routing for 'category/new'
@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        #Send message to user in main.html
        flash('New category created')
        return redirect(url_for('showItems'))
    return render_template('new_category.html')


#Routing for 'category/<int:category_id>/edit'
@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        #Send message to user in main.html
        flash('Category edited')
        return redirect(url_for('showItems'))
    else:
        return render_template('edit_category.html', category_id=category_id, category=editedCategory)


#Routing for 'category/<int:category_id>/delete'
@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    deletedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(deletedCategory)
        session.commit()
        #Send message to user in main.html
        flash('Category deleted')
        return redirect(url_for('showItems'))
    else:
        return render_template('delete_category.html', category_id=category_id, category=deletedCategory)


#Routing for 'item/new'
@app.route('/item/new', methods=['GET', 'POST'])
def newItem():
    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'], description=request.form['description'], category_id=request.form['radio'])
        session.add(newItem)
        session.commit()
        #Send message to user in main.html
        flash('New item created')
        return redirect(url_for('showItems'))
    return render_template('new_item.html', categories=categories)


#Routing for 'item/<int:item_id>/edit'
@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):
    editedItem = session.query(CatalogItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        #Send message to user in main.html
        flash('Item edited')
        return redirect(url_for('showItems'))
    else:
        return render_template('edit_item.html', item_id=item_id, item=editedItem)


#Routing for 'item/<int:item_id>/delete'
@app.route('/item/<int:item_id>/delete', methods = ['GET', 'POST'])
def deleteItem(item_id):
    deletedItem = session.query(CatalogItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        #Send message to user in main.html
        flash('Item deleted')
        return redirect(url_for('showItems'))
    else:
        return render_template('delete_item.html', item_id=item_id, item=deletedItem)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
