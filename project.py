import json
import random
import string
from functools import wraps

import httplib2
import requests
from flask import session as login_session
from flask import (Flask, flash, jsonify, make_response, redirect,
                   render_template, request, url_for)
from oauth2client.client import FlowExchangeError, flow_from_clientsecrets
from sqlalchemy import asc, create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///item-catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('showLogin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def createUser(login_session):
    """ Helper function for creating an user """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserID(email):
    """ Helper function for getting the users id based on the email adress """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    """ Helper function for getting the user by id """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getAllCategories():
    """ Helper function for getting all categories """
    categories = session.query(Category).all()
    return categories


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """ Handles google authentication """
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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
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
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("you are now logged in as %s" % login_session['username'])
    return render_template('login_callback.html')


@app.route('/login')
def showLogin():
    """ Displays login screen for all providers """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/disconnect')
def disconnect():
    """ Disconnects based on the provider """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


@app.route('/gdisconnect')
def gdisconnect():
    """ Disconnects from the Google backend """
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/item/new/', methods=['GET', 'POST'])
@login_required
def newItem():
    """ Displays page for creating a new item """
    if request.method == 'POST':
        newItem = Item(title=request.form['title'],
                       description=request.form['description'],
                       category_id=request.form['category'],
                       user_id=login_session['user_id'])
        session.add(newItem)
        flash('New Item %s Successfully Created' % newItem.title)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        categories = getAllCategories()
        return render_template('newItem.html', categories=categories)


@app.route('/item/<int:item_id>/')
def showItem(item_id):
    """ Displays page for reading an item """
    item = session.query(Item).filter_by(id=item_id).one()
    creator = getUserInfo(item.user_id)
    return render_template('item.html', item=item, creator=creator)


@app.route('/item/<int:item_id>/edit/', methods=['GET', 'POST'])
@login_required
def editItem(item_id):
    """ Displays page for updating an item """
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if editedItem.user_id != login_session['user_id']:
        return """<script>function myFunction() {alert('You are not authorized
                  to edit this item. Please create your own item in order
                  to edit.');}</script><body onload='myFunction()'>"""
    if request.method == 'POST':
        editedItem.title = request.form['title']
        editedItem.description = request.form['description']
        editedItem.category_id = request.form['category']
        flash('Item Successfully Edited %s' % editedItem.title)
        return redirect(url_for('showCatalog'))
    else:
        categories = getAllCategories()
        return render_template('editItem.html', categories=categories,
                               item=editedItem)


@app.route('/item/<int:item_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteItem(item_id):
    """Displays page for deleting an item """
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        return """<script>function myFunction() {alert('You are not authorized
                  to delete this item. Please create your own item in order
                  to delete.');}</script><body onload='myFunction()'>"""
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.title)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items/')
def showCategory(category_id):
    """ Displays page for reading a category """
    categories = getAllCategories()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('category.html', categories=categories, items=items,
                           category=category)


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    """ Main Page - Displays item catalog """
    categories = getAllCategories()
    latestItems = session.query(Item).order_by(Item.id.desc()).limit(10).all()
    return render_template('item-catalog.html', categories=categories,
                           latestItems=latestItems)


@app.route('/catalog.json')
def showCatalogAsJSON():
    """ Displays data as json string """
    categories = []
    for category in getAllCategories():
        items = session.query(Item).filter_by(category_id=category.id).all()
        serializedItems = [i.serialize for i in items]
        serializedCategory = category.serialize
        serializedCategory['items'] = serializedItems
        categories.append(serializedCategory)
    return jsonify(categories=categories)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
