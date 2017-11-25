#Import flask and sqlalchemy library
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#Import asc desc
from sqlalchemy import asc, desc


#Import from database_setup.py
from database_setup import Base, User, Category, QuoteItem

app = Flask(__name__)

#Create database connection
engine = create_engine('sqlite:///quotes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Making API Endpoint for '/quotes/JSON'
@app.route('/quotes/JSON')
def quotesJSON():
    quotes = session.query(QuoteItem).all()
    return jsonify(quotes=[q.serialize for q in quotes])


#Making API Endpoint for '/quote/<int:quote_id>/JSON'
@app.route('/quote/<int:quote_id>/JSON')
def quoteJSON(quote_id):
    quote = session.query(QuoteItem).filter_by(id=quote_id).one()
    return jsonify(quote=quote.serialize)


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
@app.route('/quotes')
def showQuotes():
    categories = session.query(Category).order_by(asc(Category.name))
    quotes = session.query(QuoteItem).order_by(desc(QuoteItem.id))
    return render_template('main.html', categories=categories, quotes=quotes)


#Routing for '/category/<int:category_id>'
@app.route('/category/<int:category_id>')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    quotes = session.query(QuoteItem).filter_by(category_id=category_id)
    return render_template('category.html', category_id=category_id, quotes=quotes, category=category)

#Routing for 'category/new'
@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        #Send message to user in main.html
        flash('New category created')
        return redirect(url_for('showQuotes'))
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
        return redirect(url_for('showQuotes'))
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
        return redirect(url_for('showQuotes'))
    else:
        return render_template('delete_category.html', category_id=category_id, category=deletedCategory)


#Routing for 'quote/new'
@app.route('/quote/new', methods=['GET', 'POST'])
def newQuote():
    categories = session.query(Category).all()
    if request.method == 'POST':
        newQuote = QuoteItem(name=request.form['name'], content=request.form['content'], author=request.form['author'], category_id=request.form['radio'])
        session.add(newQuote)
        session.commit()
        #Send message to user in main.html
        flash('New quote created')
        return redirect(url_for('showQuotes'))
    return render_template('new_quote.html', categories=categories)


#Routing for 'quote/<int:quote_id>/edit'
@app.route('/quote/<int:quote_id>/edit', methods=['GET', 'POST'])
def editQuote(quote_id):
    editedQuote = session.query(QuoteItem).filter_by(id=quote_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedQuote.name = request.form['name']
        session.add(editedQuote)
        session.commit()
        #Send message to user in main.html
        flash('Quote edited')
        return redirect(url_for('showQuotes'))
    else:
        return render_template('edit_quote.html', quote_id=quote_id, quote=editedQuote)


#Routing for 'quote/<int:quote_id>/delete'
@app.route('/quote/<int:quote_id>/delete', methods = ['GET', 'POST'])
def deleteQuote(quote_id):
    deletedQuote = session.query(QuoteItem).filter_by(id=quote_id).one()
    if request.method == 'POST':
        session.delete(deletedQuote)
        session.commit()
        #Send message to user in main.html
        flash('Quote deleted')
        return redirect(url_for('showQuotes'))
    else:
        return render_template('delete_quote.html', quote_id=quote_id, quote=deletedQuote)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
