import jwt
from functools import wraps
from flask import Flask, request

from db import db_session, init_db, add_user
import auth

init_db()

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/auth/register/', methods=['POST'])
def register():
    try:
        if add_user(request.json['username'], request.json['password']):
            return {'message': 'Registration successful'}, 201
        else:
            return {'message': 'Username taken'}, 403
    except KeyError:
        return {'message': 'Registration failed'}, 400


@app.route('/auth/login/', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
    except KeyError:
        return {'message': 'Login failed'}, 400

    token = auth.login(username, password)

    if token is False:
        return {'message': 'Login failed'}, 400

    return {'message': 'Login successful', 'token': token.decode('utf-8')}


def login_required(f):
    @wraps(f)
    def decorated_f(*args, **kwargs):
        try:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1]

            auth.verify_token(token)
        except (KeyError, IndexError, jwt.InvalidTokenError):
            # invalid token
            return {'message': 'Access denied'}, 403

        # valid token, continue to route
        return f(*args, **kwargs)

    return decorated_f


@app.route('/protected/')
@login_required
def protected():
    return {"message": "Nudes here"}


app.run()
