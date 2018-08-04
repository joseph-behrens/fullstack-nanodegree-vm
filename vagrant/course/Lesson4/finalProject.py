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
        return self.session.query(Restaurant).filter_by(
            id=restaurant_id).one()

    def get_menu(self, restaurant_id):
        return self.session.query(
            MenuItem).filter_by(
                restaurant_id=restaurant_id)

    def get_menu_item(self, menu_id):
        return self.session.query(MenuItem).filter_by(
            id=menu_id).one()


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    db = DB_Connection()
    restaurants = db.get_all_restaurants()
    return render_template('index.html', restaurants=restaurants)


@app.route('/restaurants/new')
def newRestaurant():
    return render_template('new-restaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    return render_template('edit-restaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    return render_template('delete-restaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    menu = db.get_menu(restaurant_id)
    return render_template('menu.html', restaurant=restaurant, menu=menu)


@app.route('/restaurants/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    return render_template('new-menu-item.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    menu_item = db.get_menu_item(menu_id)
    return render_template(
        "edit-menu-item.html", restaurant=restaurant, menu_item=menu_item)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    menu_item = db.get_menu_item(menu_id)
    return render_template(
        'delete-menu-item.html', restaurant=restaurant, menu_item=menu_item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
