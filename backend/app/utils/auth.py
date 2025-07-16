from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import jsonify, make_response

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != required_role:
                return make_response(jsonify({"message": "Access denied"}), 403)
            return fn(*args, **kwargs)
        return decorator
    return wrapper
