from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Chapter, Subject, Quiz, Question, Option, Attempt, QuizSession, AttemptResponse
from app import db
from datetime import datetime, date, timedelta
from app.utils.auth import role_required
from app.utils.validators import validate_string, validate_int, validate_date, validate_time, validate_bool
from app.utils.formatters import format_date, format_time

class QuizSessionResource(Resource):
    # start or check status for a quiz
    @jwt_required()
    def get(self, quiz_id):
        user_id = get_jwt_identity()

        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not(quiz):
            return {"message": f"Quiz with id {quiz_id} not found"}, 404
        
        attempt = Attempt.query.filter_by(quiz_id = quiz_id, user_id = user_id).first()
        if attempt:
            return {"message": f"Quiz with id {quiz_id} already submitted"}, 400        

        quiz_session = QuizSession.query.filter_by(quiz_id = quiz_id, user_id = user_id).first()
        if quiz_session:
            time_elapsed = datetime.now() - quiz_session.started_at
            remaining = timedelta(minutes=quiz.duration) - time_elapsed
            if time_elapsed > timedelta(minutes=quiz.duration):
                return {"message": "Quiz time has expired"}, 400
            else:
                return {
                    "message": "Quiz time ongoing",
                    "remaining_time": int(remaining.total_seconds() // 60)
                    }, 200
        else:
            return {"message": "Quiz not started yet"}, 200
        
    @jwt_required()
    def post(self, quiz_id):
        user_id = get_jwt_identity()

        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not(quiz):
            return {"message": f"Quiz with id {quiz_id} not found"}, 404
        
        if not quiz.is_started:
            return {"message": "Quiz time hasn't started yet"}, 400
        
        quiz_session = QuizSession.query.filter_by(quiz_id = quiz_id, user_id = user_id).first()
        if quiz_session:
            return {"message": f"Quiz with id {quiz_id} has already been started"}, 400
        

        
        quiz_session = QuizSession(
            user_id = user_id,
            quiz_id = quiz_id
        )

        db.session.add(quiz_session)
        db.session.commit()

        return {"message": "Quiz started successfully"}, 201

        
class AttemptResource(Resource):
    # submit a quiz or retrieve submitted answers
    @jwt_required()
    def get(self, quiz_id):
        user_id = get_jwt_identity()

        # 1. Check if quiz exists
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": f"Quiz with id {quiz_id} not found"}, 404

        # 2. Check if user has completed the quiz
        attempt = Attempt.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
        if not attempt or not attempt.completed:
            return {"message": "Quiz not submitted yet"}, 400

        # 3. Fetch all questions
        questions = Question.query.filter_by(quiz_id=quiz_id).all()

        # 4. Fetch all responses
        responses = AttemptResponse.query.filter_by(user_id=user_id, quiz_id=quiz_id).all()
        response_map = {}
        for r in responses:
            response_map[r.question_id] = r

        # 5. Fetch all selected options
        option_ids = []
        for r in responses:
            option_ids.append(r.option_id)

        options = Option.query.filter(Option.id.in_(option_ids)).all()
        option_map = {}
        for opt in options:
            option_map[opt.id] = opt

        # 6. Build result using normal for loop
        result = []
        for question in questions:
            question_id = question.id
            if question_id in response_map:
                response = response_map[question_id]
                option_id = response.option_id

                if option_id in option_map:
                    selected_option = option_map[option_id]
                    selected_option_data = selected_option.to_dict()
                else:
                    selected_option_data = None

                question_data = question.to_dict()
                entry = {
                    "question": question_data,
                    "selected_option": selected_option_data
                }
                result.append(entry)

        return result, 200


    @jwt_required()
    def post(self, quiz_id):
        user_id = get_jwt_identity()

        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not(quiz):
            return {"message": f"Quiz with id {quiz_id} not found"}, 404
        
        attempt = Attempt.query.filter_by(quiz_id = quiz_id, user_id = user_id).first()
        if attempt:
            return {"message": f"Quiz with id {quiz_id} already submitted"}, 400
        
        session = QuizSession.query.filter_by(user_id = user_id, quiz_id = quiz_id).first()
        if not session:
            return {"message": f"Quiz with id {quiz_id} not started or expired"}, 400
        
        data = request.get_json()
        responses = data.get("responses")
        if not responses:
            return {"message": "No responses provided"}, 422
        
        total_correct = 0
        total_score = 0
        total_marks = 0

        for resp in responses:
            question_id = resp.get("question_id")
            option_id = resp.get("option_id")

            question = Question.query.filter_by(id = question_id).first()
            option = Option.query.filter_by(id = option_id).first()

            if not question or not option or option.question_id != question_id:
                continue

            total_marks += question.marks
            if option.is_correct:
                total_correct += 1
                total_score += question.marks

            answer = AttemptResponse(
                user_id = user_id,
                quiz_id = quiz_id,
                question_id = question_id,
                option_id = option_id,
            )
            db.session.add(answer)

        
        total_questions = len(responses)
        attempt = Attempt(
            user_id = user_id,
            quiz_id = quiz_id,
            total_marks = total_marks,
            total_questions = total_questions,
            total_score = total_score,
            total_correct = total_correct,
            completed = True
        )

        db.session.add(attempt)

        db.session.delete(session) # cleanup quiz session
        db.session.commit()

        return {"message": "Quiz submitted successfully"}, 201


class AllQuestionsResource(Resource):
    # fetch all questions
    @jwt_required()
    def get(self, quiz_id):
        user = get_jwt()
        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not(quiz):
            return {"message": f"Quiz with id {quiz_id} not found"}, 404
        
        questions = []
        for q in quiz.questions:
            q_dict = q.to_dict()
            if user.get("role") == 'admin':
                q_dict["options"] = [o.to_dict(include_internal = True) for o in q.options]
            else:
                q_dict["options"] = [o.to_dict() for o in q.options]
            questions.append(q_dict)
        return questions, 200

class ResultResource(Resource):
    # fetch quiz result
    @jwt_required()
    def get(self, quiz_id):
        user_id = get_jwt_identity()

        quiz = Quiz.query.filter_by(id = quiz_id).first()
        if not(quiz):
            return {"message": f"Quiz with id {quiz_id} not found"}, 404

        attempt = Attempt.query.filter_by(quiz_id = quiz_id, user_id = user_id).first()
        if not attempt:
            return {"message": f"Quiz not attempted"}, 400

        return attempt.to_dict(), 200        

def register_attempt_routes(api):
    api.add_resource(QuizSessionResource, '/api/quiz/<int:quiz_id>/start')
    api.add_resource(AttemptResource, '/api/quiz/<int:quiz_id>/submit')
    api.add_resource(AllQuestionsResource, '/api/quiz/<int:quiz_id>/questions')
    api.add_resource(ResultResource, '/api/quiz/<int:quiz_id>/result')
