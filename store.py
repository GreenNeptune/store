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
      connection.commit()
      response.status = 201
      response["status__line"] = "category created successfully"
      success = {"STATUS":"The category was created successfully"}
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
      categories = {"CATEGORIES": result, "STATUS":"The category was created successfully"}

      return json.dumps(categories)
    except Exception as e:
          error = {"STATUS": "ERROR", "MSG": "inernal error"}
          return json.dumps(error)   

# products endpoints
        
#TODO create a error and success messages 
@post("/product")
def add_or_edit_product():
  with connection.cursor() as cursor:
    try:
      product_column_names = ["category", "description", "price", "title", "favorite", "favorite", "img_url", "id"]
      # print(request.json.keys())
       
      for key in request.json.keys():
        if key not in product_column_names:
          return "missing parameters"
      return "200 ok"
      product_id = request.json.get("id")
      search_product_query = f'select * from products where id = {product_id}'
      cursor.execute(search_product_query)
      product_exists = cursor.fetchone()
       
        
      #  valid the product id    
      prod = request.json
      if product_exists:
        # updating a new procut
        update_product_query = "UPDATE products SET category={},description='{}',price={},title='{}',favorite={} ,img_url='{}' where id = {}".format(prod["category"],prod["description"], prod["price"], prod["title"], prod["favorite"],prod["img_url"], prod["id"])
        cursor.execute(update_product_query)
        connection.commit() 
        return "products updated"  
      else:
        # creating a new procut
        create_product_query = "INSERT INTO products (category, description, price, title, favorite, img_url,id)"
        create_product_query += "values({},'{}',{},'{}',{} ,'{}',{})".format(prod["category"],prod["description"], prod["price"], prod["title"], prod["favorite"],prod["img_url"], prod["id"])
        print(create_product_query)
        cursor.execute(create_product_query)
        connection.commit() 
        return "new products created"      
    except Exception as e:
      response.status = 500
      response["status__line"] = "internal Error"
      error = {"STATUS": "ERROR", "MSG": "internal Error", "PRODUCT _ID":product_id}
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
      print(product_exists)
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

def convert_bit_to_str(bin_bit):
  bit =  str(bin_bit)
  return bit[5]


run(host='localhost', port=argv[1], reloader=True, debug=True)
