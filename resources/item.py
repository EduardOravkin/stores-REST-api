from flask_restful import Resource, reqparse
from flask_jwt  import JWT, jwt_required
from models.item import ItemModel

class Item(Resource):

    @jwt_required()
    def get(self, name): # i.e. accessible by a get request

        item = ItemModel.find_by_name(name)

        if item:
            return item.json()

        return {"message":"Item not found"}, 404

    def post(self, name):

        #can do both self.find_by_name or Item.find_by_name as it's a class method
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name {name} already exists"}, 409 # status code 409 means conflict, 400 means bad request

        # the parser makes sure that only the price is updated
        # and no other field
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help="This field cannot be left blank!"
                            )
        parser.add_argument('store_id',
                            type=int,
                            required=True,
                            help="This field cannot be left blank!"
                            )
        data = parser.parse_args()

        item = ItemModel(name = name, price = data['price'], store_id = data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message' : "An error ocurred inserting the item."}, 500 # internal server error

        return item.json(), 201


        #item = next(filter(lambda x: x['name']==name, items), None)

        #if item is not None:
        #    return {'message': f"An item with name {name} already exists"}, 400 # status code 409 means conflict, 400 means bad request
        #else:
        #    item = {k:data[k] for k in data.keys()}
        #    item['name'] = name
        #    items.append(item)
        #    return {'item' : item }, 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "item deleted"}
        else:
            return {"message" : "item not found"}

    def put(self, name): # should be idempotent (applied twice is same as applied once)
        # the parser makes sure that only the price is updated
        # and no other field
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help="This field cannot be left blank!"
                            )
        data = parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name = name, price = data['price'], store_id = data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        return {"items":[item.json() for item in ItemModel.query.all()]}
