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
      category_name = request.forms.get("name")
      if category_name is None:
        response.status = 400
        response["status__line"] = "name parameter is missing"
        error = {"STATUS": "ERROR", "MSG": "name parameter is missing"}
        return json.dumps(error)   
      
      search_category_query = f'select name from categories where name = "{category_name}"'
      cursor.execute(search_category_query)
      category_exists = cursor.fetchone() 
      if category_exists:
        response.status = 200
        response["status__line"] = "category already exists"
        error = {"STATUS": "ERROR", "MSG": "category already exists"}
        return json.dumps(error)

      sql = 'INSERT INTO categories VALUES(null,"{}")'.format(category_name)
      cursor.execute(sql)
      connection.commit()
      response.status = 201
      response["status__line"] = "category created successfully"
      success = {"STATUS":"The category was created successfully", "CAT_ID": cursor.lastrowid}
      return json.dumps(success)
    except Exception as e:
      response.status = 500
      response["status__line"] = "internal Error"
      error = {"STATUS": "ERROR", "MSG": "internal Error"}
      return json.dumps(error)
            
@delete("/category/<id>")
def delete_category(id):
  cat_id = id
  with connection.cursor() as cursor:
    try:
      search_category_query = 'select name from categories where id = {}'.format(cat_id)
      cursor.execute(search_category_query)
      category_exists = cursor.fetchone() 
      if not category_exists:
        response.status = 404
        response["status__line"] = "category not found"
        error = {"STATUS": "ERROR", "MSG": "category not found"}
        return json.dumps(error)   
      sql = 'DELETE FROM categories WHERE id = "{}"'.format(cat_id)
      cursor.execute(sql)
      connection.commit()
      response.status = 201
      response["status__line"] = "category deleted successfully"
      success = {"STATUS":"The category was deleted successfully"}
      json.dumps(success)

    except Exception as e:
      response.status = 500
      response["status__line"] = "internal Error"
      error = {"STATUS": "ERROR", "MSG": "internal Error"}
      return json.dumps(error)   

@get("/categories")
def get_all_categories():
  with connection.cursor() as cursor:
    try:
      sql = 'SELECT * FROM categories'
      cursor.execute(sql)
      result = cursor.fetchall()
      categories = {"CATEGORIES": result, "STATUS":"Categories fetched"}
      response.status = 200
      response["status__line"] = "Categories fetched"
      return json.dumps(categories)
    except Exception as e:
          error = {"STATUS": "ERROR", "MSG": "inernal error"}
          response.status = 500
          response["status__line"] = "internal error"
          return json.dumps(error)   

# products endpoints
@post("/product")
def add_or_edit_product():
  with connection.cursor() as cursor:
    try:
      # get the prduct id
      
      # missing parameters
      product_column_names = ["category", "desc", "price", "title", "img_url", "id"]
      for key in product_column_names:
        if key not in request.forms.keys():
          response.status = 400
          response["status__line"] = "missing parameters"
          error = {"STATUS": "ERROR", "MSG": "missing parameters"}
          return json.dumps(error)
          
     
      # category not found
      product_category = request.forms.get("category")
      search_category_query = f'select * from categories where id = {product_category}'
      cursor.execute(search_category_query)
      category_exists = cursor.fetchone()
      
      if not category_exists:
        response.status = 404
        response["status__line"] = "Category not found"
        error = {"STATUS": "ERROR", "MSG": "Category not found"}
        return json.dumps(error)
      #  valid the product id
        

      category = request.forms.get("category")
      description = request.forms.get("desc")
      price = request.forms.get("price")
      title = request.forms.get("title")
      favorite = request.forms.get("favorite")
      img_url = request.forms.get("img_url")
      if favorite == "on":
        favorite = 1
      else:
        favorite = 0     
      product_id = request.forms.get("id")
      if product_id == "":
        # creating a new procut          
        create_product_query = "INSERT INTO products (category, description, price, title, favorite, img_url) values('{}','{}',{},'{}',{},'{}')".format(category, description, price,title, favorite,img_url)
        cursor.execute(create_product_query)
        connection.commit()
        success = {"STATUS":"The product was added/updated successfully"} 
        response.status = 201
        response["status__line"] = "The product was added/updated successfully"
        return json.dumps(success)
     
      search_product_query = f'select * from products where id = {product_id}'
      cursor.execute(search_product_query)
      product_exists = cursor.fetchone()         
      if product_exists:  
        update_product_query = "UPDATE products SET category={},description='{}',price={},title='{}',favorite={} ,img_url='{}' where id = {}".format(category, description, price,title, favorite,img_url, product_id)
        cursor.execute(update_product_query)
        connection.commit() 
        success = {"STATUS":"The product was added/updated successfully"} 
        response.status = 201
        response["status__line"] = "The product was added/updated successfully"
        return json.dumps(success)  
    
             
    except Exception as e:
      response.status = 500
      response["status__line"] = "internal Error"
      error = {"STATUS": "ERROR", "MSG": "internal Error"}
      return json.dumps(error)  
   
