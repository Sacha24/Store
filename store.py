from bottle import run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql


connection = pymysql.connect(host="localhost",
                             user="root",
                             password="rebecca09",
                             db="Store",
                             charset="utf8",
                             cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@post("/category")
def create_category():
    try:
        with connection.cursor() as cursor:
            newCatName = request.forms.get("name")
            if len(newCatName) == 0:
                return json.dumps({"STATUS": "ERROR", "MSG": "Name parameter is missing"})
            sql = "INSERT INTO Categories (name) VALUES ('{}')".format(newCatName)
            cursor.execute(sql)
            connection.commit()
            catId = cursor.lastrowid
            return json.dumps({"STATUS": "SUCCESS", "MSG": "The category was successfully created", "CAT_ID": catId})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": str(e)})


@delete("/category/<catId>")
def delete_category(catId):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM Categories WHERE id = {}".format(catId)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "The category was successfully deleted"})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": str(e)})


@get("/categories")
def load_categories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Categories"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "CATEGORIES": result})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": str(e)})


@post("/product")
def create_edit_product():
    try:
        with connection.cursor() as cursor:
            catId = request.forms.get("category")
            product_name = request.forms.get("title")
            price = request.forms.get("price")
            desc = request.forms.get("desc")
            img = request.forms.get("img_url")

            favorite = request.forms.get("favorite")
            if favorite == "on":
                favorite = True
            else:
                favorite = False

            sql1 = "INSERT INTO Products (title, description, price, img_url, category, favorite) "
            sql2 = "VALUES ('{}', '{}', {}, '{}', {}, {})".format(product_name, desc, price, img, catId, favorite)
            cursor.execute(sql1 + sql2)
            connection.commit()
            return json.dumps({'STATUS': 'SUCCESS', 'MSG': 'The product was added/updated successfully'})
    except:
        try:
            with connection.cursor() as cursor:
                catId = request.forms.get("category")
                product_name = request.forms.get("title")
                price = request.forms.get("price")
                desc = request.forms.get("desc")
                img = request.forms.get("img_url")

                favorite = request.forms.get("favorite")
                if favorite == 'on':
                    favorite = True
                else:
                    favorite = False

                sql1 = "UPDATE Products SET description='{}', price={}, img_url='{}', category={}, favorite={} ".format(desc, price, img, catId, favorite)
                sql2 = "WHERE title='{}'".format(product_name)
                cursor.execute(sql1 + sql2)
                connection.commit()
                return json.dumps({"STATUS": "SUCCESS", "MSG": "The product was updated successfully !"})
        except Exception as e:
            return json.dumps({"STATUS": "ERROR", "MSG": str(e)})


@get("/product/<id>")
def get_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Products WHERE id = {}".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCT": result})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": str(e)})


@delete("/product/<id>")
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM Products WHERE id = {}".format(id)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": "The product was deleted successfully"})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": str(e)})


@get('/products')
def load_products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Products"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result})
    except Exception as e:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": str(e)})


@get('/category/<id>/products')
def list_products_by_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Products WHERE id = {} ORDER BY favorite DESC, id ASC".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result})
    except Exception as e:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": str(e)})


run(host='localhost', port=7000)
#run(host='0.0.0.0', port=argv[1])
