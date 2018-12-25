from bottle import route, run, template, static_file, get, post, delete, request, redirect
from sys import argv
import json
import pymysql


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/categories")
def index():
    return template("index.html")


@route('/')
def handle_root_url():
    redirect("/categories")


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
    name = request.forms.get("name")
    return name


run(host='localhost', port=7000)
#run(host='0.0.0.0', port=argv[1])