@get("/product/<id>")
def get_product(id):
  prod_id = id
  with connection.cursor() as cursor:
    try:
      search_category_query = 'select * from products where id = {}'.format(prod_id)
      cursor.execute(search_category_query)
      product_exists = cursor.fetchone() 
      product_exists["favorite"] = convert_bit_to_str(product_exists["favorite"])
      if not product_exists:
        response.status = 404
        response["status__line"] = "product not found"
        error = {"STATUS": "ERROR", "MSG": "product not found"}
        return json.dumps(error)   
      response.status = 200
      response["status__line"] = "The product was fetched successfullyy"
      products = {"PRODUCTS": product_exists, "STATUS":"The product was fetched successfullyy"} 
      return json.dumps(products)
    except Exception as e:
      response.status = 500
      response["status__line"] = "internal Error"
      error = {"STATUS": "ERROR", "MSG": "internal Error"}
      return json.dumps(error) 

@delete("/product/<id>")
def delete_poduct(id):
  prod_id = id
  with connection.cursor() as cursor:
    try:
      search_product_query = 'select * from products where id = {}'.format(prod_id)
      cursor.execute(search_product_query)
      product_exists = cursor.fetchone() 
      if not product_exists:
        response.status = 404
        response["status__line"] = "product not found"
        error = {"STATUS": "ERROR", "MSG": "product not found"}
        return json.dumps(error)   
      sql = 'DELETE FROM products WHERE id = "{}"'.format(prod_id)
      cursor.execute(sql)
      connection.commit()
      response.status = 201
      response["status__line"] = "product deleted successfully"
      success = {"STATUS":"The product was deleted successfully"}
      json.dumps(success)
    except Exception as e:
      response.status = 500
      response["status__line"] = "internal Error"
      error = {"STATUS": "ERROR", "MSG": "internal Error"}
      return json.dumps(error)

@get("/products")
def get_all_products():
  with connection.cursor() as cursor:
    try:
      sql = 'SELECT * FROM products'
      cursor.execute(sql)
      result = cursor.fetchall()
      for product in result:
        product["favorite"] = convert_bit_to_str(product["favorite"])
      products = {"PRODUCTS": result, "STATUS":"Products fetched"}
      response.status = 200
      response["status__line"] = "Products fetched"
      return json.dumps(products)
    except Exception as e:
      response.status = 500
      response["status__line"] = "internal error"
      error = {"STATUS": "ERROR", "MSG": "inernal error"}
      return json.dumps(error)

@get("/category/<id>/products")
def list_products_by_category(id):
  cat_id = id
  with connection.cursor() as cursor:
    try:
      sql = 'SELECT * FROM products where category = {}'.format(cat_id)
      cursor.execute(sql)
      result = cursor.fetchall()
      for product in result:
        product["favorite"] = convert_bit_to_str(product["favorite"])
      products = {"PRODUCTS": result, "STATUS":"Products fetched"}
      response.status = 200
      response["status__line"] = "Products fetched"
      return json.dumps(products)
    except Exception as e:
      response.status = 500
      response["status__line"] = "internal error"
      error = {"STATUS": "ERROR", "MSG": "inernal error"}
      return json.dumps(error)

# index endpoint
@get("/")
def index():
    return template("index.html" )

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

def convert_bit_to_str(bin_bit):
  bit =  str(bin_bit)
  return bit[5]


run(host='localhost', port=argv[1], reloader=True, debug=True)