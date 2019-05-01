from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="this field cannot be blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="this field cannot be blank")

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "the user already exist"}, 400

        else:
            user = UserModel(**data) # **data = data['username'],data['password']
            user.save_to_db()
            return {"message": "User created successfully"}, 201

class GetUsers(Resource):
    def get(self):
        return {'Users':[item.json() for item in UserModel.query.all()]}



