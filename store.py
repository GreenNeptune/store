from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

# categories endpoints


@post("/category")
def create_category(category_name):
    pass


@delete("/category/<id>")
def delete_category(id):
    pass


@get("/categories")
def get_all_categories():
    pass

# products endpoints


@post("product")
def add_or_edit_product():
    pass


@get("/product/<id>")
def get_product(id):
    pass


@delete("/product/<id>")
def delete_poduct():
    pass


@get("/products")
def get_all_products():
    pass

# index endpoint


@get("/")
def index():
    return template("index.html")

# admin endpoint


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='localhost', port=argv[1], reloader=True, debug=True)
