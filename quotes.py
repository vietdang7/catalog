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
    quotes = session.query(QuoteItem)
    return 'This page will show quotes of category %s' % category_id

#Routing for 'category/new'
@app.route('/category/new')
def newCategory():
    return 'This page for creating new category'


#Routing for 'category/<int:category_id>/edit'
@app.route('/category/<int:category_id>/edit')
def editCategory(category_id):
    return 'This page for editing category %s' % category_id


#Routing for 'category/<int:category_id>/delete'
@app.route('/category/<int:category_id>/delete')
def deleteCategory(category_id):
    return 'This page for deleting category %s' % category_id


#Routing for 'quote/new'
@app.route('/quote/new')
def newQuote():
    return 'This page for creating new quote'


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
