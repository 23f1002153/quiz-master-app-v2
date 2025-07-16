from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Chapter, Subject, Quiz, Question, Option
from app import db
from datetime import datetime, date
from app.utils.auth import role_required
from app.utils.validators import validate_string, validate_int, validate_date, validate_time, validate_bool
from app.utils.formatters import format_date, format_time

class OptionResource(Resource):
    @jwt_required()
    def get(self, option_id):
        option = Option.query.filter_by(id = option_id).first()
        if not(option):
            return {"message": f"Option with id {option_id} not found"}, 404
        user = get_jwt()
        if user.get("role") == 'admin' or (option.question.quiz.is_ended):        
            return option.to_dict(include_internal = True), 200
        else:
            return option.to_dict(), 200
        
    @role_required('admin')
    def patch(self, option_id):
        option = Option.query.filter_by(id = option_id).first()
        if not(option):
            return {"message": f"Option with id {option_id} not found"}, 404
            
        data = request.get_json()

        text = data.get("text")
        is_correct = data.get("is_correct")

        if not(text) and not(is_correct):
            return {"message": "Invalid Request. Nothing to update"}, 422

        if text:
            error = validate_string(text, 'text')
            if error:
                return {"message": error}, 422
            option.text = text.strip()

        if is_correct is not None:
            is_correct, error = validate_bool(is_correct, field='is_correct')
            if error:
                return {"message": error}, 422

        db.session.commit()

        return {"message": "Option updated successfully"}, 200
    
    @role_required('admin')
    def delete(self, option_id):
        option = Option.query.filter_by(id = option_id).first()
        if not(option):
            return {"message": f"Option with id {option_id} not found"}, 404

        db.session.delete(option)
        db.session.commit()

        return {"message": "Option deleted successfully"}, 200

class OptionListResource(Resource):
    @jwt_required()
    def get(self, question_id):
        question = db.session.query(Question).filter_by(id = question_id).first()
        if not(question):
            return {"message": f"Question with id {question_id} not found"}, 404

        options = db.session.query(Option).filter_by(question_id = question_id).all()
        user = get_jwt()
        if user.get("role") == 'admin' or question.quiz.is_ended:
            return [option.to_dict(include_internal=True) for option in options]
        else:
            return [option.to_dict() for option in options]

    @role_required('admin')
    def post(self, question_id):
        question = db.session.query(Question).filter_by(id = question_id).first()
        if not(question):
            return {"message": f"Question with id {question_id} not found"}, 404

        data = request.get_json()

        text = data.get("text")
        is_correct = data.get("is_correct")

        error = (validate_string(text, 'text')
                  or validate_bool(is_correct, 'is_correct')[1])
        if error:
            return {"message": error}, 422

        is_correct = validate_bool(is_correct, 'is_correct')[0]

        option = Option(
            text = text.strip(),
            is_correct = is_correct,
            question_id = question_id
        )              

        db.session.add(option)
        db.session.commit()

        return {"message": "Option created successfully"}, 201
    
def register_option_routes(api):
    api.add_resource(OptionResource, '/api/option/<int:option_id>')
    api.add_resource(OptionListResource, '/api/options/<int:question_id>')