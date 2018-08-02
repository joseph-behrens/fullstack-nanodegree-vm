#!/usr/bin/env python2

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import re
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


def connect_db(engine_address):
    engine = create_engine(engine_address)
    Base.metadata.bind=engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    return session


def get_restaurants(id_filter = None):
    session = connect_db('sqlite:///restaurantMenu.db')
    if id_filter == None:
        restaurants = session.query(Restaurant).order_by(Restaurant.name)
    else:
        restaurants = session.query(Restaurant).filter_by(id = id_filter).one()
    return restaurants

def get_restaurant_id_from_url(self):
    return re.search('/restaurants/(\d+)/*',self.path).group(1)


def create_restaurant(restaurant_name):
    session = connect_db('sqlite:///restaurantMenu.db')
    new_restaurant = Restaurant(name=restaurant_name)
    session.add(new_restaurant)
    session.commit()


def delete_restaurant(restaurant_to_delete):
    session = connect_db('sqlite:///restaurantMenu.db')
    deletion = session.query(Restaurant).filter_by(id = restaurant_to_delete.id).one()
    session.delete(deletion)
    session.commit()


def edit_restaurant(restaurant, new_name):
    print("Changing {0} to {1}".format(restaurant.name,new_name))
    session = connect_db('sqlite:///restaurantMenu.db')
    restaurant.name = new_name
    session.add(restaurant)
    session.commit()


def get_form_message(field_name, self):
    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
    if ctype == 'multipart/form-data':
        fields = cgi.parse_multipart(self.rfile, pdict)
        return fields.get(field_name)[0]
    else:
        return "Field {} not found".format(field_name)
    

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text-html')
            self.end_headers()

            output = ""
            output += """\
                <html>
                    <body>
                    <h1>Restaurant List</h1>
                    <p><a href='/restaurants/new'>Create a New Restaurant</a></p>
                        <table>
            """
            for restaurant in get_restaurants():
                output += """\
                    <tr>
                        <td>
                            <a href='/restaurants/{0}/edit'>edit</a>
                        </td>
                        <td>
                            <a href='/restaurants/{0}/delete'>delete</a>
                        </td>
                        <td> -- 
                    """.format(restaurant.id)
                output += restaurant.name
                output += "</td></tr>"
            output += """\
                        </table>
                    <body>
                </html>
            """
            self.wfile.write(output)
            print(output)
            return

        elif self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text-html')
            self.end_headers()

            output = ""
            output += """\
                <html>
                    <body>
                        <h1>Create a New Restaurant</h1>
                        <a href='/restaurants'>Back to Restaurant List</a>
                        <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                            <h2>What is the name of the new restaurant?</h2>
                            <input name='restaurant' type='text'>
                            <input type='submit' value='Submit'>
                        </form>
                </body>
            </html>"""
            self.wfile.write(output)
            print(output)
            return

        elif self.path.endswith("/edit"):
            self.send_response(200)
            self.send_header('Content-type', 'text-html')
            self.end_headers()

            restaurant_id = get_restaurant_id_from_url(self)
            restaurant = get_restaurants(restaurant_id)
            output = ""
            output += """\
                <html>
                    <body>
                        <h1>Edit {0}</h1>
                        <a href='/restaurants'>Back to Restaurant List</a>
                        <form method='POST' enctype='multipart/form-data' action='/restaurants/{1}/edit'>
                            <h2>What is the new name of {0}?</h2>
                            <input name='restaurant' type='text' value='{0}'>
                            <input type='submit' value='Submit'>
                        </form>
                </body>
            </html>""".format(restaurant.name,restaurant.id)
            self.wfile.write(output)
            print(output)
            return

        elif self.path.endswith("/delete"):
            self.send_response(200)
            self.send_header('Content-type', 'text-html')
            self.end_headers()

            restaurant_id = get_restaurant_id_from_url(self)
            restaurant = get_restaurants(restaurant_id)
            output = ""
            output += """\
                <html>
                    <body>
                        <h1>Are you sure you want to delete {0}?</h1>
                        <a href='/restaurants'>Back to Restaurant List</a>
                        <form method='POST' enctype='multipart/form-data' action='/restaurants/{1}/delete'>
                            <input type='submit' value='Yes'>
                        </form>
                </body>
            </html>""".format(restaurant.name,restaurant.id)
            self.wfile.write(output)
            print(output)
            return
        else:
            self.send_error(404, "File Not Found %s" % self.path)


    def do_POST(self):
        if self.path.endswith("/restaurants/new"):
            create_restaurant(get_form_message('restaurant', self))

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location','/restaurants')
            self.end_headers()

        elif self.path.endswith("/edit"):
            restaurant_id = get_restaurant_id_from_url(self)
            restaurant = get_restaurants(restaurant_id)
            new_name = get_form_message('restaurant', self)
            edit_restaurant(restaurant, new_name)

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location','/restaurants')
            self.end_headers()

        elif self.path.endswith("/delete"):
            restaurant_id = get_restaurant_id_from_url(self)
            restaurant = get_restaurants(restaurant_id)
            delete_restaurant(restaurant)

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location','/restaurants')
            self.end_headers()


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
