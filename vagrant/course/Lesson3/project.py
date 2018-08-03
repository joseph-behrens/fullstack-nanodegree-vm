#!/usr/bin/env python2

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)


def create_db_session():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    session = create_db_session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    session = create_db_session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New item {} created!'.format(newItem.name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'newmenuitem.html',
            restaurant_id=restaurant_id,
            restaurant=restaurant)


@app.route(
    '/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
    methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    session = create_db_session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id,
            id=menu_id).one()
    if request.method == 'POST':
        menu_item.name = request.form['name']
        menu_item.description = request.form['description']
        menu_item.price = request.form['price']
        session.add(menu_item)
        session.commit()
        flash('Updated {}!'.format(menu_item.name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html',
            restaurant_id=restaurant_id,
            restaurant=restaurant,
            menu_id=menu_id,
            menu_item=menu_item)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    session = create_db_session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id,
            id=menu_id).one()
    if request.method == 'POST':
        session.delete(menu_item)
        session.commit()
        flash('Deleted {}!'.format(menu_item.name))
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deletemenuitem.html',
            restaurant_id=restaurant_id,
            restaurant=restaurant,
            menu_id=menu_id,
            menu_item=menu_item)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
