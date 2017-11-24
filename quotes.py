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
        return redirect(url_for('showQuotes'))
    return render_template('new_quote.html', categories=categories)


#Routing for 'quote/<int:quote_id>/edit'
@app.route('/quote/<int:quote_id>/edit')
def editQuote(quote_id):
    return 'This page for editing quote %s' % quote_id


#Routing for 'quote/<int:quote_id>/delete'
@app.route('/quote/<int:quote_id>/delete')
def deleteQuote(quote_id):
    return 'This page for deleting quote %s' % quote_id

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
