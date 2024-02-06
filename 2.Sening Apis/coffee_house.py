from flask import Flask, request, Response
import json
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Email, Length
# import traceback
from datetime import datetime, timedelta
# from itsdangerous.url_safe import TimedJSONWebSignatureSerializer as Serializer
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
from decimal import Decimal



app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/coffee_house.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)

# ----- DB MODELS -----

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=True)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AuthUser(db.Model):
    __tablename__ = 'auth_users'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    username = db.Column(db.String(255))
    token = db.Column(db.String(255))
    api_key = db.Column(db.String(255))
    banana = db.Column(db.String(10), default='banana')
    please = db.Column(db.String(10), default='please')
    X_DIRECTIVE_STUFF = db.Column(db.String(255))
    expires = db.Column(db.Date)

class UsedCoffee(db.Model):
    __tablename__ = 'used_coffee'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    buyerId = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(255))
    brand = db.Column(db.String(50), default='NO BRAND')
    description = db.Column(db.Text)
    image_link = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2))
    pct_left = db.Column(db.Integer)
    purchase_date = db.Column(db.String(100))
    sold = db.Column(db.Boolean, default=False)
    def to_dict(self):
        return {c.name: float(getattr(self, c.name)) if isinstance(getattr(self, c.name), Decimal) else getattr(self, c.name) for c in self.__table__.columns}

# To clear everything from database
# db.drop_all()
# After defining your models and before starting your application // only create models that is not already created
db.create_all()

# ----- AUTH MIDDLEWARE -----
def authenticate(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        abort(401)
    return user

def authenticateAdmin(who_is_the_boss):
    if who_is_the_boss != 'IAMTHEBOSS':
        return False
    return True


@app.route('/')
def home():
    return app.send_static_file('./index.html')


# -----VALIDATION----

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(message="Username is required."),
        Length(min=3, max=50, message="Username must be between 3 and 50 characters.")
    ])
    email = StringField('Email', validators=[
        InputRequired(message="Email is required."),
        Email(message='Invalid email.'),
        Length(max=50, message="Email must be less than 50 characters.")
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message="Password is required."),
        Length(min=6, max=80, message="Password must be between 6 and 80 characters.")
    ])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        InputRequired(message="Email is required."),
        Email(message='Invalid email.'),
        Length(max=50, message="Email must be less than 50 characters.")
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message="Password is required."),
        Length(min=6, max=80, message="Password must be between 6 and 80 characters.")
    ])

# ----- ROUTES AND CONTROLLERS

