from flask import request
from flask_restful import Resource
from app.models import User
from app import db
from flask_jwt_extended import create_access_token
from datetime import timedelta

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return {"message": "Username, email, and password are required."}, 400

        # Check if user already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return {"message": "Username or email already exists."}, 409

        user = User(username=username, email=email, role='user')
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully."}, 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": "Username and password are required."}, 400

        user = User.query.filter_by(username=username).first()

        if user:
            print("User ID:", user.id, type(user.id))

        if not user or not user.check_password(password):
            return {"message": "Invalid credentials."}, 401

        # Create access token (valid for 1 hour)
        access_token = create_access_token(
            identity=str(user.id),  
            additional_claims={"role": user.role},  # extra info
            expires_delta=timedelta(hours=1)
        )

        return {
            "message": "Login successful.",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        }, 200

# Register API resources
def register_auth_routes(api):

    api.add_resource(RegisterResource, '/api/auth/register')
    api.add_resource(LoginResource, '/api/auth/login')