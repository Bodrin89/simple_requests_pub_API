from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import os
from dotenv import load_dotenv, find_dotenv
from flask_migrate import Migrate

app = Flask(__name__)

load_dotenv(find_dotenv())

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{POSTGRES_USER}:" \
                                        f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:" \
                                        f"{POSTGRES_PORT}/{POSTGRES_DB}"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


@app.route('/questions/', methods=['POST'])
def get_questions():
    data = request.get_json()
    questions_num = data.get('questions_num', 0)

    # Запрос к публичному API для получения вопросов
    api_url = f"https://jservice.io/api/random?count={questions_num}"
    response = requests.get(api_url)
    if not isinstance(questions_num, int):
        return jsonify({'error': 'Не правильный тип данных'}), 400
    if response.status_code == 200:
        data = response.json()
        for item in data:
            # Проверка на уникальность вопроса в базе данных
            existing_question = Question.query.filter_by(text_question=item['question']).first()
            while existing_question:
                questions_num = 1
                response = requests.get(api_url)
                if response.status_code == 200:
                    item = response.json()[0]
                    existing_question = Question.query.filter_by(text_question=item['question']).first()
            # Сохранение вопроса в базе данных
            result = Question(
                text_question=item['question'],
                text_answer=item['answer'],
                data_question=item['created_at']
            )
            db.session.add(result)
        db.session.commit()
        try:
            latest_question = Question.query.order_by(Question.id.desc()).limit(2)[1]
            resp_question = QuestionSchema()
            return resp_question.dump(latest_question)
        except:
            return {}
    else:
        return jsonify(error='Не правильный запрос'), 500


if __name__ == '__main__':
    app.run(port=8082)
