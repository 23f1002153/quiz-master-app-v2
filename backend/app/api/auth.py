from flask import request
from flask_restful import Resource
from app.models import User
from app import db
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app.utils.validators import *
from app.utils.formatters import format_date
from datetime import datetime

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        gender = data.get("gender")
        dob = data.get("dob")
        qualification = data.get("qualification")
        college = data.get("college")
        phone = data.get("phone")

        error  = (validate_string(username, 'username') or
                  validate_email(email) or 
                  validate_date(dob, before_today=True) or 
                  validate_gender(gender) or
                  validate_phone(phone) or
                  validate_string(college, 'college') or
                  validate_string(qualification, 'qualification') or
                  validate_password(password)
                )
        if error:
            return {"message": error}, 422
                
        # Check if user already exists
        if User.query.filter((User.username == username)).first():
            return {"message": "Username already exists."}, 409
        
        # Check if email already exists
        if User.query.filter((User.email == email)).first():
            return {"message": "Email already exists."}, 409
        
        # Check if phone already exists
        if User.query.filter((User.phone == phone)).first():
            return {"message": "Phone number already exists."}, 409
        
        user = User(username=username.strip(), 
                    email=email.strip(),
                    gender = gender.strip(),
                    dob = format_date(dob),
                    qualification = qualification.strip(),
                    college = college.strip(),
                    phone = int(phone),
                    role='user')
        
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

        if not user or not user.check_password(password):
            return {"message": "Invalid username or password"}, 401

        user.last_login = datetime.now()
        db.session.commit()

        # Create access token (valid for 1 hour)
        access_token = create_access_token(
            identity=str(user.id),  
            additional_claims={"role": user.role},  # extra info
            expires_delta=timedelta(hours=10)
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