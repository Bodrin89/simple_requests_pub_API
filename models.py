from marshmallow import fields, Schema

from config import db


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    text_question = db.Column(db.String(255))
    text_answer = db.Column(db.String(255))
    data_question = db.Column(db.String(255))


class QuestionSchema(Schema):
    __tablename__ = 'question'
    id = fields.Integer()
    text_question = fields.String()
    text_answer = fields.String()
    data_question = fields.String()
