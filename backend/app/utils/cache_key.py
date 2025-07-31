from flask import request
from flask_jwt_extended import get_jwt

def role_based_cache_key():
    try:
        path = request.path
        role = get_jwt().get("role", "guest")
        return f"{path}|{role}"
    except Exception:
        return "default"