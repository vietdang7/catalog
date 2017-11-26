#Import flask and sqlalchemy library
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#Import asc desc
from sqlalchemy import asc, desc
#Import for anti forgery state token
from flask import session as login_session
import random, string


#Import for gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


# Create CLIENT_ID
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Item App"


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


#Making '/gconnect'
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']


    #Check if user exists, make new user if it doesn't.
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# Functions for User
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


#Disconnect - Revoke a current user's token and reset their login sessionmaker
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


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
