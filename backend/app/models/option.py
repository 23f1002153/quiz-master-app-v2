from app import db

class Option(db.Model):
    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(500), nullable = False)
    is_correct = db.Column(db.Boolean, nullable = False, default = False)
    option_num = db.Column(db.Integer, nullable = False)

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable = False)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_correct": self.is_correct,
            "option_num": self.option_num,
            "question_id": self.question_id
        }