# @desc Create New User
# @route POST /api/v1/auth/register
# @access Public
@app.route('/api/v1/auth/register', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        form = RegistrationForm(data=data)
        if form.validate():
            new_user = User(username=data['username'], email=data['email'], password=data['password'])
            new_user.set_password(data['password'])
            db.session.add(new_user)
            db.session.commit()
            data = {"message": "User created", "user": {"username": new_user.username, "email": new_user.email, "hashed_password": new_user.password}}
            return Response(json.dumps(data), status=200, mimetype='application/json')
        else:
            # form is not valid, return errors
            return Response(json.dumps(form.errors), status=400, mimetype='application/json')
    except IntegrityError:
        error = {"message": "Email already exists"}
        return Response(json.dumps(error), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": str(e)}), status=500, mimetype='application/json')


# @desc Login User
# @route POST /api/v1/auth/login
# @access Public
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        form = LoginForm(data=data)

        if form.validate():
            user = User.query.filter_by(email=data['email']).first()
            if user and user.check_password(data['password']):
                auth_user = AuthUser.query.filter_by(userId=user.id).first()
                if auth_user is None:
                    auth_user = AuthUser(userId=user.id, username=user.username)
                    db.session.add(auth_user)
                auth_user.token = shortuuid.uuid()
                auth_user.X_DIRECTIVE_STUFF = shortuuid.uuid()
                auth_user.api_key = shortuuid.uuid()  # Replace with your actual API key generation logic
                auth_user.expires = datetime.utcnow() + timedelta(seconds=7200)
                db.session.commit()

                auth_user_data = {
                    "username": auth_user.username,
                    "token": auth_user.token,
                    "api_key": auth_user.api_key,
                    "banana": auth_user.banana,
                    "X_DIRECTIVE_STUFF": auth_user.X_DIRECTIVE_STUFF,
                    "please": auth_user.please,
                }

                return Response(json.dumps({"message": "logged in successfully", "data": auth_user_data}), status=200, mimetype='application/json')
            else:
                error = {"message": "Invalid username or password"}
                return Response(json.dumps(error), status=400, mimetype='application/json')
        else:
            # form is not valid, return errors
            return Response(json.dumps(form.errors), status=400, mimetype='application/json')
    except Exception as e:
        # print(str(e))
        # traceback.print_exc()
        return Response(json.dumps({"message": str(e)}), status=500, mimetype='application/json')

# @desc Get All Users
# @route GET /api/v1/users
# @access Private/Admin

@app.route('/api/v1/users', methods=['GET'])
def get_all_users():
    # print(request.headers)
    isBoss = authenticateAdmin(request.headers.get('who-is-the-boss'))
    if not isBoss:
        error = {"message": "Your not my boss", "header": request.headers.get('who-is-the-boss')}
        return Response(json.dumps(error), status=401)
    if request.headers.get('banana') != 'banana':
        error = {"message": "no banana, no data", "header": request.headers.get('banana')}
        return Response(json.dumps(error), status=400)
    users = User.query.all()
    if not users:
        error = {"message": "Users not found"}
        return Response(json.dumps(error), status=404)
    users_data = [user.to_dict() for user in users]
    data = {"message":"here you go boss, thanks for banana", "data": users_data}
    return Response(json.dumps(data), status=200)

# @app.route('/happy', methods=['POST'])
# def happy():
#     data = {"message": "User created"}
#     return Response(json.dumps(data), status=200)

# @app.route('/happy', methods=['POST'])
# def happy():
#     data = {"message": "User created"}
#     return Response(json.dumps(data), status=200)




# @desc Get Single User
# @route GET /api/v1/users/<id>
# @access Private/Admin
@app.route('/api/v1/users/<int:id>', methods=['GET'])
def get_user(id):
    # print(request.headers)
    isBoss = authenticateAdmin(request.headers.get('who-is-the-boss'))
    if not isBoss:
        error = {"message": "Your not my boss", "header": request.headers.get('who-is-the-boss')}
        return Response(json.dumps(error), status=401)

    user = User.query.get(id)
    if user is None:
        error = {"message": "User Id does not exist"}
        return Response(json.dumps(error), status=404)
    data = {"user": {"id": user.id, "username": user.username, "email": user.email}}
    return Response(json.dumps(data), status=200)



# @desc Create used coffee post
# #route POST /api/v1/used-coffee
# Private

class UsedCoffeeForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message ="Please provide name")])
    description = StringField('Description', validators=[InputRequired(message ="Please provide description")])
    price = DecimalField('Price', validators=[InputRequired(message ="Please provide price")])
    pct_left = IntegerField('Pct_left', validators=[InputRequired(message = "Please provide pct_left")])
    purchase_date = StringField('Purchase_date', validators=[InputRequired(message = "Please provide purchase_date")])
    sold = BooleanField('Sold', default=False)

