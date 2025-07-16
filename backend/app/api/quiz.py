from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Chapter, Subject, Quiz
from app import db
from datetime import datetime, date
from app.utils.auth import role_required
from app.utils.validators import validate_string, validate_int, validate_date, validate_time
from app.utils.formatters import format_date, format_time

today = date.today()
now = datetime.now()
cur_time = now.time()
class QuizResource(Resource):
    @jwt_required()
    def get(self, quiz_id):
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not(quiz):
            return {"message": f"Quiz with id {quiz_id} not found"}, 404
        user = get_jwt()
        if user.get("role") == 'admin':
            return quiz.to_dict(include_internal = True), 200
        else:
            return quiz.to_dict(), 200
    
    @role_required('admin')
    def patch(self, quiz_id):
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not(quiz):
            return {"message": f"Quiz with id {quiz_id} not found"}, 404
        
        if quiz.is_started:
            return {"message": "Quiz already started"}, 400

        data = request.get_json()

        ## is_active toggle switch only
        is_active = data.get("is_active")
        if is_active is not None:
            if not isinstance(is_active, bool):
                if isinstance(is_active, str) and is_active.lower() in ["true", "false"]:
                    is_active = is_active.lower() == "true"
                else:
                    return {"message": "is_active must be a boolean"}, 422
            quiz.is_active = is_active 
            db.session().commit()
            return {"message": "Status Changed"}, 200  

        if not(quiz.is_active):
            return {"message": "Cannot edit anymore. Quiz closed"}, 400        

        name = data.get("name")
        description = data.get("description")
        date = data.get("date")
        time = data.get("time")
        duration = data.get("duration")
        remarks = data.get("remarks")
        passing = data.get("passing")

        if not(name) and not(description) and not(date) and not(time) and not(duration) and not(remarks) and not(passing):
            return {"message": "Invalid request. Nothing to update"}, 422
        
        if name:
            error = validate_string(name, 'name')
            if error:
                return {"message": error}, 422
            quiz.name = name.strip()

        if description:
            error = validate_string(description, 'description')
            if error:
                return {"message": error}, 422
            quiz.description = description.strip()

        if date:
            error = validate_date(date, after_today = True)
            if error:
                return {"message": error}, 422
            date = format_date(date)
            quiz.date = date

        if time:
            error = validate_time(time)
            if error:
                return {"message": error}, 422
            time = format_time(time)
            if date:
                if date == today:
                    if time <= cur_time:
                        return {"message": "Cannot schedule quiz in the past"}, 422
            elif quiz.date == today:
                if time <= cur_time:
                    return {"message": "Cannot schedule quiz in the past"}, 422                
            quiz.time = time.strftime("%H:%M")

        if duration:
            error = validate_int(duration, 'duration', required=True)
            if error:
                return {"message": error}, 422
            duration = int(duration)
            if duration < 1:
                return {"message": "Test duration needs to be atleast 1 minute"}, 422
            quiz.duration = duration        

        if remarks:
            error = validate_string(remarks, 'remarks', required=True)
            if error:
                return {"message": error}, 422
            quiz.remarks = remarks.strip()
            
        if passing:
            error = validate_int(passing, 'passing', required=True)
            if error:
                return {"message": error}, 422    
            passing = int(passing)
            if not(0 < passing <= 100):
                return {"message": "Passing must be within 0 and 100"}, 422   
            quiz.passing = passing  
        
        db.session.commit()

        return {"message": "Quiz updated successfully"}, 200
    
    @role_required('admin')
    def delete(self, quiz_id):
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not(quiz):
            return {"message": f"Quiz with id {quiz_id} not found"}, 404
                
        db.session.delete(quiz)
        db.session.commit()

        return {"message": "Quiz deleted successfully"}, 200

class QuizListResource(Resource):
    @jwt_required()
    def get(self, chapter_id):
        chapter = Chapter.query.filter_by(id = chapter_id).first()
        if not(chapter):
            return {"message": f"Chapter with id {chapter_id} not found"}, 404

        quizzes = Quiz.query.filter_by(chapter_id = chapter_id).all()
        user = get_jwt()
        if user.get("role") == 'admin':        
            return [quiz.to_dict(include_internal = True) for quiz in quizzes], 200
        else:
            return [quiz.to_dict() for quiz in quizzes], 200

    @role_required('admin')
    def post(self, chapter_id):
        chapter = Chapter.query.filter_by(id = chapter_id).first()
        if not(chapter):
            return {"message": f"Chapter with id {chapter_id} not found"}, 404

        data = request.get_json()

        name = data.get("name")
        description = data.get("description")
        date = data.get("date")
        time = data.get("time")
        duration = data.get("duration")
        remarks = data.get("remarks")
        passing = data.get("passing")

        error = (validate_string(name, 'name') or 
                 validate_string(description, 'description') or 
                 validate_date(date, after_today = True) or 
                 validate_time(time) or 
                 validate_int(duration, 'duration') or
                 validate_string(remarks, 'remarks', False) or
                 validate_int(passing, 'passing'))
        if error:
            return {"message": error}, 422
        
        date = format_date(date)
        time = format_time(time)

        if date == today:
            if time <= cur_time:
                return {"message": "Cannot schedule quiz in the past"}, 422

        duration = int(duration)
        if duration < 1:
            return {"message": "Test duration needs to be atleast 1 minute"}, 422    

        passing = int(passing)
        if not(0 < passing <= 100):
            return {"message": "Passing must be within 0 and 100"}, 422
        

        quiz = Quiz(
            name = name.strip(),
            description = description.strip(),
            chapter_id = chapter_id,
            date = date,
            time = time.strftime("%H:%M"),
            duration = duration,
            remarks = remarks.strip() if remarks else None,
            passing = passing
        )

        db.session.add(quiz)
        db.session.commit()

        return {"message": "Quiz created successfully"}, 201

def register_quiz_routes(api):
    api.add_resource(QuizResource, '/api/quiz/<int:quiz_id>')
    api.add_resource(QuizListResource, '/api/quizzes/<int:chapter_id>')