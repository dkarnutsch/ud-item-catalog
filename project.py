from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///item-catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items/')
def showCategory(category_id):
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    #creator = getUserInfo(restaurant.user_id)
    #items = session.query(MenuItem).filter_by(
    #    restaurant_id=restaurant_id).all()
    #if 'username' not in login_session or creator.id != login_session['user_id']:
    #    return render_template('publicmenu.html', items=items, restaurant=restaurant, creator=creator)
    #else:
    #    return render_template('menu.html', items=items, restaurant=restaurant, creator=creator)
    return "Category"

# Show all restaurants
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).all()
    print(categories)
    if 'username' not in login_session:
        return render_template('public_item-catalog.html', categories=categories)
    else:
        return render_template('item-catalog.html', categories=categories)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
