from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Subject
from app import db, cache
from datetime import datetime
from app.utils.auth import role_required
from app.utils.validators import validate_string
class SubjectResource(Resource):

    @cache.cached(timeout=3600)
    @jwt_required()
    def get(self, subject_id):

        subject = Subject.query.filter_by(id = subject_id).first()
        if not(subject):
            return {"message": f"Subject with id {subject_id} not found"}, 404
        
        user = get_jwt()
        if user.get("role") == 'admin':
            return subject.to_dict(include_internal = True), 200
        else:
            return subject.to_dict(), 200
    
    @role_required('admin')
    def patch(self, subject_id):

        data = request.get_json()

        subject = Subject.query.filter_by(id = subject_id).first()

        if not(subject):
            return {"message": "Subject not found"}, 404
        
        name = data.get("name")
        description = data.get("description")

        if not(name) and not(description):
            return {"message": "Invalid request. Nothing to update"}, 422

        if name:
            error = validate_string(name, 'name')
            if error:
                return {"message": error}, 422
            subject.name = name.strip()        

        if description:
            error = validate_string(description, 'description')
            if error:
                return {"message": error}, 422
            subject.description = description.strip()
            
        db.session.commit()
        cache.delete_memoized(SubjectResource.get)

        return {"message": "Subject updated successfully"}, 200
    
    @role_required('admin')
    def delete(self, subject_id):

        subject = Subject.query.filter_by(id = subject_id).first()
        if not(subject):
            return {"message": "Subject not found"}, 404      

        db.session.delete(subject)
        db.session.commit()

        cache.delete_memoized(SubjectResource.get)

        return {"message": "Subject deleted successfully"}, 200 

class SubjectListResource(Resource):
    @cache.cached(timeout=3600)
    @jwt_required()
    def get(self):
        user = get_jwt()
        subjects = Subject.query.all()

        if user.get("role") == 'admin':
            return [subject.to_dict(include_internal = True) for subject in subjects], 200
        else:
            return [subject.to_dict() for subject in subjects], 200
    
    @role_required('admin')
    def post(self):

        data = request.get_json()

        name = data.get("name")
        description = data.get("description")

        error = validate_string(name, 'name') or validate_string(description, 'description')
        if error:
            return {"message": error}, 422
        
        subject = Subject(
            name = name.strip(),
            description = description.strip()
        )

        db.session.add(subject)
        db.session.commit()

        cache.delete_memoized(SubjectListResource.get)

        return {"message": "Subject created successfully", "id": subject.id}, 201


def register_subject_routes(api):
    api.add_resource(SubjectResource, '/api/subject/<int:subject_id>')
    api.add_resource(SubjectListResource, '/api/subjects')
