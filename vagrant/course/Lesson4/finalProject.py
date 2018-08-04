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


@app.route('/api/restaurants')
def showRestaurantsJson():
    db = DB_Connection()
    restaurants = db.get_all_restaurants()
    return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    db = DB_Connection()
    if request.method == 'POST':
        new_restaurant = Restaurant(
            name=request.form['name']
        )
        db.session.add(new_restaurant)
        db.session.commit()
        flash('New restaurant {} created!'.format(new_restaurant.name))
        return redirect(url_for('newMenuItem', restaurant_id=new_restaurant.id))
    else:
        return render_template('new-restaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    old_name = restaurant.name
    if request.method == 'POST':
        restaurant.name = request.form['name']
        db.session.add(restaurant)
        db.session.commit()
        flash('{0} has been renamed to {1}'.format(old_name, restaurant.name))
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('edit-restaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    old_restaurant = restaurant.name
    if request.method == 'POST':
        db.session.delete(restaurant)
        db.session.commit()
        flash('{0} has been deleted'.format(old_restaurant))
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('delete-restaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    menu = db.get_menu(restaurant_id)
    return render_template('menu.html', restaurant=restaurant, menu=menu)


@app.route('/api/restaurants/<int:restaurant_id>/menu')
def showMenuJson(restaurant_id):
    db = DB_Connection()
    menu = db.get_menu(restaurant_id)
    return jsonify(MenuItem=[item.serialize for item in menu])


@app.route('/api/restaurants/<int:restaurant_id>/menu/<int:menu_id>')
def showMenuItemJson(restaurant_id, menu_id):
    db = DB_Connection()
    menu_item = db.get_menu_item(menu_id)
    return jsonify(MenuItem=menu_item.serialize)


@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    if request.method == 'POST':
        menu_item = MenuItem(
            course=request.form['course'],
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            restaurant_id=restaurant.id
        )
        db.session.add(menu_item)
        db.session.commit()
        flash("Added {0} to {1}".format(menu_item.name, restaurant.name))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    return render_template('new-menu-item.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    menu_item = db.get_menu_item(menu_id)
    old_name = menu_item.name
    old_price = menu_item.price
    if request.method == 'POST':
        menu_item.course == request.form['course']
        menu_item.name = request.form['name']
        menu_item.description = request.form['description']
        menu_item.price = request.form['price']
        db.session.add(menu_item)
        db.session.commit()
        flash("Updated {0}. It's price was {1}".format(old_name, old_price))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            "edit-menu-item.html", restaurant=restaurant, menu_item=menu_item)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    db = DB_Connection()
    restaurant = db.get_restaurant(restaurant_id)
    menu_item = db.get_menu_item(menu_id)
    item_name = menu_item.name
    if request.method == 'POST':
        db.session.delete(menu_item)
        db.session.commit()
        flash("Deleted menu item {0}".format(item_name))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'delete-menu-item.html', restaurant=restaurant, menu_item=menu_item)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'R34d23zDSdXT2NH00RLHBK6JetPtDxsg'
    app.run(host='0.0.0.0', port=5000)
