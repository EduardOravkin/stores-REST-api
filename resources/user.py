import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    for i in ["username", "password"]:
        parser.add_argument(i,
                            type=str,
                            required = True,
                            help = "This field is required"
                            )


    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]) is not None:
            return {"message": f'A user with username {data["username"]} already exists'}, 409

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201

    def get(self):
        return {'register': [user.json() for user in UserModel.query.all()]}
