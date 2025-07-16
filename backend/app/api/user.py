from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app import db
from app.utils.validators import*
from app.utils.formatters import format_date
class MeResource(Resource):
    @jwt_required()
    def get(self):
        identity = int(get_jwt_identity())
        user = User.query.get(identity)

        if not user:
            return {"message": "User not found."}, 404

        return user.to_dict(), 200
    
class UpdateProfileResource(Resource):
    @jwt_required()
    def patch(self):
        identity = int(get_jwt_identity())
        user = User.query.get(identity)

        if not user:
            return {"message": "User not found."}, 404  
        
        data = request.get_json()

        email = data.get("email")
        gender = data.get("gender")
        dob = data.get("dob")
        qualification = data.get("qualification")
        college = data.get("college")
        phone = data.get("phone")

        if not(email) and not(gender) and not(dob) and not(qualification) and not(college):
            return {"message": "Invalid request. Nothing to update"}, 422            

        # Check if email is being changed and is already taken
        if email:
            error = validate_email(email)
            if error:
                return {"message": error}, 422
            existing = User.query.filter_by(email=email).first()
            if existing and existing.id != user.id:
                return {"message": "Email already in use."}, 409  # Conflict
            user.email = email

        if gender:
            error = validate_gender(gender)
            if error:
                return {"message": error}, 422
            user.gender = gender

        if dob:
            error = validate_date(dob)
            if error:
                return {"message": error}, 422
            user.dob = format_date(dob)
            
        if qualification:
            error = validate_string(qualification, 'qualification')
            if error:
                return {"message": error}, 422
            user.qualification = qualification.strip()

        if college:
            error = validate_string(college, 'college')
            if error:
                return {"message": error}
            user.college = college.strip()

        # Check if phone is being changed and is already taken
        if phone:
            error = validate_phone(phone)
            if error:
                return {"message": error}, 422
            existing = User.query.filter_by(phone=phone).first()
            if existing and existing.id != user.id:
                return {"message": "Phone Number already in use."}, 409  # Conflict
            user.phone = int(phone)

        db.session.commit()

        return {"message": "Profile Updated Successfully"}, 200

class UpdatePasswordResource(Resource):
    @jwt_required()
    def patch(self):
        identity = int(get_jwt_identity())
        user = User.query.get(identity)

        if not user:
            return {"message": "User not found."}, 404 
        
        data = request.get_json()
        
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not(old_password) or not(new_password):
            return {"message": "Invalid Format"}, 422
        
        if user.check_password(old_password):
            error = validate_password(new_password)
            if error:
                return {"message": error}, 422
            if old_password == new_password:
                return {"message": "Password cannot be same"}, 400
            user.set_password(new_password)
            db.session.commit()
            return {"message": "Password Updated Successfully"}, 200
        else:
            return {"message": "Old Password does not match"}, 401 # Unauthorized


def register_user_routes(api):
    api.add_resource(MeResource, '/api/users/me')
    api.add_resource(UpdateProfileResource, '/api/users/update-profile')
    api.add_resource(UpdatePasswordResource, '/api/users/update-password')
    
