import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT 

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# CRUD api - create read update delete api

app = Flask(__name__)
# SQLAlchemy automatically creates the tables by the following command.

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')

# The command
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
# will not work look here https://stackoverflow.com/questions/66690321/flask-and-heroku-sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy
# to fix it do this:

sql_database_uri = os.environ.get('DATABASE_URL','sqlite:///data.db')
if 'postgres://' in sql_database_uri:
    sql_database_uri = 'postgresql'+sql_database_uri.split('postgres')[-1]

app.config['SQLALCHEMY_DATABASE_URI'] = sql_database_uri


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # new endpoint /auth

api.add_resource(Item, '/item/<string:name>') # passing <string:name> into the get method of Student
api.add_resource(ItemList, '/items') # passing <string:name> into the get method of Student
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


# this is not run by Heroku. Only when running it locally
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port = 5000, debug=True)
