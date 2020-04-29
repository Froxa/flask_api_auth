import jwt
import secrets
from werkzeug.security import check_password_hash

from db import get_users

SECRET_KEY = secrets.token_urlsafe(32)


def login(username, password):
    u = get_users().filter_by(username=username).first()

    if u is None:
        return False

    if not check_password_hash(u.password, password):
        return False

    return jwt.encode({'uid': u.id, 'uname': username}, SECRET_KEY)


def verify_token(token):
    return jwt.decode(token, SECRET_KEY)

