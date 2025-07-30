from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Chapter, Subject, Quiz, Question
from app import db
from datetime import datetime, date
from app.utils.auth import role_required
from app.utils.validators import validate_string, validate_int, validate_date, validate_time
from app.utils.formatters import format_date, format_time

class QuestionResource(Resource):
    @jwt_required()
    def get(self, question_id):
        question = Question.query.filter_by(id = question_id).first()
        if not(question):
            return {"message": f"Question with id {question_id} not found"}, 404
        
        return question.to_dict(), 200
    
    @role_required('admin')
    def patch(self, question_id):
        question = Question.query.filter_by(id = question_id).first()
        if not(question):
            return {"message": f"Question with id {question_id} not found"}, 404

        data = request.get_json()

        statement = data.get("statement")
        marks = data.get("marks")

        if not(statement) and not(marks):
            return {"message": "Invalid Request. Nothing to update"}, 422

        if statement:
            error = validate_string(statement, field='statement')
            if error:
                return {"message": error}, 422
            question.statement = statement.strip()

        if marks:
            error = validate_int(marks, field='marks')
            if error:
                return {"message": error}, 422
            marks = int(marks)
            if marks <= 0:
                return {"message": "Marks should be atleast 1"}, 422
            question.marks = marks

        db.session.commit()

        return {"message": "Question updated successfully"}, 200

    @role_required('admin')
    def delete(self, question_id):
        question = Question.query.filter_by(id = question_id).first()
        if not(question):
            return {"message": f"Question with id {question_id} not found"}, 404

        db.session.delete(question)
        db.session.commit()

        return {"message": "Question deleted successfully"}, 200        

class QuestionListResource(Resource):
    @jwt_required()
    def get(self, quiz_id):
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not(quiz):
            return {"message": f"Quiz with id {quiz_id} not found"}, 404

        questions = Question.query.filter_by(quiz_id = quiz_id).all()
        return [question.to_dict() for question in questions], 200

    @role_required('admin')
    def post(self, quiz_id):
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not(quiz):
            return {"message": f"Quiz with id {quiz_id} not found"}, 404
        
        data = request.get_json()

        statement = data.get("statement")
        marks = data.get("marks")

        error = validate_string(statement, field='statement') or validate_int(marks, field='marks')
        if error:
            return {"message": error}, 422
        
        marks = int(marks)
        if marks <= 0:
            return {"message": "Marks should be atleast 1"}, 422
        
        question = Question(
            statement = statement.strip(),
            quiz_id = quiz_id,
            marks = marks
        )

        db.session.add(question)
        db.session.commit()

        return {"message": "Question created successfully", "id": question.id}, 201
    
def register_question_routes(api):
    api.add_resource(QuestionResource, '/api/question/<int:question_id>')
    api.add_resource(QuestionListResource, '/api/questions/<int:quiz_id>')