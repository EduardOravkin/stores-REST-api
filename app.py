from flask import Flask
from flask_restful import Api
from flask_jwt import JWT #json w token (obfuscation of data)

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

# CRUD api - create read update delete api (most apis out there)

app = Flask(__name__)
# SQLAlchemy automatically creates the tables by the following command.
# Note it only creates the tables that it sees. It creates the table stores because
# it imports the Store Resource which imports the StoreModel which tells it
# to create the table 'stores'.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # switches off some changes tracker
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # new endpoint /auth

api.add_resource(Item, '/item/<string:name>') # passing <string:name> into the get method of Student
api.add_resource(ItemList, '/items') # passing <string:name> into the get method of Student
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# Finally understood why people use __name__ == '__main__' thing.
# Because if you are in another_file.py and you do import app,
# then Python automatically runs all of the code (e.g. if you have a print()
# there). if __name__ == '__main__' makes sure that this isn't run when
# importing app.py
if __name__ == '__main__':
    db.init_app(app)
    app.run(port = 5000, debug=True) #debug=True gives nice debug messages
