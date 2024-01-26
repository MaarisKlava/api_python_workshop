from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee_house.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password",)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def authenticate(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        abort(401)
    return user

def authenticateAdmin(who_is_the_boss):
    if who_is_the_boss != 'IAMTHEBOSS':
        abort(401)
    return True

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user), 201
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    try:
        authenticate(request.headers.get('api_username'), request.headers.get('api_key'))
        authenticateAdmin(request.headers.get('who_is_the_boss'))
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result) , 200
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/api/v1/users/<id>', methods=['GET'])
def get_user(id):
    try:
        authenticate(request.headers.get('api_username'), request.headers.get('api_key'))
        authenticateAdmin(request.headers.get('who_is_the_boss'))
        user = User.query.get(id)
        return user_schema.jsonify(user), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/api/v1/users/<id>', methods=['PATCH'])
def update_user(id):
    try:
        user = authenticate(request.headers.get('api_username'), request.headers.get('api_key'))
        if user.id != int(id):
            abort(403)
        password = request.json['password']
        user.password = password
        db.session.commit()
        return user_schema.jsonify(user), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/api/v1/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        authenticate(request.headers.get('api_username'), request.headers.get('api_key'))
        authenticateAdmin(request.headers.get('who_is_the_boss'))
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return user_schema.jsonify(user), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)




# PUBLIC CODE ALLOWED

# Please Create Flask with all routes + SQLite project (coffee_house.db) every route needs to be async
# it is demo project for training, could you avoid password hashing
# authentication will be sent through headers api_username and api_key for Protected routes. Protected/Admin routes should have additional header 'who_is_the_boss': "IAMTHEBOSS";
# invoke error if some @throwError column criteria is true
# could you please add try catch blocks to all routes

# #Users schema:
# data will be sent in request body.
# field unique type automatically assigned by computer default value
# userId true int true -
# username false string false -
# email true string false -
# password false string false -

# #User Routes And Controller Setup:
# before each route in code, please document it accordingly like this, IMPORTANT!:

# ```py
# # @desc Create New User
# # @route POST /api/v1/users
# # @access Public
# def create_user():
#     try:
#       ....
#     except Exception as e:
#         return jsonify(error=str(e)), 400
# ```

# | @desc                 | @route                       | @access       | @throwError                                                                                                                                                                                                                                     | @OK                                                              |
# | --------------------- | ---------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
# | Create New User       | POST /api/v1/users           | Public        | email exists; server crashes                                                                                                                                                                                                                    | json with message - user created and data without password       |
# | Get All Users         | GET /api/v1/users            | Private/Admin | need header 'api_username': "username" and "api_key":'password' and both matches db entries; needs header 'who_is_the_boss': "IAMTHEBOSS"; if server crashes                                                                                    | json with all users data                                         |
# | Get Single User       | GET /api/v1/users/:userId    | Private/Admin | need header 'api_username': "username" and "api_key":'password' and both matches db entries; needs header 'who_is_the_boss': "IAMTHEBOSS"; if server crashes; userId does not exist                                                             | json with single users data                                      |
# | Update Users Password | PATCH /api/v1/users/:userId  | Private       | need header 'api_username': "username" and "api_key":'password' and both matches db entries; needs header 'who_is_the_boss': "IAMTHEBOSS"; if server crashes; userId does not exist; password and confirmPassword fields in body does not match | json with message - user updated successfully and new users data |
# | Delete A User         | DELETE /api/v1/users/:userId | Private/Admin | need header 'api_username': "username" and "api_key":'password' and both matches db entries; needs header 'who_is_the_boss': "IAMTHEBOSS"; if server crashes; userId does not exist                                                             | json with message - user deleted successfully                    |

# Please use these formulas to authenticate protected routes accordingly
# def authenticate(username, password):
# user = User.query.filter_by(username=username, password=password).first()
# if user is None:
# abort(401)
# return user

# def authenticateAdmin(who_is_the_boss):
# if who_is_the_boss != 'IAMTHEBOSS':
# abort(401)
# return True
