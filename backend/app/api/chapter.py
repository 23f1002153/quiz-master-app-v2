from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Chapter, Subject
from app import db
from datetime import datetime
from app.utils.auth import role_required
from app.utils.validators import validate_string

class ChapterResource(Resource):
    @jwt_required()
    def get(self, chapter_id):       
        chapter = Chapter.query.filter_by(id = chapter_id).first()
        if not(chapter):
            return {"message": f"Chapter with id {chapter_id} not found"}, 404
        user = get_jwt()
        if user.get("role") == 'admin':
            return chapter.to_dict(include_internal = True), 200
        else:
            return chapter.to_dict(), 200
    
    @role_required('admin')
    def patch(self, chapter_id):
        chapter = Chapter.query.filter_by(id = chapter_id).first()
        if not(chapter):
            return {"message": f"Chapter with id {chapter_id} not found"}, 404
        
        data = request.get_json()

        name = data.get("name")
        description = data.get("description")

        if not(name) and not(description):
            return {"message": "Invalid request. Nothing to update"}, 422
        
        if name:
            error = validate_string(name, 'name')
            if error:
                return {"message": error}, 422
            chapter.name = name.strip()

        if description:
            error = validate_string(description, 'description')
            if error:
                return {"message": error}, 422
            chapter.description = description.strip()

        db.session.commit()

        return {"message": "Chapter updated successfully"}, 200
    
    @role_required('admin')
    def delete(self, chapter_id):
        chapter = Chapter.query.filter_by(id = chapter_id).first()
        if not(chapter):
            return {"message": f"Chapter with id {chapter_id} not found"}, 404
        
        db.session.delete(chapter)
        db.session.commit()

        return {"message": "Chapter deleted successfully"}, 200

class ChapterListResource(Resource):
    @jwt_required()
    def get(self, subject_id):
        
        subject = Subject.query.filter_by(id = subject_id).first()
        if not(subject):
            return {"message": f"Subject with id {subject_id} not found"}, 404
         
        chapters = Chapter.query.filter_by(subject_id = subject_id).all()

        user = get_jwt() 
        if user.get("role") == 'admin':        
            return [chapter.to_dict(include_internal = True) for chapter in chapters], 200
        else:
            return [chapter.to_dict() for chapter in chapters], 200

    @role_required('admin')
    def post(self, subject_id):

        subject = Subject.query.filter_by(id = subject_id).first()
        if not(subject):
            return {"message": f"Subject with id {subject_id} not found"}, 404 
        
        data = request.get_json()

        name = data.get("name")
        description = data.get("description")

        error = validate_string(name, 'name') or validate_string(description, 'description')
        if error:
            return {"message": error}, 422
        
        chapter = Chapter(
            name = name.strip(),
            description = description.strip(),
            subject_id = subject_id
        )

        db.session.add(chapter)
        db.session.commit()

        return {"message": "Chapter created successfully", "id": chapter.id}, 201

# class ChapterQuizResource(Resource):
#     @jwt_required()
#     def get(self, chapter_id):
#         chapter = Chapter.query.filter_by(id = chapter_id).first()
#         if not(chapter):
#             return {"message": f"Chapter with id {chapter_id} not found"}, 404
        
#         return [quiz.to_dict() for quiz in chapter.quizzes], 200
  
def register_chapter_routes(api):
    api.add_resource(ChapterResource, '/api/chapter/<int:chapter_id>')
    api.add_resource(ChapterListResource, '/api/chapters/<int:subject_id>')
    # api.add_resource(ChapterQuizResource, '/api/chapter/<int:chapter_id>/quizzes')