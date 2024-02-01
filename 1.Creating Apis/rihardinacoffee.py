
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, Response
import json
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/coffee_house.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=True)

def authenticate(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        abort(401)
    return user

def authenticateAdmin(who_is_the_boss):
    if who_is_the_boss != 'IAMTHEBOSS':
        return False
    return True

@app.route('/', methods=['GET'])
def home():
    return "Hi there"

@app.route('/foo', methods=["POST"])
def foo_page():
    # req_data = request.get_json()
    # message = req_data['message']
    # send_email(message)
    return Response(status=200)

# @desc Create New User
# @route POST /api/v1/users
# @access Public
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        new_user = User(username=data['username'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        data = {"message": "User created", "user": {"username": new_user.username, "email": new_user.email}}
        return Response(json.dumps(data), status=200)
    except IntegrityError:
        error = {"error": "Email already exists"}
        return Response(json.dumps(error), status=400)
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500)
        # return jsonify({"error": str(e)}), 500

# @desc Get Single User
# @route GET /api/v1/users/<id>
# @access Public
@app.route('/api/v1/users/<int:id>', methods=['GET'])
def get_user(id):
    print(request.headers)
    isBoss = authenticateAdmin(request.headers.get('who-is-the-boss'))
    if not isBoss:
        error = {"error": "Your not my boss", "header": request.headers.get('who-is-the-boss')}
        return Response(json.dumps(error), status=404)
    user = User.query.get(id)
    if user is None:
        error = {"error": "User not found"}
        return Response(json.dumps(error), status=404)
    data = {"user": {"id": user.id, "username": user.username, "email": user.email}}
    return Response(json.dumps(data), status=200)

@app.route('/happy', methods=['POST'])
def happy():
    data = {"message": "User created"}
    return Response(json.dumps(data), status=200)
