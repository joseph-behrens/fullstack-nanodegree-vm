#!/usr/bin/env python2.7

from flask import (Flask, render_template, request, redirect,
                   url_for, flash, jsonify)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)


class DB_Connection:
    def __init__(self):
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def get_all_restaurants(self):
        return self.session.query(Restaurant)

    def get_restaurant(self, restaurant_id):
        return self.session.query(Restaurant).filter_by(id=restaurant_id).one()

    def get_menu(self, restaurant_id):
        return self.session.query(MenuItem).filter_by(restaurant_id=restaurant_id)

    def get_menu_item(self, menu_id):
        return self.session.query(MenuItem).filter_by(id=menu_id).one()



@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    db = DB_Connection()
    restaurants = db.get_all_restaurants()
    for restaurant in restaurants:
        print(restaurant.name)
    return "This will show full list of restaurants"


@app.route('/restaurants/new')
def newRestaurant():
    return "This will have a form for new restaurant creation"


@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return "This will have a form to edit an existing restaurant ID: {}".format(restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return "This will be a confirmation page for deleting a restaurant ID: {}".format(restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return "This will show the menu for a specific restaurant ID: {}".format(restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return "This will be form to add a menu item to the restaurant ID: {}".format(restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "This will be a form to edit menu item ID: {}".format(menu_id)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "This will be a form to delete the menu item ID: {}".format(menu_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
