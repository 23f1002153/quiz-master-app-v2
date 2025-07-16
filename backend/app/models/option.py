from app import db

class Option(db.Model):
    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(500), nullable = False)
    is_correct = db.Column(db.Boolean, nullable = False, default = False)

    # Foreign Keys
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable = False)

    # Relationships
    attempt_responses = db.relationship('AttemptResponse', backref='option', lazy=True, cascade='all, delete')


    def to_dict(self, include_internal = False):
        data = {
            "id": self.id,
            "text": self.text,
            "question_id": self.question_id
        }
        if include_internal: # admin
            data.update({
                "is_correct": self.is_correct
            })

        return data