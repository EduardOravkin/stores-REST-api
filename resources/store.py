from flask_restful import Resource, reqparse
from models.store import StoreModel



class Store(Resource):

    def get(self, name):

        store = StoreModel.find_by_name(name)

        if store:
            return store.json()

        return {"message":"Item not found"}, 404


    def post(self, name):

        if StoreModel.find_by_name(name):
            return {"message":f"A store with name {name} already exists"}

        store = StoreModel(name = name)

        try:
            store.save_to_db()
        except:
            return {'message' : "An error ocurred inserting the store."}, 500 # internal server error

        return store.json(), 201


    def delete(self, name):

        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
            return {"message":"Store successfully deleted"}

        return {"message":"Store was not in the database"}


class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}
