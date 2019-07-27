from bottle import route, run, template, static_file, get, post, delete, request,response
from sys import argv
import json
import pymysql

# pymysql connector 
connection = pymysql.connect(host="localhost",    
                     user="root",        
                     passwd="root", 
                     db="store",
                     charset="utf8",
                     cursorclass=pymysql.cursors.DictCursor)


# categories endpoints

@post("/category")
def create_category():
  with connection.cursor() as cursor:
    try:
      category_name = request.json.get("name")
      
      if category_name is None:
        response.status = 400
        response["status__line"] = "name parameter is missing"
        return response
      
      search_category_query = f'select cat_name from categories where cat_name = "{category_name}"'
      cursor.execute(search_category_query)
      category_exists = cursor.fetchone() 
      if category_exists:
        response.status = 200
        response["status__line"] = "category already exists"
        return response

      sql = 'INSERT INTO categories VALUES(null,"{}")'.format(category_name)
      connection.commit()
      response.status = 201
      response["status__line"] = "category created successfully"
      return response
    except Exception as e:
      response.status = 500
      response["status__line"] = "internal Error"
      return response
            
@delete("/category/<id:int>")
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
