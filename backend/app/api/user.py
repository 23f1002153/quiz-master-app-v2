from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app import db

class MeResource(Resource):
    @jwt_required()
    def get(self):
        identity = int(get_jwt_identity())
        user = User.query.get(identity)

        if not user:
            return {"message": "User not found."}, 404

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }, 200
    
class UpdateProfileResource(Resource):
    @jwt_required()
    def patch(self):
        data = request.get_json()

        identity = int(get_jwt_identity())
        user = User.query.get(identity)

        if not user:
            return {"message": "User not found."}, 404  
        
        if "email" in data:
            user.email = data.get("email")
                                  
        db.session.commit()

        return {"message": "Profile Update Successful"}, 201

def register_user_routes(api):
    api.add_resource(MeResource, '/api/user/me')
    api.add_resource(UpdateProfileResource, '/api/user/update')
