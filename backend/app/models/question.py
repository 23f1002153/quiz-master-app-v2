from app import db

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key = True)
    statement = db.Column(db.String(1000), nullable = False)
    marks = db.Column(db.Integer, nullable = False, default = 1)

    ## Foreign Key
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable = False)

    ## Relationship
    options = db.relationship('Option', backref='question', lazy=True, cascade="all, delete")
    attempt_responses = db.relationship('AttemptResponse', backref='question', lazy=True, cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "statement": self.statement,
            "marks": self.marks,
            "quiz_id": self.quiz_id,
            "quiz_name": self.quiz.name, ## get quiz name also
            "options": [option.to_dict() for option in self.options] 
        }