@app.route('/api/v1/used-coffee', methods=['POST'])
def create_used_coffee():
    try:
        if not request.headers.get('token'):
            error = {"message": "no token provided", "token": request.headers.get('token')}
            return Response(json.dumps(error), status=400)
        if request.headers.get('please') != 'please':
            error = {"message": "What is the magic word?", "please": request.headers.get('please')}
            return Response(json.dumps(error), status=400)
        # Get the token from the token header
        token = request.headers.get('token').split(' ')[1]


        # Check if the token exists in the auth_users table
        user = AuthUser.query.filter_by(token=token).first()
        if not user:
            return Response(json.dumps({"message": "No user with token provided"}), status=401, mimetype='application/json')

        data = request.get_json()
        form = UsedCoffeeForm(data=data)
        form = UsedCoffeeForm(data=data)
        if form.validate():
            new_coffee = UsedCoffee(
                userId=user.userId,
                name=data['name'],
                description=data['description'],
                price=data['price'],
                pct_left=data['pct_left'],
                purchase_date=data['purchase_date'],
                sold=False,
                brand=data.get('brand', 'NO BRAND'),  # use the provided brand or 'Default Brand' if not provided
                image_link=data.get('image_link', '')  # use the provided image_link or 'Default Image Link' if not provided
            )
            db.session.add(new_coffee)
            db.session.commit()
            data = {"message": "Your used coffee could be someone else's treasure! Thank you for your post!", "data": new_coffee.to_dict()}
            return Response(json.dumps(data), status=200, mimetype='application/json')
        else:
            # form is not valid, return errors
            return Response(json.dumps(form.errors), status=400, mimetype='application/json')
    except IntegrityError:
        error = {"message": "Coffee already exists"}
        return Response(json.dumps(error), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": str(e)}), status=500, mimetype='application/json')


# @desc Get Users coffee posts
# @route GET /api/v1/used-coffee/my
# @access Private/Post Owner

@app.route('/api/v1/used-coffee/my', methods=['GET'])
def get_all_users_used_coffee():
    try:
        # Get the headers
        username = request.headers.get('username')
        api_key = request.headers.get('api-key')
        banana = request.headers.get('banana')

        # Check if all required headers are provided
        if not banana:
            return Response(json.dumps({"message": "no banana, no data"}), status=400, mimetype='application/json')

        # Check if the username and api-key exist in the auth_users table
        user = AuthUser.query.filter_by(username=username, api_key=api_key).first()
        if not user:
            return Response(json.dumps({"message": "Username or Api key is incorrect"}), status=401, mimetype='application/json')

        # Get the user's coffee posts
        user_coffee_posts = UsedCoffee.query.filter_by(userId=user.userId).all()
        # print('USER_COFFEES', user_coffee_posts)  # print the user_coffee_posts list for debugging
        # Convert the posts to dictionaries and return them
        data = {"message": "Here you go!", "userId":user.userId, "data": [post.to_dict() for post in user_coffee_posts]}
        return Response(json.dumps(data), status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": str(e)}), status=500, mimetype='application/json')


# @desc Get All coffee posts
# @route GET /api/v1/used-coffee
# @access Public

@app.route('/api/v1/used-coffee', methods=['GET'])
def get_all_used_coffee():
    try:
        # Get all coffee posts
        all_coffee_posts = UsedCoffee.query.all()
        # print('ALL_COFFEES', all_coffee_posts)  # print the all_coffee_posts list for debugging

        # Convert the posts to dictionaries and return them
        data = {"message": "British scientists say that used coffee is good for environment.", "data": [post.to_dict() for post in all_coffee_posts]}
        return Response(json.dumps(data), status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": str(e)}), status=500, mimetype='application/json')


# @desc Get Single coffee posts
# @route GET /api/v1/used-coffee/:id
# @access Public

@app.route('/api/v1/used-coffee/<int:id>', methods=['GET'])
def get_single_used_coffee(id):
    try:
        # Get the used coffee post
        used_coffee_post = UsedCoffee.query.get(id)

        # Check if the post exists
        if not used_coffee_post:
            return Response(json.dumps({"message": "Used Coffee Id does not exist"}), status=404, mimetype='application/json')

        # Convert the post to a dictionary and return it
        data = {"message": "Good Choice! Place Order now and regret later!", "data": used_coffee_post.to_dict()}
        return Response(json.dumps(data), status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": str(e)}), status=500, mimetype='application/json')


# @desc Update coffee posts
# @route GET /api/v1/used-coffee/:id
# @access Private

@app.route('/api/v1/used-coffee/<int:id>', methods=['PUT'])
def update_used_coffee(id):
    try:
        # Check headers
        X_DIRECTIVE_STUFF = request.headers.get('X-DIRECTIVE-STUFF')
        please = request.headers.get('please')
        if not please:
            error = {"message": "What is the magic word?",}
            return Response(json.dumps(error), status=401, mimetype='application/json')
        user = AuthUser.query.filter_by(X_DIRECTIVE_STUFF=X_DIRECTIVE_STUFF).first()
        if not user:
            return Response(json.dumps({"message": "X-DIRECTIVE-STUFF is incorrect", user:user}), status=401, mimetype='application/json')

        # Get the used coffee post
        used_coffee_post = UsedCoffee.query.get(id)

        if used_coffee_post.userId != user.userId:
            return Response(json.dumps({"message": "It is not your used coffee, hands off", "owner_id": used_coffee_post.userId, "your_id": user.userId}), status=401, mimetype='application/json')


        # Check if the post exists
        if not used_coffee_post:
            return Response(json.dumps({"message": "Used Coffee Id does not exist"}), status=404, mimetype='application/json')

        # Get the request data
        data = request.get_json()
        if not data:
            return Response(json.dumps({"message": "no new data has been provided in body"}), status=400, mimetype='application/json')
        # Validate the data using the form - all fields are optional in update as used coffee has been created
        # form = UsedCoffeeForm(data=data)
        # if not form.validate():
            # return Response(json.dumps(form.errors), status=400, mimetype='application/json')

        # Check if trying to modify 'sold' field
        if 'sold' in data and data['sold'] == True:
            return Response(json.dumps({"message": "sold field cannot be modified"}), status=400, mimetype='application/json')

        # Update the post
        used_coffee_post.name = data.get('name', used_coffee_post.name)
        used_coffee_post.description = data.get('description', used_coffee_post.description)
        used_coffee_post.price = data.get('price', used_coffee_post.price)
        used_coffee_post.pct_left = data.get('pct_left', used_coffee_post.pct_left)
        used_coffee_post.purchase_date = data.get('purchase_date', used_coffee_post.purchase_date)
        used_coffee_post.brand = data.get('brand', used_coffee_post.brand)
        used_coffee_post.image_link = data.get('image_link', used_coffee_post.image_link)

        # Save the changes
        db.session.commit()

        # Return the updated post
        return Response(json.dumps({"message": "GREAT SUCCESS!", "data": used_coffee_post.to_dict()}), status=200, mimetype='application/json')
    except IntegrityError:
        return Response(json.dumps({"message": "Coffee already exists"}), status=400, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": str(e)}), status=500, mimetype='application/json')

# @desc Update coffee posts
# @route GET /api/v1/used-coffee/:id
# @access Private



@app.route('/api/v1/used-coffee/buy/<int:id>', methods=['PATCH'])
def buy_used_coffee(id):
    try:
        # Check headers
        username = request.headers.get('username')
        api_key = request.headers.get('api-key')
        X_DIRECTIVE_STUFF = request.headers.get('X-DIRECTIVE-STUFF')

        user = AuthUser.query.filter_by(username=username, api_key=api_key).first()
        if not user:
            return Response(json.dumps({"message": "Username or Api key is incorrect"}), status=401, mimetype='application/json')

        if X_DIRECTIVE_STUFF != user.X_DIRECTIVE_STUFF:
            return Response(json.dumps({"message": "X_DIRECTIVE_STUFF is incorrect"}), status=401, mimetype='application/json')

        # Get the used coffee post
        used_coffee_post = UsedCoffee.query.get(id)

        if used_coffee_post.userId == user.userId:
            return Response(json.dumps({"message": "cannot buy your own used coffee. C'mon, I had more expectations from people who buy used coffee!"}), status=401, mimetype='application/json')

        if used_coffee_post.sold:
            return Response(json.dumps({"message": "cannot buy this coffee, someone else already got the best deal of his life!"}), status=400, mimetype='application/json')

        # Get the request data
        # data = request.get_json()

        # Update the post
        used_coffee_post.sold = True
        used_coffee_post.buyerId = user.userId


        # Save the changes
        db.session.commit()

        # Return the updated post
        return Response(json.dumps({"message": "Sit, relax and enjoy your used coffee! ", "data": used_coffee_post.to_dict()}), status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": str(e)}), status=500, mimetype='application/json')




# @desc Delete coffee post
# @route GET /api/v1/used-coffee/:id
# @access Private



@app.route('/api/v1/used-coffee/<int:id>', methods=['DELETE'])
def delete_used_coffee(id):
    try:
        # Check headers
        token = request.headers.get('token')
        banana = request.headers.get('banana')
        if not banana:
            error = {"message": "no banana, no delete",}
            return Response(json.dumps(error), status=401, mimetype='application/json')
        if not token:
            error = {"message": "no token provided", "token": request.headers.get('token')}
            return Response(json.dumps(error), status=401, mimetype='application/json')

        # Get the token from the token header
        token = request.headers.get('token').split(' ')[1]


        # Check if the token exists in the auth_users table
        user = AuthUser.query.filter_by(token=token).first()
        if not user:
            return Response(json.dumps({"message": "unauthorized to delete this masterpiece"}), status=401, mimetype='application/json')

        # Get the used coffee post
        used_coffee_post = UsedCoffee.query.get(id)

        if used_coffee_post.userId != user.userId:
            return Response(json.dumps({"message": "it is not your used coffee, hands off!"}), status=401, mimetype='application/json')

        # Check if the post exists
        if not used_coffee_post:
            return Response(json.dumps({"message": "Used Coffee Id does not exist"}), status=404, mimetype='application/json')

        # Delete the post
        db.session.delete(used_coffee_post)
        db.session.commit()

        # Return the deleted post
        return Response(json.dumps({"message": "Noooooo! What have you done! Used Coffee post deleted. I am sad. ", "data": used_coffee_post.to_dict()}), status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": str(e)}), status=500, mimetype='application/json')